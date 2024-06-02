#Pydantic model
from pydantic import BaseModel, EmailStr #For schema
from datetime import datetime

class ProductBase(BaseModel):
    name : str
    price : int
    is_sale : bool
    inventory : int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass


class Product(BaseModel):
    name : str
    price : int
    is_sale : bool

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    customer_name : str
    method_of_pay : str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(BaseModel):
    customer_id : int
    customer_name : str
    method_of_pay : str
    
    class Config:
        orm_mode = True