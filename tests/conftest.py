import os
import pytest
import json
from src.models.profile import Profile
from src.database import Session, init_db, engine, Base
from src.server.config import config
from src.server.app import create_app
from werkzeug.security import generate_password_hash

from dotenv import dotenv_values


config_env = dotenv_values(".env")


@pytest.fixture(scope="session")
def test_app():
    app = create_app()
    app.config.from_object(config)
    with app.app_context():
        init_db()
        yield app


@pytest.fixture(scope="session")
def create_user():
    with Session() as session:
        profile = Profile(
            username="test",
            password=generate_password_hash("123"),
            name="Test",
            email="test@test.com",
        )
        session.add(profile)
        session.commit()
        yield profile


@pytest.fixture(scope="session")
def token(test_app):
    client = test_app.test_client()
    payload = {"username": "test", "password": "123"}
    response = client.post(
        "/login", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    token = json.loads(response.data)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    yield headers


def pytest_sessionfinish(session, exitstatus):
    Base.metadata.create_all(bind=engine)
    os.remove("memory.db")
