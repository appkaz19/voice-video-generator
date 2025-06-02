import os
import subprocess
import uuid
import sys


def enhance_lip_sync(video_path: str, audio_path: str, output_dir="assets/wav2lip") -> str:
    """Run Wav2Lip to refine lip sync and return path to mp4."""
    os.makedirs(output_dir, exist_ok=True)
    base_dir = os.path.join(os.path.dirname(__file__), "..", "Wav2Lip-master")
    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.mp4")
    checkpoint = os.getenv("WAV2LIP_CHECKPOINT", "checkpoints/wav2lip.pth")
    script = os.path.join(base_dir, "inference.py")
    command = [
        sys.executable,
        script,
        "--checkpoint_path",
        checkpoint,
        "--face",
        video_path,
        "--audio",
        audio_path,
        "--outfile",
        output_path,
    ]
    subprocess.run(command, check=True, cwd=base_dir)
    return output_path
