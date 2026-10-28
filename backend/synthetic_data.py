"""
SignBridge Synthetic Benchmark & Data Augmentation Pipeline
Generates high-fidelity 3D skeletal landmark trajectories for demonstration scenarios,
and provides augmentation tools (temporal warping, spatial jittering, 3D rotational perturbation).
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from config import TOTAL_LANDMARKS, COORDINATE_DIM, NUM_POSE_LANDMARKS, NUM_HAND_LANDMARKS


def create_base_skeleton() -> np.ndarray:
    """
    Creates a canonical neutral rest skeleton (TOTAL_LANDMARKS, 3).
    """
    pts = np.zeros((TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)

    # 1. Pose landmarks
    # Nose (0)
    pts[0] = [0.0, -0.6, 0.0]
    # Left eye (2), Right eye (5)
    pts[2] = [-0.08, -0.65, -0.05]
    pts[5] = [0.08, -0.65, -0.05]
    # Left shoulder (11), Right shoulder (12)
    pts[11] = [-0.5, 0.0, 0.0]
    pts[12] = [0.5, 0.0, 0.0]
    # Left elbow (13), Right elbow (14)
    pts[13] = [-0.65, 0.45, 0.05]
    pts[14] = [0.65, 0.45, 0.05]
    # Left wrist (15), Right wrist (16)
    pts[15] = [-0.4, 0.8, 0.1]
    pts[16] = [0.4, 0.8, 0.1]
    # Left hip (23), Right hip (24)
    pts[23] = [-0.35, 1.2, 0.0]
    pts[24] = [0.35, 1.2, 0.0]

    # 2. Hands (21 pts each)
    lh_offset = NUM_POSE_LANDMARKS
    rh_offset = NUM_POSE_LANDMARKS + NUM_HAND_LANDMARKS
    for i in range(21):
        # Left hand offsets from left wrist
        pts[lh_offset + i] = pts[15] + np.array([-0.02 * (i % 5), 0.03 * (i // 5), 0.01 * (i % 3)], dtype=np.float32)
        # Right hand offsets from right wrist
        pts[rh_offset + i] = pts[16] + np.array([0.02 * (i % 5), 0.03 * (i // 5), 0.01 * (i % 3)], dtype=np.float32)

    # 3. Face contours (40 pts)
    face_offset = NUM_POSE_LANDMARKS + (NUM_HAND_LANDMARKS * 2)
    for i in range(40):
        angle = 2.0 * np.pi * (i / 40.0)
        pts[face_offset + i] = [0.18 * np.cos(angle), -0.6 + 0.22 * np.sin(angle), -0.05]

    return pts


def generate_sign_trajectory(sign_name: str, num_frames: int = 30) -> np.ndarray:
    """
    Generates realistic 3D skeletal motion sequence (T, TOTAL_LANDMARKS, 3) for a specific ISL sign.
    """
    base_skel = create_base_skeleton()
    trajectory = np.repeat(base_skel[np.newaxis, :, :], num_frames, axis=0) # (T, V, 3)

    t_norm = np.linspace(0, np.pi, num_frames)
    envelope = np.sin(t_norm)[:, np.newaxis] # (T, 1)

    lh_offset = NUM_POSE_LANDMARKS
    rh_offset = NUM_POSE_LANDMARKS + NUM_HAND_LANDMARKS

    if sign_name == "DOCTOR":
        # Right hand moves to tap Left wrist pulse repeatedly
        for t in range(num_frames):
            pulse = np.sin(t * 0.8) * 0.08
            target = trajectory[t, 15] + np.array([0.05, -0.05 + pulse, -0.05], dtype=np.float32)
            # Interpolate right wrist toward left wrist
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target * envelope[t, 0]
            # Move right hand fingers with wrist
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "CHEST":
        # Both hands press flat against chest
        for t in range(num_frames):
            target_lh = np.array([-0.2, 0.1, -0.1], dtype=np.float32)
            target_rh = np.array([0.2, 0.1, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "PAIN":
        # Both hands twist/shake rapidly at chest level
        for t in range(num_frames):
            shake_x = np.sin(t * 1.5) * 0.15
            shake_y = np.cos(t * 1.5) * 0.1
            target_lh = np.array([-0.25 + shake_x, 0.2 + shake_y, -0.1], dtype=np.float32)
            target_rh = np.array([0.25 - shake_x, 0.2 - shake_y, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "SEVERE":
        # Rapid downward stroke with both hands
        for t in range(num_frames):
            prog = t / max(num_frames - 1, 1)
            target_lh = np.array([-0.3, -0.1 + prog * 0.6, -0.1], dtype=np.float32)
            target_rh = np.array([0.3, -0.1 + prog * 0.6, -0.1], dtype=np.float32)
            trajectory[t, 15] = target_lh
            trajectory[t, 16] = target_rh
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "POLICE":
        # Right hand rises to right temple (salute/badge position)
        for t in range(num_frames):
            target_rh = np.array([0.35, -0.55, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "STATION":
        # Both hands form box boundaries at mid chest
        for t in range(num_frames):
            target_lh = np.array([-0.35, 0.15, -0.15], dtype=np.float32)
            target_rh = np.array([0.35, 0.15, -0.15], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "WHERE":
        # Open palms facing up, lateral shrug
        for t in range(num_frames):
            shrug = np.sin(t * 0.6) * 0.12
            target_lh = np.array([-0.45 - shrug, 0.3, -0.1], dtype=np.float32)
            target_rh = np.array([0.45 + shrug, 0.3, -0.1], dtype=np.float32)
            trajectory[t, 15] = target_lh
            trajectory[t, 16] = target_rh
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "HOSPITAL":
        # Two-handed Intersecting Cross (+): Left hand vertical, Right hand horizontal intersecting at chest
        for t in range(num_frames):
            target_lh = np.array([-0.02, 0.18, -0.1], dtype=np.float32)
            target_rh = np.array([0.02, 0.18, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "GO":
        # Pointing and forward extension
        for t in range(num_frames):
            target_rh = np.array([0.2, 0.1, -0.3 * (t / num_frames)], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "HOW":
        # Palms rolling upwards
        for t in range(num_frames):
            target_lh = np.array([-0.25, 0.3 - 0.25 * (t / num_frames), -0.1], dtype=np.float32)
            target_rh = np.array([0.25, 0.3 - 0.25 * (t / num_frames), -0.1], dtype=np.float32)
            trajectory[t, 15] = target_lh
            trajectory[t, 16] = target_rh
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "YES":
        # Right fist nods vertically in signing space
        for t in range(num_frames):
            nod = np.sin(t * 1.2) * 0.12
            target_rh = np.array([0.25, 0.1 + nod, -0.15], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "NO":
        # Right hand snaps fingers closed onto thumb with horizontal shake
        for t in range(num_frames):
            shake = np.sin(t * 1.2) * 0.10
            target_rh = np.array([0.25 + shake, 0.15, -0.15], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "HELP":
        # Left open palm lifts right fist upward
        for t in range(num_frames):
            lift = (t / num_frames) * 0.20
            target_lh = np.array([-0.05, 0.28 - lift, -0.15], dtype=np.float32)
            target_rh = np.array([0.02, 0.22 - lift, -0.15], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "HELLO":
        # Open hand waves near right temple
        for t in range(num_frames):
            wave = np.sin(t * 1.5) * 0.10
            target_rh = np.array([0.35 + wave, -0.45, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "WATER":
        # 'W' hand taps near chin
        for t in range(num_frames):
            tap = np.sin(t * 1.0) * 0.06
            target_rh = np.array([0.10, -0.30 + tap, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "10":
        # Upright thumb shaking
        for t in range(num_frames):
            shake = np.sin(t * 1.5) * 0.08
            target_rh = np.array([0.28 + shake, 0.05, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "SIT":
        # Two fingers tap on non-dominant fingers
        for t in range(num_frames):
            target_lh = np.array([-0.1, 0.25, -0.1], dtype=np.float32)
            target_rh = np.array([-0.06, 0.23, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "WAIT":
        # Both hands in front fluttering
        for t in range(num_frames):
            wiggle_l = np.sin(t * 1.5) * 0.04
            wiggle_r = np.cos(t * 1.5) * 0.04
            target_lh = np.array([-0.25, 0.20 + wiggle_l, -0.1], dtype=np.float32)
            target_rh = np.array([0.25, 0.20 + wiggle_r, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "MINUTES":
        # Right index rotates on left palm
        for t in range(num_frames):
            angle = t * 0.3
            target_lh = np.array([-0.15, 0.25, -0.1], dtype=np.float32)
            target_rh = np.array([-0.15 + np.cos(angle) * 0.08, 0.25 + np.sin(angle) * 0.08, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "ME":
        # Right index touches center of chest
        for t in range(num_frames):
            target_rh = np.array([0.05, 0.15, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "PLEASE":
        # Flat hand rubs center of chest circularly
        for t in range(num_frames):
            circle_x = np.cos(t * 0.8) * 0.08
            circle_y = np.sin(t * 0.8) * 0.08
            target_rh = np.array([circle_x, 0.15 + circle_y, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "THANK_YOU":
        # Flat hand from chin moves forward
        for t in range(num_frames):
            prog = t / num_frames
            target_rh = np.array([0.1, -0.25 + prog * 0.3, -0.1 - prog * 0.2], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "MEDICINE":
        for t in range(num_frames):
            tap = np.sin(t * 1.2) * 0.05
            target_lh = np.array([-0.12, 0.28, -0.1], dtype=np.float32)
            target_rh = np.array([-0.10, 0.26 + tap, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "TIME":
        for t in range(num_frames):
            tap = np.sin(t * 1.0) * 0.04
            target_lh = np.array([-0.25, 0.32, -0.05], dtype=np.float32)
            target_rh = np.array([-0.22, 0.30 + tap, -0.05], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "WHAT":
        for t in range(num_frames):
            shrug = np.sin(t * 1.4) * 0.08
            target_lh = np.array([-0.28 + shrug, 0.28, -0.1], dtype=np.float32)
            target_rh = np.array([0.28 - shrug, 0.28, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "NAME":
        for t in range(num_frames):
            tap = np.sin(t * 1.5) * 0.04
            target_lh = np.array([-0.05, 0.24, -0.1], dtype=np.float32)
            target_rh = np.array([0.02, 0.22 + tap, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "YOUR":
        for t in range(num_frames):
            target_rh = np.array([0.22, 0.20, -0.30 * (t / num_frames)], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "NEED":
        for t in range(num_frames):
            prog = (t / num_frames) * 0.22
            target_rh = np.array([0.22, 0.12 + prog, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "EMERGENCY":
        for t in range(num_frames):
            urgent_x = np.sin(t * 2.0) * 0.18
            target_lh = np.array([-0.35 + urgent_x, 0.15, -0.1], dtype=np.float32)
            target_rh = np.array([0.35 - urgent_x, 0.15, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "FEVER":
        for t in range(num_frames):
            prog = t / num_frames
            target_rh = np.array([0.05 + prog * 0.25, -0.65 + prog * 0.35, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "BREATHING":
        for t in range(num_frames):
            expansion = np.sin(t * 0.8) * 0.16
            target_lh = np.array([-0.22, 0.18, -0.05 - expansion], dtype=np.float32)
            target_rh = np.array([0.22, 0.18, -0.05 - expansion], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "PROBLEM":
        for t in range(num_frames):
            twist = np.sin(t * 1.5) * 0.12
            target_lh = np.array([-0.18 - twist, 0.22, -0.1], dtype=np.float32)
            target_rh = np.array([0.18 + twist, 0.22, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "CALL":
        for t in range(num_frames):
            target_rh = np.array([0.38, -0.60, -0.05], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "FAMILY":
        for t in range(num_frames):
            circle = (t / num_frames) * 0.35
            target_lh = np.array([-0.05 - circle, 0.22, -0.1], dtype=np.float32)
            target_rh = np.array([0.05 + circle, 0.22, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "MONEY":
        for t in range(num_frames):
            rub = np.sin(t * 1.5) * 0.05
            target_lh = np.array([-0.15, 0.30, -0.1], dtype=np.float32)
            target_rh = np.array([-0.08 + rub, 0.28, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "ACCOUNT":
        for t in range(num_frames):
            tap = np.sin(t * 1.2) * 0.06
            target_lh = np.array([-0.20, 0.28, -0.1], dtype=np.float32)
            target_rh = np.array([-0.18, 0.24 + tap, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "BANK":
        for t in range(num_frames):
            pillar = (t / num_frames) * 0.25
            target_lh = np.array([-0.30, 0.10 + pillar, -0.1], dtype=np.float32)
            target_rh = np.array([0.30, 0.10 + pillar, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "DEPOSIT":
        for t in range(num_frames):
            dip = (t / num_frames) * 0.18
            target_lh = np.array([-0.18, 0.32, -0.1], dtype=np.float32)
            target_rh = np.array([-0.14, 0.18 + dip, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "WITHDRAW":
        for t in range(num_frames):
            pull = (t / num_frames) * 0.18
            target_lh = np.array([-0.18, 0.32, -0.1], dtype=np.float32)
            target_rh = np.array([-0.14, 0.32 - pull, -0.1 + pull], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "SIGN":
        for t in range(num_frames):
            circ_r_x = np.cos(t * 1.4) * 0.08
            circ_r_y = np.sin(t * 1.4) * 0.08
            circ_l_x = np.cos(t * 1.4 + np.pi) * 0.08
            circ_l_y = np.sin(t * 1.4 + np.pi) * 0.08
            target_lh = np.array([-0.18 + circ_l_x, 0.22 + circ_l_y, -0.1], dtype=np.float32)
            target_rh = np.array([0.18 + circ_r_x, 0.22 + circ_r_y, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "LANGUAGE":
        for t in range(num_frames):
            apart = (np.sin(t * 1.0)) * 0.18
            target_lh = np.array([-0.15 - apart, -0.10, -0.1], dtype=np.float32)
            target_rh = np.array([0.15 + apart, -0.10, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "INTERPRETER":
        for t in range(num_frames):
            twist_l = np.sin(t * 1.5) * 0.08
            twist_r = np.sin(t * 1.5 + np.pi) * 0.08
            target_lh = np.array([-0.18, 0.20 + twist_l, -0.1], dtype=np.float32)
            target_rh = np.array([0.18, 0.20 + twist_r, -0.1], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "CARD":
        # Left hand flat palm up; right hand pinches card and swipes across left palm
        for t in range(num_frames):
            swipe = (t / num_frames) * 0.18
            target_lh = np.array([-0.16, 0.26, -0.10], dtype=np.float32)
            target_rh = np.array([-0.22 + swipe, 0.22, -0.08], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "COME":
        # Both hands with open palms facing inward, beckoning inward towards chest
        for t in range(num_frames):
            beckon = np.sin(t * 1.4) * 0.12
            target_lh = np.array([-0.20, 0.16, -0.18 + beckon], dtype=np.float32)
            target_rh = np.array([0.20, 0.16, -0.18 + beckon], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "STOP":
        # Right hand held upright with palm forward in firm halt gesture
        for t in range(num_frames):
            push = (t / num_frames) * 0.08
            target_lh = np.array([-0.20, 0.35, -0.05], dtype=np.float32)
            target_rh = np.array([0.22, 0.08, -0.22 - push], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "LEARN":
        # Left palm open at chest (book); right fingertips touch palm then rise to temple
        for t in range(num_frames):
            progress = t / num_frames
            target_lh = np.array([-0.18, 0.24, -0.10], dtype=np.float32)
            target_rh = np.array([
                -0.12 * (1.0 - progress) + 0.22 * progress,
                0.20 * (1.0 - progress) - 0.48 * progress,
                -0.08
            ], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "TEACHER":
        # Both hands form O/flat shape near temples and push forward/downward in instructive motion
        for t in range(num_frames):
            instruct = (t / num_frames) * 0.18
            target_lh = np.array([-0.22, -0.38 + instruct, -0.12 - instruct], dtype=np.float32)
            target_rh = np.array([0.22, -0.38 + instruct, -0.12 - instruct], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "STUDENT":
        # Compound gesture: learn motion followed by downward personal descent
        for t in range(num_frames):
            descent = (t / num_frames) * 0.28
            target_lh = np.array([-0.25, 0.10 + descent, -0.08], dtype=np.float32)
            target_rh = np.array([0.25, 0.10 + descent, -0.08], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "SCHOOL":
        # Both open hands clap horizontally twice
        for t in range(num_frames):
            clap = np.abs(np.sin(t * 1.5)) * 0.10
            target_lh = np.array([-0.08, 0.20, -0.10], dtype=np.float32)
            target_rh = np.array([-0.08, 0.20 - clap, -0.10], dtype=np.float32)
            trajectory[t, 15] = trajectory[t, 15] * (1.0 - envelope[t, 0]) + target_lh * envelope[t, 0]
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, lh_offset:lh_offset + 21] += (trajectory[t, 15] - base_skel[15])
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "FOOD":
        # Right hand brings clustered fingertips to mouth repeatedly (one-handed dominant)
        for t in range(num_frames):
            eat = np.sin(t * 1.6) * 0.07
            target_rh = np.array([0.08, -0.42 + eat, -0.12 - eat], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    elif sign_name == "SLEEP":
        # Right hand rests against cheek/temple with gentle sideways head tilt (one-handed dominant)
        for t in range(num_frames):
            target_rh = np.array([0.18, -0.46, -0.08], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    else:
        # Fallback gentle gesture movement
        for t in range(num_frames):
            target_rh = np.array([0.3, 0.2 + np.sin(t * 0.5) * 0.2, -0.1], dtype=np.float32)
            trajectory[t, 16] = trajectory[t, 16] * (1.0 - envelope[t, 0]) + target_rh * envelope[t, 0]
            trajectory[t, rh_offset:rh_offset + 21] += (trajectory[t, 16] - base_skel[16])

    return trajectory


def generate_continuous_scenario_sequence(scenario_id: str) -> Tuple[np.ndarray, List[str]]:
    """
    Generates a continuous multi-sign sequence with natural transition co-articulation.
    """
    scenarios = {
        "emergency": ["DOCTOR", "CHEST", "PAIN", "SEVERE"],
        "police": ["POLICE", "STATION", "WHERE"],
        "hospital": ["HOSPITAL", "GO", "HOW"],
        "banking": ["MONEY", "ACCOUNT", "BANK", "DEPOSIT"],
        "assistance": ["HELP", "ME", "PLEASE"],
        "reverse_demo": ["SIT", "WAIT", "10", "MINUTES"]
    }

    gloss_list = scenarios.get(scenario_id, ["DOCTOR", "CHEST", "PAIN", "SEVERE"])
    full_trajectory = []

    # Generate each sign with 25-30 frames plus 5 frames of smooth co-articulation transition
    for idx, gloss in enumerate(gloss_list):
        sign_traj = generate_sign_trajectory(gloss, num_frames=26)
        full_trajectory.append(sign_traj)
        
        # Add transition frames if not last
        if idx < len(gloss_list) - 1:
            last_frame = sign_traj[-1:]
            next_base = generate_sign_trajectory(gloss_list[idx + 1], num_frames=26)[0:1]
            transition = np.zeros((6, TOTAL_LANDMARKS, 3), dtype=np.float32)
            for step in range(6):
                alpha = step / 5.0
                transition[step] = (1.0 - alpha) * last_frame[0] + alpha * next_base[0]
            full_trajectory.append(transition)

    combined = np.concatenate(full_trajectory, axis=0)
    return combined, gloss_list


def apply_data_augmentation(sequence: np.ndarray, jitter_sigma: float = 0.015, rot_range_deg: float = 15.0) -> np.ndarray:
    """
    Applies synthetic data augmentations:
    - 3D Spatial Jittering: Gaussian noise
    - 3D Rotational Perturbation: Affine rotation matrix
    """
    augmented = sequence.copy()
    T, V, C = augmented.shape

    # 1. Spatial Jittering
    noise = np.random.normal(0.0, jitter_sigma, size=augmented.shape).astype(np.float32)
    augmented += noise

    # 2. 3D Rotation matrix
    theta_y = np.radians(np.random.uniform(-rot_range_deg, rot_range_deg))
    cos_y, sin_y = np.cos(theta_y), np.sin(theta_y)
    R_y = np.array([
        [cos_y, 0, sin_y],
        [0, 1, 0],
        [-sin_y, 0, cos_y]
    ], dtype=np.float32)

    for t in range(T):
        augmented[t] = augmented[t] @ R_y.T

    return augmented
