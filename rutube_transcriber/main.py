import sys
from pathlib import Path
from rutube_transcriber.downloader import download_audio
from rutube_transcriber.transcriber import transcribe
from rutube_transcriber.database import init_db, is_exists, save, get_all, DB_PATH


def process(url: str, db_path: Path):
    video = download_audio(url)

    if is_exists(video.video_id, db_path):
        print(f"Uzhe v baze: {video.video_id}")
        return

    text = transcribe(video.audio_path)

    save(
        db_path,
        video_id=video.video_id,
        url=video.url,
        title=video.title,
        transcription=text,
    )

    video_file = Path(video.audio_path)
    if video_file.exists():
        video_file.unlink()

    print(f"\nGotovo!")
    print(f"   Nazvanie: {video.title}")
    print(f"   Simvolov: {len(text)}")


def list_videos(db_path: Path):
    rows = get_all(db_path)
    if not rows:
        print("Baza pustaja.")
        return

    for i, (vid_id, url, title, transcription) in enumerate(rows, 1):
        print(f"\n{'=' * 80}")
        print(f"#{i}")
        print(f"Nazvanie:      {title}")
        print(f"URL:           {url}")
        print(f"video_id:      {vid_id}")
        print(f"Transkribacija:\n{transcription}")

    print(f"\n{'=' * 80}")


if __name__ == "__main__":
    init_db(DB_PATH)

    if "--list" in sys.argv:
        list_videos(DB_PATH)
    elif len(sys.argv) >= 2:
        process(sys.argv[1], DB_PATH)
    else:
        url = input("Vvedi ssylku: ").strip()
        if not url:
            sys.exit(1)
        process(url, DB_PATH)
