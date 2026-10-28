"""
SignBridge Dataset Manager
Handles collection, persistence, loading, indexing, and person-independent splitting
of MediaPipe 3D skeletal landmark sequences for all 42 Indian Sign Language (ISL) signs.
Supports both real webcam recordings and procedural biomechanical synthetic samples.
"""

import os
import json
import time
import shutil
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

from config import VOCABULARY, VOCAB_TO_IDX, TOTAL_LANDMARKS, COORDINATE_DIM

DATASET_ROOT = os.path.join(os.path.dirname(__file__), "dataset")
RAW_DIR = os.path.join(DATASET_ROOT, "raw")
AUG_DIR = os.path.join(DATASET_ROOT, "augmented")
SPLITS_DIR = os.path.join(DATASET_ROOT, "splits")
MANIFEST_PATH = os.path.join(DATASET_ROOT, "manifest.json")
MANIFEST_BAK_PATH = os.path.join(DATASET_ROOT, "manifest.json.bak")


class DatasetManager:
    def __init__(self, dataset_dir: str = DATASET_ROOT):
        self.dataset_dir = os.path.abspath(dataset_dir)
        self.raw_dir = os.path.join(self.dataset_dir, "raw")
        self.aug_dir = os.path.join(self.dataset_dir, "augmented")
        self.splits_dir = os.path.join(self.dataset_dir, "splits")
        self.manifest_path = os.path.join(self.dataset_dir, "manifest.json")
        self.manifest_bak_path = os.path.join(self.dataset_dir, "manifest.json.bak")
        self._ensure_directories()
        self._sanitize_existing_manifest()

    def _ensure_directories(self):
        for d in [self.dataset_dir, self.raw_dir, self.aug_dir, self.splits_dir]:
            os.makedirs(d, exist_ok=True)
        if not os.path.exists(self.manifest_path):
            self._save_manifest({"samples": [], "created_at": time.time(), "version": "1.1"})

    def _load_manifest(self) -> Dict[str, Any]:
        if not os.path.exists(self.manifest_path):
            return {"samples": [], "version": "1.1"}
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[DatasetManager Warning] Failed to load {self.manifest_path}: {e}")
            if os.path.exists(self.manifest_bak_path):
                try:
                    with open(self.manifest_bak_path, "r", encoding="utf-8") as f_bak:
                        data = json.load(f_bak)
                        print("[DatasetManager Notice] Successfully recovered manifest from backup.")
                        return data
                except Exception:
                    pass
            raise RuntimeError(f"Corrupt manifest file at {self.manifest_path}. Please inspect or restore from backup.")

    def _save_manifest(self, data: Dict[str, Any]):
        # Keep safe backup before overwriting
        if os.path.exists(self.manifest_path):
            try:
                shutil.copy2(self.manifest_path, self.manifest_bak_path)
            except Exception:
                pass

        temp_path = self.manifest_path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, self.manifest_path)

    def _sanitize_existing_manifest(self):
        """
        Migrates legacy absolute Windows paths to relative paths and removes stray test entries.
        """
        try:
            manifest = self._load_manifest()
            modified = False
            clean_samples = []

            for s in manifest.get("samples", []):
                # Remove stray one-off manual test entries
                if s.get("user_id") == "test_signer":
                    modified = True
                    continue

                # Ensure relative path stored for cross-platform and directory relocation safety
                fn = s.get("filename") or os.path.basename(s.get("filepath", ""))
                rel_path = os.path.join("raw", fn).replace("\\", "/")
                if s.get("relative_path") != rel_path:
                    s["relative_path"] = rel_path
                    modified = True

                # Honestly label procedural data
                meta = s.get("metadata", {})
                if meta.get("source") == "ground_truth_motion_capture":
                    meta["source"] = "procedural_biomechanical_synthesis"
                    modified = True

                clean_samples.append(s)

            if modified:
                manifest["samples"] = clean_samples
                manifest["updated_at"] = time.time()
                self._save_manifest(manifest)
        except Exception:
            pass

    def save_recording(
        self,
        sequence: np.ndarray,
        gloss: str,
        user_id: str,
        fps: float = 30.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Saves a recorded landmark sequence as compressed .npz.
        Stores relative paths in manifest for portability.
        """
        gloss = gloss.upper().strip()
        if gloss not in VOCAB_TO_IDX or gloss == "<BLANK>":
            raise ValueError(f"Invalid gloss '{gloss}'. Must be one of {len(VOCABULARY)-1} vocabulary signs.")

        arr = np.array(sequence, dtype=np.float32)
        if arr.ndim == 2 and arr.shape[1] == TOTAL_LANDMARKS * COORDINATE_DIM:
            arr = arr.reshape(-1, TOTAL_LANDMARKS, COORDINATE_DIM)
        elif arr.ndim != 3 or arr.shape[1] != TOTAL_LANDMARKS or arr.shape[2] != COORDINATE_DIM:
            raise ValueError(f"Expected landmark shape (T, {TOTAL_LANDMARKS}, {COORDINATE_DIM}), got {arr.shape}")

        T = arr.shape[0]
        timestamp = time.time()
        file_id = f"{user_id}_{gloss}_{int(timestamp * 1000)}"
        filename = f"{file_id}.npz"
        filepath = os.path.join(self.raw_dir, filename)
        relative_path = os.path.join("raw", filename).replace("\\", "/")

        np.savez_compressed(
            filepath,
            landmarks=arr,
            gloss=gloss,
            user_id=user_id,
            fps=float(fps),
            timestamp=timestamp,
            num_frames=T
        )

        entry = {
            "file_id": file_id,
            "filename": filename,
            "relative_path": relative_path,
            "filepath": filepath,
            "gloss": gloss,
            "user_id": user_id,
            "num_frames": T,
            "fps": round(float(fps), 2),
            "timestamp": timestamp,
            "metadata": metadata or {}
        }

        manifest = self._load_manifest()
        manifest["samples"].append(entry)
        manifest["updated_at"] = time.time()
        self._save_manifest(manifest)

        return entry

    def resolve_filepath(self, filepath_or_relative: str) -> str:
        """
        Resolves an absolute path or relative path to a live file on disk.
        """
        if os.path.isabs(filepath_or_relative) and os.path.exists(filepath_or_relative):
            return filepath_or_relative

        # Try relative to dataset dir
        candidate = os.path.join(self.dataset_dir, filepath_or_relative)
        if os.path.exists(candidate):
            return candidate

        # Try raw dir with basename
        base_cand = os.path.join(self.raw_dir, os.path.basename(filepath_or_relative))
        if os.path.exists(base_cand):
            return base_cand

        return filepath_or_relative

    def load_sample(self, filepath: str) -> Dict[str, Any]:
        """
        Loads an NPZ sample from disk, resolving paths robustly.
        """
        resolved = self.resolve_filepath(filepath)
        data = np.load(resolved, allow_pickle=True)
        return {
            "landmarks": data["landmarks"],
            "gloss": str(data["gloss"]),
            "user_id": str(data["user_id"]),
            "fps": float(data.get("fps", 30.0)),
            "timestamp": float(data.get("timestamp", 0.0))
        }

    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Returns comprehensive breakdown of recorded dataset.
        """
        manifest = self._load_manifest()
        samples = manifest.get("samples", [])

        per_sign_counts = {token: 0 for token in VOCABULARY if token != "<BLANK>"}
        per_user_counts: Dict[str, int] = {}
        total_frames = 0

        for s in samples:
            g = s.get("gloss")
            u = s.get("user_id")
            if g in per_sign_counts:
                per_sign_counts[g] += 1
            per_user_counts[u] = per_user_counts.get(u, 0) + 1
            total_frames += s.get("num_frames", 0)

        num_signs_with_data = sum(1 for c in per_sign_counts.values() if c > 0)

        return {
            "total_samples": len(samples),
            "num_vocabulary_signs": len(per_sign_counts),
            "signs_covered": num_signs_with_data,
            "coverage_pct": round((num_signs_with_data / max(1, len(per_sign_counts))) * 100, 1),
            "per_sign_counts": per_sign_counts,
            "per_user_counts": per_user_counts,
            "users": sorted(list(per_user_counts.keys())),
            "total_frames_recorded": total_frames,
            "manifest_path": self.manifest_path
        }

    def create_person_independent_split(
        self,
        test_users: Optional[List[str]] = None,
        val_users: Optional[List[str]] = None
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Partitions recorded samples by person/subject using exact user_id matching
        so that the evaluation test set contains ONLY signers unseen during training.
        """
        if test_users is None:
            test_users = ["user_test", "held_out_signer", "user_04"]
        if val_users is None:
            val_users = ["user_03"]

        test_user_set = set(test_users)
        val_user_set = set(val_users)

        manifest = self._load_manifest()
        samples = manifest.get("samples", [])

        train_set, val_set, test_set = [], [], []

        for s in samples:
            u = s.get("user_id", "")
            # Exact match instead of loose substring matching
            if u in test_user_set:
                test_set.append(s)
            elif u in val_user_set:
                val_set.append(s)
            else:
                train_set.append(s)

        # Fallback if split leaves test empty
        if not test_set and len(samples) > 2:
            all_users = sorted(list(set(s.get("user_id") for s in samples)))
            if len(all_users) >= 2:
                auto_test_user = all_users[-1]
                test_set = [s for s in samples if s.get("user_id") == auto_test_user]
                train_set = [s for s in samples if s.get("user_id") != auto_test_user]

        split_meta = {
            "train_count": len(train_set),
            "val_count": len(val_set),
            "test_count": len(test_set),
            "test_users": test_users,
            "val_users": val_users,
            "train_users": sorted(list(set(s.get("user_id") for s in train_set))),
            "generated_at": time.time()
        }

        with open(os.path.join(self.splits_dir, "person_split.json"), "w", encoding="utf-8") as f:
            json.dump(split_meta, f, indent=2)

        return train_set, val_set, test_set
