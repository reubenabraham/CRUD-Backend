from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    #print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to Mock-Strava! go to /docs route to use the Swagger."
    assert res.status_code == 200


#Testing create user route.
def test_create_user(client):
    res = client.post("/users/", json = {"email":"hello123@gmail.com", "password":"password123"})
    #This pydantic model checks if the returned json maintains structure of UserOut
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
