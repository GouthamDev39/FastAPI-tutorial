#SQL alchemy models

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
#from sqlalchemy.orm import relationship
from database import Base

class Produtcs(Base):
    __tablename__ = "products"

    id = Column(Integer, nullable= False,primary_key = True)
    name = Column(String, nullable= False)
    price = Column(Integer, nullable= False,)
    is_sale = Column(Boolean, nullable= False)
    inventory = Column(Integer, nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))


class Customer(Base):
    __tablename__ = "cutsomer"

    customer_id = Column(Integer, nullable= False, primary_key= True)
    customer_name = Column(String, nullable= False)
    method_of_pay = Column(String,nullable= False, server_default= "cash")
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

