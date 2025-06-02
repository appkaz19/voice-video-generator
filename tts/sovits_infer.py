import os
import subprocess
import uuid
import shutil
import sys
from glob import glob


def convert_voice(input_wav: str, speaker: str, output_dir="assets/converted") -> str:
    """Run so-vits-svc voice conversion and return path to converted WAV."""
    os.makedirs(output_dir, exist_ok=True)
    base_dir = os.path.join(os.path.dirname(__file__), "..", "so-vits-svc-4.1-Stable")
    raw_dir = os.path.join(base_dir, "raw")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    temp_name = f"{uuid.uuid4()}.wav"
    temp_input = os.path.join(raw_dir, temp_name)
    shutil.copy(input_wav, temp_input)

    model_path = os.getenv("SOVITS_MODEL", "logs/44k/G_0.pth")
    config_path = os.getenv("SOVITS_CONFIG", "logs/44k/config.json")
    svc_script = os.path.join(base_dir, "inference_main.py")
    command = [
        sys.executable,
        svc_script,
        "-m",
        model_path,
        "-c",
        config_path,
        "-n",
        temp_name,
        "-s",
        speaker,
    ]
    subprocess.run(command, check=True, cwd=base_dir)

    candidates = sorted(glob(os.path.join(results_dir, f"{os.path.splitext(temp_name)[0]}_*")))
    if not candidates:
        raise RuntimeError("so-vits-svc did not produce output")
    converted = candidates[-1]
    output_path = os.path.join(output_dir, os.path.basename(converted))
    shutil.move(converted, output_path)
    os.remove(temp_input)
    return output_path
