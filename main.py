"""
Использование:
    python main.py                          # спросит ссылку интерактивно
    python main.py <url>                    # ссылка аргументом
    python main.py --list                   # показать все видео в базе
    python main.py --show <video_id>        # показать транскрипцию видео
"""

import sys
from pathlib import Path
from downloader import download_audio
from transcriber import transcribe
from database import init_db, is_exists, save, get_all, get_transcription


def process(url: str):
    # 1. Скачиваем аудио
    video = download_audio(url)

    # 2. Проверяем — вдруг уже транскрибировали
    if is_exists(video.video_id):
        print(f"[main] Это видео уже есть в базе: {video.video_id}")
        return

    # 3. Транскрибируем
    text = transcribe(video.audio_path)

    # 4. Сохраняем в БД
    save(
        video_id=video.video_id,
        url=video.url,
        title=video.title,
        duration=video.duration,
        transcription=text,
    )

    # 5. Удаляем аудиофайл — транскрибация уже в базе, файл больше не нужен
    audio_file = Path(video.audio_path)
    if audio_file.exists():
        audio_file.unlink()
        print(f"[main] Аудиофайл удалён: {audio_file.name}")

    print(f"\n✅ Готово!")
    print(f"   Название:  {video.title}")
    print(f"   Длина:     {video.duration // 60}:{video.duration % 60:02d}")
    print(f"   Символов:  {len(text)}")
    print(f"   База:      transcriptions.db")


def list_videos():
    rows = get_all()
    if not rows:
        print("База пустая.")
        return
    print(f"\n{'#':<4} {'video_id':<34} {'длина':>6}  {'название'}")
    print("-" * 80)
    for i, (vid_id, url, title, duration, created_at) in enumerate(rows, 1):
        dur = f"{duration // 60}:{duration % 60:02d}" if duration else "?"
        print(f"{i:<4} {vid_id:<34} {dur:>6}  {title}")
    print(f"\nЧтобы посмотреть транскрипцию: python main.py --show <video_id>")


def show_transcription(video_id: str):
    row = get_transcription(video_id)
    if not row:
        print(f"❌ Видео не найдено: {video_id}")
        return
    title, url, transcription = row
    print(f"\n📹 {title}")
    print(f"   {url}")
    print(f"\n{'-' * 80}\n")
    print(transcription)
    print(f"\n{'-' * 80}")
    print(f"Символов: {len(transcription)}")


if __name__ == "__main__":
    init_db()

    if "--list" in sys.argv:
        list_videos()
    elif "--show" in sys.argv:
        idx = sys.argv.index("--show")
        if idx + 1 >= len(sys.argv):
            print("❌ Укажи video_id: python main.py --show <video_id>")
            sys.exit(1)
        show_transcription(sys.argv[idx + 1])
    elif len(sys.argv) >= 2:
        process(sys.argv[1])
    else:
        url = input("Введите ссылку на видео Рутуб: ").strip()
        if not url:
            print("❌ Ссылка не введена.")
            sys.exit(1)
        process(url)
