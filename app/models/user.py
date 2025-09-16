""" from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.usuario_materia import usuario_materia
from app.database.database import Base

class User(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)      # no unique, con max length 50
    apellido = Column(String(50), nullable=False)    # no unique, con max length 50
    mail = Column(String(100), unique=True, nullable=False, index=True)  # UNIQUE
    contrasena = Column(String(255), nullable=False)
    is_profe = Column(Boolean, nullable=False)
    dni = Column(String(20), nullable=True)          # nullable porque no tiene NOT NULL

    # Relación con materias (muchos a muchos)
    materias = relationship(
        "Materia",
        secondary=usuario_materia,
        back_populates="usuarios"
    ) """


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User  # tu modelo SQLAlchemy
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    mail: str
    contrasena: str
    is_profe: bool
    dni: str | None = None  # opcional porque en tu modelo es nullable

@app.post("/usuarios/")
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    nuevo_usuario = User(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        mail=usuario.mail,
        contrasena=usuario.contrasena,
        is_profe=usuario.is_profe,
        dni=usuario.dni
    )
    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
