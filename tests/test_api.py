import io
import os
import sys
import types
from fastapi.testclient import TestClient

sys.modules.setdefault(
    "tts.xtts_infer",
    types.SimpleNamespace(generate_tts=lambda *a, **k: "tts.wav"),
)
sys.modules.setdefault(
    "tts.sovits_infer",
    types.SimpleNamespace(convert_voice=lambda *a, **k: "vc.wav"),
)
sys.modules.setdefault(
    "face.sadtalker_infer",
    types.SimpleNamespace(generate_video=lambda *a, **k: "video.mp4"),
)
sys.modules.setdefault(
    "face.wav2lip_infer",
    types.SimpleNamespace(enhance_lip_sync=lambda *a, **k: "video.mp4"),
)

import backend.api as api

class DummyTask:
    id = "dummy123"

def test_generate_and_result(monkeypatch, tmp_path):
    monkeypatch.setattr(api, "_save_upload", lambda upload, folder: str(tmp_path / upload.filename))

    def fake_delay(image_path, text, language, speaker_audio_path=None):
        return DummyTask
    monkeypatch.setattr(api.generate_video_task, "delay", fake_delay)

    client = TestClient(api.app)
    files = {"image": ("test.png", b"data", "image/png")}
    data = {"text": "hello", "language": "en"}

    response = client.post("/generate", files=files, data=data)
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    assert task_id == DummyTask.id

    class DummyResult:
        status = "SUCCESS"
        result = "/tmp/video.mp4"
        def ready(self):
            return True

    monkeypatch.setattr(api, "AsyncResult", lambda task_id, app=None: DummyResult())
    result_resp = client.get(f"/result/{task_id}")
    assert result_resp.status_code == 200
    assert result_resp.json() == {"status": "completed", "video_path": "/tmp/video.mp4"}


def test_save_upload_secure_filename(tmp_path):
    class DummyUpload:
        def __init__(self, filename: str, data: bytes = b"data"):
            self.filename = filename
            self.file = io.BytesIO(data)

    dangerous_name = "../evil.txt"
    upload = DummyUpload(dangerous_name)
    path = api._save_upload(upload, str(tmp_path))

    assert path.startswith(str(tmp_path))
    # ensure the basename doesn't include path traversal elements
    assert ".." not in os.path.relpath(path, start=tmp_path)
    with open(path, "rb") as f:
        assert f.read() == b"data"
