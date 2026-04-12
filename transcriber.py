import whisper
from pathlib import Path

# Модель загружается один раз при старте.
# Варианты: tiny, base, small, medium, large
# Для русского рекомендуем medium — хороший баланс скорости и качества.
MODEL_NAME = "medium"

_model = None


def _get_model():
    global _model
    if _model is None:
        print(f"[transcriber] Загружаем модель Whisper ({MODEL_NAME})...")
        _model = whisper.load_model(MODEL_NAME)
        print(f"[transcriber] Модель загружена.")
    return _model


def transcribe(audio_path: str) -> str:
    """
    Транскрибирует аудиофайл и возвращает текст.
    """
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Аудиофайл не найден: {audio_path}")

    print(f"[transcriber] Транскрибируем: {path.name}")
    model = _get_model()
    result = model.transcribe(str(path), language="ru")
    text = result["text"].strip()
    print(f"[transcriber] Готово. Символов: {len(text)}")
    return text
