from sqlalchemy import String, Integer, Column
from database import Base

class Chef(Base):
    __tablename__ = "Chef"
    chef_id = Column (Integer, primary_key=True, index=True, autoincrement="auto")
    nombre_chef = Column(String(100))
    password = Column(String(30))
    descripcion = Column(String(500))
    ubicacion = Column(String(20))
    email = Column(String(30), unique=True)
          
class Cliente(Base):
    __tablename__ = "Cliente"
    cliente_id = Column (Integer, primary_key=True, index=True, autoincrement="auto")
    nombre_cliente = Column(String(100))
    password = Column(String(30))
    email = Column(String(30), unique=True)
  
class Administrador(Base):
    __tablename__ = "Administrador"
    administrador_id = Column (Integer, primary_key=True, index=True, autoincrement="auto")
    nombre_administrador = Column(String(100))
    password = Column(String(30))
    email = Column(String(30), unique=True)