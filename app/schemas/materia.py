from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING


class MateriaBase(BaseModel):
    nombre_materia: str

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id_materia: int
    usuarios: Optional[List["UserOut"]] = None

    class Config:
        orm_mode = True




