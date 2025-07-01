import torch
from torch.serialization import add_safe_globals

# Fix for PyTorch 2.6+ weights_only bug with trusted models
_original_torch_load = torch.load
def patched_load(*args, **kwargs):
    kwargs["weights_only"] = False  # Force it OFF
    return _original_torch_load(*args, **kwargs)
torch.load = patched_load

# Add all required classes to PyTorch's safe globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig])

import numpy as np
from TTS.api import TTS
import os

# ===== SETTINGS =====
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
EMBEDDING_PATH = "C:/Users/padme/OneDrive/DOCUMENTS/Computational Paradigm/HRD/PYTHON/padmesh_en_emb.npy"

# ===== Load XTTS Model =====
print("🔁 Loading XTTS-v2 model...")
try:
    tts = TTS(MODEL_NAME)
    print("✅ XTTS-v2 model loaded successfully.")
except Exception as e:
    print("❌ Failed to load XTTS model.")
    print("Error:", e)
    exit()

# ===== Load Speaker Embedding =====
print(f"\n🔁 Loading speaker embedding from:\n{EMBEDDING_PATH}")
if not os.path.exists(EMBEDDING_PATH):
    print("❌ Speaker embedding file not found!")
    exit()

try:
    embedding = np.load(EMBEDDING_PATH)

    # Fix shape if needed
    if embedding.shape != (512,):
        embedding = embedding.reshape(-1)

    print("✅ Speaker embedding loaded.")
    print(f"📐 Shape: {embedding.shape}")
    print(f"📄 Dtype: {embedding.dtype}")
except Exception as e:
    print("❌ Failed to load embedding file.")
    print("Error:", e)
    exit()

# ===== Check Validity =====
if embedding.shape != (512,) or embedding.dtype != np.float32:
    print("❌ Invalid embedding format!")
    print("Expected shape: (512,), dtype: float32")
else:
    print("✅ Speaker embedding is valid and ready to use.")
