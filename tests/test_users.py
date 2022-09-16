from pydoc import cli
from app import schemas

import pytest
from jose import jwt
from app.config import settings


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


def test_login_user(client, test_user):
    #Instead of passing json, we pass 'data' to this post because it expects a form type - check postman too
    res = client.post("/login", data = {"username":test_user['email'], "password":test_user['password']})
    #Also test if the use has a valid access token - decode the jwt token and check if the user_id matches
    #Also check if the token is a bearer token
    login_res = schemas.Token(**res.json()) 
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[('wrongemail@gmail.com','password123', 403),('reuben_test@gmail.com','WrongPassword', 403),('wrongemail@gmail.com','WrongPassword',403),(None, 'password', 422),('reuben_test@gmail.com',None, 422)])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data = {"username":email, "password":password})    
    assert res.status_code == status_code
    