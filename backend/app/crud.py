from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from . import models, schemas


# ------------------------------
# Groups
# ------------------------------
def list_groups(db: Session):
    rows = (
        db.query(models.Group, func.count(models.Person.code).label('people_count'))
        .outerjoin(models.Person, models.Person.group_code == models.Group.code)
        .group_by(models.Group.code)
        .order_by(models.Group.group.asc())
        .all()
    )

    result = []
    for group, people_count in rows:
        result.append(
            schemas.GroupOut(
                code=group.code,
                group=group.group,
                is_active=group.is_active,
                people_count=people_count,
            )
        )
    return result


def create_group(db: Session, payload: schemas.GroupCreate):
    group = models.Group(group=payload.group.strip(), is_active=payload.is_active)
    db.add(group)
    try:
        db.commit()
        db.refresh(group)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Ya existe un grupo con ese nombre.')

    return schemas.GroupOut(code=group.code, group=group.group, is_active=group.is_active, people_count=0)


def update_group(db: Session, code: str, payload: schemas.GroupUpdate):
    group = db.get(models.Group, code)
    if not group:
        raise HTTPException(status_code=404, detail='Grupo no encontrado.')

    group.group = payload.group.strip()
    group.is_active = payload.is_active

    try:
        db.commit()
        db.refresh(group)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='No se pudo actualizar el grupo por duplicidad.')

    people_count = db.query(func.count(models.Person.code)).filter(models.Person.group_code == group.code).scalar() or 0
    return schemas.GroupOut(code=group.code, group=group.group, is_active=group.is_active, people_count=people_count)


# ------------------------------
# Persons
# ------------------------------
def list_persons(db: Session):
    persons = (
        db.query(models.Person)
        .options(joinedload(models.Person.group_ref))
        .order_by(models.Person.names.asc(), models.Person.last_names.asc())
        .all()
    )

    return [
        schemas.PersonOut(
            code=p.code,
            names=p.names,
            last_names=p.last_names,
            email=p.email,
            cell_number=p.cell_number,
            address=p.address,
            observations=p.observations,
            photo_base64=p.photo_base64,
            is_active=p.is_active,
            group_code=p.group_code,
            group_name=p.group_ref.group if p.group_ref else 'Sin grupo',
        )
        for p in persons
    ]


def create_person(db: Session, payload: schemas.PersonCreate):
    group = db.get(models.Group, payload.group_code)
    if not group:
        raise HTTPException(status_code=404, detail='El grupo seleccionado no existe.')

    person = models.Person(
        names=payload.names.strip(),
        last_names=payload.last_names.strip(),
        email=payload.email.lower().strip(),
        cell_number=payload.cell_number.strip(),
        address=payload.address.strip(),
        observations=(payload.observations or '').strip() or None,
        photo_base64=payload.photo_base64,
        is_active=payload.is_active,
        group_code=payload.group_code,
    )
    db.add(person)

    try:
        db.commit()
        db.refresh(person)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='El correo ya está registrado.')

    return schemas.PersonOut(
        code=person.code,
        names=person.names,
        last_names=person.last_names,
        email=person.email,
        cell_number=person.cell_number,
        address=person.address,
        observations=person.observations,
        photo_base64=person.photo_base64,
        is_active=person.is_active,
        group_code=person.group_code,
        group_name=group.group,
    )


def update_person(db: Session, code: str, payload: schemas.PersonUpdate):
    person = db.get(models.Person, code)
    if not person:
        raise HTTPException(status_code=404, detail='Persona no encontrada.')

    group = db.get(models.Group, payload.group_code)
    if not group:
        raise HTTPException(status_code=404, detail='El grupo seleccionado no existe.')

    person.names = payload.names.strip()
    person.last_names = payload.last_names.strip()
    person.email = payload.email.lower().strip()
    person.cell_number = payload.cell_number.strip()
    person.address = payload.address.strip()
    person.observations = (payload.observations or '').strip() or None
    person.photo_base64 = payload.photo_base64
    person.is_active = payload.is_active
    person.group_code = payload.group_code

    try:
        db.commit()
        db.refresh(person)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='No se pudo actualizar la persona por duplicidad de correo.')

    return schemas.PersonOut(
        code=person.code,
        names=person.names,
        last_names=person.last_names,
        email=person.email,
        cell_number=person.cell_number,
        address=person.address,
        observations=person.observations,
        photo_base64=person.photo_base64,
        is_active=person.is_active,
        group_code=person.group_code,
        group_name=group.group,
    )
