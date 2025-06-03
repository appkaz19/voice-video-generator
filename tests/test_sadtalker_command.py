import os
import sys

import face.sadtalker_infer as si


def test_command_uses_sys_executable(monkeypatch, tmp_path):
    captured = {}

    def fake_run(cmd, check=True):
        captured['cmd'] = cmd
    monkeypatch.setattr(si.subprocess, 'run', fake_run)
    monkeypatch.setattr(si.os.path, 'exists', lambda path: False)
    monkeypatch.setattr(si.os, 'replace', lambda src, dst: None)

    si.generate_video('img.png', 'audio.wav', output_dir=str(tmp_path))

    expected_sadtalker = os.path.join(os.path.dirname(si.__file__), '..', 'SadTalker-main', 'inference.py')
    expected_command = [
        sys.executable,
        expected_sadtalker,
        '--driven_audio',
        'audio.wav',
        '--source_image',
        'img.png',
        '--result_dir',
        str(tmp_path),
        '--enhancer',
        'gfpgan',
        '--still',
        '--preprocess',
        'full',
    ]
    assert captured['cmd'] == expected_command
