import json
from src.database import Session
from src.models import Note, Tag


def test_list_notes_empty(test_app):
    client = test_app.test_client()
    response = client.get("/notes")
    assert not json.loads(response.data)
    assert response.status_code == 200


def test_list_notes(test_app, create_user):
    client = test_app.test_client()

    with Session() as session:
        for index in range(0, 5):
            note = Note(text=f"{index}", profile_id=create_user.id)
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
        for index in range(0, 4):
            note = Note(text=f"{index}", profile_id=create_user.id, is_active=False)
            session.add(note)
            session.commit()

    response = client.get("/notes/trash/", headers=token)
    res = json.loads(response.data)
    assert res
    assert len(res) == 4
    assert response.status_code == 200


def test_create_note(test_app, token):
    client = test_app.test_client()
    payload = {"text": "new note"}

    response = client.post("/notes", data=json.dumps(payload), headers=token)
    data = json.loads(response.data)
    assert data
    assert response.status_code == 201
    assert data["text"] == "new note"
    assert data["is_active"]


def test_create_note_not_authentication(test_app, token):
    client = test_app.test_client()

    response = client.post("/notes")
    data = json.loads(response.data)
    assert response.status_code == 401


def test_create_note_by_tag(test_app, token, create_user, create_tag):
    client = test_app.test_client()
    payload = {"text": "new note", "tag_id": create_tag.id}

    response = client.post("/notes", data=json.dumps(payload), headers=token)
    data = json.loads(response.data)
    assert data
    assert response.status_code == 201
    assert data["text"] == "new note"
    assert data["tag_id"]
    assert data["is_active"]


def test_create_note_no_payload(test_app, token):
    client = test_app.test_client()

    response = client.post("/notes", data=json.dumps({}), headers=token)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["message"] == "No payload"


def test_create_note_err_entity(test_app, token):
    client = test_app.test_client()
    payload = {"text1": "new note"}

    response = client.post("/notes", data=json.dumps(payload), headers=token)
    data = json.loads(response.data)

    assert response.status_code == 422
    assert data["error"]


def test_remove_note(test_app, token, create_user):
    client = test_app.test_client()
    note_id = None
    with Session() as session:
        note = Note(text="new_note", profile_id=create_user.id)

        session.add(note)
        session.commit()
        note_id = note.id

    response = client.post(f"/notes/{note_id}", headers=token)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert not data["is_active"]


def test_remove_note_not_found(test_app, token):
    client = test_app.test_client()

    response = client.post(f"/notes/{0}", headers=token)
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data["message"] == "Note not found"


def test_list_notes_by_current_user(test_app, token):
    client = test_app.test_client()

    response = client.get("/me/notes", headers=token)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 12


def test_list_notes_by_tags(test_app, create_user, token):
    client = test_app.test_client()
    tag_id = None

    with Session() as session:
        tag = Tag(tag="ye", profile_id=create_user.id)
        session.add(tag)
        session.commit()
        tag_id = tag.id
        for index in range(0, 6):
            note = Note(
                text=f"{index}",
                tag_id=tag_id,
                profile_id=create_user.id,
                is_active=False,
            )
            session.add(note)
            session.commit()

    response = client.get(f"/notes/tags/{tag_id}", headers=token)

    res = json.loads(response.data)
    assert response.status_code == 200
    assert res
    assert len(res) == 6
