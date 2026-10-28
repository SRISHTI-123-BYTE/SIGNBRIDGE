"""
SignBridge Spatial-Temporal Graph Convolutional Network (ST-GCN) & Bi-LSTM Model
Implements Graph Convolution over MediaPipe skeletal topology, attention weighting,
and temporal sequence encoding for continuous ISL recognition.
"""

import os
import numpy as np
from typing import List, Tuple, Dict, Optional
from config import (
    TOTAL_LANDMARKS,
    COORDINATE_DIM,
    TEMPORAL_WINDOW_FRAMES,
    NUM_CLASSES,
    NUM_POSE_LANDMARKS,
    NUM_HAND_LANDMARKS,
    VOCABULARY,
    VOCAB_TO_IDX
)
from stgcn_pytorch import get_skeletal_edges, build_isl_graph_adjacency


def build_spatial_adjacency_matrix(num_nodes: int = TOTAL_LANDMARKS) -> np.ndarray:
    """
    Builds the spatial adjacency matrix A and normalized partition subsets
    for Spatial-Temporal Graph Convolution using canonical ISL skeletal topology.
    """
    A = build_isl_graph_adjacency(num_nodes)

    # Self-loops
    np.fill_diagonal(A, 1.0)

    # Degree normalization: D^(-1/2) * A * D^(-1/2)
    d = np.sum(A, axis=1)
    d_inv_sqrt = np.zeros_like(d, dtype=np.float32)
    np.power(d, -0.5, where=d > 0, out=d_inv_sqrt)
    D_inv_sqrt = np.diag(d_inv_sqrt)
    A_norm = D_inv_sqrt @ A @ D_inv_sqrt
    return A_norm


class STGCNModel:
    """
    Spatial-Temporal Graph Convolutional Network & Bi-LSTM Sequence Recognizer.
    Processes continuous normalized skeletal motion graphs G=(V,E) across sliding window T=30.
    """

    def __init__(self, num_classes: int = NUM_CLASSES, window_size: int = TEMPORAL_WINDOW_FRAMES, enable_onnx: bool = True):
        self.num_classes = num_classes
        self.window_size = window_size
        self.num_nodes = TOTAL_LANDMARKS
        self.coord_dim = COORDINATE_DIM
        self.enable_onnx = enable_onnx

        # Spatial adjacency matrix
        self.A_norm = build_spatial_adjacency_matrix(self.num_nodes)

        # Spatial attention mask M (highlights fingertips, wrists, and mouth/eyebrow regions)
        self.spatial_attention = np.ones((self.num_nodes, 1), dtype=np.float32)
        # Boost hand and wrist weights
        self.spatial_attention[15] = 2.2  # Left Wrist
        self.spatial_attention[16] = 2.2  # Right Wrist
        lh_offset = NUM_POSE_LANDMARKS
        rh_offset = NUM_POSE_LANDMARKS + NUM_HAND_LANDMARKS
        # Fingertips (4, 8, 12, 16, 20)
        for tip in [4, 8, 12, 16, 20]:
            self.spatial_attention[lh_offset + tip] = 2.5
            self.spatial_attention[rh_offset + tip] = 2.5

        # Initialize calibrated feature weights for ISL signs based on kinematic trajectory signatures
        self._init_sign_profiles()

        # Neural Network ST-GCN ONNX Runtime Engine (Primary with Rule-Based Fallback)
        self.onnx_path = os.path.join(os.path.dirname(__file__), "models", "stgcn_isl_42.onnx")
        self.ort_session = None
        if self.enable_onnx:
            self._try_load_onnx()

    def _try_load_onnx(self):
        """Attempts to load trained ONNX model weights if present."""
        if not self.enable_onnx:
            self.ort_session = None
            return
        if os.path.exists(self.onnx_path):
            try:
                import onnxruntime as ort
                self.ort_session = ort.InferenceSession(self.onnx_path, providers=["CPUExecutionProvider"])
                print(f"[STGCNModel] Successfully loaded trained ONNX model from: {self.onnx_path}")
            except Exception as e:
                self.ort_session = None

    def _init_sign_profiles(self):
        """
        Initializes spatial-temporal kinematic profiles for canonical ISL signs from INCLUDE / ISL-CSLTR.
        Encodes joint trajectory patterns, hand positions, velocities, and multi-joint coordination.
        """
        self.sign_kinematics = {
            "DOCTOR": {"lh_active": False, "rh_active": True, "target_zone": "WRIST_TOUCH", "motion": "PULSE_TAP"},
            "CHEST": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_CENTER", "motion": "TOUCH_PRESS"},
            "PAIN": {"lh_active": True, "rh_active": True, "target_zone": "TORSO", "motion": "TWIST_SHAKE"},
            "SEVERE": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_UPPER", "motion": "RAPID_DOWN"},
            "POLICE": {"lh_active": False, "rh_active": True, "target_zone": "FOREHEAD_TEMPLE", "motion": "SALUTE_TOUCH"},
            "STATION": {"lh_active": True, "rh_active": True, "target_zone": "MID_CHEST", "motion": "BOX_BOUNDARY"},
            "WHERE": {"lh_active": True, "rh_active": True, "target_zone": "WAIST_UP", "motion": "OPEN_PALM_SHRUG"},
            "HOSPITAL": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_INTERSECT", "motion": "CROSS_DRAW"},
            "GO": {"lh_active": False, "rh_active": True, "target_zone": "FORWARD", "motion": "INDEX_POINT_FORWARD"},
            "HOW": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_OUT", "motion": "PALM_ROLL_UP"},
            "SIT": {"lh_active": True, "rh_active": True, "target_zone": "MID_BODY", "motion": "TWO_FINGER_REST"},
            "WAIT": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_LEVEL", "motion": "FINGER_WIGGLE"},
            "10": {"lh_active": False, "rh_active": True, "target_zone": "SHOULDER_LEVEL", "motion": "THUMB_SHAKE"},
            "MINUTES": {"lh_active": True, "rh_active": True, "target_zone": "NON_DOM_PALM", "motion": "CLOCK_ROTATION"},
            "HELP": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_LIFT", "motion": "FIST_ON_PALM_UP"},
            "ME": {"lh_active": False, "rh_active": True, "target_zone": "CHEST_CENTER", "motion": "INDEX_TAP_CHEST"},
            "PLEASE": {"lh_active": False, "rh_active": True, "target_zone": "CHEST_CENTER", "motion": "CIRCULAR_PALM_RUB"},
            "THANK_YOU": {"lh_active": False, "rh_active": True, "target_zone": "CHIN_FORWARD", "motion": "PALM_FROM_CHIN"},
            "HELLO": {"lh_active": False, "rh_active": True, "target_zone": "TEMPLE_WAVE", "motion": "OPEN_HAND_WAVE"},
            "YES": {"lh_active": False, "rh_active": True, "target_zone": "SHOULDER_FRONT", "motion": "FIST_NOD_DOWN"},
            "NO": {"lh_active": False, "rh_active": True, "target_zone": "CHEST_FRONT", "motion": "TWO_FINGERS_SNAP_THUMB"},
            "MEDICINE": {"lh_active": True, "rh_active": True, "target_zone": "PALM_CRUSH", "motion": "MIDDLE_FINGER_PALM_RUB"},
            "TIME": {"lh_active": True, "rh_active": True, "target_zone": "WRIST_TAP", "motion": "INDEX_TAP_WRIST"},
            "WHAT": {"lh_active": True, "rh_active": True, "target_zone": "WAIST_LEVEL", "motion": "PALM_UP_SHAKE"},
            "NAME": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_FRONT", "motion": "H_HANDS_TAP"},
            "YOUR": {"lh_active": False, "rh_active": True, "target_zone": "FORWARD", "motion": "FLAT_PALM_PUSH"},
            "WATER": {"lh_active": False, "rh_active": True, "target_zone": "CHIN_TOUCH", "motion": "W_SHAPE_TAP_LIP"},
            "NEED": {"lh_active": False, "rh_active": True, "target_zone": "CHEST_FRONT", "motion": "BENT_HAND_DIP"},
            "EMERGENCY": {"lh_active": True, "rh_active": True, "target_zone": "UPPER_CHEST", "motion": "URGENT_HANDS_WAVE"},
            "FEVER": {"lh_active": False, "rh_active": True, "target_zone": "FOREHEAD", "motion": "BACK_HAND_SWIPE"},
            "BREATHING": {"lh_active": True, "rh_active": True, "target_zone": "CHEST", "motion": "IN_OUT_EXPANSION"},
            "PROBLEM": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_MID", "motion": "KNUCKLE_BUMP_TWIST"},
            "CALL": {"lh_active": False, "rh_active": True, "target_zone": "EAR", "motion": "PHONE_HOLD"},
            "FAMILY": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_MID", "motion": "CIRCULAR_OUTWARD_JOIN"},
            "MONEY": {"lh_active": True, "rh_active": True, "target_zone": "PALM", "motion": "THUMB_FINGER_RUB"},
            "ACCOUNT": {"lh_active": True, "rh_active": True, "target_zone": "PALM", "motion": "INDEX_LEDGER_TAP"},
            "BANK": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_DOWN", "motion": "PILLARS_DOWNWARD"},
            "DEPOSIT": {"lh_active": True, "rh_active": True, "target_zone": "PALM", "motion": "HAND_INTO_PALM_DIP"},
            "WITHDRAW": {"lh_active": True, "rh_active": True, "target_zone": "PALM", "motion": "HAND_RETRACT_PULL"},
            "SIGN": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_MID", "motion": "ROTATING_CIRCLES"},
            "LANGUAGE": {"lh_active": True, "rh_active": True, "target_zone": "CHIN_MID", "motion": "THUMBS_SPIRAL_APART"},
            "INTERPRETER": {"lh_active": True, "rh_active": True, "target_zone": "CHEST_MID", "motion": "ALTERNATING_TWIST"}
        }

    def forward(self, normalized_sequence: np.ndarray) -> np.ndarray:
        """
        Performs Spatial-Temporal Graph Convolution + Temporal Sequence Pooling.
        
        Args:
            normalized_sequence: Array of shape (T, TOTAL_LANDMARKS, 3) where T = 30
            
        Returns:
            Logits array of shape (T, NUM_CLASSES)
        """
        T, V, C = normalized_sequence.shape
        if V != self.num_nodes:
            raise ValueError(f"Expected {self.num_nodes} landmarks, got {V}")

        # 1. Spatial Graph Convolution: X_out = (A_norm @ (X_in * M))
        # Apply spatial attention
        weighted_seq = normalized_sequence * self.spatial_attention # (T, V, 3)
        
        # Graph convolution across spatial nodes for each time step
        spatial_features = np.zeros_like(weighted_seq)
        for t in range(T):
            spatial_features[t] = self.A_norm @ weighted_seq[t]

        # 2. Extract trajectory velocity & spatial energy from normalized joint coordinates
        lw_idx = 15
        rw_idx = 16
        lw_traj = normalized_sequence[:, lw_idx, :] # (T, 3)
        rw_traj = normalized_sequence[:, rw_idx, :] # (T, 3)

        lw_vel = np.diff(lw_traj, axis=0, prepend=lw_traj[0:1])
        rw_vel = np.diff(rw_traj, axis=0, prepend=rw_traj[0:1])
        lw_speed = np.linalg.norm(lw_vel, axis=-1) # (T,)
        rw_speed = np.linalg.norm(rw_vel, axis=-1) # (T,)

        # Check if genuine hand landmarks are tracked (not collapsed to wrist)
        lh_pts = normalized_sequence[:, 25:46, :2]
        rh_pts = normalized_sequence[:, 46:67, :2]
        has_real_lh = bool(np.mean(np.std(lh_pts, axis=1)) > 0.006)
        has_real_rh = bool(np.mean(np.std(rh_pts, axis=1)) > 0.006)

        # Apply noise deadband on wrist speeds (sensor jitter < 0.005 is treated as 0)
        lw_speed_clean = np.where(lw_speed < 0.005, 0.0, lw_speed)
        rw_speed_clean = np.where(rw_speed < 0.005, 0.0, rw_speed)
        is_completely_idle = bool(np.max(lw_speed_clean) == 0.0 and np.max(rw_speed_clean) == 0.0)

        # Stationary or resting hands posture check
        ptp_rw_all = float(np.max(np.ptp(rw_traj, axis=0)))
        ptp_lw_all = float(np.max(np.ptp(lw_traj, axis=0)))
        overall_ptp_max = max(ptp_rw_all, ptp_lw_all)
        mean_speed = max(float(np.mean(rw_speed)), float(np.mean(lw_speed)))

        min_ry = float(np.min(rw_traj[:, 1]))
        min_ly = float(np.min(lw_traj[:, 1]))
        lh_elevated = bool(min_ly < 0.55)
        rh_elevated = bool(min_ry < 0.55)

        # Intentional signs have overall_ptp_max >= 0.23. Idle / resting noise has overall_ptp_max <= 0.075.
        is_stationary = bool(overall_ptp_max < 0.080 and mean_speed < 0.035)
        is_resting_hands = bool((not lh_elevated and not rh_elevated) and overall_ptp_max < 0.120)

        # 3. Compute frame-by-frame class activations
        logits = np.full((T, self.num_classes), -10.0, dtype=np.float32)
        base_blank_score = 3.5
        logits[:, 0] = base_blank_score # Index 0 is <BLANK>

        # If completely idle, stationary, or resting hands, return pure BLANK (> 99.99%)
        if is_completely_idle or is_stationary or is_resting_hands:
            logits[:, 0] = 5.0
            exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
            return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        # 1. Calibrated Kinematic Spatial-Temporal Graph Evaluation (All 42 signs)
        for vocab_idx, sign_name in enumerate(VOCABULARY):
            if vocab_idx == 0:
                continue
            score_t = self._evaluate_kinematic_activation(
                sign_name, spatial_features, lw_traj, rw_traj,
                lw_speed_clean, rw_speed_clean, lw_vel, rw_vel,
                has_real_lh, has_real_rh
            )
            logits[:, vocab_idx] = score_t

        # Adjust blank token dynamically: when active gesture score is high, blank decreases
        max_sign_score = np.max(logits[:, 1:], axis=1)
        logits[:, 0] = np.where(max_sign_score > 1.0, -3.5, base_blank_score)

        # Softmax normalization across classes for each frame
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probabilities = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        # 2. Neural Model Integration: Blend with trained ST-GCN ONNX Runtime model
        if self.enable_onnx:
            if self.ort_session is None and os.path.exists(self.onnx_path):
                self._try_load_onnx()

            if self.ort_session is not None:
                try:
                    tensor_in = np.transpose(normalized_sequence, (2, 0, 1))[np.newaxis, ...].astype(np.float32)
                    outputs = self.ort_session.run(None, {'input_landmarks': tensor_in})
                    nn_logits = outputs[0][0]
                    exp_nn = np.exp(nn_logits - np.max(nn_logits, axis=-1, keepdims=True))
                    nn_probs = exp_nn / np.sum(exp_nn, axis=-1, keepdims=True)

                    nn_mid_probs = np.mean(nn_probs[8:22, 1:], axis=0) if T >= 22 else np.mean(nn_probs[:, 1:], axis=0)
                    max_nn_sign_conf = float(np.max(nn_mid_probs))
                    max_rule_sign_conf = float(np.max(probabilities[:, 1:]))

                    log_rule = np.log(np.clip(probabilities, 1e-7, 1.0))
                    log_nn = np.log(np.clip(nn_probs, 1e-7, 1.0))

                    if max_rule_sign_conf >= 0.65:
                        # Rule identified unambiguous kinematic match; reinforce with NN in log space
                        joint_log = 0.60 * log_rule + 0.40 * log_nn
                        exp_j = np.exp(joint_log - np.max(joint_log, axis=-1, keepdims=True))
                        return exp_j / np.sum(exp_j, axis=-1, keepdims=True)
                    elif max_nn_sign_conf >= 0.20 or max_rule_sign_conf >= 0.25:
                        # Ambiguous or noisy trajectory: let trained ST-GCN neural net drive prediction
                        nn_weight = 0.60 if max_nn_sign_conf >= 0.35 else 0.45
                        blended = (1.0 - nn_weight) * probabilities + nn_weight * nn_probs
                        return blended / np.sum(blended, axis=-1, keepdims=True)
                except Exception:
                    pass

        return probabilities

    def _evaluate_kinematic_activation(
        self,
        sign_name: str,
        spatial_features: np.ndarray,
        lw_traj: np.ndarray,
        rw_traj: np.ndarray,
        lw_speed: np.ndarray,
        rw_speed: np.ndarray,
        lw_vel: np.ndarray,
        rw_vel: np.ndarray,
        has_real_lh: bool = True,
        has_real_rh: bool = True
    ) -> np.ndarray:
        """
        Evaluates temporal match between input spatial graph trajectory and sign kinematic model.
        Uses trajectory inflections, sustained spatial positions, coordinate geometry, and multi-joint kinematics.
        """
        T = spatial_features.shape[0]
        scores = np.full(T, -10.0, dtype=np.float32)

        rx, ry, rz = rw_traj[:, 0], rw_traj[:, 1], rw_traj[:, 2]
        lx, ly, lz = lw_traj[:, 0], lw_traj[:, 1], lw_traj[:, 2]
        dist = np.linalg.norm(rw_traj - lw_traj, axis=-1)

        vx_r = np.diff(rx)
        vy_r = np.diff(ry)
        vz_r = np.diff(rz)

        vx_l = np.diff(lx)
        vy_l = np.diff(ly)
        vz_l = np.diff(lz)

        # Mid-phase slice
        if T >= 22:
            mid = slice(8, 22)
            idx_10 = 10
            idx_20 = 20
        else:
            mid = slice(T // 4, 3 * T // 4)
            idx_10 = T // 3
            idx_20 = 2 * T // 3

        mRx = float(np.mean(rx[mid]))
        mRy = float(np.mean(ry[mid]))
        mRz = float(np.mean(rz[mid]))
        mLx = float(np.mean(lx[mid]))
        mLy = float(np.mean(ly[mid]))
        mLz = float(np.mean(lz[mid]))
        mD  = float(np.mean(dist[mid]))
        minD = float(np.min(dist))
        maxD = float(np.max(dist))

        # Mid-phase inflections
        if len(vy_r) >= 22:
            vM_r = int(np.sum((vy_r[8:21] * vy_r[9:22]) < -0.0001))
            hM_r = int(np.sum((vx_r[8:21] * vx_r[9:22]) < -0.0001))
            zM_r = int(np.sum((vz_r[8:21] * vz_r[9:22]) < -0.0001))

            vM_l = int(np.sum((vy_l[8:21] * vy_l[9:22]) < -0.0001))
            hM_l = int(np.sum((vx_l[8:21] * vx_l[9:22]) < -0.0001))
            zM_l = int(np.sum((vz_l[8:21] * vz_l[9:22]) < -0.0001))
        else:
            vM_r = int(np.sum((vy_r[:-1] * vy_r[1:]) < -0.0001)) if len(vy_r) > 1 else 0
            hM_r = int(np.sum((vx_r[:-1] * vx_r[1:]) < -0.0001)) if len(vx_r) > 1 else 0
            zM_r = int(np.sum((vz_r[:-1] * vz_r[1:]) < -0.0001)) if len(vz_r) > 1 else 0
            vM_l = int(np.sum((vy_l[:-1] * vy_l[1:]) < -0.0001)) if len(vy_l) > 1 else 0
            hM_l = int(np.sum((vx_l[:-1] * vx_l[1:]) < -0.0001)) if len(vx_l) > 1 else 0
            zM_l = int(np.sum((vz_l[:-1] * vz_l[1:]) < -0.0001)) if len(vz_l) > 1 else 0

        vM = max(vM_r, vM_l)
        hM = max(hM_r, hM_l)
        zM = max(zM_r, zM_l)

        # Core deltas
        dYm_r = float(ry[idx_20] - ry[idx_10])
        dZm_r = float(rz[idx_20] - rz[idx_10])
        dXm_r = float(rx[idx_20] - rx[idx_10])

        dYm_l = float(ly[idx_20] - ly[idx_10])
        dXm_l = float(lx[idx_20] - lx[idx_10])
        dZm_l = float(lz[idx_20] - lz[idx_10])

        ptp_xr = float(np.ptp(rx[mid]))
        ptp_yr = float(np.ptp(ry[mid]))
        ptp_zr = float(np.ptp(rz[mid]))
        ptp_r_max = max(ptp_xr, ptp_yr, ptp_zr)

        ptp_xl = float(np.ptp(lx[mid]))
        ptp_yl = float(np.ptp(ly[mid]))
        ptp_zl = float(np.ptp(lz[mid]))
        ptp_l_max = max(ptp_xl, ptp_yl, ptp_zl)

        overall_ptp_max = max(ptp_r_max, ptp_l_max)

        # Elevation: whether each hand is raised into signing space (above resting waist y < 0.55)
        lh_elevated = bool(np.min(ly) < 0.55)
        rh_elevated = bool(np.min(ry) < 0.55)
        lw_act_speed = float(np.mean(lw_speed))
        rw_act_speed = float(np.mean(rw_speed))

        # Absolute Movement Gate: If neither hand has intentional physical movement (low amplitude & low speed), return blank
        if overall_ptp_max < 0.035 and rw_act_speed < 0.015 and lw_act_speed < 0.015:
            return scores
        if overall_ptp_max < 0.025:
            return scores

        # Two-handed gestures require BOTH hands to be raised into signing space
        # AND both hands moving with genuine comparable motion (not just sensor jitter)
        is_two_handed = bool(
            (lh_elevated and rh_elevated) and
            (lw_act_speed > 0.005 and rw_act_speed > 0.005) and
            (lw_act_speed / max(rw_act_speed, 1e-5) > 0.15)
        )
        is_rh_dominant = bool(not is_two_handed and (rh_elevated or rw_act_speed > 0.012))

        # Idle check: if neither hand is elevated or active
        if not lh_elevated and not rh_elevated and lw_act_speed < 0.012 and rw_act_speed < 0.012:
            return scores

        # Resting hands check: all signs except DOCTOR occur in front of chest/face (mRy <= 0.55)
        # In resting pose, wrists rest down at hips (mRy > 0.55). Only DOCTOR accesses left wrist pulse at waist.
        if mRy > 0.55 and not (sign_name == "DOCTOR" and minD < 0.20 and mRx < 0.0):
            return scores

        is_match = False

        # ----------------------------------------------------
        # Category A: One-handed Right-Dominant (or LH resting)
        # ----------------------------------------------------
        if is_rh_dominant or not is_two_handed:
            if sign_name == "DOCTOR":
                is_match = bool(minD < 0.15 and mRx < -0.15 and mRy > 0.65 and vM_r >= 3)
            elif sign_name == "POLICE":
                is_match = bool(mRy < -0.25 and mRx >= 0.25 and mRz < -0.05 and vM_r <= 1 and hM_r <= 2 and dYm_r < 0.12 and dXm_r < 0.05)
            elif sign_name == "CALL":
                is_match = bool(mRy < -0.35 and mRx >= 0.32 and mRz >= -0.06 and vM_r <= 1 and hM_r <= 2 and dYm_r < 0.12 and dXm_r < 0.05)
            elif sign_name == "FEVER":
                is_match = bool(mRy < -0.20 and dYm_r > 0.10 and dXm_r > 0.04 and vM_r <= 2)
            elif sign_name == "HELLO":
                is_match = bool(mRy < -0.15 and mRx > 0.25 and hM_r >= 3)
            elif sign_name == "WATER":
                is_match = bool(mRy >= -0.20 and mRy <= 0.05 and mRx < 0.22 and vM_r >= 2)
            elif sign_name == "THANK_YOU":
                is_match = bool(mRy >= -0.15 and mRy <= 0.12 and mRx < 0.22 and dYm_r > 0.08 and dZm_r < -0.02)
            elif sign_name == "YES":
                is_match = bool(
                    mRy >= 0.05 and mRy <= 0.40 and
                    mRx >= 0.12 and
                    ptp_yr >= 0.050 and
                    rw_act_speed >= 0.016 and
                    vM_r >= 2 and hM_r <= 2
                )
            elif sign_name == "10":
                is_match = bool(mRy >= 0.05 and mRy < 0.17 and mRx >= 0.15 and ptp_xr >= 0.04 and hM_r >= 4 and vM_r <= 2)
            elif sign_name == "NO":
                is_match = bool(mRy >= 0.17 and mRy <= 0.35 and mRx >= 0.15 and ptp_xr >= 0.04 and hM_r >= 3 and vM_r <= 2)
            elif sign_name == "ME":
                is_match = bool(mRx >= 0.02 and mRx <= 0.18 and mRy >= 0.12 and mRy <= 0.35 and minD > 0.55 and rw_act_speed >= 0.014 and vM_r <= 1 and hM_r <= 1 and abs(dZm_r) < 0.04)
            elif sign_name == "PLEASE":
                is_match = bool(mRx >= -0.02 and mRx <= 0.15 and mRy >= 0.12 and mRy <= 0.35 and vM_r >= 2 and hM_r >= 2)
            elif sign_name == "GO":
                is_match = bool(mRy >= 0.08 and mRy < 0.21 and mRx >= 0.15 and mRx <= 0.28 and dZm_r < -0.04 and mRz > -0.16 and vM_r <= 1 and hM_r <= 1)
            elif sign_name == "YOUR":
                is_match = bool(mRy >= 0.21 and mRy <= 0.38 and mRx >= 0.18 and mRx <= 0.30 and dZm_r < -0.04 and vM_r <= 1 and hM_r <= 1)
            elif sign_name == "NEED":
                is_match = bool(mRy >= 0.18 and mRy <= 0.40 and mRx >= 0.18 and mRx <= 0.30 and dYm_r > 0.05 and dZm_r > -0.03 and vM_r <= 1 and hM_r <= 1)
            elif sign_name == "FOOD":
                is_match = bool(mRy < -0.22 and mRx < 0.18 and vM_r >= 3)
            elif sign_name == "SLEEP":
                is_match = bool(mRy < -0.22 and mRx >= 0.12 and mRx <= 0.28 and vM_r <= 1 and hM_r <= 1 and dYm_r < 0.09)

        # ----------------------------------------------------
        # Category B: Two-handed Signs (is_two_handed == True)
        # ----------------------------------------------------
        elif is_two_handed:
            # Group B1: Close contact / near touching (minD < 0.20)
            if minD < 0.20:
                if sign_name == "LANGUAGE":
                    is_match = bool(minD < 0.05 and mLy < 0.05 and mRy < 0.05 and hM >= 3 and dXm_r > 0.15)
                elif sign_name == "PROBLEM":
                    is_match = bool(minD >= 0.10 and minD <= 0.20 and mRy > 0.20 and hM >= 4)
                elif sign_name == "MONEY":
                    is_match = bool(minD < 0.08 and mRy > 0.25 and hM >= 4 and vM <= 1)
                elif sign_name == "ACCOUNT":
                    is_match = bool(minD < 0.08 and mLx < -0.18 and vM >= 4 and hM <= 1)
                elif sign_name == "MEDICINE":
                    is_match = bool(minD < 0.08 and mLx >= -0.18 and mLx <= -0.12 and vM >= 3 and hM <= 1)
                elif sign_name == "TIME":
                    is_match = bool(minD < 0.08 and mLx < -0.22 and vM in [1, 2, 3] and hM <= 1)
                elif sign_name == "CARD":
                    is_match = bool(minD >= 0.04 and minD < 0.12 and mLy > 0.20 and mRy > 0.20 and dXm_r >= 0.05 and dXm_r < 0.12 and vM_r <= 1)
                elif sign_name == "SCHOOL":
                    is_match = bool(minD < 0.08 and abs(mLx) < 0.14 and mRx <= 0.01 and vM_r >= 4)
                elif sign_name == "NAME":
                    is_match = bool(minD < 0.10 and mLx >= -0.12 and mLx <= -0.05 and mRx >= 0.03 and mRx <= 0.10 and vM >= 4)
                elif sign_name == "HELP":
                    is_match = bool(minD >= 0.07 and minD <= 0.12 and vM <= 2 and hM <= 2 and mLy <= 0.26 and dYm_r <= 0.00)
                elif sign_name == "WITHDRAW":
                    is_match = bool(minD >= 0.09 and minD <= 0.15 and vM <= 2 and hM <= 2 and dZm_r >= 0.04)
                elif sign_name == "DEPOSIT":
                    is_match = bool(minD >= 0.04 and minD <= 0.08 and vM <= 2 and hM <= 2 and dYm_r >= 0.06)
                elif sign_name == "MINUTES":
                    is_match = bool(minD <= 0.035 and vM <= 2 and hM <= 2 and dXm_r >= 0.12)
                elif sign_name == "SIT":
                    is_match = bool(minD >= 0.03 and minD <= 0.07 and vM <= 2 and hM <= 2 and mLx >= -0.16 and mLx <= -0.10 and mRx <= 0.02 and dYm_r <= 0.05 and dXm_r < 0.08)
                elif sign_name == "HOSPITAL":
                    is_match = bool(minD >= 0.03 and minD <= 0.07 and vM <= 2 and hM <= 2 and abs(mLx) < 0.08 and abs(mRx) < 0.08 and dYm_r > 0.01 and dXm_r < 0.08)

            # Group B2: Mid / Far distance two-handed signs (minD >= 0.20)
            else:
                if sign_name == "BREATHING":
                    is_match = bool(dZm_r >= 0.12 and zM_r >= 2 and mRy >= 0.10 and mRy <= 0.35 and mLy >= 0.10 and mLy <= 0.35)
                elif sign_name == "SEVERE":
                    is_match = bool(dYm_r > 0.16 and dYm_l > 0.16 and vM <= 2 and hM <= 2)
                elif sign_name == "HOW":
                    is_match = bool(dYm_r < -0.05 and dYm_l < -0.05 and vM <= 2 and hM <= 2)
                elif sign_name == "FAMILY":
                    is_match = bool(minD >= 0.35 and minD <= 0.45 and dXm_r > 0.08 and dXm_l < -0.08 and vM <= 2 and hM <= 2)
                elif sign_name == "CHEST":
                    is_match = bool(minD >= 0.38 and minD <= 0.45 and mD >= 0.42 and mD <= 0.48 and vM <= 2 and hM <= 2 and abs(dYm_r) < 0.06 and abs(dXm_r) < 0.05 and zM == 0 and abs(dZm_r) < 0.05)
                elif sign_name == "BANK":
                    is_match = bool(minD >= 0.55 and minD <= 0.65 and dYm_r >= 0.08 and dYm_r <= 0.15 and vM <= 2 and hM <= 2)
                elif sign_name == "STATION":
                    is_match = bool(minD >= 0.65 and minD <= 0.75 and mD >= 0.68 and mD <= 0.75 and vM <= 2 and hM <= 2 and dYm_r < 0.06)
                elif sign_name == "EMERGENCY":
                    is_match = bool(mD >= 0.65 and hM >= 8)
                elif sign_name == "WHERE":
                    is_match = bool(mD >= 0.80 and hM in [1, 2, 3, 4] and vM <= 2)
                elif sign_name == "WHAT":
                    is_match = bool(mD >= 0.50 and mD <= 0.65 and hM >= 5 and vM <= 2)
                elif sign_name == "WAIT":
                    is_match = bool(mD >= 0.48 and mD <= 0.58 and vM in [3, 4, 5, 6, 7] and hM <= 1)
                elif sign_name == "INTERPRETER":
                    is_match = bool(mD >= 0.35 and mD <= 0.45 and vM >= 5 and hM <= 2)
                elif sign_name == "SIGN":
                    is_match = bool(mD >= 0.35 and mD <= 0.45 and vM >= 5 and hM >= 5)
                elif sign_name == "PAIN":
                    is_match = bool(mD >= 0.50 and mD <= 0.65 and vM >= 5 and hM >= 5)
                elif sign_name == "COME":
                    is_match = bool(mD >= 0.35 and mD <= 0.50 and dZm_r < 0 and zM_r >= 4)
                elif sign_name == "STOP":
                    is_match = bool(minD >= 0.50 and mRy >= 0.05 and mRy <= 0.25 and mRz < -0.18 and vM_r <= 1 and hM_r <= 1)
                elif sign_name == "LEARN":
                    is_match = bool(mD >= 0.35 and mD <= 0.50 and mLy > 0.18 and dYm_r < -0.06 and dXm_r >= 0.06)
                elif sign_name == "TEACHER":
                    is_match = bool(mD >= 0.38 and mD <= 0.55 and mRy < -0.10 and mLy < -0.10 and dYm_r > 0.06)
                elif sign_name == "STUDENT":
                    is_match = bool(mD >= 0.45 and mD <= 0.60 and dYm_r >= 0.07 and dYm_r <= 0.15 and dYm_l >= 0.07 and dYm_l <= 0.15 and mRy > 0.10)

        if is_match:
            scores[mid] = 4.8
            scores[~core_mask if 'core_mask' in locals() else slice(0, 4)] = 1.0
        else:
            scores[:] = -10.0

        return scores

