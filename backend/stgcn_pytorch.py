"""
SignBridge PyTorch Spatial-Temporal Graph Convolutional Network (ST-GCN)
End-to-end trainable neural network for continuous Indian Sign Language (ISL) recognition
with 107-node skeletal topology and ONNX export capability.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import numpy as np
from typing import Tuple, List, Optional

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from config import TOTAL_LANDMARKS, COORDINATE_DIM, VOCABULARY, NUM_CLASSES, STGCN_HIDDEN_DIM


def get_skeletal_edges(num_nodes: int = TOTAL_LANDMARKS) -> List[Tuple[int, int]]:
    """
    Constructs the anatomical spatial edges (bones) connecting joints in the
    MediaPipe Holistic landmark set (25 pose + 21 LH + 21 RH + 40 face = 107 joints).
    """
    edges = []
    # 1. Pose connections (Upper body subset: Nose=0, Shoulders=11,12, Elbows=13,14, Wrists=15,16, Hips=23,24)
    pose_links = [
        (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
        (11, 12),           # Inter-shoulder
        (11, 13), (13, 15), # Left arm (shoulder -> elbow -> wrist)
        (12, 14), (14, 16), # Right arm (shoulder -> elbow -> wrist)
        (11, 23), (12, 24), # Torso (shoulders to hips)
        (23, 24)            # Inter-hip
    ]
    edges.extend(pose_links)

    # 2. Hand finger chains helper
    hand_links = [
        (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),        # Index
        (0, 9), (9, 10), (10, 11), (11, 12),   # Middle
        (0, 13), (13, 14), (14, 15), (15, 16), # Ring
        (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
        (5, 9), (9, 13), (13, 17)              # Palm base cross-links
    ]

    # Left Hand (25..45) connected to pose Left Wrist (15)
    lh_offset = 25
    edges.append((15, lh_offset))
    for u, v in hand_links:
        edges.append((lh_offset + u, lh_offset + v))

    # Right Hand (46..66) connected to pose Right Wrist (16)
    rh_offset = 46
    edges.append((16, rh_offset))
    for u, v in hand_links:
        edges.append((rh_offset + u, rh_offset + v))

    # 3. Face Contours (67..106: 40 joints) connected to Nose (0)
    face_offset = 67
    face_count = min(40, num_nodes - face_offset)
    if face_count > 0:
        edges.append((0, face_offset))
        # Chain all 40 face nodes sequentially (i=1..39 connects 0..39)
        for i in range(1, face_count):
            edges.append((face_offset + i - 1, face_offset + i))
        # Close face loop
        edges.append((face_offset + face_count - 1, face_offset))

    return edges


def build_isl_graph_adjacency(num_nodes: int = TOTAL_LANDMARKS) -> np.ndarray:
    """
    Constructs connectivity adjacency matrix for 107 ISL landmarks.
    """
    A = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    edges = get_skeletal_edges(num_nodes)
    for u, v in edges:
        if u < num_nodes and v < num_nodes:
            A[u, v] = 1.0
            A[v, u] = 1.0
    return A


def get_normalized_laplacian(A: np.ndarray) -> np.ndarray:
    """
    Computes symmetric normalized graph Laplacian:
    A_norm = D^{-1/2} * (A + I) * D^{-1/2}
    """
    N = A.shape[0]
    A_self = A + np.eye(N, dtype=np.float32)
    degrees = np.sum(A_self, axis=1)
    d_inv_sqrt = np.zeros_like(degrees, dtype=np.float32)
    positive_mask = degrees > 0
    d_inv_sqrt[positive_mask] = np.power(degrees[positive_mask], -0.5)
    D_mat = np.diag(d_inv_sqrt)
    return D_mat @ A_self @ D_mat


if TORCH_AVAILABLE:
    class SpatialGraphConv(nn.Module):
        """
        Spatial Graph Convolution Layer over skeletal landmark graph.
        X: (B, C_in, T, V) -> Y: (B, C_out, T, V)
        """
        def __init__(self, in_channels: int, out_channels: int, A_norm: torch.Tensor):
            super().__init__()
            self.register_buffer("A", A_norm)
            self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
            self.bn = nn.BatchNorm2d(out_channels)
            self.relu = nn.ReLU(inplace=True)
            self.res = nn.Conv2d(in_channels, out_channels, kernel_size=1) if in_channels != out_channels else nn.Identity()

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x: (B, C, T, V)
            res = self.res(x)
            out_graph = torch.matmul(x, self.A)
            out = self.relu(self.bn(self.conv(out_graph)) + res)
            return out

    class TemporalConv(nn.Module):
        """
        Temporal 1D convolution with residual connection along time dimension.
        """
        def __init__(self, channels: int, kernel_size: int = 5, stride: int = 1):
            super().__init__()
            padding = (kernel_size - 1) // 2
            self.conv = nn.Conv2d(channels, channels, kernel_size=(kernel_size, 1), stride=(stride, 1), padding=(padding, 0))
            self.bn = nn.BatchNorm2d(channels)
            self.relu = nn.ReLU(inplace=True)
            self.dropout = nn.Dropout(0.10)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            res = x
            out = self.dropout(self.relu(self.bn(self.conv(x))))
            return out + res

    class STGCNBlock(nn.Module):
        """
        Combined Spatial Graph Conv + Temporal Conv block.
        """
        def __init__(self, in_channels: int, out_channels: int, A_norm: torch.Tensor, kernel_size: int = 5):
            super().__init__()
            self.sgc = SpatialGraphConv(in_channels, out_channels, A_norm)
            self.tc = TemporalConv(out_channels, kernel_size=kernel_size)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.tc(self.sgc(x))

    class STGCNISLNet(nn.Module):
        """
        End-to-End Deep ST-GCN Network for Continuous Indian Sign Language (ISL).
        Input: (B, C, T, V) = (Batch, 3, Frames, 107)
        Output: Logits (B, T, NUM_CLASSES) for sustained CTC and dense sequence recognition.
        """
        def __init__(
            self,
            in_channels: int = 3,
            num_classes: int = NUM_CLASSES,
            num_nodes: int = TOTAL_LANDMARKS,
            hidden_dim: int = STGCN_HIDDEN_DIM
        ):
            super().__init__()
            A_raw = build_isl_graph_adjacency(num_nodes)
            A_norm = get_normalized_laplacian(A_raw)
            A_tensor = torch.tensor(A_norm, dtype=torch.float32)

            self.num_classes = num_classes
            self.hidden_dim = hidden_dim

            # Feature projection blocks
            self.block1 = STGCNBlock(in_channels, hidden_dim, A_tensor)
            self.block2 = STGCNBlock(hidden_dim, hidden_dim, A_tensor)
            self.block3 = STGCNBlock(hidden_dim, hidden_dim, A_tensor)

            # Joint pooling: hands (25..67), global context, max activation
            feat_dim = hidden_dim * 3
            self.temporal_gru = nn.GRU(
                input_size=feat_dim,
                hidden_size=hidden_dim,
                num_layers=1,
                batch_first=True,
                bidirectional=True,
                dropout=0.0
            )

            # Frame-level classification projection
            self.classifier = nn.Sequential(
                nn.Dropout(0.15),
                nn.Linear(hidden_dim * 2, hidden_dim),
                nn.ReLU(inplace=True),
                nn.Linear(hidden_dim, num_classes)
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            x: (B, C, T, V) or (B, T, V, C)
            Returns: logits of shape (B, T, num_classes)
            """
            if x.dim() == 4 and x.size(1) != 3 and x.size(3) == 3:
                x = x.permute(0, 3, 1, 2).contiguous()

            B, C, T, V = x.size()

            out = self.block1(x)
            out = self.block2(out)
            out = self.block3(out) # (B, C_out, T, V)

            # Multi-region skeletal pooling: hands priority (25..67) + global context + max
            hands_pool = torch.mean(out[:, :, :, 25:67], dim=3) # (B, C_out, T)
            global_pool = torch.mean(out, dim=3)               # (B, C_out, T)
            max_pool = torch.max(out, dim=3)[0]                # (B, C_out, T)

            pooled = torch.cat([hands_pool, global_pool, max_pool], dim=1) # (B, C_out * 3, T)
            seq_feat = pooled.permute(0, 2, 1).contiguous()               # (B, T, C_out * 3)

            rnn_out, _ = self.temporal_gru(seq_feat) # (B, T, hidden_dim * 2)
            logits = self.classifier(rnn_out)       # (B, T, num_classes)
            return logits

        def export_onnx(self, output_path: str, dummy_input: Optional[torch.Tensor] = None):
            """
            Exports trained PyTorch weights to standard ONNX runtime format with dynamic temporal axes.
            """
            self.eval()
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            if dummy_input is None:
                dummy_input = torch.randn(1, 3, 30, TOTAL_LANDMARKS, dtype=torch.float32)

            if hasattr(sys.stdout, 'reconfigure'):
                try:
                    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                except Exception:
                    pass

            torch.onnx.export(
                self,
                dummy_input,
                output_path,
                export_params=True,
                opset_version=18,
                dynamo=False,
                do_constant_folding=True,
                input_names=['input_landmarks'],
                output_names=['logits'],
                dynamic_axes={
                    'input_landmarks': {0: 'batch_size', 2: 'num_frames'},
                    'logits': {0: 'batch_size', 1: 'num_frames'}
                }
            )
            return output_path
else:
    class STGCNISLNet:
        pass
