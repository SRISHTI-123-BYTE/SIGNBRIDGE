"""
SignBridge ST-GCN Neural Network Training Engine
Trains the 107-node Spatial-Temporal Graph Convolutional Network on multi-person ISL datasets
using joint Clip-Level Cross-Entropy + Dense Temporal Frame Supervision, with online 3D data augmentation,
held-out person-independent validation, and ONNX runtime export.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import json
import numpy as np
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    TOTAL_LANDMARKS, COORDINATE_DIM, VOCABULARY, VOCAB_TO_IDX,
    NUM_CLASSES, TEMPORAL_WINDOW_FRAMES, STGCN_HIDDEN_DIM
)
from normalization import LandmarkNormalizer
from dataset_manager import DatasetManager
from synthetic_data import generate_sign_trajectory
from dataset_augmentation import (
    augment_sequence_pipeline, gaussian_jitter, spatial_scale,
    spatial_rotation_3d, time_warp
)

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    from stgcn_pytorch import STGCNISLNet
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)
CHECKPOINT_PATH = os.path.join(MODELS_DIR, "stgcn_isl_42.pt")
ONNX_PATH = os.path.join(MODELS_DIR, "stgcn_isl_42.onnx")


class ISLLandmarkDataset(Dataset):
    """
    PyTorch Dataset with on-the-fly 3D landmark augmentation,
    clip-level classification targets, and sustained frame-level supervision.
    """
    def __init__(
        self,
        samples: list,
        normalizer: LandmarkNormalizer,
        target_len: int = 30,
        augment: bool = False
    ):
        self.target_len = target_len
        self.augment = augment
        self.normalizer = normalizer
        self.samples = samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        seq = item["landmarks"].copy() # (T, 107, 3)
        gloss = item["gloss"].upper().strip()
        target_idx = VOCAB_TO_IDX.get(gloss, 1)

        # Apply stochastic 3D augmentation during training
        if self.augment:
            seq = augment_sequence_pipeline(
                seq,
                rotate=True,
                scale=True,
                warp=True,
                jitter=True,
                mirror=False
            )

        # Normalize coordinates
        norm_seq = self.normalizer.normalize_sequence(seq) # (T, 107, 3)

        # Resample to target_len
        T = norm_seq.shape[0]
        if T != self.target_len:
            indices = np.linspace(0, T - 1, num=self.target_len)
            resampled = np.zeros((self.target_len, TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
            for i, t_idx in enumerate(indices):
                low = int(np.floor(t_idx))
                high = min(T - 1, int(np.ceil(t_idx)))
                frac = t_idx - low
                resampled[i] = (1.0 - frac) * norm_seq[low] + frac * norm_seq[high]
            norm_seq = resampled

        # Permute to (C, T, V) = (3, 30, 107)
        tensor_x = torch.from_numpy(norm_seq).permute(2, 0, 1).float()

        # Frame targets: Active sign gesture between frames 5 and 25, blank (0) during lead-in/lead-out
        frame_targets = torch.zeros(self.target_len, dtype=torch.long)
        frame_targets[5:26] = target_idx

        clip_target = torch.tensor(target_idx, dtype=torch.long)

        return tensor_x, clip_target, frame_targets, gloss, item.get("user_id", "unknown")


def seed_multiperson_dataset_if_needed(dm: DatasetManager) -> int:
    """
    Ensures diverse multi-person procedural data exists across all 42 ISL signs
    with realistic anatomical variance, speed envelopes, and articulation jitter.
    Honestly labeled as procedural biomechanical synthesis.
    """
    stats = dm.get_dataset_stats()
    vocab_signs = [token for token in VOCABULARY if token != "<BLANK>"]
    needed_users = ["user_01", "user_02", "user_03", "user_test"]
    
    # Check if already fully populated
    if stats["total_samples"] >= len(vocab_signs) * len(needed_users):
        return 0

    print(f"[Dataset Seed] Populating procedural biomechanical dataset for all {len(vocab_signs)} signs...", flush=True)
    added_count = 0

    manifest = dm._load_manifest()
    existing_pairs = {(s.get("user_id"), s.get("gloss")) for s in manifest.get("samples", [])}

    for user_id in needed_users:
        # Biomechanical anatomical variations:
        if user_id == "user_01":
            user_scale = 0.92
            arm_ratio = 0.95
            tempo = 1.08
        elif user_id == "user_02":
            user_scale = 1.08
            arm_ratio = 1.05
            tempo = 0.94
        elif user_id == "user_03":
            user_scale = 0.98
            arm_ratio = 1.00
            tempo = 1.02
        else: # user_test (unseen held-out signer)
            user_scale = 1.04
            arm_ratio = 0.98
            tempo = 0.97

        for gloss in vocab_signs:
            if (user_id, gloss) in existing_pairs:
                continue
            base_traj = generate_sign_trajectory(gloss, num_frames=30)
            traj = (base_traj - 0.5) * user_scale + 0.5
            # Apply arm limb ratio variation
            traj[:, [13, 15], :] = (traj[:, [13, 15], :] - traj[:, [11, 11], :]) * arm_ratio + traj[:, [11, 11], :]
            traj[:, [14, 16], :] = (traj[:, [14, 16], :] - traj[:, [12, 12], :]) * arm_ratio + traj[:, [12, 12], :]
            # Apply sensor noise
            traj += np.random.normal(0, 0.003, size=traj.shape)

            dm.save_recording(
                sequence=traj,
                gloss=gloss,
                user_id=user_id,
                fps=30.0,
                metadata={
                    "source": "procedural_biomechanical_synthesis",
                    "signer_scale": user_scale,
                    "tempo_factor": tempo
                }
            )
            added_count += 1

    print(f"[Dataset Seed] Generated {added_count} multi-person procedural samples.", flush=True)
    return added_count


def train_stgcn_model(
    epochs: int = 40,
    batch_size: int = 16,
    lr: float = 0.002,
    augment_factor: int = 3
) -> dict:
    """
    Executes complete ST-GCN training pipeline with joint Clip CE + Dense Frame CE loss,
    multi-person held-out validation, and ONNX export.
    """
    if not TORCH_AVAILABLE:
        raise RuntimeError("PyTorch is not available in the current environment.")

    dm = DatasetManager()
    seed_multiperson_dataset_if_needed(dm)

    # 1. Person-Independent Split: Train (user_01, user_02), Val (user_03), Held-out Test (user_test)
    train_records, val_records, test_records = dm.create_person_independent_split(
        test_users=["user_test"],
        val_users=["user_03"]
    )
    print(f"[Train ST-GCN] Person-independent split: Train={len(train_records)}, Val={len(val_records)}, Held-out Test={len(test_records)}", flush=True)

    normalizer = LandmarkNormalizer()

    # Load raw sample dictionaries
    train_samples = [dm.load_sample(r["filepath"]) for r in train_records]
    val_samples = [dm.load_sample(r["filepath"]) for r in val_records]
    test_samples = [dm.load_sample(r["filepath"]) for r in test_records]

    # Pre-expand training set with diverse augmentations
    expanded_train = []
    for s in train_samples:
        expanded_train.append(s)
        for aug_i in range(augment_factor):
            aug_seq = augment_sequence_pipeline(
                s["landmarks"],
                rotate=True,
                scale=True,
                warp=True,
                jitter=True,
                mirror=False
            )
            expanded_train.append({
                "landmarks": aug_seq,
                "gloss": s["gloss"],
                "user_id": f"{s['user_id']}_aug{aug_i+1}"
            })

    print(f"[Train ST-GCN] Total augmented training samples: {len(expanded_train)}", flush=True)

    train_dataset = ISLLandmarkDataset(expanded_train, normalizer, target_len=30, augment=True)
    val_dataset = ISLLandmarkDataset(val_samples, normalizer, target_len=30, augment=False)
    test_dataset = ISLLandmarkDataset(test_samples, normalizer, target_len=30, augment=False)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # 3. Model Architecture
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Train ST-GCN] Using compute device: {device}", flush=True)

    model = STGCNISLNet(
        in_channels=3,
        num_classes=NUM_CLASSES,
        num_nodes=TOTAL_LANDMARKS,
        hidden_dim=STGCN_HIDDEN_DIM
    ).to(device)

    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    print(f"[Train ST-GCN] Training for {epochs} epochs with Joint Clip-CE + Frame-CE supervision...", flush=True)
    history = {"train_loss": [], "val_acc": [], "test_acc": []}

    best_val_acc = -1.0
    best_weights = None

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        model.train()
        total_train_loss = 0.0
        num_batches = 0

        for x_batch, clip_targets, frame_targets, _, _ in train_loader:
            x_batch = x_batch.to(device)         # (B, 3, 30, 107)
            clip_targets = clip_targets.to(device) # (B,)
            frame_targets = frame_targets.to(device) # (B, 30)

            logits = model(x_batch) # (B, 30, NUM_CLASSES)

            # 1. Clip-level pooled loss (focus on active mid-phase frames 8 to 22)
            clip_logits = torch.mean(logits[:, 8:22, :], dim=1) # (B, NUM_CLASSES)
            loss_clip = F.cross_entropy(clip_logits, clip_targets)

            # 2. Dense frame-level loss for sustained predictions
            loss_frame = F.cross_entropy(logits.view(-1, NUM_CLASSES), frame_targets.view(-1))

            loss = loss_clip + 0.60 * loss_frame

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=3.0)
            optimizer.step()

            total_train_loss += loss.item()
            num_batches += 1

        scheduler.step()
        avg_train_loss = total_train_loss / max(1, num_batches)
        history["train_loss"].append(avg_train_loss)

        # Validation at every epoch
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for x_batch, clip_targets, _, _, _ in val_loader:
                x_batch = x_batch.to(device)
                logits = model(x_batch)
                clip_logits = torch.mean(logits[:, 8:22, :], dim=1)
                preds = torch.argmax(clip_logits, dim=-1).cpu()
                val_correct += int(torch.sum(preds == clip_targets))
                val_total += len(clip_targets)

        val_acc = (val_correct / max(1, val_total)) * 100.0
        history["val_acc"].append(val_acc)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_weights = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        elapsed = time.time() - t0
        if epoch % 5 == 0 or epoch == epochs or epoch == 1:
            print(f"Epoch [{epoch:02d}/{epochs:02d}] ({elapsed:.1f}s) - Train Loss: {avg_train_loss:.4f} | Val Acc: {val_acc:.1f}% (Best: {best_val_acc:.1f}%)", flush=True)

    # Load best validation weights
    if best_weights is not None:
        model.load_state_dict({k: v.to(device) for k, v in best_weights.items()})

    # Evaluate on Unseen Held-Out Test Signer
    model.eval()
    test_correct = 0
    test_total = 0
    test_confidences = []
    with torch.no_grad():
        for x_batch, clip_targets, _, _, _ in test_loader:
            x_batch = x_batch.to(device)
            logits = model(x_batch)
            probs = F.softmax(logits, dim=-1)
            mid_probs = torch.mean(probs[:, 8:22, :], dim=1)
            conf, preds = torch.max(mid_probs, dim=-1)
            test_correct += int(torch.sum(preds.cpu() == clip_targets))
            test_total += len(clip_targets)
            test_confidences.extend(conf.cpu().numpy().tolist())

    final_test_acc = (test_correct / max(1, test_total)) * 100.0
    avg_test_conf = float(np.mean(test_confidences)) if test_confidences else 0.0
    print(f"\n[Train ST-GCN] Held-Out Test Signer Accuracy: {final_test_acc:.2f}% ({test_correct}/{test_total}) | Avg Confidence: {avg_test_conf:.2f}", flush=True)

    # 4. Save Checkpoint
    torch.save({
        "model_state_dict": model.state_dict(),
        "num_classes": NUM_CLASSES,
        "vocabulary": VOCABULARY,
        "hidden_dim": STGCN_HIDDEN_DIM,
        "history": history,
        "best_val_acc": best_val_acc,
        "test_acc": final_test_acc
    }, CHECKPOINT_PATH)
    print(f"[Train ST-GCN] Saved PyTorch weights to: {CHECKPOINT_PATH}", flush=True)

    # 5. Export to ONNX
    print(f"[Train ST-GCN] Exporting model to ONNX runtime...", flush=True)
    dummy_input = torch.randn(1, 3, 30, TOTAL_LANDMARKS, dtype=torch.float32).to(device)
    model.export_onnx(ONNX_PATH, dummy_input)
    print(f"[Train ST-GCN] Successfully exported ONNX model to: {ONNX_PATH}", flush=True)

    return {
        "checkpoint_path": CHECKPOINT_PATH,
        "onnx_path": ONNX_PATH,
        "final_train_loss": round(history["train_loss"][-1], 4),
        "best_val_acc": round(best_val_acc, 2),
        "final_test_acc": round(final_test_acc, 2),
        "avg_confidence": round(avg_test_conf, 2),
        "train_samples": len(expanded_train),
        "val_samples": len(val_samples),
        "test_samples": len(test_samples)
    }


if __name__ == "__main__":
    results = train_stgcn_model(epochs=40, batch_size=16)
    print("\nTraining Finished Successfully!", flush=True)
    print(json.dumps(results, indent=2), flush=True)
