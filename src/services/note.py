from flask_restful import Resource
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask import request

from database.connect import engine
from models import Note, Profile
from schemas import NoteSchema
from utils.constants import (HTTP_200_ACCEPTED, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY)


class NoteListView(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = NoteSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        text, profile_id = data['text'], data['profile_id']
        with Session(engine) as session:

            profile = session.get(Profile, profile_id)
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



class ProfileMeNotes(Resource):
    def get(self, profile_id):
        with Session(engine) as session:
            notes = session.exec(select(Note).where(Note.profile_id == profile_id))
            return NoteSchema(many=True).dump(notes), HTTP_200_ACCEPTED
