import json
from src.database import Session
from src.models.note import Note


def test_list_notes_empty(test_app):
    client = test_app.test_client()
    response = client.get("/notes")
    assert not json.loads(response.data)
    assert response.status_code == 200


def test_list_notes(test_app, create_user):
    client = test_app.test_client()

    with Session() as session:
        for nn in range(0, 5):
            note = Note(text=f'{nn}', profile_id=create_user.id)
            session.add(note)
            session.commit()

    response = client.get("/notes")
    res = json.loads(response.data)

    assert res
    assert len(res) == 5
    assert response.status_code == 200


def test_list_notes_in_trash(test_app, create_user, token):
    client = test_app.test_client()

    with Session() as session:
        for nn in range(0, 4):
            print('OI AMIGO: ', nn)
            note = Note(text=f'{nn}', profile_id=create_user.id, is_active=False)
            session.add(note)
            session.commit()

    response = client.get("/notes/trash/", headers=token)
    res = json.loads(response.data)
    assert res
    assert len(res) == 4
    assert response.status_code == 200
