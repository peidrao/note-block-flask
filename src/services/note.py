from marshmallow import ValidationError
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.database import Session
from src.models import Note, Profile
from src.schemas.note import NoteSchema
from src.utils import status


class NoteListView(MethodView):
    @jwt_required()
    def post(self):
        profile_id = get_jwt_identity()
        json_data = request.get_json()
        if not json_data:
            return {"message": "No payload"}, status.HTTP_400_BAD_REQUEST

        try:
            data = NoteSchema().load(json_data)
        except ValidationError as err:
            return {"error": err.messages}, status.HTTP_422_UNPROCESSABLE_ENTITY

        text, tag_id = data["text"], data.get("tag_id")
        with Session() as session:
            profile = (
                session.query(Profile).filter(Profile.id == profile_id).one_or_none()
            )

            if profile:
                note = Note(text=text, profile_id=profile.id, tag_id=tag_id)
                session.add(note)
                session.commit()
                return (
                    NoteSchema().dump(session.get(Note, note.id)),
                    status.HTTP_201_CREATED,
                )

    def get(self):
        with Session() as session:
            notes = session.query(Note).filter(Note.is_active)
            return NoteSchema(many=True).dump(notes), status.HTTP_200_ACCEPTED


class NoteDetailsView(MethodView):
    @jwt_required()
    def post(self, note_id):
        with Session() as session:
            note = session.query(Note).filter(Note.id == note_id).one_or_none()
            if note:
                note.is_active = False
                session.commit()
                return NoteSchema().dump(note), status.HTTP_200_ACCEPTED

            return {"message": "Note not found"}, status.HTTP_404_NOT_FOUND


class NotesTrashView(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        with Session() as session:
            notes = session.query(Note).filter(
                Note.profile_id == current_user, ~Note.is_active
            )
            return NoteSchema(many=True).dump(notes), status.HTTP_200_ACCEPTED


class ProfileMeNotes(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        with Session() as session:
            notes = session.query(Note).filter(Note.profile_id == current_user)
            return NoteSchema(many=True).dump(notes), status.HTTP_200_ACCEPTED


class NotesByTagView(MethodView):
    @jwt_required()
    def get(self, tag_id):
        current_user = get_jwt_identity()
        with Session() as session:
            notes = session.query(Note).filter(
                Note.profile_id == current_user, Note.tag_id == tag_id
            )
            return NoteSchema(many=True).dump(notes), status.HTTP_200_ACCEPTED
