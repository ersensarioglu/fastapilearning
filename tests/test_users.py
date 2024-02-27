from app import schemas
from tests.database import client,session

def test_root(client):
    print("Root path")
    res = client.get("/")
    assert res.json().get('message') == 'Welcome to my API!!'
    assert res.status_code == 200

def test_create_user(client):
    print("Create user")
    res = client.post("/users/", json={"email": "test@fastapi.com", "password": "123456"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.id > 0
    assert new_user.email == "test@fastapi.com"
    assert new_user.created_at != ""
    assert res.status_code == 201