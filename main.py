# uvicorn main:app --reload

from fastapi import  FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import  SessionLocal
import models
from typing import Annotated
from sqlalchemy.orm import Session
from jwt import encode, decode
from datetime import datetime, timedelta
from sqlalchemy.sql import or_
from security import codif, descodif


app = FastAPI()

class UsuarioBase(BaseModel):
    id: int
    usuario: str
    nombre:str
    password:str
    descripcion: str
    ubicacion:str
    email:str
    telefono: str
    tipo: str
    comida: str
    servicio: str
    valoracion: float

class ReservaBase(BaseModel):
    id: int
    usuario_cliente: str
    usuario_chef: str
    fecha: datetime
    valoracion: float
    comentario: str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/usuario/login/token/{usuario}/{password}", status_code=status.HTTP_200_OK)
async def login_respuesta_token(usuario: str, password: str, db: db_dependency):
    """
    Método que sirve para el login en la app.
    
    Parámetros:
    usuario (str): Nombre de usuario.
    password (str): Contraseña del usuario.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    dict: Token de sesión.
    """
    
    key_string = "ffef4bdb71362d718712ebf1224600f0"
    key_bytes = bytes.fromhex(key_string)
    
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario ==usuario).first()
    if db_usuario is None:
        return {"error": "Usuario no encontrado"}
    
    pass_user = db_usuario.password
    
    print("Pass encriptado: " + pass_user)
    pass_decrip = descodif(key_bytes, pass_user).decode("utf-8")
    print("Pass DESencriptado: " + pass_decrip)
        
    if pass_decrip != password:        
        return {"error": "Contraseña incorrecta"}
    
    token_payload = {
        "usuario": usuario,
        "exp": datetime.now() + timedelta(minutes=60),
    }

    token = encode(token_payload, "secret_key", algorithm="HS256")

    return {"token": token}
 
@app.get("/usuario/perfil/", status_code=status.HTTP_200_OK)
async def obtener_perfil(token: str, db: db_dependency):
    """
    Método que sirve para mostrar usuario.
    
    Parámetros:
    token (str): Token de sesión.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    dict: Perfil de usuario completo.
    """
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
        return db_usuario
    
    except Exception as e:
        print(f"Error al obtener perfil: {e}")
        return {"error": "Error al obtener perfil"}
    
@app.get("/chef/listar/", status_code=status.HTTP_200_OK)
async def listar_chef(db: db_dependency):
    """
    Metodo para listar los chefs.
    
    Parámetros:
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de chefs.
    """
    db_chefs = db.query(models.Usuario) \
        .filter(models.Usuario.tipo == "chef") \
        .all()
    if not db_chefs:
        raise HTTPException(status_code=404, detail="No se encontrarosn chefs")
    return db_chefs

@app.get("/provincias/conChef/", status_code=status.HTTP_200_OK)
async def listar_ubicaciones_con_chefs(db: db_dependency):
    """
    Metodo que sirve para listar las provincias (por ubicación) en las que al menos hay un chef.
    
    Parámetros:
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de ubicaciones con chefs.
    """
    ubicaciones = db.query(models.Usuario.ubicacion) \
        .filter(models.Usuario.tipo == "chef") \
        .distinct() \
        .all()
    lista_ubicaciones = [ubicacion[0] for ubicacion in ubicaciones]
    
    if not lista_ubicaciones:
        raise HTTPException(status_code=404, detail="No se encontraron chefs en ninguna ubicacion")
    return lista_ubicaciones

@app.get("/chef/listar/por/{ubicacion}/{comida}/{servicio}", status_code=status.HTTP_200_OK)
async def listar_chef_por_ubicacion_comida_servicio(ubicacion: str, comida: str, servicio: str, db: db_dependency):
    """
    Metodo que sirve para listar chefs por ubicacion, comida y servicio.
    
    Parámetros:
    ubicacion (str): Ubicación del chef.
    comida (str): Tipo de comida que ofrece el chef.
    servicio (str): Tipo de servicio que ofrece el chef.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de chefs por los tres filtros.
    """
    db_chefs = db.query(models.Usuario) \
        .filter(models.Usuario.tipo == "chef") \
        .filter(models.Usuario.ubicacion == ubicacion) \
        .filter(models.Usuario.comida == comida) \
        .filter(models.Usuario.servicio == servicio) \
        .all()    
        
    if not db_chefs:
        raise HTTPException(status_code=404, detail="No se encontrarosn chefs")
    return db_chefs

@app.post("/usuario/crear/", status_code=status.HTTP_200_OK)
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    """
    Metodo para crear usuario.
    
    Parámetros:
    usuario (UsuarioBase): Objeto que contiene los datos del usuario.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si el usuario se ha registrado correctamente.
    """
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario.usuario).first()
    if db_usuario is None:
        key_string = "ffef4bdb71362d718712ebf1224600f0"
        key_bytes = bytes.fromhex(key_string)
        
        password = usuario.password
        codePass = (password).encode('utf-8')
        cripPass = codif(key_bytes, codePass)
        usuario.password = cripPass
        db_usuario = models.Usuario(**usuario.dict())
        db.add(db_usuario)
        db.commit()
        return "El usuario se ha registrado correctamente"
    else:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

@app.post("/usuario/modificar/", status_code=status.HTTP_200_OK)
async def modificar_usuario (usuario_actualizado: UsuarioBase, token: str, db: db_dependency):
    """
    Metodo para modificar usuario.
    
    Parámetros:
    usuario_actualizado (UsuarioBase): Objeto que contiene los datos actualizados del usuario.
    token (str): Token de sesión.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si el usuario se ha modificado correctamente.
    """
    try:
        decoded_token = decode(token, "secret_key", algorithms=["HS256"])
        username = decoded_token["usuario"]
    except Exception as e:
        print(f"Error al decodificar token: {e}")
        return {"error": "Token no válido"}
    
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == username).first()
        
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_usuario.usuario = usuario_actualizado.usuario
    db_usuario.nombre = usuario_actualizado.nombre
    db_usuario.password = usuario_actualizado.password
    db_usuario.descripcion = usuario_actualizado.descripcion
    db_usuario.ubicacion = usuario_actualizado.ubicacion
    db_usuario.email = usuario_actualizado.email
    db_usuario.telefono = usuario_actualizado.telefono
    db_usuario.tipo = usuario_actualizado.tipo
    db_usuario.comida = usuario_actualizado.comida
    db_usuario.servicio = usuario_actualizado.servicio
    db_usuario.valoracion = usuario_actualizado.valoracion
    
    db.commit()
    return "El usuario se ha modificado correctamente"

# METODOS PARA EL USUARIO ADMINISTRADOR

@app.get("/admin/listar/", status_code=status.HTTP_200_OK)
async def listar_todos_usuarios(db: db_dependency):
    """
    Método para listar todos los usuarios.
    
    Parámetros:
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de todos los usuarios.
    """
    db_usuarios = db.query(models.Usuario).all() 
    
    if not db_usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return db_usuarios   

@app.get("/admin/perfil/", status_code=status.HTTP_200_OK)
async def obtener_perfil_admin(usuario: str, db: db_dependency):
    """
    Método para obtener el perfil de un determinado usuario.
    
    Parámetros:
    usuario (str): Nombre de usuario.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    dict: Perfil del usuario.
    """
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()

    if db_usuario is None:
        return {"error": "Usuario no encontrado"}

    try:
        return db_usuario
    
    except Exception as e:
        print(f"Error al obtener perfil: {e}")
        return {"error": "Error al obtener perfil"}

@app.post("/admin/modificar/{usuario}", status_code=status.HTTP_200_OK)
async def modificar_usuario_admin (usuario_actualizado: UsuarioBase, usuario: str, db: db_dependency):
    """
    Método para que el admin pueda modificar un determinado usuario.
    
    Parámetros:
    usuario_actualizado (UsuarioBase): Objeto que contiene los datos actualizados del usuario.
    usuario (str): Nombre de usuario a modificar.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si el usuario se ha modificado correctamente.
    """
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()
    
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado") 
    db_usuario.usuario = usuario_actualizado.usuario
    db_usuario.nombre = usuario_actualizado.nombre
    db_usuario.password = usuario_actualizado.password
    db_usuario.descripcion = usuario_actualizado.descripcion
    db_usuario.ubicacion = usuario_actualizado.ubicacion
    db_usuario.email = usuario_actualizado.email
    db_usuario.telefono = usuario_actualizado.telefono
    db_usuario.tipo = usuario_actualizado.tipo
    db_usuario.comida = usuario_actualizado.comida
    db_usuario.servicio = usuario_actualizado.servicio
    db_usuario.valoracion = usuario_actualizado.valoracion
    
    db.commit()
    return "El usuario se ha modificado correctamente"

@app.delete("/usuario/{usuario}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(usuario:str, db: db_dependency):
    """
    Método que sirve para eliminar usuario.
    
    Parámetros:
    usuario (str): Nombre de usuario a eliminar.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si el usuario se ha eliminado correctamente.
    """
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        db.delete(db_usuario)
        db.commit()
        return "Usuario eliminado"

# METODOS PARA LAS RESERVAS

@app.post("/reserva/crear/", status_code=status.HTTP_200_OK)
async def crear_reserva(reserva: ReservaBase, db: db_dependency):
    """
    Método para crear una nueva reserva.
    
    Parámetros:
    reserva (ReservaBase): Objeto que contiene los datos de la reserva.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si la reserva se ha registrado correctamente.
    """
    
    # Validar que los campos están ok
    if not reserva.usuario_cliente or not reserva.usuario_chef or not reserva.fecha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Faltan datos obligatorios")

    # Chequear si el chef ya tiene una reserva para la misma fecha
    existe_reserva = db.query(models.Reserva) \
        .filter(models.Reserva.usuario_chef == reserva.usuario_chef) \
        .filter(models.Reserva.fecha == reserva.fecha) \
        .first()

    if existe_reserva:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El chef ya tiene una reserva para esa fecha")

    # Añadir la reserva a la base de datos
    db_reserva = models.Reserva(**reserva.dict())
    db.add(db_reserva)
    db.commit()
    return "La reserva se ha registrado correctamente"
    
@app.post("/reserva/modificar/{id}", status_code=status.HTTP_200_OK)
async def modificar_reserva (reserva_actualizada: ReservaBase, id: int, db: db_dependency):
    """
    Método para modificar la reserva.
    
    Parámetros:
    reserva_actualizada (ReservaBase): Objeto que contiene los datos actualizados de la reserva.
    id (int): ID de la reserva a modificar.
    db (db_dependency): Dependencia de la base de datos.
    En el json, es necesario rellenar todos los datos para que no de error.

    Retorna:
    str: Mensaje de éxito si la reserva se ha modificado correctamente.
    """
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == id).first()
    
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada") 
    db_reserva.usuario_cliente = reserva_actualizada.usuario_cliente
    db_reserva.usuario_chef = reserva_actualizada.usuario_chef
    db_reserva.valoracion = reserva_actualizada.valoracion
    db_reserva.comentario = reserva_actualizada.comentario
    db_reserva.fecha = reserva_actualizada.fecha
    
    db.commit()
    return "La reserva se ha modificado correctamente"

@app.get("/reserva/listar/{token}", status_code=status.HTTP_200_OK)
async def listar_reserva(token:str, db: db_dependency):
    """
    Método para listar todas las reservas que tiene un usuario.
    
    Parámetros:
    token (str): Token del usuario.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de reservas del usuario.
    """
    try:
        decoded_token = decode(token, "secret_key", algorithms=["HS256"])
        usuario = decoded_token["usuario"]
    except Exception as e:
        print(f"Error al decodificar token: {e}")
        return {"error": "Token no válido"}

    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()

    if db_usuario is None:
        return {"error": "Usuario no encontrado"}

    reservas = db.query(models.Reserva) \
        .filter(or_(models.Reserva.usuario_cliente == usuario,  
                    models.Reserva.usuario_chef == usuario)) \
        .all()
    return reservas

@app.get("/reserva/listar/todas/", status_code=status.HTTP_200_OK)
async def listar_reserva_todas(db: db_dependency):
    """
    Método para listar todas las reservas.
    
    Parámetros:
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de todas las reservas existentes en la bd.
    """    
    
    db_reservas = db.query(models.Reserva).all()
    #return reservas

    #db_usuarios = db.query(models.Usuario).all() 
    
    if not db_reservas:
        raise HTTPException(status_code=404, detail="No se encontraron reservas")
    return db_reservas   

@app.get("/reserva/listar/chef/{usuario}", status_code=status.HTTP_200_OK)
async def listar_reserva_chef(usuario:str, db: db_dependency):
    """
    Método para listar todas las reservas que tiene un usuario chef.
    
    Parámetros:
    usuario (str): usuario del usuario chef.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    list: Lista de reservas del usuario chef.
    """
    
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()

    if db_usuario is None:
        return {"error": "Usuario no encontrado"}

    reservas = db.query(models.Reserva) \
        .filter(models.Reserva.usuario_chef == usuario) \
        .all()
    return reservas

@app.delete("/borrar/reserva/{id}", status_code=status.HTTP_200_OK)
async def eliminar_reserva(id:int, db: db_dependency):
    """
    Método que sirve para eliminar una reserva por su id.
    
    Parámetros:
    id (int): Id de reserva a eliminar.
    db (db_dependency): Dependencia de la base de datos.

    Retorna:
    str: Mensaje de éxito si la reserva se ha eliminado correctamente.
    """
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    else:
        db.delete(db_reserva)
        db.commit()
        return "Reserva eliminada"

   
"""METODOS DESCARTADOS

# Generar token
    token_payload = {
        "usuario": usuario,
        "exp": datetime.now() + timedelta(minutes=60),
    }
   
    token = encode(token_payload, "secret_key", algorithm="HS256")

    return {"token": token}

reservas = db.query(models.Reserva) \
        .join(models.Reserva.usuario_cliente) \
        .join(models.Reserva.usuario_chef) \
        .filter(or_(models.Reserva.usuario_cliente == usuario,  
                    models.Reserva.usuario_chef == usuario)) \
        .all()
    return reservas

reservas = db.query(models.Reserva) \
        .join(models.Usuario.usuario == models.Reserva.usuario_cliente) \
        .join(models.Usuario.usuario == models.Reserva.usuario_chef) \
        .filter(models.Usuario.usuario == usuario) \
        .all()

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

@app.route("/usuario/crear", methods=["POST"])
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    return "El usuario se ha registrado correctamente"

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

title="ChooseChef API REST",
                description="API para la app ChooseChef",
                version="4.5"

"""