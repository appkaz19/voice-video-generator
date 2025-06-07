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

CMD ["uvicorn", "services.vc_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
