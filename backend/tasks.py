from celery import Celery

import logging

logging.basicConfig(level=logging.INFO)

import boto3
import os
import httpx


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

TTS_SERVICE_URL = os.getenv("TTS_SERVICE_URL")
VC_SERVICE_URL = os.getenv("SOVITS_SERVICE_URL")
SADTALKER_SERVICE_URL = os.getenv("SADTALKER_SERVICE_URL")
WAV2LIP_SERVICE_URL = os.getenv("WAV2LIP_SERVICE_URL")


def _generate_tts(text: str, speaker_audio: str | None, language: str) -> str:
    if TTS_SERVICE_URL:
        data = {"text": text, "language": language}
        if speaker_audio:
            with open(speaker_audio, "rb") as f:
                resp = httpx.post(
                    TTS_SERVICE_URL,
                    data=data,
                    files={"speaker_audio": f},
                )
        else:
            resp = httpx.post(
                TTS_SERVICE_URL,
                data=data,
            )
        resp.raise_for_status()
        return resp.json()["audio_path"]
    from tts.xtts_infer import generate_tts
    return generate_tts(text, speaker_audio, language)


def _convert_voice(wav_path: str, speaker: str) -> str:
    if VC_SERVICE_URL:
        with open(wav_path, "rb") as f:
            resp = httpx.post(
                VC_SERVICE_URL,
                data={"speaker": speaker},
                files={"audio": f},
            )
        resp.raise_for_status()
        return resp.json()["audio_path"]
    from tts.sovits_infer import convert_voice
    return convert_voice(wav_path, speaker)


def _generate_video(image_path: str, audio_path: str) -> str:
    if SADTALKER_SERVICE_URL:
        with open(image_path, "rb") as img, open(audio_path, "rb") as aud:
            resp = httpx.post(
                SADTALKER_SERVICE_URL,
                files={"image": img, "audio": aud},
            )
        resp.raise_for_status()
        return resp.json()["video_path"]
    from face.sadtalker_infer import generate_video
    return generate_video(image_path, audio_path)


def _enhance_lip_sync(video_path: str, audio_path: str) -> str:
    if WAV2LIP_SERVICE_URL:
        with open(video_path, "rb") as vf, open(audio_path, "rb") as af:
            resp = httpx.post(
                WAV2LIP_SERVICE_URL,
                files={"video": vf, "audio": af},
            )
        resp.raise_for_status()
        return resp.json()["video_path"]
    from face.wav2lip_infer import enhance_lip_sync
    return enhance_lip_sync(video_path, audio_path)
@celery_app.task
def generate_video_task(image_path: str, text: str, language: str, speaker_audio: str | None = None):
    tts_audio = _generate_tts(text, speaker_audio, language)

    speaker = os.getenv("SOVITS_SPK", "default")
    try:
        vc_audio = _convert_voice(tts_audio, speaker)
    except Exception:
        logging.exception("Voice conversion failed")
        vc_audio = tts_audio

    video_path = _generate_video(image_path, vc_audio)

    try:
        final_video = _enhance_lip_sync(video_path, vc_audio)
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
