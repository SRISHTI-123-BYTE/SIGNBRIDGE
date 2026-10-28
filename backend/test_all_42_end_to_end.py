import numpy as np
from config import VOCABULARY, TOTAL_LANDMARKS
from normalization import LandmarkNormalizer
from stgcn_model import STGCNModel
from ctc_decoder import CTCDecoder
from synthetic_data import generate_sign_trajectory, create_base_skeleton

def test_all_42_signs_recognition():
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.70)

    all_signs = VOCABULARY[1:]
    success = []
    failures = []

    for sign in all_signs:
        traj = generate_sign_trajectory(sign, num_frames=30)
        norm_seq = normalizer.normalize_sequence(traj)
        probs = model.forward(norm_seq)
        tokens = decoder.decode_greedy(probs)

        predicted_glosses = [t["gloss"] for t in tokens]
        if sign in predicted_glosses:
            success.append(sign)
        else:
            failures.append((sign, predicted_glosses))

    print(f"Recognized {len(success)}/{len(all_signs)} signs: {success}")
    if failures:
        print(f"Failures ({len(failures)}): {failures}")
    assert len(failures) == 0, f"Failed signs: {failures}"

def test_stationary_idle_produces_no_tokens():
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.70)

    skel = create_base_skeleton()
    idle_seq = np.repeat(skel[np.newaxis, :, :], 30, axis=0)
    norm_seq = normalizer.normalize_sequence(idle_seq)
    probs = model.forward(norm_seq)
    tokens = decoder.decode_greedy(probs)

    assert len(tokens) == 0, f"Expected 0 tokens on idle, got: {tokens}"

def test_desk_resting_hands_with_camera_jitter_produces_no_tokens():
    """Verifies that resting hands on a desk with camera sensor jitter produces 0 false-positive tokens."""
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.50)

    for seed in range(25):
        np.random.seed(seed)
        T = 30
        V = TOTAL_LANDMARKS
        raw = np.zeros((T, V, 3), dtype=np.float32)
        raw[:, 11] = [-0.20, 0.0, 0.0]
        raw[:, 12] = [0.20, 0.0, 0.0]
        base_x = np.random.uniform(0.15, 0.30)
        base_y = np.random.uniform(0.15, 0.35)
        for t in range(T):
            jitter = np.random.normal(0, 0.005, 3)
            raw[t, 16] = [base_x + jitter[0], base_y + jitter[1], jitter[2]]
            for h in range(46, 67):
                raw[t, h] = raw[t, 16] + np.random.uniform(-0.02, 0.02, 3)
            raw[t, 15] = [-0.25 + jitter[0], 0.45 + jitter[1], jitter[2]]

        norm_seq = normalizer.normalize_sequence(raw)
        probs = model.forward(norm_seq)
        tokens = decoder.decode_greedy(probs)
        assert len(tokens) == 0, f"False positive detected on seed {seed}: {[t['gloss'] for t in tokens]}"

if __name__ == "__main__":
    test_all_42_signs_recognition()
    test_stationary_idle_produces_no_tokens()
    print(f"ALL {len(VOCABULARY)-1} SIGNS + IDLE TEST PASSED!")
