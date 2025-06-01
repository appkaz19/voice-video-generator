import logging
import gradio as gr
from tts.xtts_infer import generate_tts
from face.sadtalker_infer import generate_video

logging.basicConfig(level=logging.INFO)

def generate_avatar_video(image, text, language, speaker_audio=None):
    tts_audio = generate_tts(text, speaker_audio, language)
    output_video = generate_video(image, tts_audio)
    return output_video

iface = gr.Interface(
    fn=generate_avatar_video,
    inputs=[
        gr.Image(type="filepath", label="Фото"),
        gr.Textbox(label="Текст"),
        gr.Dropdown(["ru", "en", "es", "de", "fr"], label="Язык"),
        gr.Audio(type="filepath", optional=True, label="Ваш голос (опционально)")
    ],
    outputs=gr.Video(label="Сгенерированное видео"),
    title="AI Говорящий Аватар",
    description="Введите текст и фото — получите видео с анимированным говорящим лицом."
)

iface.launch()
