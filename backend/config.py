"""
SignBridge Backend Configuration
Real-Time Continuous ISL Recognition, Grammar Synthesis & Bi-Directional Speech Translation System
"""

import os
from typing import List, Dict

# MediaPipe Landmark Topology Dimensions
NUM_POSE_LANDMARKS = 25       # Upper body + head pose
NUM_HAND_LANDMARKS = 21       # Per hand (21 * 2 = 42)
NUM_FACE_LANDMARKS = 40       # Expressive face contour & non-manual markers (eyebrows, mouth, eyes)
TOTAL_LANDMARKS = NUM_POSE_LANDMARKS + (NUM_HAND_LANDMARKS * 2) + NUM_FACE_LANDMARKS # 107 joints
COORDINATE_DIM = 3            # (X, Y, Z)
INPUT_FEATURE_DIM = TOTAL_LANDMARKS * COORDINATE_DIM # 321 features per frame

# Temporal Window & Sampling Parameters
TEMPORAL_WINDOW_FRAMES = 30   # Sliding window (approx 1.0 second @ 30 FPS)
TEMPORAL_STRIDE_FRAMES = 5    # Continuous inference stride
TARGET_FPS = 30
CONFIDENCE_THRESHOLD = 0.50   # CTC gloss trigger threshold
STGCN_HIDDEN_DIM = 64         # Standardized hidden dimension for ST-GCN network

# CTC Vocabulary Tokens (Index 0 reserved for CTC Blank token <BLANK>)
VOCABULARY: List[str] = [
    "<BLANK>",
    "DOCTOR",
    "CHEST",
    "PAIN",
    "SEVERE",
    "POLICE",
    "STATION",
    "WHERE",
    "HOSPITAL",
    "GO",
    "HOW",
    "SIT",
    "WAIT",
    "10",
    "MINUTES",
    "HELP",
    "ME",
    "PLEASE",
    "MEDICINE",
    "TIME",
    "WHAT",
    "NAME",
    "YOUR",
    "YES",
    "NO",
    "THANK_YOU",
    "HELLO",
    "WATER",
    "NEED",
    "EMERGENCY",
    "FEVER",
    "BREATHING",
    "PROBLEM",
    "CALL",
    "FAMILY",
    "MONEY",
    "ACCOUNT",
    "BANK",
    "DEPOSIT",
    "WITHDRAW",
    "SIGN",
    "LANGUAGE",
    "INTERPRETER",
    "CARD",
    "COME",
    "STOP",
    "LEARN",
    "TEACHER",
    "STUDENT",
    "SCHOOL",
    "FOOD",
    "SLEEP"
]

VOCAB_TO_IDX: Dict[str, int] = {token: idx for idx, token in enumerate(VOCABULARY)}
IDX_TO_VOCAB: Dict[int, str] = {idx: token for idx, token in enumerate(VOCABULARY)}
NUM_CLASSES = len(VOCABULARY)

# Server & Network Settings
HOST = "127.0.0.1"
PORT = 8000
WS_PATH = "/ws/live-sign"

# Supported Multilingual Targets
SUPPORTED_LANGUAGES = ["en", "hi", "ta"]
DEFAULT_LANGUAGE = "en"
