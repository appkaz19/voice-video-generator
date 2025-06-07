from fastapi import FastAPI, UploadFile, File, Form
from tts.xtts_infer import generate_tts
import os
import tempfile

app = FastAPI()

@app.post("/generate")
async def generate(text: str = Form(...), language: str = Form(...), speaker_audio: UploadFile | None = File(None)):
    wav_path = None
    if speaker_audio is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await speaker_audio.read())
            wav_path = tmp.name
    result = generate_tts(text, wav_path, language)
    if wav_path:
        os.remove(wav_path)
    return {"audio_path": result}
