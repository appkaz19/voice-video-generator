import ffmpeg

def merge_audio_video(audio_path, video_path, output_path):
    """Merge separate audio and video files into a single output."""

    video_input = ffmpeg.input(video_path)
    audio_input = ffmpeg.input(audio_path)

    (
        ffmpeg
        .output(video_input, audio_input, output_path,
                vcodec='copy', acodec='aac', strict='experimental')
        .overwrite_output()
        .run()
    )
