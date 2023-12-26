from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database
from .. import schemas
from .. import models
from .. import hashing
from .. import tokenAuthentication
router = APIRouter(tags=['Authentications'])

@router.post("/login", response_model=schemas.AccessToken)
def login( user_credentials :OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    userquery= db.query(models.AlchemyUsers).filter(models.AlchemyUsers.email == user_credentials.username)
    user = userquery.first()
    if not user:
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN ,detail=f"Invalid credentials")

    if not hashing.verifyPassword(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token=tokenAuthentication.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}