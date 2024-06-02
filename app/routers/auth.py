from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schema, models, util, Oauth2


router = APIRouter(tags= ['Authentication'])


@router.post("/login", response_model= schema.Token)
def login(user_creddentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    
    #Oauthowdres will have fields username and password by default

    user = db.query(models.User).filter(models.User.email == user_creddentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not util.verify(user_creddentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = Oauth2.create_access_token(data = {"user_id" : user.id})

    return {"access_token" : access_token, "token_type" : "Bearer"}




#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzE1OTc0MjUzfQ.MIrDv6JrWxqiKxLfUUkLwkdMwU-MbV580Vikc4cw1NA