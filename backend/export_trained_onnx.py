"""
Exports the trained ST-GCN PyTorch model checkpoint to ONNX runtime format.
"""

import os
import sys
import torch

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(__file__))

from config import TOTAL_LANDMARKS, NUM_CLASSES, STGCN_HIDDEN_DIM
from stgcn_pytorch import STGCNISLNet

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
PT_PATH = os.path.join(MODELS_DIR, "stgcn_isl_42.pt")
ONNX_PATH = os.path.join(MODELS_DIR, "stgcn_isl_42.onnx")

def export():
    print(f"Loading checkpoint from: {PT_PATH}")
    if not os.path.exists(PT_PATH):
        raise FileNotFoundError(f"Checkpoint not found at: {PT_PATH}")

    ckpt = torch.load(PT_PATH, map_location="cpu")
    model = STGCNISLNet(in_channels=3, num_classes=NUM_CLASSES, hidden_dim=STGCN_HIDDEN_DIM)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()

    dummy_input = torch.randn(1, 3, 30, TOTAL_LANDMARKS, dtype=torch.float32)

    torch.onnx.export(
        model,
        dummy_input,
        ONNX_PATH,
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
    print(f"Successfully exported to ONNX: {ONNX_PATH}")

if __name__ == "__main__":
    export()
