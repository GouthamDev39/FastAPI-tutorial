from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg as dbs
from psycopg.rows import dict_row #For getting column output
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ipaddress/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()

def get_db():#dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = dbs.connect(host='localhost', dbname ='fastapi', user='postgres',
#                                 password='pswd', row_factory = dict_row)
#         cursor = conn.cursor()
#         print("Databse connection succesful")
#         break

#     except Exception as error:
#         print("Connection Failed")
#         print("Error was", error)
#         time.sleep(3)