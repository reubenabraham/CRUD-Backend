from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote
from . import models
from .database import engine, SessionLocal
from .config import settings


#We no longer need this as alembic creates all the tables and constraints for us
#models.database.Base.metadata.create_all(bind=engine)


app = FastAPI()
#Here, provide the list of domains/urls that can talk to your API
#To let everyone talk to your web-app -
origins=["*"] 
#origins=["https://www.google.com"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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

@app.get("/")
def root():
    return {"message":"Welcome to Mock-Strava! go to /docs route to use the Swagger."}