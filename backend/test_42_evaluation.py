"""
SignBridge 42 ISL Sign Evaluation & Assertion Suite
Tests model recognition accuracy across clean trajectories, noisy sensor inputs, and stationary postures.
"""

import pytest
import numpy as np
from config import VOCABULARY
from normalization import LandmarkNormalizer
from synthetic_data import generate_sign_trajectory, create_base_skeleton
from stgcn_model import STGCNModel
from ctc_decoder import CTCDecoder


@pytest.fixture(scope="module")
def pipeline():
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.60)
    return normalizer, model, decoder


def test_clean_trajectory_recognition_all_42_signs(pipeline):
    """Asserts that all 42 official ISL vocabulary signs are correctly recognized on canonical inputs."""
    normalizer, model, decoder = pipeline
    all_signs = VOCABULARY[1:]

    failures = []
    for sign in all_signs:
        traj = generate_sign_trajectory(sign, num_frames=30)
        norm = normalizer.normalize_sequence(traj)
        probs = model.forward(norm)
        tokens = decoder.decode_greedy(probs)
        pred = [t['gloss'] for t in tokens]
        if sign not in pred:
            failures.append((sign, pred))

    assert len(failures) == 0, f"Failed signs on clean evaluation: {failures}"


def test_sensor_jitter_robustness(pipeline):
    """Asserts that model maintains high recognition accuracy (> 85%) under realistic webcam landmark jitter."""
    normalizer, model, decoder = pipeline
    all_signs = VOCABULARY[1:]
    np.random.seed(42)

    recognized_count = 0
    for sign in all_signs:
        traj = generate_sign_trajectory(sign, num_frames=30)
        # Inject realistic webcam noise
        jitter = np.random.normal(0, 0.003, size=traj.shape)
        noisy_traj = traj + jitter
        norm = normalizer.normalize_sequence(noisy_traj)
        probs = model.forward(norm)
        tokens = decoder.decode_greedy(probs)
        pred = [t['gloss'] for t in tokens]
        if sign in pred:
            recognized_count += 1

    acc = (recognized_count / len(all_signs)) * 100.0
    print(f"\nRobustness under sensor jitter: {acc:.1f}% ({recognized_count}/42)")
    assert acc >= 85.0, f"Accuracy under sensor jitter {acc:.1f}% fell below 85% requirement"


def test_stationary_posture_rejection(pipeline):
    """Asserts that resting hands or idle poses emit 0 false-positive tokens."""
    normalizer, model, decoder = pipeline
    skel = create_base_skeleton()
    idle_seq = np.repeat(skel[np.newaxis, :, :], 30, axis=0)
    norm = normalizer.normalize_sequence(idle_seq)
    probs = model.forward(norm)
    tokens = decoder.decode_greedy(probs)
    assert len(tokens) == 0, f"Stationary pose unexpectedly produced tokens: {tokens}"


if __name__ == "__main__":
    norm = LandmarkNormalizer()
    m = STGCNModel()
    d = CTCDecoder(min_persistence_frames=2, min_confidence=0.60)
    p = (norm, m, d)
    test_clean_trajectory_recognition_all_42_signs(p)
    test_sensor_jitter_robustness(p)
    test_stationary_posture_rejection(p)
    print("\nALL 42-SIGN EVALUATION ASSERTIONS PASSED!")
