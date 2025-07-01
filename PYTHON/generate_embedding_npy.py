from TTS.api import TTS
import numpy as np

# Load model on CPU instead of GPU
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu = False)  # or add: gpu=False

# Path to your voice sample
audio_path = "padmesh_english_voice.wav"  # Make sure this path and file exists

# Generate speaker embedding
gpt_cond_latent, speaker_embedding = tts.synthesizer.tts_model.get_conditioning_latents(audio_path=[audio_path])

# Save the embedding
np.save("padmesh_en_emb.npy", speaker_embedding)

print("✅ Speaker embedding saved successfully.")
