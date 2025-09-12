# app/models/usuario_materia.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.database import Base

usuario_materia = Table(
    "usuario_materia",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), primary_key=True),
    Column("id_materia", Integer, ForeignKey("materia.id_materia", ondelete="CASCADE"), primary_key=True)
)
