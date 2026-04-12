import sqlite3
from pathlib import Path

DB_PATH = Path("transcriptions.db")


def init_db():
    """Создаёт базу и таблицу если их ещё нет."""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id      TEXT    UNIQUE NOT NULL,
            url           TEXT    NOT NULL,
            title         TEXT,
            duration      INTEGER,
            transcription TEXT    NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()
    print(f"[database] База готова: {DB_PATH}")


def is_exists(video_id: str) -> bool:
    """Проверяет, есть ли уже запись с таким video_id."""
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT 1 FROM videos WHERE video_id = ?", (video_id,)
    ).fetchone()
    con.close()
    return row is not None


def save(video_id: str, url: str, title: str, duration: int, transcription: str):
    """Сохраняет запись. Если video_id уже есть — пропускает."""
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute(
            """
            INSERT INTO videos (video_id, url, title, duration, transcription)
            VALUES (?, ?, ?, ?, ?)
            """,
            (video_id, url, title, duration, transcription),
        )
        con.commit()
        print(f"[database] Сохранено: {video_id}")
    except sqlite3.IntegrityError:
        print(f"[database] Уже в базе, пропускаем: {video_id}")
    finally:
        con.close()


def get_all():
    """Возвращает все записи (для отладки)."""
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT video_id, url, title, duration, created_at FROM videos ORDER BY created_at DESC"
    ).fetchall()
    con.close()
    return rows


def get_transcription(video_id: str):
    """Возвращает транскрипцию одного видео по video_id."""
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT title, url, transcription FROM videos WHERE video_id = ?",
        (video_id,)
    ).fetchone()
    con.close()
    return row
