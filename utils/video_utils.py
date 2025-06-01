import ffmpeg


def merge_audio_video(audio_path: str, video_path: str, output_path: str) -> None:
    """Mux audio into video file."""
    (
        ffmpeg.input(video_path)
        .output(output_path, audio=audio_path, vcodec="copy", acodec="aac")
        .run()
    )
