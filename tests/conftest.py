import pytest

from src.server.config import test_config
from src.server.app import create_app



@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object(test_config)
    with app.app_context():
        yield app
