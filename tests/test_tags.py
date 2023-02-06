import json


def test_tag_create_not_payload(test_app, token):
    client = test_app.test_client()
    payload = {"tag": "new tag"}

    response = client.post("/tags", data=json.dumps(payload), headers=token)

    res = json.loads(response.data)
    assert response.status_code == 201
    assert res["tag"] == "new tag"
    assert res["is_active"]
