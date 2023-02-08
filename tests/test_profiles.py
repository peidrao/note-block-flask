import json


def test_list_profiles(test_app, token):
    client = test_app.test_client()
    response = client.get("/profile", headers=token)
    res = json.loads(response.data)

    assert response.status_code == 200
    assert res


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


def test_get_profile_not_token(test_app):
    client = test_app.test_client()
    response = client.get("/profile/1")
    assert response.status_code == 401


def test_get_profile(test_app, token):
    client = test_app.test_client()
    response = client.get("/profile/1", headers=token)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data.get("email") == "test@test.com"


def test_delete_profile_not_permission(test_app, token):
    client = test_app.test_client()
    response = client.delete("/profile/121", headers=token)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data["message"] == "You don't have permission for this action"


def test_delete_profile(test_app, token, create_user):
    client = test_app.test_client()
    response = client.delete(f"/profile/{create_user.id}", headers=token)

    assert response.status_code == 204


def test_get_profile_me(test_app, token):
    client = test_app.test_client()
    response = client.get("/me", headers=token)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data.get("email") == "test@test.com"
    assert data.get("id") == 1
    assert data.get("name") == "Test"
    assert data.get("username") == "test"


def test_get_profile_me_not_token(test_app):
    client = test_app.test_client()
    response = client.get("/me")
    assert response.status_code == 401
