from pathlib import Path

from fastapi.testclient import TestClient

import app.database as database
from app.main import app


def test_flujo_principal(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")

    with TestClient(app) as client:
        usuario = client.post(
            "/usuarios",
            json={
                "nombre": "Laura Méndez",
                "email": "laura@example.com",
                "rol": "Empleado",
            },
        )
        assert usuario.status_code == 201
        usuario_id = usuario.json()["id"]

        duplicado = client.post(
            "/usuarios",
            json={
                "nombre": "Otra Laura",
                "email": "laura@example.com",
                "rol": "Consulta",
            },
        )
        assert duplicado.status_code == 409

        solicitud = client.post(
            "/solicitudes",
            json={
                "usuario_id": usuario_id,
                "tipo": "Soporte técnico",
                "descripcion": "No funciona la impresora",
            },
        )
        assert solicitud.status_code == 201
        solicitud_id = solicitud.json()["id"]
        assert solicitud.json()["estado"] == "Pendiente"

        cambio = client.patch(
            f"/solicitudes/{solicitud_id}/estado",
            json={"estado": "Aprobada"},
        )
        assert cambio.status_code == 200
        assert cambio.json()["estado"] == "Aprobada"

        eliminar = client.delete(f"/usuarios/{usuario_id}")
        assert eliminar.status_code == 409
