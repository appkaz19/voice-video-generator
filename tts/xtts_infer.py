from TTS.api import TTS
import os
import uuid

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)


def generate_tts(text, speaker_wav_path, language, output_dir="assets"):
    """Generate speech from text and return path to the WAV file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav_path,
        language=language,
        file_path=output_path,
    )
    return output_path
