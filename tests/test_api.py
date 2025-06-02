import io
from fastapi.testclient import TestClient
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
