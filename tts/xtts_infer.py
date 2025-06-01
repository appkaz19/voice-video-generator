from TTS.api import TTS
import os
import logging

logger = logging.getLogger(__name__)

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

def generate_tts(text, speaker_wav_path, language, output_path="assets/tts.wav"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    logger.info("Generating speech to %s", output_path)
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav_path,
        language=language,
        file_path=output_path,
    )
    return output_path
