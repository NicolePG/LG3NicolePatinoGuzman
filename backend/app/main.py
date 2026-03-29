from pathlib import Path
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / 'frontend'

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Agenda Cloud de Contactos',
    version='1.0.0',
    description='Aplicación de contactos con arquitectura frontend/backend y PostgreSQL.'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory=FRONTEND_DIR), name='static')


@app.get('/')
def home():
    return FileResponse(FRONTEND_DIR / 'index.html')


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/api/groups', response_model=list[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return crud.list_groups(db)


@app.post('/api/groups', response_model=schemas.GroupOut)
def post_group(payload: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, payload)


@app.put('/api/groups/{code}', response_model=schemas.GroupOut)
def put_group(code: str, payload: schemas.GroupUpdate, db: Session = Depends(get_db)):
    return crud.update_group(db, code, payload)


@app.get('/api/persons', response_model=list[schemas.PersonOut])
def get_persons(db: Session = Depends(get_db)):
    return crud.list_persons(db)


@app.post('/api/persons', response_model=schemas.PersonOut)
def post_person(payload: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db, payload)


@app.put('/api/persons/{code}', response_model=schemas.PersonOut)
def put_person(code: str, payload: schemas.PersonUpdate, db: Session = Depends(get_db)):
    return crud.update_person(db, code, payload)
