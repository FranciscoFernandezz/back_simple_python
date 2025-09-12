from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.materias import Materia
from app.schemas.materia import MateriaCreate, MateriaResponse

router = APIRouter(prefix="/materias", tags=["materias"])

@router.post("/", response_model=MateriaResponse)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    nueva_materia = Materia(**materia.dict())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia

@router.get("/hello")
def hello():
    return {"message": "Hola desde el endpoint de materias"}
