import os
import subprocess
import uuid
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tts.sovits_infer as sovits
from tts.sovits_infer import convert_voice


def test_convert_voice_process_failure(monkeypatch, tmp_path):
    # create dummy wav file
    wav_in = tmp_path / "in.wav"
    wav_in.write_bytes(b"0")

    # use predictable uuid
    monkeypatch.setattr(uuid, "uuid4", lambda: "testid")

    # simulate failure of subprocess.run
    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0])
    monkeypatch.setattr(subprocess, "run", fake_run)

    base_dir = os.path.join(os.path.dirname(sovits.__file__), "..", "so-vits-svc-4.1-Stable")
    raw_dir = os.path.join(base_dir, "raw")
    temp_input = os.path.join(raw_dir, "testid.wav")
    # ensure clean state
    if os.path.exists(temp_input):
        os.remove(temp_input)

    with pytest.raises(RuntimeError, match="so-vits-svc failed"):
        convert_voice(str(wav_in), "spk")

    assert not os.path.exists(temp_input)
