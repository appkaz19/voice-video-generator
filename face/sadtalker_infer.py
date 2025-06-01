import subprocess
import os

import logging
from utils.video_utils import merge_audio_video

logger = logging.getLogger(__name__)

def generate_video(input_image, input_audio, output_path="assets/output/result.mp4", sadtalker_root=None):
    if sadtalker_root is None:
        sadtalker_root = os.getenv("SADTALKER_ROOT", "SadTalker")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sadtalker_path = os.path.join(sadtalker_root, "inference.py")
    command = [

        "python",
        sadtalker_path,
        "--driven_audio",
        input_audio,
        "--source_image",
        input_image,
        "--result_dir",
        os.path.dirname(output_path),
        "--enhancer",
        "gfpgan",
        "--still",
        "--preprocess",

        "python", sadtalker_path,
        "--driven_audio", input_audio,
        "--source_image", input_image,
        "--result_dir", os.path.dirname(output_path),
        "--enhancer", "gfpgan",
        "--still", "--preprocess", "full"

    ]

    logger.info("Running SadTalker: %s", " ".join(command))
    subprocess.run(command, check=True)

    # locate generated video inside result_dir
    result_dir = os.path.dirname(output_path)
    generated_video = None
    for fname in os.listdir(result_dir):
        if fname.lower().endswith(".mp4"):
            generated_video = os.path.join(result_dir, fname)
            break

    if not generated_video:
        raise FileNotFoundError("SadTalker did not generate a video")

    if generated_video != output_path:
        merge_audio_video(input_audio, generated_video, output_path)
    return output_path
