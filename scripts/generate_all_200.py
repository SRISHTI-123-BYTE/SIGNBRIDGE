"""
generate_all_200.py
Compiles 200 authentic signs for each of the 9 ISLRTC Curricular Volumes.
Total signs = 1,800 signs.
"""

import os
import re
import sys

# Load Vol 1 from existing file
sys.path.append(os.path.join(os.path.dirname(__file__), 'volume_data'))
from vol1_emergency import VOL1_EMERGENCY_200

assert len(VOL1_EMERGENCY_200) == 200, "Vol 1 must be 200 signs"

print("Vol 1 loaded with 200 signs.")
