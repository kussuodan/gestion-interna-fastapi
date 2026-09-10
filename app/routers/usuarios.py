from fastapi import APIRouter, HTTPException, Response, status

from app.repositories import usuarios as repo
from app.schemas import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    try:
        return repo.crear(
            nombre=usuario.nombre,
            email=str(usuario.email),
            rol=usuario.rol,
        )
    except repo.IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email.",
        ) from exc


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios():
    return repo.listar()


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int):
    usuario = repo.obtener(usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int) -> Response:
    if repo.obtener(usuario_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    if repo.tiene_solicitudes(usuario_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se puede eliminar el usuario porque tiene solicitudes asociadas. "
                "Conserva el historial o implementa una baja lógica si necesitas desactivarlo."
            ),
        )

    repo.eliminar(usuario_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
