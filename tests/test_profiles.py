import json


def test_list_profiles(test_app):
    client = test_app.test_client()
    response = client.get("/profile")
    assert response.status_code == 200


def test_create_profile(test_app):
    client = test_app.test_client()
    payload = {
        "username": "carolina",
        "email": "carolina@gmail.com",
        "name": "Carolina",
        "password": "123",
    }
    response = client.post(
        "/signup",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    data = json.loads(response.data)
    assert data
    assert response.status_code == 201
    assert data.get("email") == payload.get("email")
    assert data.get("name") == payload.get("name")
    assert data.get("username") == payload.get("username")


def test_detail_profile(test_app):
    client = test_app.test_client()
    response = client.get("/profile/1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data.get("email") == "test@test.com"
