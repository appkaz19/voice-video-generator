import os
import subprocess
import uuid
import sys


def generate_video(input_image, input_audio, output_dir="assets/output"):
    """Generate talking head video and return path to the MP4 file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.mp4")

    sadtalker_path = os.path.join(
        os.path.dirname(__file__), "..", "SadTalker-main", "inference.py"
    )
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
    # SadTalker saves result as result.mp4; rename it to our unique path
    default_output = os.path.join(output_dir, "result.mp4")
    if os.path.exists(default_output):
        os.replace(default_output, output_path)
    return output_path
