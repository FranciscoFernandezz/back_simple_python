from pydantic import BaseModel, EmailStr
from typing import Optional, List, TYPE_CHECKING


class UserBase(BaseModel):
    nombre: str
    apellido: str
    mail: EmailStr

class UserCreate(UserBase):
    contrasena: str
    is_profe: bool
    dni: Optional[str] = None

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    mail: Optional[EmailStr] = None
    is_profe: Optional[bool] = None
    contrasena: Optional[str] = None
    dni: Optional[str] = None

class UserOut(UserBase):
    id_usuario: int
    is_profe: bool
    dni: Optional[str] = None
    materias: List["MateriaResponse"] = []  # ← Usamos string

    class Config:
        orm_mode = True

