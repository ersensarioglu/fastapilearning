from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base

SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Dependency for controlling db session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

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