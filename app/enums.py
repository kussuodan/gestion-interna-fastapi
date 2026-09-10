from enum import Enum


class RolUsuario(str, Enum):
    ADMIN = "Admin"
    EMPLEADO = "Empleado"
    CONSULTA = "Consulta"


class EstadoSolicitud(str, Enum):
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"
    FINALIZADA = "Finalizada"
