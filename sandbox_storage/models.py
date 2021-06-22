from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from .database import Base

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    ForeignKey,
    String,
)

class Visa(Base):
    __tablename__    = 'visas'
    id               = Column(Integer, primary_key=True)
    elixir_id        = Column(String, nullable=False)
    passport         = Column(JSON, nullable=False)

class DrsObject(Base):
    __tablename__    = 'drs_objects'
    id               = Column(Integer, primary_key=True)
    drs_id           = Column(String, nullable=False)
    path             = Column(String, nullable=False)