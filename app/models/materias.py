from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuario_materia import usuario_materia
from app.database.database import Base

class Materia(Base):
    __tablename__ = "materia"

    id_materia = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(255), nullable=False)
    id_docente = Column(Integer, ForeignKey("usuario.id_usuario"))

    usuarios = relationship(
        "User",
        secondary=usuario_materia,
        back_populates="materias"
    )
