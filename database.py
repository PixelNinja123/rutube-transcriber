import sqlite3
from pathlib import Path

DB_PATH = Path("transcriptions.db")


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id      TEXT    UNIQUE NOT NULL,
            url           TEXT    NOT NULL,
            title         TEXT,
            transcription TEXT    NOT NULL
        )
    """)
    con.commit()
    con.close()


def is_exists(video_id: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    row = con.execute("SELECT 1 FROM videos WHERE video_id = ?", (video_id,)).fetchone()
    con.close()
    return row is not None


def save(video_id: str, url: str, title: str, transcription: str):
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute(
            "INSERT INTO videos (video_id, url, title, transcription) VALUES (?, ?, ?, ?)",
            (video_id, url, title, transcription),
        )
        con.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        con.close()


def get_all():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT video_id, url, title, transcription FROM videos ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows
