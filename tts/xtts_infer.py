from TTS.api import TTS
import os
import uuid


# Модель инициализируется лениво при первом вызове generate_tts
tts_model = None



def generate_tts(text: str, speaker_wav_path: str | None, language: str,
                 output_dir: str = "assets") -> str:
    """Generate speech from text and return path to the WAV file."""
    global tts_model

    if tts_model is None:
        tts_model = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
        )

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")
    tts_model.tts_to_file(
        text=text,
        speaker_wav=speaker_wav_path,
        language=language,
        file_path=output_path,
    )
    return output_path
