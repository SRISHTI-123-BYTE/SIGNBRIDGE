"""
SignBridge Evaluation & Benchmarking Harness
Executes rigorous person-independent held-out evaluation on real and procedural recordings,
comparing Rule-Based ST-GCN vs Trained Neural ST-GCN across Top-1, Top-3, Precision, Recall, F1, and Latency.
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
from typing import Dict, List, Any, Tuple, Optional

sys.path.insert(0, os.path.dirname(__file__))

from config import (
    TOTAL_LANDMARKS, VOCABULARY, VOCAB_TO_IDX,
    NUM_CLASSES, CONFIDENCE_THRESHOLD, STGCN_HIDDEN_DIM
)
from normalization import LandmarkNormalizer
from dataset_manager import DatasetManager
from stgcn_model import STGCNModel
from ctc_decoder import CTCDecoder

try:
    import torch
    from stgcn_pytorch import STGCNISLNet
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import onnxruntime as ort
    ORT_AVAILABLE = True
except ImportError:
    ORT_AVAILABLE = False


CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "models", "stgcn_isl_42.pt")
ONNX_PATH = os.path.join(os.path.dirname(__file__), "models", "stgcn_isl_42.onnx")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "dataset", "splits")
os.makedirs(REPORTS_DIR, exist_ok=True)


class Evaluator:
    def __init__(self):
        self.normalizer = LandmarkNormalizer()
        # Pure rule-based model with ONNX blending explicitly DISABLED for true baseline comparison
        self.rule_model = STGCNModel(enable_onnx=False)
        self.rule_decoder = CTCDecoder(min_confidence=CONFIDENCE_THRESHOLD)

        # PyTorch model loader
        self.pytorch_model = None
        self.ort_session = None

        if TORCH_AVAILABLE and os.path.exists(CHECKPOINT_PATH):
            try:
                ckpt = torch.load(CHECKPOINT_PATH, map_location="cpu")
                h_dim = ckpt.get("hidden_dim", STGCN_HIDDEN_DIM)
                net = STGCNISLNet(in_channels=3, num_classes=NUM_CLASSES, hidden_dim=h_dim)
                net.load_state_dict(ckpt["model_state_dict"])
                net.eval()
                self.pytorch_model = net
                print(f"[Evaluator] Loaded PyTorch checkpoint from {CHECKPOINT_PATH}")
            except Exception as e:
                print(f"[Evaluator] PyTorch load notice: {e}")

        if ORT_AVAILABLE and os.path.exists(ONNX_PATH):
            try:
                self.ort_session = ort.InferenceSession(ONNX_PATH, providers=["CPUExecutionProvider"])
                print(f"[Evaluator] Loaded ONNX Runtime session from {ONNX_PATH}")
            except Exception as e:
                print(f"[Evaluator] ONNX load notice: {e}")

    def evaluate_sequence_rule(self, raw_seq: np.ndarray, return_top3: bool = False) -> Any:
        """
        Runs pure rule-based ST-GCN on a landmark sequence.
        Returns: (top1_gloss, top3_glosses, confidence, latency_ms)
        """
        t0 = time.perf_counter()
        norm_seq = self.normalizer.normalize_sequence(raw_seq)
        probs = self.rule_model.forward(norm_seq)
        recognized = self.rule_decoder.decode_greedy(probs)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        if recognized:
            top_tok = recognized[0]
            top1 = top_tok["gloss"]
            conf = float(top_tok["confidence"])
            top3 = [t["gloss"] for t in recognized[:3]]
            if return_top3:
                return top1, top3, conf, latency_ms
            return top1, conf, latency_ms

        # Direct active slice fallback if CTC had no sustained trigger
        active_slice = probs[:, 1:]
        mean_p = np.mean(active_slice, axis=0)
        top3_indices = np.argsort(mean_p)[-3:][::-1]
        top3_glosses = [VOCABULARY[idx + 1] for idx in top3_indices]
        top1 = top3_glosses[0] if mean_p[top3_indices[0]] > 0.05 else "<BLANK>"
        conf = float(mean_p[top3_indices[0]]) if top1 != "<BLANK>" else 0.0
        if return_top3:
            return top1, top3_glosses, conf, latency_ms
        return top1, conf, latency_ms

    def evaluate_sequence_pytorch(self, raw_seq: np.ndarray, return_top3: bool = False) -> Any:
        """
        Runs trained PyTorch / ONNX model on a landmark sequence.
        Returns: (top1_gloss, top3_glosses, confidence, latency_ms)
        """
        if self.pytorch_model is None and self.ort_session is None:
            return self.evaluate_sequence_rule(raw_seq)

        t0 = time.perf_counter()
        norm_seq = self.normalizer.normalize_sequence(raw_seq)

        # Resample to 30 frames if necessary
        T = norm_seq.shape[0]
        if T != 30:
            indices = np.linspace(0, T - 1, num=30)
            resampled = np.zeros((30, norm_seq.shape[1], norm_seq.shape[2]), dtype=np.float32)
            for i, t_idx in enumerate(indices):
                low = int(np.floor(t_idx))
                high = min(T - 1, int(np.ceil(t_idx)))
                frac = t_idx - low
                resampled[i] = (1.0 - frac) * norm_seq[low] + frac * norm_seq[high]
            norm_seq = resampled

        # Inference via ONNX or PyTorch
        if self.ort_session is not None:
            tensor_in = np.transpose(norm_seq, (2, 0, 1))[np.newaxis, ...].astype(np.float32)
            outputs = self.ort_session.run(None, {"input_landmarks": tensor_in})
            logits = outputs[0][0] # (T, NUM_CLASSES)
            exp_l = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
            probs = exp_l / np.sum(exp_l, axis=-1, keepdims=True)
        else:
            with torch.no_grad():
                tensor_in = torch.from_numpy(norm_seq).permute(2, 0, 1).unsqueeze(0).float()
                logits = self.pytorch_model(tensor_in)[0].cpu().numpy()
                exp_l = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
                probs = exp_l / np.sum(exp_l, axis=-1, keepdims=True)

        latency_ms = (time.perf_counter() - t0) * 1000.0

        # CTC decoding
        tokens = self.rule_decoder.decode_greedy(probs)
        if tokens:
            top1 = tokens[0]["gloss"]
            conf = float(tokens[0]["confidence"])
            top3 = [t["gloss"] for t in tokens[:3]]
            if return_top3:
                return top1, top3, conf, latency_ms
            return top1, conf, latency_ms

        # Direct clip classification across active signing window
        active_slice = probs[8:22, 1:] if probs.shape[0] >= 22 else probs[:, 1:]
        mean_probs = np.mean(active_slice, axis=0) # (NUM_CLASSES - 1,)
        top3_indices = np.argsort(mean_probs)[-3:][::-1]
        top3_glosses = [VOCABULARY[idx + 1] for idx in top3_indices]
        top1 = top3_glosses[0]
        conf = float(mean_probs[top3_indices[0]])
        if return_top3:
            return top1, top3_glosses, conf, latency_ms
        return top1, conf, latency_ms

    def run_benchmark_on_held_out(self, test_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes complete comparison between Model A (Rule-Based) and Model B (Trained Neural Net).
        Computes Top-1, Top-3, Precision, Recall, F1, Confusion Matrix, and Latency breakdown.
        """
        dm = DatasetManager()
        vocab_42 = [v for v in VOCABULARY if v != "<BLANK>"]
        vocab_map = {g: i for i, g in enumerate(vocab_42)}
        num_v = len(vocab_42)

        # Include <BLANK> as index num_v to track missed detections
        conf_matrix_rule = np.zeros((num_v, num_v + 1), dtype=int)
        conf_matrix_nn = np.zeros((num_v, num_v + 1), dtype=int)

        rule_top1_correct = 0
        rule_top3_correct = 0
        nn_top1_correct = 0
        nn_top3_correct = 0
        total_eval = 0

        rule_latencies = []
        nn_latencies = []

        per_sign_stats = {
            g: {
                "ground_truth": 0,
                "rule_correct": 0,
                "nn_correct": 0,
                "rule_pred_count": 0,
                "nn_pred_count": 0
            }
            for g in vocab_42
        }

        print(f"\n=======================================================")
        print(f"  HELD-OUT BENCHMARK ON UNSEEN SIGNERS (N={len(test_records)})")
        print(f"  Evaluation Mode: Person-Independent Test Split")
        print(f"=======================================================\n")

        for idx, rec in enumerate(test_records):
            sample = dm.load_sample(rec["filepath"])
            true_gloss = sample["gloss"].upper()
            landmarks = sample["landmarks"]

            if true_gloss not in vocab_map:
                continue

            true_idx = vocab_map[true_gloss]
            per_sign_stats[true_gloss]["ground_truth"] += 1
            total_eval += 1

            # 1. Rule-based evaluation
            pred_rule, top3_rule, conf_rule, lat_rule = self.evaluate_sequence_rule(landmarks, return_top3=True)
            rule_latencies.append(lat_rule)
            if pred_rule == true_gloss:
                rule_top1_correct += 1
                per_sign_stats[true_gloss]["rule_correct"] += 1
            if true_gloss in top3_rule:
                rule_top3_correct += 1

            pred_col_rule = vocab_map[pred_rule] if pred_rule in vocab_map else num_v
            conf_matrix_rule[true_idx, pred_col_rule] += 1
            if pred_rule in per_sign_stats:
                per_sign_stats[pred_rule]["rule_pred_count"] += 1

            # 2. Trained PyTorch / ONNX ST-GCN evaluation
            pred_nn, top3_nn, conf_nn, lat_nn = self.evaluate_sequence_pytorch(landmarks, return_top3=True)
            nn_latencies.append(lat_nn)
            if pred_nn == true_gloss:
                nn_top1_correct += 1
                per_sign_stats[true_gloss]["nn_correct"] += 1
            if true_gloss in top3_nn:
                nn_top3_correct += 1

            pred_col_nn = vocab_map[pred_nn] if pred_nn in vocab_map else num_v
            conf_matrix_nn[true_idx, pred_col_nn] += 1
            if pred_nn in per_sign_stats:
                per_sign_stats[pred_nn]["nn_pred_count"] += 1

        # Macro-Averaged Precision, Recall, F1 calculation
        rule_precisions, rule_recalls, rule_f1s = [], [], []
        nn_precisions, nn_recalls, nn_f1s = [], [], []

        for g in vocab_42:
            st = per_sign_stats[g]
            gt = st["ground_truth"]

            # Rule metrics
            r_tp = st["rule_correct"]
            r_fp = st["rule_pred_count"] - r_tp
            r_prec = r_tp / max(1, (r_tp + r_fp))
            r_rec = r_tp / max(1, gt)
            r_f1 = (2 * r_prec * r_rec) / max(1e-6, (r_prec + r_rec))
            rule_precisions.append(r_prec)
            rule_recalls.append(r_rec)
            rule_f1s.append(r_f1)

            # NN metrics
            nn_tp = st["nn_correct"]
            nn_fp = st["nn_pred_count"] - nn_tp
            nn_prec = nn_tp / max(1, (nn_tp + nn_fp))
            nn_rec = nn_tp / max(1, gt)
            nn_f1 = (2 * nn_prec * nn_rec) / max(1e-6, (nn_prec + nn_rec))
            nn_precisions.append(nn_prec)
            nn_recalls.append(nn_rec)
            nn_f1s.append(nn_f1)

        rule_top1 = (rule_top1_correct / max(1, total_eval)) * 100.0
        rule_top3 = (rule_top3_correct / max(1, total_eval)) * 100.0
        nn_top1 = (nn_top1_correct / max(1, total_eval)) * 100.0
        nn_top3 = (nn_top3_correct / max(1, total_eval)) * 100.0

        avg_lat_rule = np.mean(rule_latencies) if rule_latencies else 0.0
        avg_lat_nn = np.mean(nn_latencies) if nn_latencies else 0.0

        # Confusions lists
        confusions_rule = []
        confusions_nn = []
        for i in range(num_v):
            for j in range(num_v + 1):
                if i != j:
                    pred_name = vocab_42[j] if j < num_v else "<BLANK>"
                    if conf_matrix_rule[i, j] > 0:
                        confusions_rule.append({
                            "true": vocab_42[i],
                            "predicted": pred_name,
                            "count": int(conf_matrix_rule[i, j])
                        })
                    if conf_matrix_nn[i, j] > 0:
                        confusions_nn.append({
                            "true": vocab_42[i],
                            "predicted": pred_name,
                            "count": int(conf_matrix_nn[i, j])
                        })

        report = {
            "evaluation_timestamp": time.time(),
            "total_test_samples": total_eval,
            "test_users": sorted(list(set(r.get("user_id", "") for r in test_records))),
            "comparison": {
                "rule_based_stgcn": {
                    "top1_accuracy_pct": round(rule_top1, 2),
                    "top3_accuracy_pct": round(rule_top3, 2),
                    "macro_precision": round(float(np.mean(rule_precisions)), 4),
                    "macro_recall": round(float(np.mean(rule_recalls)), 4),
                    "macro_f1": round(float(np.mean(rule_f1s)), 4),
                    "mean_latency_ms": round(float(avg_lat_rule), 2),
                    "fps_throughput": round(1000.0 / max(0.1, avg_lat_rule), 1),
                    "total_correct": rule_top1_correct,
                    "total_confusions": len(confusions_rule)
                },
                "trained_pytorch_stgcn": {
                    "top1_accuracy_pct": round(nn_top1, 2),
                    "top3_accuracy_pct": round(nn_top3, 2),
                    "macro_precision": round(float(np.mean(nn_precisions)), 4),
                    "macro_recall": round(float(np.mean(nn_recalls)), 4),
                    "macro_f1": round(float(np.mean(nn_f1s)), 4),
                    "mean_latency_ms": round(float(avg_lat_nn), 2),
                    "fps_throughput": round(1000.0 / max(0.1, avg_lat_nn), 1),
                    "total_correct": nn_top1_correct,
                    "total_confusions": len(confusions_nn)
                }
            },
            "per_sign_breakdown": per_sign_stats,
            "top_rule_confusions": sorted(confusions_rule, key=lambda x: x["count"], reverse=True)[:5],
            "top_nn_confusions": sorted(confusions_nn, key=lambda x: x["count"], reverse=True)[:5]
        }

        # Save reports
        report_file = os.path.join(REPORTS_DIR, "evaluation_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        np.savez_compressed(
            os.path.join(REPORTS_DIR, "confusion_matrices.npz"),
            labels=np.array(vocab_42 + ["<BLANK>"]),
            matrix_rule=conf_matrix_rule,
            matrix_nn=conf_matrix_nn
        )

        return report


def print_evaluation_summary(report: Dict[str, Any]):
    comp = report["comparison"]
    r_rule = comp["rule_based_stgcn"]
    r_nn = comp["trained_pytorch_stgcn"]

    print("+----------------------------------+-------------------+--------------------+")
    print("| Metric                           | Rule-Based ST-GCN | Trained Neural Net |")
    print("+----------------------------------+-------------------+--------------------+")
    print(f"| Held-Out Top-1 Accuracy          | {r_rule['top1_accuracy_pct']:>15.2f}% | {r_nn['top1_accuracy_pct']:>16.2f}% |")
    print(f"| Held-Out Top-3 Accuracy          | {r_rule['top3_accuracy_pct']:>15.2f}% | {r_nn['top3_accuracy_pct']:>16.2f}% |")
    print(f"| Macro Precision                  | {r_rule['macro_precision']:>17.4f} | {r_nn['macro_precision']:>18.4f} |")
    print(f"| Macro Recall                     | {r_rule['macro_recall']:>17.4f} | {r_nn['macro_recall']:>18.4f} |")
    print(f"| Macro F1-Score                   | {r_rule['macro_f1']:>17.4f} | {r_nn['macro_f1']:>18.4f} |")
    print(f"| Mean Forward Latency             | {r_rule['mean_latency_ms']:>14.2f} ms | {r_nn['mean_latency_ms']:>15.2f} ms |")
    print(f"| Inference Throughput             | {r_rule['fps_throughput']:>14.1f} FPS| {r_nn['fps_throughput']:>15.1f} FPS|")
    print(f"| Total Test Samples Evaluated     | {report['total_test_samples']:>17d} | {report['total_test_samples']:>18d} |")
    print(f"| Total Errors / Confusions        | {r_rule['total_confusions']:>17d} | {r_nn['total_confusions']:>18d} |")
    print("+----------------------------------+-------------------+--------------------+")

    if report["top_rule_confusions"]:
        print("\nTop Rule-Based Confusions:")
        for c in report["top_rule_confusions"]:
            print(f"  - True [{c['true']}] predicted as [{c['predicted']}] ({c['count']} times)")

    if report["top_nn_confusions"]:
        print("\nTop Neural Network Confusions:")
        for c in report["top_nn_confusions"]:
            print(f"  - True [{c['true']}] predicted as [{c['predicted']}] ({c['count']} times)")


if __name__ == "__main__":
    dm = DatasetManager()
    _, _, test_recs = dm.create_person_independent_split(test_users=["user_test"])
    if not test_recs:
        from train_stgcn import seed_multiperson_dataset_if_needed
        seed_multiperson_dataset_if_needed(dm)
        _, _, test_recs = dm.create_person_independent_split(test_users=["user_test"])

    evaluator = Evaluator()
    rep = evaluator.run_benchmark_on_held_out(test_recs)
    print_evaluation_summary(rep)
    print(f"\nEvaluation report saved to: {os.path.join(REPORTS_DIR, 'evaluation_report.json')}")
