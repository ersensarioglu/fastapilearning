import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    print("Get all posts")
    res = authorized_client.get("/saposts/")
    def validate(post):
        return schemas.Response(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert posts_list[0].id == test_posts[0].id
    assert posts_list[1].id == test_posts[1].id
    assert posts_list[2].id == test_posts[2].id
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    print("Get all posts for unauthorized")
    res = client.get("/saposts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    print("Get all posts for unauthorized")
    res = client.get(f"/saposts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    print("Get one post for id does not exist")
    res = authorized_client.get("/saposts/55")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    print("Get one post")
    res = authorized_client.get(f"/saposts/{test_posts[0].id}")
    post = schemas.Response(**res.json())
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.created_by == test_posts[0].created_by
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("awesome title", "awesome content", True),
    ("pizza", "pepperoni", False),
    ("tallest building", "wahoo", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    print("Create post")
    res = authorized_client.post("/saposts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Response(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.created_by == test_user['id']
    assert res.status_code == 201

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    print("Create post default published")
    res = authorized_client.post("/saposts/", json={"title": "my title", "content": "my content"})
    created_post = schemas.Response(**res.json())
    assert created_post.title == "my title"
    assert created_post.content == "my content"
    assert created_post.published == True
    assert created_post.created_by == test_user['id']
    assert res.status_code == 201    

def test_unauthorized_user_create_post(client, test_user, test_posts):
    print("Create post for unauthorized user")
    res = client.post("/saposts/", json={"title": "my title", "content": "my content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    print("Delete post for unauthorized user")
    res = client.delete(f"/saposts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    print("Delete post")
    res = authorized_client.delete(f"/saposts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    print("Delete post not exist")
    res = authorized_client.delete(f"/saposts/55")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    print("Delete post of other user")
    res = authorized_client.delete(f"/saposts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    print("Update post")
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    res = authorized_client.put(f"/saposts/{test_posts[0].id}", json=data)
    assert res.json()['data']['title'] == data['title']
    assert res.json()['data']['content'] == data['content']
    assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_posts):
    print("Update post of other user")
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    res = authorized_client.put(f"/saposts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_unauthorized_user_post(client, test_user, test_posts):
    print("Update unauthorized user")
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    res = client.put(f"/saposts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    print("Update post not exist")
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    res = authorized_client.put("/saposts/55", json=data)
    assert res.status_code == 404 