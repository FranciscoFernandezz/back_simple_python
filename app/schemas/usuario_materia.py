from pydantic import BaseModel


# Para asignar materia a usuario
class UsuarioMateriaBase(BaseModel):
    id_usuario: int
    id_materia: int


# Para devolver relación
class UsuarioMateriaResponse(UsuarioMateriaBase):
    class Config:
        orm_mode = True