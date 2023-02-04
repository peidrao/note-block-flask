import json
from src.utils import status


def test_login(test_app, create_user):
    client = test_app.test_client()
    payload = {"username": "test", "password": "123"}
    response = client.post(
        "/login", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_200_ACCEPTED


def test_login_error_password(test_app, create_user):
    client = test_app.test_client()
    payload = {"username": "test", "password": "12"}
    response = client.post(
        "/login", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
