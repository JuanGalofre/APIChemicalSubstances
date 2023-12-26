from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from . import models
from .database import engine,sessionLocal 
from .schemas import Substance, ReturningSubstance, User, ReturnUser
from . import hashing
from .routers import substances, users, authentication, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)
origins=[""]
app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(substances.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")
def default_function():
    return {"message":"hello there"}


