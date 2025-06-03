import ffmpeg

def merge_audio_video(audio_path, video_path, output_path):
    ffmpeg.input(video_path).output(audio_path, output_path, vcodec='copy', acodec='aac', strict='experimental').run()
