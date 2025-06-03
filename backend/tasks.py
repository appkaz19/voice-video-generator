from celery import Celery

import logging

logging.basicConfig(level=logging.INFO)

import boto3
import os


BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/1")

celery_app = Celery("voice_video_tasks", broker=BROKER_URL, backend=BACKEND_URL)

s3_bucket = os.getenv("S3_BUCKET")
s3_endpoint = os.getenv("S3_ENDPOINT")
s3_region = os.getenv("S3_REGION")
s3_access_key = os.getenv("S3_ACCESS_KEY_ID")
s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
s3_url_bucket = os.getenv("S3_URL_BUCKET")
s3_client = (
    boto3.client(
        "s3",
        endpoint_url=s3_endpoint,
        region_name=s3_region,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
    )
    if s3_bucket
    else None
)
@celery_app.task
def generate_video_task(image_path: str, text: str, language: str, speaker_audio: str | None = None):
    from tts.xtts_infer import generate_tts
    from tts.sovits_infer import convert_voice
    from face.sadtalker_infer import generate_video
    from face.wav2lip_infer import enhance_lip_sync
    tts_audio = generate_tts(text, speaker_audio, language)

    speaker = os.getenv("SOVITS_SPK", "default")
    try:
        vc_audio = convert_voice(tts_audio, speaker)
    except Exception:
        logging.exception("Voice conversion failed")
        vc_audio = tts_audio

    video_path = generate_video(image_path, vc_audio)

    try:
        final_video = enhance_lip_sync(video_path, vc_audio)
    except Exception:
        logging.exception("Lip sync enhancement failed")
        final_video = video_path

    if s3_client:
        key = os.path.basename(final_video)
        try:
            logging.info("Uploading %s to S3 bucket %s", final_video, s3_bucket)
            s3_client.upload_file(final_video, s3_bucket, key)
            if s3_url_bucket:
                url = f"{s3_url_bucket}/{key}"
            else:
                url = f"https://{s3_bucket}.s3.amazonaws.com/{key}"
            logging.info("File uploaded successfully: %s", url)
            return url
        except Exception:
            logging.exception("Failed to upload file to S3")
            return final_video

    return final_video
