import os
import subprocess
import sys

def generate_video(input_image: str, input_audio: str, output_path: str = "assets/output/result.mp4") -> str:
    """Запустить SadTalker и вернуть путь к полученному видео."""

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    default_root = os.path.join(os.path.dirname(__file__), "..", "SadTalker-main")
    base_dir = os.environ.get("SADTALKER_ROOT", default_root)
    sadtalker_path = os.path.join(base_dir, "inference.py")

    command = [
        sys.executable,
        sadtalker_path,
        "--driven_audio",
        input_audio,
        "--source_image",
        input_image,
        "--result_dir",
        output_dir,
        "--enhancer",
        "gfpgan",
        "--still",
        "--preprocess",
        "full",
    ]

    subprocess.run(command, check=True)

    default_output = os.path.join(output_dir, "result.mp4")
    if os.path.exists(default_output):
        os.replace(default_output, output_path)
    return output_path
