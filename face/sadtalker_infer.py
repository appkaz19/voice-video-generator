import subprocess
import os

def generate_video(input_image, input_audio, output_path="assets/output/result.mp4", sadtalker_root=None):
    if sadtalker_root is None:
        sadtalker_root = os.getenv("SADTALKER_ROOT", "SadTalker")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sadtalker_path = os.path.join(sadtalker_root, "inference.py")
    command = [
        "python", sadtalker_path,
        "--driven_audio", input_audio,
        "--source_image", input_image,
        "--result_dir", os.path.dirname(output_path),
        "--enhancer", "gfpgan",
        "--still", "--preprocess", "full"
    ]
    subprocess.run(command)
    return output_path
