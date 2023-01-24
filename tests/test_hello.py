import json


def test_index(test_app):
    client = test_app.test_client()
    response = client.get("/")
    assert json.loads(response.data) == {"hello": "world"}
    assert response.status_code == 200
