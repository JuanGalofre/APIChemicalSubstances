from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from .. import models
from .. import schemas
from .. import tokenAuthentication
from sqlalchemy.orm import Session, joinedload, subqueryload, aliased
from sqlalchemy import func as funk
from ..schemas import Substance, ReturningSubstance, User, ReturnUser, ReturningSubstanceVotes, MassiveSubstance, ReturningMassiveSubstances, SubstanceToModify, MassiveSubstancesToModify
from ..database import get_db
from typing import Optional



router = APIRouter( prefix="/substances",tags=['Substances'])


@router.get("/",response_model=List[schemas.ReturningSubstanceVotes] )
def get_substances(db: Session =Depends(get_db), 
                   molecularFormula:str = None,
                   limit:int = 10,
                   search: Optional[str] ="",
                   current_user: int = Depends(tokenAuthentication.get_current_user)):
    if molecularFormula:
        substances= (
            db.query(models.AlchemySubstances, funk.count(models.AlchemySubstances.id).label("votes"))
            .outerjoin(models.AlchemyVotes, models.AlchemySubstances.id == models.AlchemyVotes.substance_id)
            .options(subqueryload(models.AlchemySubstances.owner)) 
            .group_by(models.AlchemySubstances.id)
            .filter(models.AlchemySubstances.molecular_formula==molecularFormula)
            .limit(limit)
            .all()
        )
    else:
        if search:
            substances= (
            db.query(models.AlchemySubstances, funk.count(models.AlchemySubstances.id).label("votes"))
            .outerjoin(models.AlchemyVotes, models.AlchemySubstances.id == models.AlchemyVotes.substance_id)
            .options(subqueryload(models.AlchemySubstances.owner)) 
            .group_by(models.AlchemySubstances.id)
            .filter(models.AlchemySubstances.name.contains(search))
            .limit(limit)
            .all()
            )

        else:
            substances= (
            db.query(models.AlchemySubstances,funk.count(models.AlchemySubstances.id).label("votes"))
            .outerjoin(models.AlchemyVotes, models.AlchemySubstances.id == models.AlchemyVotes.substance_id)
            .options(subqueryload(models.AlchemySubstances.owner)) 
            .group_by(models.AlchemySubstances.id)
            .all()
            )
    return substances

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=ReturningSubstance)
def create_substances(substance: Substance, db: Session =Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    new_substance=models.AlchemySubstances(owner_id=current_user.id,**substance.model_dump())
    db.add(new_substance)
    db.commit()
    db.refresh(new_substance)
    return new_substance


@router.post("/massive",status_code=status.HTTP_201_CREATED,response_model=ReturningMassiveSubstances)
def create_batch_substances(substances:MassiveSubstance , db: Session =Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    massive_list=substances.model_dump()["massive"]
    response_list=[]
    for i in massive_list:
        new_substance=models.AlchemySubstances(owner_id=current_user.id,**i)
        db.add(new_substance)
        db.commit()
        db.refresh(new_substance)
        response_list.append(new_substance)
    return {"massive":response_list}


@router.get("/{id}", response_model=ReturningSubstanceVotes)
def get_substance(id:int, db:Session = Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    substance= (
            db.query(models.AlchemySubstances, funk.count(models.AlchemySubstances.id).label("votes"))
            .outerjoin(models.AlchemyVotes, models.AlchemySubstances.id == models.AlchemyVotes.substance_id)
            .options(subqueryload(models.AlchemySubstances.owner)) 
            .group_by(models.AlchemySubstances.id)
            .filter(models.AlchemySubstances.id == id)
            .first()
            )
    if not substance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Substance with id: {id} was not found")
    return substance

@router.delete("/{id}")
def delete_substance(id:int, db:Session=Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    substance = db.query(models.AlchemySubstances).filter(models.AlchemySubstances.id == id)
    if substance.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Substance with id: {id} was not found")
    else:
        if substance.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized action")
        substance.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/massive",status_code=status.HTTP_201_CREATED,response_model=ReturningMassiveSubstances)
def update_batch_substance(substances: MassiveSubstancesToModify ,db:Session=Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    massive_list=substances.model_dump()["massive"]
    mod_substances=[]
    for i in massive_list:
        substance_query = db.query(models.AlchemySubstances).filter(models.AlchemySubstances.id == i["id_to_modify"])
        substance_obtained= substance_query.first()
        if not substance_obtained:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Substance with id: {id} was not found")
        if substance_obtained.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized action")
        i.pop("id_to_modify")
        substance_query.update(i)
        db.commit()
        mod_substances.append(substance_obtained)
    return {"massive":mod_substances}


@router.put("/{numero}",response_model=ReturningSubstance)
def update_substance(numero:int, substance: Substance, db:Session=Depends(get_db),current_user: int = Depends(tokenAuthentication.get_current_user)):
    substance_query = db.query(models.AlchemySubstances).filter(models.AlchemySubstances.id == numero)
    substance_obtained= substance_query.first()
    if not substance_obtained:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Substance with id: {id} was not found")
    if substance_obtained.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized action")
    substance_query.update(substance.model_dump())
    db.commit()
    return substance_query.first()





