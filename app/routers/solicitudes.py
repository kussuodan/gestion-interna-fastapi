from fastapi import APIRouter, HTTPException, status

from app.repositories import solicitudes as repo
from app.schemas import SolicitudCreate, SolicitudEstadoUpdate, SolicitudOut

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("", response_model=SolicitudOut, status_code=status.HTTP_201_CREATED)
def crear_solicitud(solicitud: SolicitudCreate):
    creada = repo.crear(
        usuario_id=solicitud.usuario_id,
        tipo=solicitud.tipo,
        descripcion=solicitud.descripcion,
    )
    if creada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario indicado no existe.",
        )
    return creada


@router.get("", response_model=list[SolicitudOut])
def listar_solicitudes():
    return repo.listar()


@router.patch("/{solicitud_id}/estado", response_model=SolicitudOut)
def actualizar_estado_solicitud(
    solicitud_id: int,
    update: SolicitudEstadoUpdate,
):
    actualizada = repo.actualizar_estado(solicitud_id, update.estado)
    if actualizada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitud no encontrada.",
        )
    return actualizada


# Compatibilidad con el frontend/API original.
@router.put("/{solicitud_id}", response_model=SolicitudOut, deprecated=True)
def actualizar_estado_solicitud_legacy(
    solicitud_id: int,
    update: SolicitudEstadoUpdate,
):
    return actualizar_estado_solicitud(solicitud_id, update)
