import json

def test_signin_profile(test_app, create_user):
    client = test_app.test_client()
    payload = {
        "username": "test",
        "password": "123"
    }
    response = client.post(
        '/login',
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
