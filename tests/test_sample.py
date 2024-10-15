import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app, populate_db
from app.database import Base, get_db
from app.models import User, Post, Comment, Tag
from app.database import engine

@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn: 
       await conn.run_sync(Base.metadata.drop_all)  
       await conn.run_sync(Base.metadata.create_all)  

    async with AsyncSession(engine) as db:
            await populate_db(db)


def test_get_posts(test_app):
    response = test_app.get("/api/posts?status=draft&include=tags,user")
    assert response.status_code == 200


def test_get_post(test_app):
    response = test_app.get("/api/posts/1?include=tags,user,comments")
    assert response.status_code == 200


def test_get_user(test_app):
    response = test_app.get("/api/users/1?include=posts,comments")
    assert response.status_code == 200


