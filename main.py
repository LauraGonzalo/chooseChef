# uvicorn main:app --reload
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

class UsuarioBase(BaseModel):
    id:int
    usuario: str
    nombre:str
    password:str
    descripcion: str
    ubicacion:str
    email:str
    telefono: str
    tipo: str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/usuario/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def mostrar_usuario(usuario: str, password: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Nombre de usuario no encontrado") 
    else:
        if db_usuario.password == password:
            return db_usuario
        else:
            raise HTTPException(status_code=404, detail="Usuario o password incorrecto") 
 
@app.post("/usuario/crear/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    return "El usuario se ha registrado correctamente"

@app.post("/usuario/modificar/", status_code=status.HTTP_200_OK)
async def modificar_usuario (usuario: UsuarioBase, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario.id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado") 
    db_usuario.usuario = usuario.usuario
    db_usuario.nombre = usuario.nombre
    db_usuario.password = usuario.password
    db_usuario.descripcion = usuario.descripcion
    db_usuario.ubicacion = usuario.ubicacion
    db_usuario.telefono = usuario.telefono
    db.commit()
    return "El usuario se ha modificado correctamente"
    
@app.delete("/usuario/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        db.delete(db_usuario)
        db.commit()
        return "Usuario eliminado"
    
    