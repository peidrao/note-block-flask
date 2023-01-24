import json


def test_list_notes(test_app):
    client = test_app.test_client()
    response = client.get("/notes")
    assert not json.loads(response.data)
    assert response.status_code == 200
