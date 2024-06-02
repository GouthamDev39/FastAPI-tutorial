from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, Oauth2, database
# from typing import List, Optional


router = APIRouter(
    prefix="/vote",
    tags = ['Vote']
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schema.Vote, db : Session = Depends(database.get_db), current_user : int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")


    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"{current_user.email} already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message" : "voted" }
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User hasnt voted")
        
        vote_query.delete(synchronize_session= False)
        db.commit()

        return  {"Message" : "Succefully deleted"}