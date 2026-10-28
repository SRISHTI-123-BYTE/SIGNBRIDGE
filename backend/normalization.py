"""
SignBridge Geometric Invariance & Coordinate Normalization Engine
Implements torso-centering, biometric shoulder scale normalization, velocity extraction,
and Non-Manual Marker (NMM) facial affect analysis.
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
from config import TOTAL_LANDMARKS, COORDINATE_DIM, NUM_POSE_LANDMARKS, NUM_HAND_LANDMARKS

# Keypoint indices in MediaPipe Holistic upper body subset:
# Left Shoulder = 11, Right Shoulder = 12 (in standard MediaPipe Pose)
# Nose = 0, Left Eye = 2, Right Eye = 5, Left Ear = 7, Right Ear = 8, Left Wrist = 15, Right Wrist = 16
LEFT_SHOULDER_IDX = 11
RIGHT_SHOULDER_IDX = 12
NOSE_IDX = 0
LEFT_EYE_IDX = 2
RIGHT_EYE_IDX = 5
LEFT_WRIST_IDX = 15
RIGHT_WRIST_IDX = 16


class LandmarkNormalizer:
    """
    Applies affine transformations to 3D skeletal landmark coordinates to achieve
    complete geometric invariance with respect to user height, body shape, camera distance,
    and translation.
    """

    def __init__(self, eps: float = 1e-6):
        self.eps = eps
        self.prev_normalized_landmarks: Optional[np.ndarray] = None

    def normalize_frame(self, raw_landmarks: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Normalizes a single frame of raw 3D landmarks (N, 3) or flattened (N*3).
        
        Args:
            raw_landmarks: Array of shape (TOTAL_LANDMARKS, 3) or (TOTAL_LANDMARKS * 3,)
            
        Returns:
            Tuple of:
                - normalized_landmarks: Array of shape (TOTAL_LANDMARKS, 3)
                - metadata: Dict containing scale factor, center point, and NMM metrics
        """
        landmarks = np.array(raw_landmarks, dtype=np.float32)
        if landmarks.ndim == 1:
            landmarks = landmarks.reshape(-1, COORDINATE_DIM)

        # Fallback if fewer landmarks provided
        if landmarks.shape[0] < NUM_POSE_LANDMARKS:
            padded = np.zeros((TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
            padded[:landmarks.shape[0]] = landmarks
            landmarks = padded
        elif landmarks.shape[0] < TOTAL_LANDMARKS:
            padded = np.zeros((TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
            padded[:landmarks.shape[0]] = landmarks
            landmarks = padded

        # 1. Compute Torso Center = (P_left_shoulder + P_right_shoulder) / 2
        left_shoulder = landmarks[LEFT_SHOULDER_IDX]
        right_shoulder = landmarks[RIGHT_SHOULDER_IDX]
        
        # If shoulders are degenerate (e.g. zeros in hand-only test), use upper body centroid
        shoulder_dist = np.linalg.norm(left_shoulder - right_shoulder)
        if shoulder_dist < self.eps:
            # Fallback center to mean of pose landmarks or origin
            pose_pts = landmarks[:NUM_POSE_LANDMARKS]
            valid_mask = np.any(pose_pts != 0, axis=-1)
            if np.any(valid_mask):
                center = np.mean(pose_pts[valid_mask], axis=0)
            else:
                center = np.zeros(3, dtype=np.float32)
            scale = 1.0
        else:
            center = (left_shoulder + right_shoulder) / 2.0
            scale = float(shoulder_dist)

        # Prevent division by zero
        scale = max(scale, self.eps)

        # 2. Geometric Affine Normalization: P_hat = (P - P_center) / scale
        normalized = (landmarks - center) / scale

        # Standardize orientation: Person's right shoulder must be at +X, left shoulder at -X
        # In webcam/camera selfie view, left_shoulder.x > right_shoulder.x
        if normalized[LEFT_SHOULDER_IDX, 0] > normalized[RIGHT_SHOULDER_IDX, 0]:
            normalized[:, 0] = -normalized[:, 0]

        # 3. Non-Manual Marker (NMM) Analysis (Facial affect, question indicators, head motion)
        nmm_metrics = self.extract_non_manual_markers(landmarks, normalized)

        # 4. Velocity computation if previous frame available
        if self.prev_normalized_landmarks is not None:
            velocity = normalized - self.prev_normalized_landmarks
            speed = np.mean(np.linalg.norm(velocity, axis=-1))
        else:
            velocity = np.zeros_like(normalized)
            speed = 0.0

        self.prev_normalized_landmarks = normalized.copy()

        metadata = {
            "scale": scale,
            "center": center.tolist(),
            "mean_joint_speed": float(speed),
            "nmm": nmm_metrics
        }

        return normalized, metadata

    def extract_non_manual_markers(self, raw_pts: np.ndarray, norm_pts: np.ndarray) -> Dict[str, Any]:
        """
        Analyzes facial contours and head posture to extract grammatical Non-Manual Markers (NMMs).
        In ISL, facial expressions differentiate questions, negations, imperatives, and emotions.
        """
        # Pose and facial landmark subsets
        nose = norm_pts[NOSE_IDX]
        left_eye = norm_pts[LEFT_EYE_IDX]
        right_eye = norm_pts[RIGHT_EYE_IDX]

        # Inter-ocular distance
        eye_dist = np.linalg.norm(left_eye - right_eye) + self.eps

        # Head roll/tilt calculation (angle between eye line and horizontal)
        d_y = right_eye[1] - left_eye[1]
        d_x = right_eye[0] - left_eye[0]
        head_roll_deg = float(np.degrees(np.arctan2(d_y, d_x)))

        # Head pitch (nose vertical offset relative to mid-eye point)
        mid_eye = (left_eye + right_eye) / 2.0
        head_pitch = float((nose[1] - mid_eye[1]) / eye_dist)

        # Head yaw (lateral nose asymmetry relative to eyes)
        dist_nose_left = np.linalg.norm(nose[:2] - left_eye[:2])
        dist_nose_right = np.linalg.norm(nose[:2] - right_eye[:2])
        head_yaw = float((dist_nose_right - dist_nose_left) / eye_dist)

        # Question / Interrogative marker detection (Eyebrow raise + slight forward head pitch)
        is_interrogative = bool(head_pitch > 0.65 or abs(head_roll_deg) > 12.0)
        
        # Urgency / Intensity marker (High movement dynamics + furrowed / focused posture)
        is_urgent = bool(head_pitch > 0.75)

        # Head gestures
        head_nod = bool(abs(head_pitch - 0.5) > 0.25)
        head_shake = bool(abs(head_yaw) > 0.35)

        return {
            "head_roll_deg": round(head_roll_deg, 2),
            "head_pitch": round(head_pitch, 3),
            "head_yaw": round(head_yaw, 3),
            "is_interrogative": is_interrogative,
            "is_urgent": is_urgent,
            "head_nod": head_nod,
            "head_shake": head_shake,
            "expression_tag": "INTERROGATIVE" if is_interrogative else ("URGENT" if is_urgent else "NEUTRAL")
        }

    def normalize_sequence(self, sequence: np.ndarray) -> np.ndarray:
        """
        Normalizes a temporal sequence of frames (T, TOTAL_LANDMARKS, 3) or (T, TOTAL_LANDMARKS*3).
        Always returns array of shape (T, TOTAL_LANDMARKS, COORDINATE_DIM).
        """
        seq = np.array(sequence, dtype=np.float32)
        if seq.ndim == 2:
            T, D = seq.shape
            seq = seq.reshape(T, -1, COORDINATE_DIM)
        
        T, N, C = seq.shape
        normalized_seq = np.zeros((T, TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
        for t in range(T):
            norm_frame, _ = self.normalize_frame(seq[t])
            normalized_seq[t] = norm_frame
            
        return normalized_seq
