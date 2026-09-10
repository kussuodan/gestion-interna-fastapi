from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import solicitudes, usuarios


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Sistema de Gestión de Usuarios y Solicitudes Internas",
    description=(
        "API para una intranet corporativa: gestión de usuarios y "
        "registro/seguimiento de solicitudes internas."
    ),
    version="1.1.0",
    lifespan=lifespan,
)

# Desarrollo local: el frontend no usa cookies ni autenticación por sesión.
# Si se despliega en producción, sustituir '*' por el origen real del frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(solicitudes.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "API del Sistema de Gestión de Usuarios y Solicitudes Internas",
        "documentacion": "/docs",
        "version": app.version,
    }
