# uvicorn main:app --reload
from collections import defaultdict
from secrets import token_urlsafe
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from typing import Annotated
from sqlalchemy.orm import Session
from jwt import encode, decode
from datetime import datetime, timedelta

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

usuario_token_map = defaultdict(list)

@app.get("/usuario/login/token/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def login_respuesta_token(usuario: str, password: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()
    if db_usuario is None:
        return False
    else:
        if db_usuario.password == password:
            token = token_urlsafe(16)
            usuario_token_map[usuario].append(token)
            ##print(lista_token)
            
            return token
        else:
            return False

@app.get("/usuario/login/token2/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def login_respuesta_token2(usuario: str, password: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()

    if db_usuario is None:
        return {"error": "Usuario no encontrado"}

    if db_usuario.password != password:
        return {"error": "Contraseña incorrecta"}

    # Generar token
    token_payload = {
        "usuario": usuario,
        "exp": datetime.now() + timedelta(minutes=60),
    }

    token = encode(token_payload, "secret_key", algorithm="HS256")

    return {"token": token}

@app.get("/usuario/perfil", status_code=status.HTTP_200_OK)
async def obtener_perfil(token: str, db: db_dependency):
    try:
        decoded_token = decode(token, "secret_key", algorithms=["HS256"])
        usuario = decoded_token["usuario"]
    except Exception as e:
        print(f"Error al decodificar token: {e}")
        return {"error": "Token no válido"}

    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()

    if db_usuario is None:
        return {"error": "Usuario no encontrado"}

    try:
        return {
            "password": db_usuario.password,
            "nombre": db_usuario.nombre,
            "telefono": db_usuario.telefono,
            "ubicacion": db_usuario.ubicacion,
        }
    except Exception as e:
        print(f"Error al obtener perfil: {e}")
        return {"error": "Error al obtener perfil"}

@app.get("/usuario/login/respuesta/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def login_respuesta(usuario: str, password: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()
    if db_usuario is None:
        return False
    else:
        if db_usuario.password == password:
            return True
        else:
            return False
    ##    else:
    ##        return False
    ##        raise HTTPException(status_code=404, detail="Usuario o password incorrecto") 

@app.get("/usuario/login/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def login_usuario(usuario: str, password: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Nombre de usuario no encontrado") 
    else:
        if db_usuario.password == password:
            return db_usuario
        else:
            raise HTTPException(status_code=404, detail="Usuario o password incorrecto") 
        
@app.get("/usuario/mostrar/{token}/{id}", status_code=status.HTTP_200_OK)
async def mostrar_usuario(token: str, id: int, db: db_dependency):
    if token in usuario_token_map:
        db_usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado") 
        else:
            return db_usuario
    else:
        raise HTTPException(status_code=404, detail="El token no es válido")    

@app.get("/usuario/mostrar/porusuario/{usuario}", status_code=status.HTTP_200_OK)
async def mostrar_porUsuario(usuario: str, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return db_usuario.nombre, db_usuario.telefono, db_usuario.ubicacion
 
@app.post("/usuario/crear/basico", status_code=status.HTTP_201_CREATED)
async def crear_usuario_basico(usuario: UsuarioBase, db: db_dependency):
    new_user = models.Usuario(
        usuario=usuario.usuario,
        password=usuario.password,
        tipo=usuario.tipo,
    )
    db.add(new_user)
    db.commit()
    return "El usuario se ha registrado correctamente"

@app.post("/usuario/crear", status_code=status.HTTP_201_CREATED)
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

@app.post("/usuario/modificar/porusuario", status_code=status.HTTP_200_OK)
async def modificar_usuario (usuario: UsuarioBase, db: db_dependency):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario.usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado") 
    db_usuario.usuario = usuario.usuario
    db_usuario.nombre = usuario.nombre
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
    
    