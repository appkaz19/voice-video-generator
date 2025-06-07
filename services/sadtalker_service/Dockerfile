FROM python:3.10-slim

WORKDIR /app

# Устанавливаем системные пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    libsndfile1 \
    wget \
    git \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем локальную зависимость TTS
RUN pip install ./TTS-dev

# Скачиваем модели SadTalker для корректной работы
RUN bash SadTalker-main/scripts/download_models.sh

CMD ["uvicorn", "services.sadtalker_service.main:app", "--host", "0.0.0.0", "--port", "8003"]
