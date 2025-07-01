import numpy as np
import torch
from TTS.api import TTS
from torch.serialization import add_safe_globals

# Add globals needed for safe PyTorch loading
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseDatasetConfig

add_safe_globals([XttsConfig, BaseDatasetConfig])

# Force torch.load to allow full loading
torch_load = torch.load
def torch_load_fixed(*args, **kwargs):
    kwargs["weights_only"] = False
    return torch_load(*args, **kwargs)
torch.load = torch_load_fixed

# === Load your speaker embedding ===
embedding_path = r"C:/Users/padme/OneDrive/DOCUMENTS/Computational Paradigm/HRD/PYTHON/padmesh_en_emb.npy"
print(f"🔁 Loading speaker embedding from:\n{embedding_path}")
speaker_embedding = np.load(embedding_path)

# === Fix shape if needed ===
if speaker_embedding.shape == (1, 512, 1):
    speaker_embedding = speaker_embedding.reshape(512,)
    print("🔧 Reshaped speaker embedding from (1, 512, 1) ➜ (512,)")

# === Validate embedding ===
if speaker_embedding.shape != (512,):
    raise ValueError(f"❌ Invalid embedding shape: {speaker_embedding.shape}. Must be (512,)")

if speaker_embedding.dtype != np.float32:
    raise ValueError(f"❌ Invalid dtype: {speaker_embedding.dtype}. Must be float32")

print("✅ Speaker embedding loaded and valid.")

# === Load the XTTS model ===
print("🔁 Loading XTTS-v2 model...")
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(MODEL_NAME, gpu=torch.cuda.is_available(), progress_bar=False)
print("✅ Model loaded.")

# === Register the custom speaker ===
tts.speakers["custom"] = {"embedding": speaker_embedding}
print("✅ Custom speaker registered.")

# === Text-to-Speech ===
text = "Hello, this is your cloned voice speaking using XTTS version 2."
language = "en"
output_path = r"C:/Users/padme/OneDrive/DOCUMENTS/Computational Paradigm/HRD/PYTHON/output_audio.wav"

print(f"🎤 Generating audio in language: {language}")
tts.tts_to_file(
    text=text,
    speaker="custom",
    language=language,
    file_path=output_path
)

print(f"✅ Audio saved to:\n{output_path}")
