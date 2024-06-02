from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pswd@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ipaddress/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()#we usethis class to inherit to create each db models 

def get_db():#dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
