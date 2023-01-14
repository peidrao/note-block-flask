import json
from src.app import app

app.testing = True
client = app.test_client()


def test_index():
    response = client.get('/')
    assert json.loads(response.data) == {'hello': 'world'}
    assert response.status_code == 200
