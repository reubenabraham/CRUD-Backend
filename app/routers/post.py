
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from ..database import engine, SessionLocal, get_db
from .. import models, oauth2, schemas

'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

router = APIRouter( 
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.PostOut])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
       
    #Picking up votes for each post. Joins in sqlalchemy are by default left inner join.
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()    
    return posts

#To fetch the id of a specific post
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #Using a filter is the equivalent of using a WHERE clause    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} not found!")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    
    #** = unpacking so we dont have to manually map the request fields to the db columns    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}")
def delete_posts(id: int, status_code = status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #This will generate just the delete query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #Run the query, and it if returns nothing, then raise a 404
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} doesn't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    #if the post exists
    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    #The post that's passed from the API call
    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()

    return post_query.first()

