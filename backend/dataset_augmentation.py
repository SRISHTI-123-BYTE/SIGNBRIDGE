"""
SignBridge ISL 3D Landmark Sequence Augmentation Engine
Implements 3D spatial rotation, scaling, time-warping, Gaussian jitter,
and bilateral mirroring for robust person-independent and environment-invariant training.
"""

import numpy as np
from typing import Tuple, List, Optional

# Landmark layout constants
POSE_LEFT_SHOULDER = 11
POSE_RIGHT_SHOULDER = 12
POSE_LEFT_HIP = 23
POSE_RIGHT_HIP = 24
POSE_LEFT_ELBOW = 13
POSE_RIGHT_ELBOW = 14
POSE_LEFT_WRIST = 15
POSE_RIGHT_WRIST = 16

LEFT_HAND_START = 25
LEFT_HAND_END = 46  # 21 joints
RIGHT_HAND_START = 46
RIGHT_HAND_END = 67  # 21 joints
FACE_START = 67
FACE_END = 107      # 40 joints

# Pose bilateral swap pairs (left <-> right)
POSE_SWAP_PAIRS = [
    (1, 4),   # eye inner
    (2, 5),   # eye
    (3, 6),   # eye outer
    (7, 8),   # ear
    (9, 10),  # mouth corner
    (11, 12), # shoulder
    (13, 14), # elbow
    (15, 16), # wrist
    (17, 18), # pinky knuckle
    (19, 20), # index knuckle
    (21, 22), # thumb knuckle
    (23, 24)  # hip
]


def get_torso_center(seq: np.ndarray) -> np.ndarray:
    """
    Computes average torso center (midpoint of shoulders) across sequence.
    seq: (T, 107, 3)
    Returns: (3,)
    """
    ls = seq[:, POSE_LEFT_SHOULDER, :3]
    rs = seq[:, POSE_RIGHT_SHOULDER, :3]
    center = (ls + rs) / 2.0
    return np.mean(center, axis=0)


def spatial_rotation_3d(seq: np.ndarray, max_angle_deg: float = 12.0) -> np.ndarray:
    """
    Applies small random 3D rotation (yaw, pitch, roll) around torso center.
    seq: (T, 107, 3)
    """
    angles = np.radians(np.random.uniform(-max_angle_deg, max_angle_deg, size=3))
    ax, ay, az = angles

    # Rotation matrices
    Rx = np.array([
        [1.0, 0.0, 0.0],
        [0.0, np.cos(ax), -np.sin(ax)],
        [0.0, np.sin(ax), np.cos(ax)]
    ])
    Ry = np.array([
        [np.cos(ay), 0.0, np.sin(ay)],
        [0.0, 1.0, 0.0],
        [-np.sin(ay), 0.0, np.cos(ay)]
    ])
    Rz = np.array([
        [np.cos(az), -np.sin(az), 0.0],
        [np.sin(az), np.cos(az), 0.0],
        [0.0, 0.0, 1.0]
    ])
    R = Rz @ Ry @ Rx

    center = get_torso_center(seq)
    out = seq.copy()
    coords = out[:, :, :3] - center
    # Matrix multiply: (T, 107, 3) @ (3, 3).T
    rotated = np.einsum('ijk,lk->ijl', coords, R)
    out[:, :, :3] = rotated + center
    return out


def spatial_scale(seq: np.ndarray, scale_range: Tuple[float, float] = (0.88, 1.12)) -> np.ndarray:
    """
    Scales skeleton coordinates relative to torso center.
    Simulates variations in subject distance from webcam or body proportions.
    """
    s = np.random.uniform(scale_range[0], scale_range[1])
    center = get_torso_center(seq)
    out = seq.copy()
    out[:, :, :3] = (out[:, :, :3] - center) * s + center
    return out


def time_warp(seq: np.ndarray, warp_range: Tuple[float, float] = (0.80, 1.20), target_len: Optional[int] = None) -> np.ndarray:
    """
    Changes speed of signing by temporally interpolating trajectory.
    If target_len is None, maintains current length T after non-linear warping.
    """
    T = seq.shape[0]
    if T <= 2:
        return seq.copy()

    orig_target_len = target_len if target_len is not None else T
    # Create non-linear or random speed curve
    warp_factor = np.random.uniform(warp_range[0], warp_range[1])
    warped_len = max(6, int(round(T * warp_factor)))

    # Step 1: Resample to warped duration
    src_indices = np.linspace(0, T - 1, num=warped_len)
    warped = np.zeros((warped_len, seq.shape[1], seq.shape[2]), dtype=np.float32)

    for i, t_idx in enumerate(src_indices):
        low = int(np.floor(t_idx))
        high = min(T - 1, int(np.ceil(t_idx)))
        frac = t_idx - low
        warped[i] = (1.0 - frac) * seq[low] + frac * seq[high]

    # Step 2: Resample to final target_len
    if warped_len == orig_target_len:
        return warped

    final = np.zeros((orig_target_len, seq.shape[1], seq.shape[2]), dtype=np.float32)
    final_indices = np.linspace(0, warped_len - 1, num=orig_target_len)
    for i, t_idx in enumerate(final_indices):
        low = int(np.floor(t_idx))
        high = min(warped_len - 1, int(np.ceil(t_idx)))
        frac = t_idx - low
        final[i] = (1.0 - frac) * warped[low] + frac * warped[high]

    return final


def gaussian_jitter(seq: np.ndarray, sigma: float = 0.0035) -> np.ndarray:
    """
    Adds Gaussian sensor noise to mimic webcam sensor landmark jitter.
    """
    out = seq.copy()
    noise = np.random.normal(0, sigma, size=seq.shape)
    out[:, :, :3] += noise[:, :, :3]
    return out


def mirror_sequence(seq: np.ndarray) -> np.ndarray:
    """
    Bilateral mirroring (left-right reflection):
    Flips X-coordinate and exchanges left-hand with right-hand joints and pose left/right joints.
    """
    center = get_torso_center(seq)
    out = seq.copy()

    # Flip X around torso center
    out[:, :, 0] = 2.0 * center[0] - out[:, :, 0]

    # Swap left and right pose joints
    for left_idx, right_idx in POSE_SWAP_PAIRS:
        temp = out[:, left_idx, :].copy()
        out[:, left_idx, :] = out[:, right_idx, :]
        out[:, right_idx, :] = temp

    # Swap Left Hand (25..45) with Right Hand (46..66)
    lh = out[:, LEFT_HAND_START:LEFT_HAND_END, :].copy()
    rh = out[:, RIGHT_HAND_START:RIGHT_HAND_END, :].copy()
    out[:, LEFT_HAND_START:LEFT_HAND_END, :] = rh
    out[:, RIGHT_HAND_START:RIGHT_HAND_END, :] = lh

    return out


def augment_sequence_pipeline(
    seq: np.ndarray,
    rotate: bool = True,
    scale: bool = True,
    warp: bool = True,
    jitter: bool = True,
    mirror: bool = False
) -> np.ndarray:
    """
    Chains multiple stochastic augmentations together into a single unified transform.
    """
    out = seq.copy()

    if mirror and np.random.rand() > 0.5:
        out = mirror_sequence(out)

    if warp:
        out = time_warp(out, warp_range=(0.85, 1.15))

    if rotate:
        out = spatial_rotation_3d(out, max_angle_deg=10.0)

    if scale:
        out = spatial_scale(out, scale_range=(0.90, 1.10))

    if jitter:
        out = gaussian_jitter(out, sigma=0.003)

    return out.astype(np.float32)


def generate_augmented_dataset(
    raw_samples: List[dict],
    augment_factor: int = 4
) -> List[dict]:
    """
    Expands a list of raw sample dicts:
    each sample: {"landmarks": (T, 107, 3), "gloss": str, "user_id": str, "fps": float}
    Returns expanded list including original and augmented samples.
    """
    expanded = []
    for sample in raw_samples:
        expanded.append(sample) # include clean raw sample
        base_seq = sample["landmarks"]

        for aug_i in range(augment_factor):
            # Apply combination of transforms
            aug_seq = augment_sequence_pipeline(
                base_seq,
                rotate=True,
                scale=True,
                warp=True,
                jitter=True,
                mirror=(aug_i % 2 == 1) # alternate mirroring
            )
            augmented_entry = {
                "landmarks": aug_seq,
                "gloss": sample["gloss"],
                "user_id": f"{sample['user_id']}_aug{aug_i+1}",
                "fps": sample.get("fps", 30.0),
                "is_augmented": True,
                "parent_id": sample.get("file_id", "raw")
            }
            expanded.append(augmented_entry)

    return expanded
