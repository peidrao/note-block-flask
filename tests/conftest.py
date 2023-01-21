import os
import pytest
from sqlmodel import Session
from src.models.profile import Profile

from src.server.config import config
from src.server.app import create_app
from src.database.connect import engine
from werkzeug.security import generate_password_hash


from src.database.connect import create_db_and_tables, drop_db_and_tables

from dotenv import dotenv_values


config_env = dotenv_values(".env")


@pytest.fixture(scope='session')
def test_app():
    app = create_app()
    app.config.from_object(config)
    with app.app_context():
        create_db_and_tables()
        yield app


@pytest.fixture()
def create_user():
    with Session(engine) as session:

        profile = Profile(
            username='test',
            password=generate_password_hash('123'),
            name='Test',
            email='test@test.com'
        )

        session.add(profile)
        session.commit()
        yield profile


def pytest_sessionfinish(session, exitstatus):
    drop_db_and_tables()
    os.remove('memory.db')
