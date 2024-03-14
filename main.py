from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

class ChefBase(BaseModel):
    chefId:int
    usuarioChef: str
    nombreChef:str
    password:str
    descripcion: str
    telefono: str
    ubicacion:str
    email:str

class ClienteBase(BaseModel):
    clienteId:int
    usuarioCliente: str
    nombreCliente:str
    password:str
    email:str

class AdministradorBase(BaseModel):
    administradorId:int
    usuarioAdministrador: str
    password:str
    email:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/login/{nombre}/{password}", status_code=status.HTTP_200_OK)
async def login_usuario(nombre: str, password: str):
    if(nombre == "julio" and password == "leon"):
        return True
    else: 
        return False
            
    
@app.post("/chef/", status_code=status.HTTP_201_CREATED)
async def insertar_chef(chef: ChefBase, db: db_dependency):
    db_chef = models.Chef(**chef.dict())
    db.add(db_chef)
    db.commit()
    return "El chef se ha registrado correctamente"
