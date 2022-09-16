#from http import client
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from app.database import Base
from app.database import SessionLocal, get_db
from app.oauth2 import create_access_token
from app import models


#'postgresql://postgres:postgres@localhost/fastapi'
# f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'

#This is slightly changed to reflect a test-db - look at the end of the URL
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Returns testing DB
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

#Returns TestClient
@pytest.fixture(scope="function")
def client(session):
    #Run some code before we run the test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

@pytest.fixture
def test_user(client):
    user_data = {"email":"reuben_test@gmail.com", "password":"password123"}
    res = client.post("/users/", json=user_data)    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def test_user_2(client):
    user_data = {"email":"reuben_test_2@gmail.com", "password":"password1234"}
    res = client.post("/users/", json=user_data)    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


#----------- Fixtures for Post Testing ----------

#For testing posts, we need to be authenticated, so we have this fixture to do that for us.
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})


#This gives us an authenticated client unlike the fixture further up
#Adds the token to the header of the request
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):

    posts_data = [{"title":"first title","content":"first-content","owner_id": test_user['id']}, {"title":"2nd title","content":"2nd content","owner_id":test_user['id']}, {"title":"3rd title","content":"3rd content","owner_id":test_user['id']}, {"title":"4th title","content":"4th content","owner_id":test_user_2['id']}]

    def create_post_model(post):
        return models.Post(**post)

    #Converts the posts_data dict into Post models
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts_returned = session.query(models.Post).all()
    return posts_returned