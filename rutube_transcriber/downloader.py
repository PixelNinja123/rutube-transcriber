import re
import yt_dlp
from pathlib import Path
from dataclasses import dataclass

VIDEO_DIR = Path("video")
VIDEO_DIR.mkdir(exist_ok=True)


@dataclass
class VideoInfo:
    video_id: str
    url: str
    title: str
    audio_path: str


def _extract_video_id(url: str) -> str:
    match = re.search(r"rutube\.ru/video/([a-zA-Z0-9]+)", url)
    if not match:
        raise ValueError(f"Ne udalos izvlech video_id iz ssylki: {url}")
    return match.group(1)


def _find_file(video_id: str) -> Path | None:
    for f in VIDEO_DIR.iterdir():
        if f.stem == video_id:
            return f
    return None


def download_audio(url: str, verbose: bool = False) -> VideoInfo:
    video_id = _extract_video_id(url)
    existing = _find_file(video_id)

    ydl_opts = {
        "format": "worstvideo+bestaudio/worst",
        "outtmpl": str(VIDEO_DIR / f"{video_id}.%(ext)s"),
        "quiet": not verbose,
        "no_warnings": not verbose,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if existing:
            print(f"[downloader] Uzhe skachano: {existing.name}")
            info = ydl.extract_info(url, download=False)
            file_path = existing
        else:
            print(f"[downloader] Skachivagem video (worst quality)...")
            info = ydl.extract_info(url, download=True)
            file_path = _find_file(video_id)
            print(f"[downloader] Sokhraneno: {file_path}")

    return VideoInfo(
        video_id=video_id,
        url=url,
        title=info.get("title", ""),
        audio_path=str(file_path),
    )
