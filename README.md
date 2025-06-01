# Voice Video Generator Backend

Приложение объединяет генерацию речи и анимацию лица. Для обработки запросов используется FastAPI, а задачи выполняются асинхронно через Celery c брокером Redis.

## Установка

```bash
pip install -r requirements.txt
```

Не забудьте установить и запустить Redis локально или указать адрес работающего сервера.

## Запуск API и Celery

Запустите воркер Celery:

```bash
celery -A backend.tasks worker --loglevel=info
```

Запустите сервер FastAPI:

```bash
uvicorn backend.api:app --reload
```

## Использование

Отправьте POST запрос на `/generate` с форм-данными:

- `image` – изображение лица
- `text` – текст для озвучивания
- `language` – код языка (`ru`, `en`, `es`, `de`, `fr`)
- `speaker_audio` – опциональный пример голоса

В ответе будет `task_id`. Статус и путь до готового видео можно получить по `/result/{task_id}`.
