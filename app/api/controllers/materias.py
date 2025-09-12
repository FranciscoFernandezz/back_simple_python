# app/controllers/materia_controller.py

from sqlalchemy.orm import Session
from app.models.materias import Materia
from app.schemas.materia import MateriaCreate

def crear_materia_controller(materia_data: MateriaCreate, db: Session) -> Materia:
    nueva_materia = Materia(**materia_data.dict())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia
