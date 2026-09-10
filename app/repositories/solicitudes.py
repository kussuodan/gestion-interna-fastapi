from datetime import datetime, timezone

from app.database import get_connection
from app.enums import EstadoSolicitud

SELECT_SOLICITUDES = """
    SELECT
        s.id,
        s.usuario_id,
        u.nombre AS usuario_nombre,
        s.tipo,
        s.descripcion,
        s.estado,
        s.fecha_creacion
    FROM solicitudes AS s
    INNER JOIN usuarios AS u ON u.id = s.usuario_id
"""


def crear(usuario_id: int, tipo: str, descripcion: str) -> dict | None:
    fecha = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as conn:
        usuario = conn.execute(
            "SELECT id, nombre FROM usuarios WHERE id = ?",
            (usuario_id,),
        ).fetchone()
        if usuario is None:
            return None

        cursor = conn.execute(
            """
            INSERT INTO solicitudes
                (usuario_id, tipo, descripcion, estado, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario_id,
                tipo.strip(),
                descripcion.strip(),
                EstadoSolicitud.PENDIENTE.value,
                fecha,
            ),
        )
        conn.commit()

        row = conn.execute(
            SELECT_SOLICITUDES + " WHERE s.id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def listar() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            SELECT_SOLICITUDES + " ORDER BY s.id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def actualizar_estado(
    solicitud_id: int,
    estado: EstadoSolicitud,
) -> dict | None:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE solicitudes SET estado = ? WHERE id = ?",
            (estado.value, solicitud_id),
        )
        if cursor.rowcount == 0:
            return None

        conn.commit()
        row = conn.execute(
            SELECT_SOLICITUDES + " WHERE s.id = ?",
            (solicitud_id,),
        ).fetchone()

    return dict(row)
