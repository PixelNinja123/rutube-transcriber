import sqlite3
from pathlib import Path

DB_PATH = Path("transcriptions.db")


def init_db(db_path: Path):
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id      TEXT    UNIQUE NOT NULL,
            url           TEXT    NOT NULL,
            title         TEXT,
            transcription TEXT    NOT NULL,
            tag           TEXT
        )
    """)
    con.commit()
    con.close()


def is_exists(video_id: str, db_path: Path) -> bool:
    con = sqlite3.connect(db_path)
    row = con.execute("SELECT 1 FROM videos WHERE video_id = ?", (video_id,)).fetchone()
    con.close()
    return row is not None


def save(db_path: Path, video_id: str, url: str, title: str, transcription: str, tag: str = 'NULL'):
    con = sqlite3.connect(db_path)
    try:
        con.execute(
            f"INSERT INTO videos (video_id, url, title, transcription, tag) VALUES (?, ?, ?, ?, ?)",
            (video_id, url, title, transcription, tag),
        )
        con.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        con.close()


def get_all(db_path: Path):
    con = sqlite3.connect(db_path)
    rows = con.execute(
        "SELECT video_id, url, title, transcription, tag FROM videos ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows
