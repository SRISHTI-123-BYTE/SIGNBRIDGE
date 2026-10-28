"""
SignBridge Backend Pipeline Unit Tests
Verifies mathematical coordinate normalization, ST-GCN graph passes, CTC decoding,
and NLP Grammar Translation across English, Hindi, and Tamil.
"""

import numpy as np
import pytest

from config import TOTAL_LANDMARKS, COORDINATE_DIM, TEMPORAL_WINDOW_FRAMES, VOCABULARY
from normalization import LandmarkNormalizer
from stgcn_model import STGCNModel, build_spatial_adjacency_matrix
from ctc_decoder import CTCDecoder
from grammar_engine import GrammarEngine
from synthetic_data import generate_sign_trajectory, generate_continuous_scenario_sequence


def test_landmark_normalization_invariance():
    """Verifies that affine transformations make keypoints invariant to scale & translation."""
    normalizer = LandmarkNormalizer()
    base_landmarks = np.random.randn(TOTAL_LANDMARKS, 3).astype(np.float32)
    # Set defined shoulder positions
    base_landmarks[11] = [-0.4, 0.0, 0.0] # Left shoulder
    base_landmarks[12] = [0.4, 0.0, 0.0]  # Right shoulder

    norm1, meta1 = normalizer.normalize_frame(base_landmarks)

    # Apply global translation of (+10, -5, +2) and scale by 3.0
    translated_scaled = (base_landmarks * 3.0) + np.array([10.0, -5.0, 2.0], dtype=np.float32)
    norm2, meta2 = normalizer.normalize_frame(translated_scaled)

    # Shoulders distance in norm1 and norm2 should be exactly 1.0
    dist1 = np.linalg.norm(norm1[11] - norm1[12])
    dist2 = np.linalg.norm(norm2[11] - norm2[12])

    assert np.isclose(dist1, 1.0, atol=1e-4)
    assert np.isclose(dist2, 1.0, atol=1e-4)
    # Normalized coordinates should match across translations
    assert np.allclose(norm1, norm2, atol=1e-3)


def test_stgcn_forward_pass():
    """Verifies ST-GCN graph convolution and output probability distribution."""
    model = STGCNModel()
    dummy_sequence = np.random.randn(TEMPORAL_WINDOW_FRAMES, TOTAL_LANDMARKS, COORDINATE_DIM).astype(np.float32)

    probs = model.forward(dummy_sequence)

    assert probs.shape == (TEMPORAL_WINDOW_FRAMES, len(VOCABULARY))
    # Softmax probabilities should sum to 1 across classes for each frame
    row_sums = np.sum(probs, axis=-1)
    assert np.allclose(row_sums, 1.0, atol=1e-4)


def test_ctc_greedy_decoding():
    """Verifies CTC blank collapsing and sequence extraction."""
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.5)

    # Create dummy probability matrix: 10 frames
    # Frames 0-2: Blank (idx 0)
    # Frames 3-6: "DOCTOR" (idx 1)
    # Frames 7-9: "CHEST" (idx 2)
    probs = np.zeros((10, len(VOCABULARY)), dtype=np.float32)
    probs[0:3, 0] = 0.95
    probs[3:7, 1] = 0.92
    probs[7:10, 2] = 0.88

    tokens = decoder.decode_greedy(probs)
    assert len(tokens) == 2
    assert tokens[0]["gloss"] == "DOCTOR"
    assert tokens[1]["gloss"] == "CHEST"
    assert tokens[0]["duration_frames"] == 4
    assert tokens[1]["duration_frames"] == 3


def test_grammar_engine_scenarios():
    """Verifies NLP Grammar Reordering for English, Hindi, and Tamil on core scenarios."""
    engine = GrammarEngine()

    # Scenario 1: Healthcare Emergency
    res1 = engine.translate_gloss_sequence(["DOCTOR", "CHEST", "PAIN", "SEVERE"])
    assert "severe chest pain" in res1["translations"]["en"].lower()
    assert "सीने में" in res1["translations"]["hi"]
    assert "மார்பு வலி" in res1["translations"]["ta"]

    # Scenario 2: Police Navigation
    res2 = engine.translate_gloss_sequence(["POLICE", "STATION", "WHERE"])
    assert "police station" in res2["translations"]["en"].lower()
    assert "कहाँ है" in res2["translations"]["hi"]
    assert "காவல் நிலையம்" in res2["translations"]["ta"]

    # Scenario 3: Hospital Direction
    res3 = engine.translate_gloss_sequence(["HOSPITAL", "GO", "HOW"])
    assert "hospital" in res3["translations"]["en"].lower()
    assert "अस्पताल" in res3["translations"]["hi"]
    assert "மருத்துவமனை" in res3["translations"]["ta"]

    # Scenario 4: Reverse Tokenizer
    spoken = "Please sit down and wait for 10 minutes"
    reverse_glosses = engine.speech_to_isl_glosses(spoken)
    extracted_names = [item["gloss"] for item in reverse_glosses]
    assert "SIT" in extracted_names
    assert "WAIT" in extracted_names
    assert "10" in extracted_names
    assert "MINUTES" in extracted_names


def test_synthetic_scenario_generation():
    """Verifies continuous multi-sign trajectory simulation."""
    traj, glosses = generate_continuous_scenario_sequence("emergency")
    assert traj.ndim == 3
    assert traj.shape[1] == TOTAL_LANDMARKS
    assert traj.shape[2] == 3
    assert glosses == ["DOCTOR", "CHEST", "PAIN", "SEVERE"]


def test_partial_landmarks_normalization_and_inference():
    """Verifies that sequence normalization correctly handles partial landmark sequences (e.g. 65 pts)."""
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    
    # Simulate a sequence with only 65 landmarks (missing hands)
    partial_seq = np.random.randn(30, 65, 3).astype(np.float32)
    # Set shoulders
    partial_seq[:, 11] = [-0.4, 0.0, 0.0]
    partial_seq[:, 12] = [0.4, 0.0, 0.0]
    
    norm_seq = normalizer.normalize_sequence(partial_seq)
    assert norm_seq.shape == (30, TOTAL_LANDMARKS, 3)
    
    probs = model.forward(norm_seq)
    assert probs.shape == (30, len(VOCABULARY))


def test_idle_pose_produces_no_tokens_and_empty_translation():
    """
    Verifies that sitting still with minor camera noise does NOT trigger YES, WHERE, or any other sign.
    Guarantees strict NO_SIGN behavior, empty tokens, and empty translation sentences.
    """
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.70)
    engine = GrammarEngine()

    # Simulate 30 frames of stationary person sitting still
    # Resting pose: torso centered, wrists down at hips (y = 0.80), slight random jitter (0.003)
    stationary_seq = np.zeros((30, TOTAL_LANDMARKS, 3), dtype=np.float32)
    # Nose
    stationary_seq[:, 0] = [0.5, 0.25, 0.0]
    # Shoulders
    stationary_seq[:, 11] = [0.35, 0.42, 0.0]
    stationary_seq[:, 12] = [0.65, 0.42, 0.0]
    # Wrists at rest down near waist
    stationary_seq[:, 15] = [0.35, 0.80, 0.0]
    stationary_seq[:, 16] = [0.65, 0.80, 0.0]
    # Hands anchored at wrists
    for f in range(30):
        for h in range(21):
            stationary_seq[f, 25 + h] = stationary_seq[f, 15]
            stationary_seq[f, 46 + h] = stationary_seq[f, 16]

    # Add realistic sensor micro-jitter (scale 0.003)
    jitter = np.random.uniform(-0.003, 0.003, size=stationary_seq.shape).astype(np.float32)
    noisy_idle_seq = stationary_seq + jitter

    norm_seq = normalizer.normalize_sequence(noisy_idle_seq)
    probs = model.forward(norm_seq)

    # Frame 0 to 29 must all predict blank (index 0) with dominance > 99%
    for f in range(30):
        assert probs[f, 0] > 0.99, f"Frame {f} blank probability was {probs[f, 0]}, expected > 0.99"
        # Ensure YES (index 8) and WHERE (index 12) are completely suppressed
        assert probs[f, 8] < 0.01, f"Frame {f} falsely elevated YES: {probs[f, 8]}"
        assert probs[f, 12] < 0.01, f"Frame {f} falsely elevated WHERE: {probs[f, 12]}"

    # CTC Greedy decoder MUST return zero tokens
    tokens = decoder.decode_greedy(probs)
    assert len(tokens) == 0, f"Expected 0 tokens for idle sequence, got: {tokens}"

    # Grammar translation for empty sequence MUST return empty translations
    trans = engine.translate_gloss_sequence([t["gloss"] for t in tokens])
    assert trans["translations"]["en"] == ""
    assert trans["translations"]["hi"] == ""
    assert trans["translations"]["ta"] == ""
    assert trans["sentence_type"] == "EMPTY"


def test_intentional_gestures_classified_accurately():
    """
    Verifies that genuine intentional gestures are recognized with high confidence.
    """
    normalizer = LandmarkNormalizer()
    model = STGCNModel()
    decoder = CTCDecoder(min_persistence_frames=2, min_confidence=0.70)

    for sign in VOCABULARY[1:]:
        traj = generate_sign_trajectory(sign, num_frames=30)
        norm_seq = normalizer.normalize_sequence(traj)
        probs = model.forward(norm_seq)
        tokens = decoder.decode_greedy(probs)

        assert len(tokens) >= 1, f"Failed to detect intentional sign {sign}"
        matched = any(t["gloss"] == sign and t["confidence"] >= 0.70 for t in tokens)
        assert matched, f"Sign {sign} not recognized with >= 0.70 confidence: {tokens}"


