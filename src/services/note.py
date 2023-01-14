# from flask_restful import Resource
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask import request
from flask.views import MethodView

from database.connect import engine
from models import Note, Profile
from schemas.note import NoteSchema
from utils.auth import token_required
from utils.constants import (HTTP_200_ACCEPTED, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY)


class NoteListView(MethodView):
    @token_required
    def post(self, _):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = NoteSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        text= data['text']
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
    @token_required
    def get(self, request):
        with Session(engine) as session:
            notes = session.exec(select(Note).where(Note.profile_id == self.id))
            return NoteSchema(many=True).dump(notes), HTTP_200_ACCEPTED
