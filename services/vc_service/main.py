from fastapi import FastAPI, UploadFile, File, Form
from tts.sovits_infer import convert_voice
import os
import tempfile

app = FastAPI()

@app.post("/convert")
async def convert(audio: UploadFile = File(...), speaker: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        audio_path = tmp.name
    result = convert_voice(audio_path, speaker)
    os.remove(audio_path)
    return {"audio_path": result}
