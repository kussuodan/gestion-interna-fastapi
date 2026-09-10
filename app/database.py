from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                rol TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS solicitudes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                fecha_creacion TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE RESTRICT
            );

            CREATE INDEX IF NOT EXISTS idx_solicitudes_usuario_id
            ON solicitudes (usuario_id);

            CREATE INDEX IF NOT EXISTS idx_solicitudes_estado
            ON solicitudes (estado);
            """
        )
        conn.commit()
