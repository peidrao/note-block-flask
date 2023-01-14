import pytest
# import tempfile

from src.server.config import test_config
from src.server.app import create_app
# from src.database.connect import create_db_and_tables



@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object(test_config)
    with app.app_context():
        yield app


# @pytest.fixture
# def client(app):
    # return app.test_client()
