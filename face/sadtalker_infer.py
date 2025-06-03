import os
import subprocess

def generate_video(input_image, input_audio, output_path="assets/output/result.mp4"):
    sadtalker_path = "./SadTalker/inference.py"
    command = [
        "python", sadtalker_path,
        "--driven_audio", input_audio,
        "--source_image", input_image,
        "--result_dir", "assets/output",
        "--enhancer", "gfpgan",
        "--still", "--preprocess", "full"
    ]
    subprocess.run(command, check=True)
    # SadTalker saves result as result.mp4; rename it to our unique path
    default_output = os.path.join(output_dir, "result.mp4")
    if os.path.exists(default_output):
        os.replace(default_output, output_path)
    return output_path
