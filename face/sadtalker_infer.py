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
    subprocess.run(command)
    return output_path
