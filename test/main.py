import time
from typing import List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body, Depends
from pydantic import BaseModel #For schema
import psycopg as db
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
import model, schemas
from database import engine, get_db


test = FastAPI()

model.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = db.connect(host='localhost', dbname ='fastapi', user='postgres',
                                password='pswd', row_factory = dict_row)
        cursor = conn.cursor()
        print("Databse connection succesful")
        break

    except Exception as error:
        print("Connection Failed")
        print("Error was", error)
        time.sleep(3)


@test.get("/")
def read_root():
    return {"Message": "Welcome Back Batman"}



@test.get("/sqlalchemy")
def get_post(db : Session = Depends(get_db)):
    return{"Message" : "Succesful"}


@test.get("/products",response_model= List[schemas.Product])
def get_posts(db : Session = Depends(get_db)):
    
    produtcs = db.query(model.Produtcs).all()
    return produtcs


@test.post("/products", status_code=status.HTTP_201_CREATED, response_model= schemas.Product)
def post_new(products : schemas.ProductCreate,db : Session = Depends(get_db) ):
    # cursor.execute(""" INSERT INTO products (name,price,is_sale,inventory) VALUES (%s,%s,%s,%s) RETURNING * """,(products.name,
    #         products.price,products.is_sale,products.inventory))
    
    new_product = model.Produtcs(**products.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@test.get("/products/{id}")
def get_post(id):
    cursor.execute((f""" SELECT * FROM products WHERE id = {(str(id))} """))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")

    return {"data" : post}



@test.put("/products/{id}")
def update_post(id: int, updated_post : schemas.ProductUpdate, db : Session = Depends(get_db)):
    # cursor.execute(""" UPDATE public.products SET name = %s, price = %s, is_sale = %s, inventory = %s WHERE id = %s RETURNING *""",
    #                (products.name,products.price,products.is_sale,products.inventory,str(id)))
    
    post_query = db.query(model.Produtcs).filter(model.Produtcs.id == id)


    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")

    post_query.update(updated_post.dict(), synchronize_session= False)

    db.commit()
    
    return post_query.first()


@test.delete("/products/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db)):
    product_query = db.query(model.Produtcs).filter(model.Produtcs.id == id)
    product = product_query.first()


    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post with id {id} was not found")


    return f"Delted row no {id}", Response(status_code=status.HTTP_204_NO_CONTENT)


@test.get("/customer", response_model= List[schemas.Customer])
def get_customers(db : Session = Depends (get_db)):
    customer = db.query(model.Customer).all()
    return customer


@test.post("/customer", status_code=status.HTTP_201_CREATED,response_model= schemas.Customer)
def create_customer(customer : schemas.CustomerCreate,db : Session = Depends(get_db) ):

    new_customer = model.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
