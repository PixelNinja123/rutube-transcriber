import re
import yt_dlp
from pathlib import Path
from dataclasses import dataclass

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)


@dataclass
class VideoInfo:
    video_id: str
    url: str
    title: str
    duration: int
    audio_path: str


def _extract_video_id(url: str) -> str:
    match = re.search(r"rutube\.ru/video/([a-zA-Z0-9]+)", url)
    if not match:
        raise ValueError(f"Не удалось извлечь video_id из ссылки: {url}")
    return match.group(1)


def _find_audio_file(video_id: str) -> Path | None:
    """Ищет уже скачанный файл с любым расширением."""
    for f in AUDIO_DIR.iterdir():
        if f.stem == video_id:
            return f
    return None


def download_audio(url: str, verbose: bool = False) -> VideoInfo:
    """
    Скачивает аудио с Рутуба без конвертации (ffmpeg не нужен).
    Формат берётся такой, какой отдаёт сам Рутуб (обычно m4a или webm).
    """
    video_id = _extract_video_id(url)

    # Проверяем — вдруг уже скачано
    existing = _find_audio_file(video_id)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(AUDIO_DIR / f"{video_id}.%(ext)s"),
        "quiet": not verbose,
        "no_warnings": not verbose,
        # ffmpeg НЕ используем — никаких postprocessors
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if existing:
            print(f"[downloader] Уже скачано, пропускаем: {existing.name}")
            info = ydl.extract_info(url, download=False)
            audio_path = existing
        else:
            print(f"[downloader] Скачиваем аудио...")
            info = ydl.extract_info(url, download=True)
            audio_path = _find_audio_file(video_id)
            print(f"[downloader] Сохранено: {audio_path}")

    return VideoInfo(
        video_id=video_id,
        url=url,
        title=info.get("title", ""),
        duration=info.get("duration", 0),
        audio_path=str(audio_path),
    )
