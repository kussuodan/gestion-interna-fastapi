# Sistema de Gestión de Usuarios y Solicitudes Internas

Proyecto de ejemplo para una intranet corporativa. Incluye un backend en **FastAPI + SQLite** y un frontend en **HTML, CSS y JavaScript** sin frameworks.

## Estructura

```text
gestion-interna/
├── app/
│   ├── main.py                 # Configuración de FastAPI
│   ├── database.py             # Conexión e inicialización de SQLite
│   ├── enums.py                # Roles y estados válidos
│   ├── schemas.py              # Modelos Pydantic de entrada/salida
│   ├── repositories/           # Consultas SQL y acceso a datos
│   │   ├── usuarios.py
│   │   └── solicitudes.py
│   └── routers/                # Endpoints HTTP
│       ├── usuarios.py
│       └── solicitudes.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   └── test_api.py
├── main.py                     # Permite seguir usando `python main.py`
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
└── README.md
```

La separación es intencionalmente moderada: los routers se ocupan de HTTP, los repositorios de SQL y los schemas de validación. No se añadieron capas de servicios o arquitectura hexagonal porque, para el tamaño actual, solo agregarían complejidad sin beneficio real.

## Ejecutar el proyecto

### 1. Crear y activar un entorno virtual (recomendado)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Levantar la API

```bash
python main.py
```

API: <http://localhost:8000>  
Swagger: <http://localhost:8000/docs>

### 4. Levantar el frontend

Desde la raíz del proyecto:

```bash
python -m http.server 5500 --directory frontend
```

Después abre <http://localhost:5500>.

También puedes abrir `frontend/index.html` directamente, aunque servirlo por HTTP es más parecido a un entorno real.

## Endpoints

### Usuarios

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/usuarios` | Crea un usuario |
| GET | `/usuarios` | Lista los usuarios |
| GET | `/usuarios/{id}` | Obtiene un usuario |
| DELETE | `/usuarios/{id}` | Elimina un usuario si no tiene historial asociado |

Roles válidos: `Admin`, `Empleado`, `Consulta`.

### Solicitudes

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/solicitudes` | Crea una solicitud |
| GET | `/solicitudes` | Lista las solicitudes |
| PATCH | `/solicitudes/{id}/estado` | Cambia únicamente el estado |
| PUT | `/solicitudes/{id}` | Endpoint anterior, conservado como compatibilidad y marcado como deprecated |

Estados válidos: `Pendiente`, `Aprobada`, `Rechazada`, `Finalizada`.

## Mejoras aplicadas

- Separación del backend en routers, schemas, enums, base de datos y repositorios.
- Inicialización de SQLite mediante el ciclo de vida de FastAPI en lugar de ejecutar efectos secundarios al importar módulos.
- `Enum` para roles y estados; Swagger muestra automáticamente los valores permitidos.
- Validaciones de longitud y de IDs mediante Pydantic.
- Fechas almacenadas en UTC y expuestas como `datetime`.
- Email normalizado a minúsculas antes de guardarse.
- Código de error `409 Conflict` para emails duplicados y para intentar borrar usuarios con solicitudes.
- Protección explícita del historial de solicitudes con `ON DELETE RESTRICT`.
- Índices SQLite para `usuario_id` y `estado`.
- Endpoint semántico `PATCH /solicitudes/{id}/estado` para actualizar solo el estado.
- Endpoint `PUT` anterior conservado para no romper clientes existentes.
- CORS de desarrollo sin `allow_credentials=True`, ya que el proyecto no usa cookies de sesión.
- Frontend dividido en HTML, CSS y JavaScript.
- `.gitignore` y pruebas básicas de integración.

## Pruebas

Instala las dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Ejecuta:

```bash
pytest
```

Las pruebas usan una base SQLite temporal y no modifican `database.db`.

## Decisiones de diseño

SQLite sigue siendo una buena elección para esta demo. Si el proyecto creciera hacia un sistema multiusuario real, el siguiente paso natural sería migrar el acceso a datos a SQLAlchemy/SQLModel y usar PostgreSQL, además de añadir autenticación, autorización por rol, migraciones (Alembic), paginación y logging estructurado.
