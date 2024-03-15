import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_create_user(client):
    print("Create user")
    res = client.post("/users/", json={"email": "test@fastapi.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.id > 0
    assert new_user.email == "test@fastapi.com"
    assert new_user.created_at != ""
    assert res.status_code == 201

def test_get_user(authorized_client, test_user):
    res = authorized_client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200

def test_get_wrong_user(authorized_client, test_user2):
    res = authorized_client.get(f"/users/{test_user2['id']}")
    assert res.status_code == 404

def test_get_user_not_exist(authorized_client, test_user2):
    res = authorized_client.get("/users/55")
    assert res.status_code == 404

def test_login_user(client, test_user):
    print("Login user")
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    new_token = schemas.Token(**res.json())
    payload = jwt.decode(new_token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") == test_user['id']
    assert new_token.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@mail.com", "123456", 403),
    ("test@fastapi.com", "wrong", 403),
    ("wrong@mail.com", "123456", 403),
    (None, '123456', 422),
    ("test@fastapi.com", None, 422)
    ])
def test_incorrect_login(client, test_user, email, password, status_code):
    print("Incorrect login")
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
