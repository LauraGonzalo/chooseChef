from sqlalchemy import String, Integer, Column
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column (Integer, primary_key=True, index=True, autoincrement="auto")
    usuario = Column(String(45))
    nombre = Column(String(130))
    password = Column(String(30))
    email = Column(String(45))
    tipo = Column(String(45))
    descripcion = Column(String(500))
    ubicacion = Column(String(45))
    telefono = Column(String(15))
    comida = Column(String(130))
    servicio = Column(String(130))
    
          
