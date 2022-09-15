from operator import mod
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..database import engine, SessionLocal, get_db

'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        #Post doesn't exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist")


    #First check if this user has voted on this post already
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()


    if vote.dir == 1:
        
        if found_vote:
            #This guy has already voted on this post, we should raise an exception.
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted for post {vote.post_id}")

        else:
            #Create a vote, add an entry into this table.
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}

    else:

        #Vote direction is 0 here - remember pydantic already checks dir will be either 1/0
        if not found_vote:
            #Can't decrement the vote count for a post that doesn't exist.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        else:
            #If we found a vote, we have to delete it. 
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message":"successfully deleted vote."}



