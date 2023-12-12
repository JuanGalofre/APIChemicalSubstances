from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from .. import models, tokenAuthentication
from sqlalchemy.orm import Session
from ..schemas import Substance, ReturningSubstance, User, ReturnUser
from .. import hashing
from ..database import get_db

router = APIRouter( prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReturnUser )
def create_user(user:User, db:Session=Depends(get_db)):
    user.password=hashing.hash(user.password)
    new_user=models.AlchemyUsers(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[ReturnUser])
def get_user(db:Session=Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    users= db.query(models.AlchemyUsers).all()
    return users
 
@router.get("/{id}", response_model=ReturnUser)
def get_user(id: int, db:Session=Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    user= db.query(models.AlchemyUsers).filter(models.AlchemyUsers.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} was not found")
    return user


