import ffmpeg

def merge_audio_video(audio_path, video_path, output_path):
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)
    ffmpeg.output(video, audio, output_path,
                  vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True)
