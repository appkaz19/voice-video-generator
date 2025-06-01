from celery import Celery
from tts.xtts_infer import generate_tts
from face.sadtalker_infer import generate_video

import boto3
import os


BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")

celery_app = Celery("voice_video_tasks", broker=BROKER_URL, backend=BACKEND_URL)

s3_bucket = os.getenv("S3_BUCKET")
s3_client = boto3.client("s3") if s3_bucket else None
@celery_app.task
def generate_video_task(image_path: str, text: str, language: str, speaker_audio: str | None = None):
    tts_audio = generate_tts(text, speaker_audio, language)
    video_path = generate_video(image_path, tts_audio)

    if s3_client:
        key = os.path.basename(video_path)
        s3_client.upload_file(video_path, s3_bucket, key)
        url = f"https://{s3_bucket}.s3.amazonaws.com/{key}"
        return url

    return video_path
