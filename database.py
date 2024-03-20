from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:Proyecto79@choosechef.crwqywcc0npi.eu-north-1.rds.amazonaws.com:3306/choosechef"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#BD LOGIN online
# "mysql+pymysql://if0_36174272:Proyecto1979@sql108.infinityfree.com:3306/if0_36174272_chooseChef"
#nombre: choosechef
#usuario: root
#contraseña: Proyecto79
#hostname: choosechef.crwqywcc0npi.eu-north-1.rds.amazonaws.com
#puerto: 3306

#BD LOGIN local  "mysql+pymysql://root:123456@localhost:3306/choosechef"
#nombre: choosechef
#usuario: root
#contraseña: 123456
#hostname: localhost
#puerto: 3306



