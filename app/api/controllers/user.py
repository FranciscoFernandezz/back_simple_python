from sqlalchemy.orm import Session
from app.models.user import User  # tu modelo SQLAlchemy
from app.schemas.user import UserCreate  # tus esquemas Pydantic

from app.security.hash import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.contrasena)
    db_user = User(
        nombre=user.nombre,
        apellido=user.apellido,
        mail=user.mail,
        contrasena=hashed_pw,
        is_profe=user.is_profe,
        dni=user.dni
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
