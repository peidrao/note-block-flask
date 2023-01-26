import os
import pytest
from sqlmodel import Session
from src.models.profile import Profile
from sqlmodel import SQLModel
from src.server.config import config
from src.server.app import create_app
from src.database.connect import engine
from werkzeug.security import generate_password_hash
# from src.models import Note, Profile

from dotenv import dotenv_values


config_env = dotenv_values(".env")


@pytest.fixture(scope="session")
def test_app():
    app = create_app()
    app.config.from_object(config)
    with app.app_context():
        SQLModel.metadata.create_all(engine)
        yield app


@pytest.fixture()
def create_user():
    with Session(engine) as session:
        profile = Profile(
            username="test",
            password=generate_password_hash("123"),
            name="Test",
            email="test@test.com",
        )

        session.add(profile)
        session.commit()
        yield profile


def pytest_sessionfinish(session, exitstatus):
    SQLModel.metadata.drop_all(engine)
    os.remove("memory.db")
