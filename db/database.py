import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "course_ladder.db"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Доступ к колонкам по имени
    conn.execute("PRAGMA foreign_keys = ON;")  # Проверка внешних ключей
    return conn


def init_db() -> None:
    with get_connection() as conn:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema)
