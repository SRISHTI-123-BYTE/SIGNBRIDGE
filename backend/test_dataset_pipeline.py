"""
Tests for SignBridge Dataset Recording, Augmentation, ST-GCN Neural Model & Evaluation
"""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from config import TOTAL_LANDMARKS, COORDINATE_DIM, VOCABULARY, NUM_CLASSES
from dataset_manager import DatasetManager
from dataset_augmentation import (
    spatial_rotation_3d,
    spatial_scale,
    time_warp,
    gaussian_jitter,
    mirror_sequence,
    augment_sequence_pipeline
)
from stgcn_pytorch import STGCNISLNet, build_isl_graph_adjacency, get_normalized_laplacian
from evaluate_dataset import Evaluator

import torch


def test_dataset_manager_save_and_load(tmp_path):
    dm = DatasetManager(dataset_dir=str(tmp_path))
    dummy_seq = np.random.randn(30, TOTAL_LANDMARKS, COORDINATE_DIM).astype(np.float32)

    entry = dm.save_recording(
        sequence=dummy_seq,
        gloss="DOCTOR",
        user_id="user_test_mock",
        fps=30.0,
        metadata={"note": "unit test sample"}
    )
    assert os.path.exists(entry["filepath"])
    assert entry["gloss"] == "DOCTOR"
    assert entry["user_id"] == "user_test_mock"

    loaded = dm.load_sample(entry["filepath"])
    assert loaded["gloss"] == "DOCTOR"
    assert loaded["landmarks"].shape == (30, TOTAL_LANDMARKS, COORDINATE_DIM)
    assert loaded["user_id"] == "user_test_mock"


def test_augmentation_transforms():
    seq = np.zeros((30, TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
    # Give non-zero shoulder coordinates
    seq[:, 11, :] = [-0.2, 0.4, 0.0]
    seq[:, 12, :] = [0.2, 0.4, 0.0]

    # 1. Spatial rotation
    rotated = spatial_rotation_3d(seq, max_angle_deg=10.0)
    assert rotated.shape == seq.shape
    assert not np.allclose(rotated, seq)

    # 2. Spatial scale
    scaled = spatial_scale(seq, scale_range=(0.9, 1.1))
    assert scaled.shape == seq.shape

    # 3. Time warp
    warped = time_warp(seq, warp_range=(0.8, 1.2), target_len=30)
    assert warped.shape == (30, TOTAL_LANDMARKS, COORDINATE_DIM)

    # 4. Jitter
    jittered = gaussian_jitter(seq, sigma=0.005)
    assert jittered.shape == seq.shape
    assert not np.array_equal(jittered, seq)

    # 5. Mirroring
    mirrored = mirror_sequence(seq)
    assert mirrored.shape == seq.shape
    # Left and right shoulders swapped
    assert np.allclose(mirrored[:, 11, 0], -seq[:, 12, 0])


def test_stgcn_pytorch_model():
    net = STGCNISLNet(in_channels=3, num_classes=NUM_CLASSES, hidden_dim=32)
    net.eval()
    x = torch.randn(2, 3, 30, TOTAL_LANDMARKS, dtype=torch.float32)
    with torch.no_grad():
        out = net(x)
    assert out.shape == (2, 30, NUM_CLASSES)


def test_evaluator_metrics():
    evaluator = Evaluator()
    dummy_seq = np.zeros((30, TOTAL_LANDMARKS, COORDINATE_DIM), dtype=np.float32)
    gloss_rule, conf_rule, lat_rule = evaluator.evaluate_sequence_rule(dummy_seq)
    assert isinstance(gloss_rule, str)
    assert isinstance(conf_rule, float)
    assert lat_rule > 0

    gloss_nn, conf_nn, lat_nn = evaluator.evaluate_sequence_pytorch(dummy_seq)
    assert isinstance(gloss_nn, str)
    assert isinstance(conf_nn, float)
    assert lat_nn > 0
