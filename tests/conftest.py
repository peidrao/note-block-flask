import os
import pytest
os.environ['FLASK_DEBUG'] = 'test'

from src.server.config import config
from src.server.app import create_app
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


def pytest_sessionfinish(session, exitstatus):
    drop_db_and_tables()
    os.remove('memory.db')
