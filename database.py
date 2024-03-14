from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
URL_DATABASE = "mysql+pymysql://choose_chef:@localhost:5432/choose_chef"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#BD LOGIN
#nombre: choosechef2
#usuario: choosechef
#contraseña: basededatos



