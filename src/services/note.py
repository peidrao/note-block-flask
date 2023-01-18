# from flask_restful import Resource
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask import request
from flask.views import MethodView

from src.database.connect import engine
from src.models import Note, Profile
from src.schemas.note import NoteSchema
# from src.utils.auth import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.utils.constants import (
    HTTP_200_ACCEPTED, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY)


class NoteListView(MethodView):
    @jwt_required
    def post(self, _):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = NoteSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        text = data['text']

        with Session(engine) as session:

            profile = session.get(Profile, self.id)
            if profile:
                note = Note(text=text, profile_id=profile.id)
                session.add(note)
                session.commit()
                return NoteSchema().dump(session.get(Note, note.id)), HTTP_201_CREATED

            return {'message': 'Profile not found'}, HTTP_404_NOT_FOUND

    def get(self):
        with Session(engine) as session:
            notes = session.exec(select(Note)).all()
            return NoteSchema(many=True).dump(notes), HTTP_200_ACCEPTED


class ProfileMeNotes(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        with Session(engine) as session:
            notes = session.exec(select(Note).where(Note.profile_id == current_user))
            return NoteSchema(many=True).dump(notes), HTTP_200_ACCEPTED
