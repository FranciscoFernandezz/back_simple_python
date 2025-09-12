from fastapi import APIRouter
from fastapi import Depends
from app.schemas.user import UserCreate
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.api.controllers import user as user_controller

router = APIRouter()


#ruta para crear un usuario nuevo
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, user)