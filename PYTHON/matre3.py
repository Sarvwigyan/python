import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Set correct path using raw string or forward slashes
speaker_path = r"C:\Users\padme\Documents(L)\Sarvwigyan\Training_model\wavs\padmesh_english_voice.wav"

# Run TTS
wav = tts.tts(text="Hello world!", speaker_wav=speaker_path, language="en")

# Save output to file
tts.tts_to_file(text="Hello world!", speaker_wav=speaker_path, language="en", file_path="output.wav")
