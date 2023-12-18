from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
#Powered by pydantic






class User(BaseModel):
    email: EmailStr
    password:str

class ReturnUser(BaseModel):
    email: EmailStr
    created_at: datetime

class Login(BaseModel):
    email: EmailStr
    password:str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Substance(BaseModel):
    name: str
    molecular_formula: str
    molar_mass: float
    cas: str
    sga_classified: bool = True 
    hazardous_reactions: str

class ReturningSubstance(BaseModel):
    id: int
    name: str
    molecular_formula: str
    molar_mass: float
    cas: str
    sga_classified: bool = True 
    hazardous_reactions: str
    created_at: datetime
    owner_id:int 
    owner: ReturnUser
    class Config:
        from_attributes = True

#Massives

class MassiveSubstance(BaseModel):
    massive: List[Substance]

class ReturningMassiveSubstances(BaseModel):
    massive: List[ReturningSubstance]
    class Config:
        from_attributes = True

class SubstanceToModify(Substance):
    id_to_modify:int
    class Config:
        from_attributes = True

class MassiveSubstancesToModify(BaseModel):
    massive: List[SubstanceToModify]


#Votes
class Vote(BaseModel):
    substance_id: int
    direction: bool

class ReturningSubstanceVotes(BaseModel):
    AlchemySubstances: ReturningSubstance
    funk_votes: int
    class Config:
        from_attributes = True