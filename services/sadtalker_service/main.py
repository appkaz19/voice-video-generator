from fastapi import FastAPI, UploadFile, File
from face.sadtalker_infer import generate_video
import os
import tempfile

app = FastAPI()

@app.post("/animate")
async def animate(image: UploadFile = File(...), audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1] or ".png") as img_tmp:
        img_tmp.write(await image.read())
        img_path = img_tmp.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_tmp:
        audio_tmp.write(await audio.read())
        audio_path = audio_tmp.name
    result = generate_video(img_path, audio_path)
    os.remove(img_path)
    os.remove(audio_path)
    return {"video_path": result}
