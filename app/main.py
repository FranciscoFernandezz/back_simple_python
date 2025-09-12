from fastapi import FastAPI, Depends, HTTPException   # FastAPI para la app web, Depends para inyectar dependencias
from sqlalchemy.orm import Session                   # Sesiones de SQLAlchemy
from sqlalchemy import text                          # Para ejecutar SQL crudo (ej: SELECT 1)
from app.database.database import get_db             # Función que abre/cierra la conexión a la DB
from app import models

# Importar modelos y routers
from app.models import user, materias, usuario_materia # Tus modelos SQLAlchemy
from app.schemas import materia, usuario_materia     # Schemas de Pydantic
from app.api.routes import user                      # Rutas específicas de usuario

from app.security.auth import get_current_user
from app.models.user import User

from app.api.routes import auth  # ← Importa el router de login



# ---------------------------
# CREACIÓN DE LA APLICACIÓN
# ---------------------------
app = FastAPI(
    title="Sistema Educativo API",                       # Título que aparece en la doc de Swagger
    description="API para gestionar profesores, alumnos y materias",  # Descripción de la API
    version="1.0.0",                                     # Versión de la API
)

app.include_router(user.router, prefix="/user", tags=["Usuarios"])
app.include_router(auth.router, tags=["Autenticación"])  
# ---------------------------
# RUTA DE BIENVENIDA
# ---------------------------
@app.get("/")
async def root():
    """Ruta de bienvenida (GET /)."""
    return {"message": "¡Bienvenido al Sistema Educativo API!"}


# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Verificar el estado de la aplicación y la conexión a la base de datos."""
    try:
        # Ejecutamos una consulta mínima en la DB
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "La aplicación está funcionando correctamente",
        }
    except Exception as e:
        # Si algo falla, devolvemos error
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }


# ---------------------------
# ROUTER DE USUARIOS
# ---------------------------
# Todas las rutas definidas en app/api/routes/user.py
# estarán disponibles bajo el prefijo /user
app.include_router(user.router, prefix="/user", tags=["Usuarios"])


# ---------------------------
# CRUD MATERIAS
# ---------------------------

from app.security.auth import get_current_user
from app.models.user import User

@app.post("/materias/")
def crear_materia(materia: materia.MateriaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_profe:
        raise HTTPException(status_code=403, detail="Solo profesores pueden crear materias")
    nueva_materia = models.materias.Materia(**materia.dict())
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia


@app.get("/materias/")
def listar_materias(db: Session = Depends(get_db)):
    """
    Listar todas las materias disponibles.
    """
    return db.query(models.materias.Materia).all()


@app.get("/materias/{materia_id}")
def obtener_materia(materia_id: int, db: Session = Depends(get_db)):
    """
    Obtener una materia específica por su ID.
    """
    materia_db = db.query(models.materias.Materia).filter(models.materias.Materia.id_materia == materia_id).first()

    if not materia_db:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia_db


@app.put("/materias/{materia_id}")
def actualizar_materia(
    materia_id: int,
    materia: materia.MateriaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_profe:
        raise HTTPException(status_code=403, detail="Solo profesores pueden actualizar materias")

    db_materia = db.query(models.materias.Materia).filter(models.materias.Materia.id_materia == materia_id).first()

    if not db_materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    for key, value in materia.dict().items():
        setattr(db_materia, key, value)

    db.commit()
    db.refresh(db_materia)
    return db_materia



@app.delete("/materias/{materia_id}")
def eliminar_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_profe:
        raise HTTPException(status_code=403, detail="Solo profesores pueden eliminar materias")

    materia_db = db.query(models.materias.Materia).filter(models.materias.Materia.id_materia == materia_id).first()
    if not materia_db:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    db.delete(materia_db)
    db.commit()
    return {"message": "Materia eliminada correctamente"}


# ---------------------------
# RELACIÓN USUARIO - MATERIA
# ---------------------------

@app.post("/usuario_materia/")
def asignar_materia(
    usuario_materia: usuario_materia.UsuarioMateriaBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_profe:
        raise HTTPException(status_code=403, detail="Solo profesores pueden asignar materias")

    usuario = db.query(models.user.User).filter(models.user.User.id_usuario == usuario_materia.id_usuario).first()
    materia = db.query(models.materias.Materia).filter(models.materias.Materia.id_materia == usuario_materia.id_materia).first()

    if not usuario or not materia:
        raise HTTPException(status_code=404, detail="Usuario o materia no encontrados")

    # Evitar duplicados
    if materia in usuario.materias:
        raise HTTPException(status_code=400, detail="La materia ya está asignada a este usuario")

    usuario.materias.append(materia)
    db.commit()

    return {"message": "Materia asignada correctamente"}


@app.get("/usuario/{user_id}/materias")
def listar_materias_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id_usuario != user_id and not current_user.is_profe:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver las materias de otro usuario")

    usuario_db = db.query(models.user.User).filter(models.user.User.id_usuario == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_db.materias


# ---------------------------
# EJECUCIÓN DE LA APLICACIÓN
# ---------------------------
if __name__ == "__main__":
    import uvicorn
    # Inicia la app en el host 0.0.0.0 y puerto 8000, con auto-reload para desarrollo
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
