from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_name) 


#models.Base.metadata.create_all(bind=engine)#engine that calls the db and model pptys to the table

origins = ["*"]

app = FastAPI()


app.add_middleware(
    CORSMiddleware, #Request first goes thrugh middleware
    allow_origins=origins,#What domains are allowed to access our api
    allow_credentials=True,
    allow_methods=["*"],#Sepcific http method
    allow_headers=["*"],#Specofic methods
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Message": "Welcome Back Batman"}


