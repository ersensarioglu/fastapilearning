from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@fastapi.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "a@b.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "created_by": test_user['id']
        },
                {
            "title": "2nd title",
            "content": "2nd content",
            "created_by": test_user['id']
        },
                {
            "title": "3rd title",
            "content": "3rd content",
            "created_by": test_user['id']
        },
                {
            "title": "4th title",
            "content": "4th content",
            "created_by": test_user2['id']
        }
    ]
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    all_posts = session.query(models.Post).all()
    return all_posts

@pytest.fixture
def test_votes(test_user, test_user2, session):
    votes_data = [
        {
            "user_id": test_user['id'],
            "post_id": 4
        },
                {
            "user_id": test_user2['id'],
            "post_id": 1
        }
    ]
    def create_vote_model(vote):
        return models.Vote(**vote)
    vote_map = map(create_vote_model, votes_data)
    votes = list(vote_map)
    session.add_all(votes)
    session.commit()

    all_votes = session.query(models.Vote).all()
    return all_votes