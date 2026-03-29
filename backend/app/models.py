import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from .database import Base


class Group(Base):
    __tablename__ = 'groups'

    code = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group = Column(String(120), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True)

    persons = relationship('Person', back_populates='group_ref', cascade='all, delete')


class Person(Base):
    __tablename__ = 'persons'

    code = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    names = Column(String(120), nullable=False, index=True)
    last_names = Column(String(120), nullable=False, index=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    cell_number = Column(String(30), nullable=False)
    address = Column(String(250), nullable=False)
    observations = Column(Text, nullable=True)
    photo_base64 = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    group_code = Column(String(36), ForeignKey('groups.code', ondelete='CASCADE'), nullable=False, index=True)
    group_ref = relationship('Group', back_populates='persons')
