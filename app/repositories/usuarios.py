import sqlite3
from datetime import datetime, timezone

from app.database import get_connection
from app.enums import RolUsuario


def crear(nombre: str, email: str, rol: RolUsuario) -> dict:
    fecha = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO usuarios (nombre, email, rol, fecha_creacion)
            VALUES (?, ?, ?, ?)
            """,
            (nombre.strip(), email.lower(), rol.value, fecha),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def listar() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM usuarios ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def obtener(usuario_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (usuario_id,),
        ).fetchone()
    return dict(row) if row else None


def eliminar(usuario_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (usuario_id,),
        )
        conn.commit()
    return cursor.rowcount > 0


def tiene_solicitudes(usuario_id: int) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM solicitudes WHERE usuario_id = ? LIMIT 1",
            (usuario_id,),
        ).fetchone()
    return row is not None


IntegrityError = sqlite3.IntegrityError
