from fastapi import FastAPI, UploadFile, File
from face.wav2lip_infer import enhance_lip_sync
import os
import tempfile

app = FastAPI()

@app.post("/enhance")
async def enhance(video: UploadFile = File(...), audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as v_tmp:
        v_tmp.write(await video.read())
        video_path = v_tmp.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as a_tmp:
        a_tmp.write(await audio.read())
        audio_path = a_tmp.name
    result = enhance_lip_sync(video_path, audio_path)
    os.remove(video_path)
    os.remove(audio_path)
    return {"video_path": result}
