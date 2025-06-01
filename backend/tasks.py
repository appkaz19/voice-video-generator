from celery import Celery
from tts.xtts_infer import generate_tts
from face.sadtalker_infer import generate_video

celery_app = Celery(
    'voice_video_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def generate_video_task(image_path: str, text: str, language: str, speaker_audio: str | None = None):
    tts_audio = generate_tts(text, speaker_audio, language)
    video_path = generate_video(image_path, tts_audio)
    return video_path
