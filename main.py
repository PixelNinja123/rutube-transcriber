import sys
from pathlib import Path
from downloader import download_audio
from transcriber import transcribe
from database import init_db, is_exists, save, get_all


def process(url: str):
    video = download_audio(url)

    if is_exists(video.video_id):
        print(f"Uzhe v baze: {video.video_id}")
        return

    text = transcribe(video.audio_path)

    save(
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


def list_videos():
    rows = get_all()
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
    init_db()

    if "--list" in sys.argv:
        list_videos()
    elif len(sys.argv) >= 2:
        process(sys.argv[1])
    else:
        url = input("Vvedi ssylku: ").strip()
        if not url:
            sys.exit(1)
        process(url)
