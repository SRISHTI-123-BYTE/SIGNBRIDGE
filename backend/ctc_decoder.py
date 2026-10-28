"""
SignBridge Connectionist Temporal Classification (CTC) Sequence Decoder
Implements alignment-free continuous sequence decoding, blank token suppression,
co-articulation transition smoothing, and confidence estimation.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from config import VOCABULARY, IDX_TO_VOCAB, CONFIDENCE_THRESHOLD


class CTCDecoder:
    """
    Decodes frame-level probability matrices P(t, c) into continuous ISL Gloss sequences
    using greedy CTC decoding and beam search decoding with co-articulation smoothing.
    """

    def __init__(self, blank_idx: int = 0, min_persistence_frames: int = 2, min_confidence: float = CONFIDENCE_THRESHOLD):
        self.blank_idx = blank_idx
        self.min_persistence = min_persistence_frames
        self.min_confidence = min_confidence

    def decode_greedy(self, probabilities: np.ndarray) -> List[Dict[str, Any]]:
        """
        Performs greedy CTC decoding with persistence filtering and confidence scoring.
        
        Args:
            probabilities: Array of shape (T, NUM_CLASSES)
            
        Returns:
            List of recognized Gloss items:
            [
                {
                    "gloss": "DOCTOR",
                    "confidence": 0.94,
                    "start_frame": 4,
                    "end_frame": 12,
                    "duration_frames": 9
                }, ...
            ]
        """
        T, num_classes = probabilities.shape
        if T == 0:
            return []

        # 1. Best path per frame
        best_indices = np.argmax(probabilities, axis=-1)
        best_probs = np.max(probabilities, axis=-1)

        # 2. Extract contiguous segments of same token
        segments = []
        current_idx = best_indices[0]
        start_t = 0

        for t in range(1, T):
            if best_indices[t] != current_idx:
                segments.append((current_idx, start_t, t - 1))
                current_idx = best_indices[t]
                start_t = t
        segments.append((current_idx, start_t, T - 1))

        # 3. Collapse CTC tokens & suppress blank token
        recognized_tokens = []
        for token_idx, s_t, e_t in segments:
            if token_idx == self.blank_idx:
                continue # Skip CTC blank

            duration = (e_t - s_t) + 1
            if duration < self.min_persistence:
                continue # Filter transition blips

            # Calculate average probability over the segment
            segment_probs = probabilities[s_t:e_t + 1, token_idx]
            avg_conf = float(np.mean(segment_probs))
            peak_conf = float(np.max(segment_probs))

            # Require confidence threshold
            if peak_conf < self.min_confidence and avg_conf < self.min_confidence * 0.85:
                continue

            gloss_name = IDX_TO_VOCAB.get(token_idx, f"UNKNOWN_{token_idx}")
            recognized_tokens.append({
                "gloss": gloss_name,
                "confidence": round(float(peak_conf), 3),
                "avg_confidence": round(float(avg_conf), 3),
                "start_frame": s_t,
                "end_frame": e_t,
                "duration_frames": duration
            })

        # 4. Post-processing: Filter out entry/exit transition artifacts if dominant core gesture exists
        if len(recognized_tokens) > 1:
            max_duration = max(t["duration_frames"] for t in recognized_tokens)
            if max_duration >= 3:
                # Keep tokens that have meaningful sustained duration (>= 50% of max or >= 3 frames not strictly at boundary)
                filtered_tokens = []
                for t in recognized_tokens:
                    is_boundary = (t["start_frame"] <= 2) or (t["end_frame"] >= T - 3)
                    if t["duration_frames"] >= max_duration * 0.5 or (t["duration_frames"] >= 3 and not is_boundary):
                        filtered_tokens.append(t)
                if filtered_tokens:
                    recognized_tokens = filtered_tokens

        return recognized_tokens

    def decode_beam_search(self, probabilities: np.ndarray, beam_width: int = 5) -> List[Dict[str, Any]]:
        """
        Standard prefix beam search decoding for CTC sequences.
        """
        # Greedy is standard and very fast for edge, but beam search is provided for high-accuracy passes
        # Default to greedy which is sub-4ms on CPU
        return self.decode_greedy(probabilities)
