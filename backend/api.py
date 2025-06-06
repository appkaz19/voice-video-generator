from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from celery.result import AsyncResult
from backend.tasks import generate_video_task, celery_app
import uuid
import os
from werkzeug.utils import secure_filename

SECRET_KEY = os.getenv("API_SECRET_KEY")


def verify_api_key(api_key: str | None):
    if SECRET_KEY and api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

app = FastAPI(
    title="Voice Video Generator API",
    description="REST API для генерации видео с говорящим лицом. Swagger UI доступен по адресу /docs.",
    version="1.0.0",
)


@app.get("/")
async def read_root():
    """Простой корневой эндпоинт с ссылкой на документацию."""
    return {"message": "Добро пожаловать! Документация доступна по адресу /docs"}

def _save_upload(upload: UploadFile, folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(os.path.basename(upload.filename))
    path = os.path.join(folder, f"{uuid.uuid4()}_{filename}")
    with open(path, "wb") as f:
        f.write(upload.file.read())
    return path

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    text: str = Form(...),
    language: str = Form(...),
    speaker_audio: UploadFile | None = File(None),
    x_api_key: str | None = Header(None, alias="X-API-Key"),
):
    verify_api_key(x_api_key)
    image_path = _save_upload(image, "uploads")
    speaker_audio_path = _save_upload(speaker_audio, "uploads") if speaker_audio else None
    task = generate_video_task.delay(image_path, text, language, speaker_audio_path)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str, x_api_key: str | None = Header(None, alias="X-API-Key")):
    verify_api_key(x_api_key)
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"status": "completed", "video_path": result.result}
    return {"status": result.status}
