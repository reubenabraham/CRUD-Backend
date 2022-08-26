from fastapi import FastAPI
from .routers import post, user, auth, vote
from . import models
from .database import engine, SessionLocal
from .config import settings


models.database.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
