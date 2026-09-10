from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums import EstadoSolicitud, RolUsuario

Nombre = Annotated[str, Field(min_length=2, max_length=120)]
TipoSolicitud = Annotated[str, Field(min_length=2, max_length=120)]
Descripcion = Annotated[str, Field(max_length=1000)]


class UsuarioCreate(BaseModel):
    nombre: Nombre
    email: EmailStr
    rol: RolUsuario


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    rol: RolUsuario
    fecha_creacion: datetime


class SolicitudCreate(BaseModel):
    usuario_id: int = Field(gt=0)
    tipo: TipoSolicitud
    descripcion: Descripcion = ""


class SolicitudOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    usuario_nombre: str | None = None
    tipo: str
    descripcion: str = ""
    estado: EstadoSolicitud
    fecha_creacion: datetime


class SolicitudEstadoUpdate(BaseModel):
    estado: EstadoSolicitud
