# Agenda Cloud de Contactos

Aplicación pequeña en **Python** con arquitectura **frontend/backend**, base de datos **PostgreSQL** y uso obligatorio de **UUID** como código interno.

## Tecnologías
- **Backend:** FastAPI + SQLAlchemy
- **Frontend:** HTML + CSS + JavaScript
- **Base de datos:** PostgreSQL
- **Despliegue recomendado:** Render (Web Service + PostgreSQL)

## Funcionalidades
- Crear grupos
- Editar grupos
- Listar grupos
- Crear personas
- Editar personas
- Listar personas con fotografía
- Relación: una persona pertenece a un grupo
- UUID como identificador interno
- Campo `esta_activo`

## Estructura
```bash
contactos_cloud_app/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── crud.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       └── schemas.py
├── frontend/
│   ├── css/styles.css
│   ├── js/app.js
│   └── index.html
├── docs/
├── requirements.txt
├── render.yaml
└── README.md
```

## Ejecución local
### 1) Crear base PostgreSQL
```sql
CREATE DATABASE contactos_db;
```

### 2) Variables de entorno
En PowerShell:
```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:TU_PASSWORD@localhost:5432/contactos_db"
```

### 3) Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4) Ejecutar
```bash
uvicorn backend.app.main:app --reload
```

Abrir:
```text
http://127.0.0.1:8000
```

## Endpoints
- `GET /api/groups`
- `POST /api/groups`
- `PUT /api/groups/{code}`
- `GET /api/persons`
- `POST /api/persons`
- `PUT /api/persons/{code}`

## Despliegue en Render
1. Subir el proyecto a GitHub.
2. Crear cuenta en Render.
3. Elegir **New + > Blueprint**.
4. Conectar el repositorio.
5. Render leerá el archivo `render.yaml`.
6. Se crearán:
   - Un Web Service para FastAPI.
   - Una base de datos PostgreSQL.
7. Al terminar, abrir la URL pública del servicio.

## Diagrama de red
```mermaid
flowchart LR
    A[Usuario / Navegador]\nHTTPS --> B[Frontend HTML CSS JS\nRender Web Service]
    B --> C[Backend FastAPI\nRender Web Service]
    C --> D[(PostgreSQL\nRender Database)]
    E[GitHub] --> B
```

## Nota importante
Si usas el plan gratuito de Render, la documentación oficial indica que las bases de datos PostgreSQL gratuitas expiran 30 días después de su creación. Para una entrega más estable, conviene revisar eso o usar un plan pagado. 
