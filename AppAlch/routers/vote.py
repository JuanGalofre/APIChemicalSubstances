from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..tokenAuthentication import get_current_user
from ..database import get_db
from .. import schemas
from .. import models


router = APIRouter( prefix="/vote",tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def voteForASubstance(vote: schemas.Vote ,current_user: int = Depends(get_current_user),db: Session =Depends(get_db)):

    vote_query=db.query(models.AlchemyVotes).filter(models.AlchemyVotes.substance_id == vote.substance_id, models.AlchemyVotes.user_id == current_user.id)
    vote_query_result = vote_query.first()

    substance_search=db.query(models.AlchemySubstances).filter(models.AlchemySubstances.id == vote.substance_id).first()
    if not substance_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry, substance with id:  {vote.substance_id} does not exist")

    if vote.direction == True:
        if vote_query_result:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User {current_user.id} has already voted on substance {vote.substance_id}")
        else:
            new_vote= models.AlchemyVotes(user_id=current_user.id, substance_id=vote.substance_id)
            db.add(new_vote)
            db.commit()
            return {"message":"Your vote has been succesfully added"}
    else:
        if vote_query_result:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"Your vote has ben succesfully deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on substance {vote.substance_id}")