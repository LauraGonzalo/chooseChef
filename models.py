from sqlalchemy import DateTime, ForeignKey, String, Integer, Column, Float
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
    valoracion = Column(Float)

class Reserva(Base):
    __tablename__ = "reserva"
    id = Column (Integer, primary_key=True, index=True, autoincrement="auto")
    usuario_cliente = Column(String(45), ForeignKey("usuario.usuario", ondelete="CASCADE", onupdate="CASCADE"))
    usuario_chef = Column(String(45), ForeignKey("usuario.usuario", ondelete="CASCADE", onupdate="CASCADE"))
    valoracion = Column (Float)
    comentario = Column (String(500))
    fecha = Column (DateTime)   
    
    
          
