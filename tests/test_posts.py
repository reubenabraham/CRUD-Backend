
from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")    
    # def validate(post):
    #     return schemas.PostOut(**post)
    # posts_map = list(map(validate, res.json()))    
    #posts_list = list(posts_map)
    
    # assert len(posts_list) == len(test_posts)    
    assert res.status_code == 200
    

#Test to make sure an unauthenticated user does not get posts.
#For this, used the regular unauthenticated client and not the one with auth
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

#Test whether an unauthenticated user can get a specific post:
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#Test to get a post with an ID that doesn't exist
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404

#Get one actual valid post with authenticated client
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code==200

#Unauthorised user creating posts
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"arbitrary title", "content":"temp"})
    assert res.status_code == 401

#Unauthorized delete of posts.
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# #Test successfully deleting posts.
# def test_delete_post_success(authorized_client, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204

#Testing deletion of a post that doesn't exist
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8302342")
    assert res.status_code == 404

#User trying to delete a post that isn't theirs
# #Remember that authorized client is logged in as test_user_one, so we're going to try and delete the post from user_2
# def test_delete_other_user_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403

# def test_update_post(authorized_client, test_user, test_posts):
#     data = {"title":"updated title", "content":"updated content", "id": test_posts[0].id}
#     res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
#     updated_post = schemas.Post(**res.json())
#     assert res.status_code == 200
    

# def test_update_other_user_post(authorized_client, test_user, test_user_2, test_posts):
#     data = {"title":"updated title", "content":"updated content", "id": test_posts[3].id}
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403

