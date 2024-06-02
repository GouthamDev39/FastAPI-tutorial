from pydantic import BaseModel, EmailStr #For schema
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True


class user_login(BaseModel):
    email : EmailStr
    password : str



class PostBase(BaseModel):
    title: str
    content : str
    published : bool = True
    


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    user_id : int
    user : UserOut

    class Config:
        orm_mode = True


class PostOut(PostBase):
    Post : Post
    votes : int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)
