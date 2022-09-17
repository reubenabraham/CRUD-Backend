from typing import List
from app import schemas
import pytest
    
#Test to make sure an unauthenticated user does not get posts.
#For this, used the regular unauthenticated client and not the one with auth
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

#Test whether an unauthenticated user can get a specific post:
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#Unauthorised user creating posts
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"arbitrary title", "content":"temp"})
    assert res.status_code == 401

#Unauthorized delete of posts.
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

