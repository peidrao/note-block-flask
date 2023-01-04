from flask_restful import Resource
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask import request

from database.connect import engine
from models.profile import Profile
from schemas.profile import ProfileSchema
from utils.constants import (HTTP_200_ACCEPTED, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileListView(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        name = data['name']
        with Session(engine) as session:
            profile = Profile(name=name)
            session.add(profile)
            session.commit()
            result = ProfileSchema().dump(session.get(Profile, profile.id))
            return {'message': result}, HTTP_201_CREATED


    def get(self):
        with Session(engine) as session:
            profiles = session.exec(select(Profile)).all()
            return ProfileSchema(many=True).dump(profiles)


class ProfileDetailsView(Resource):

    def get(self, profile_id):
        with Session(engine) as session:
            profile = session.get(Profile, profile_id)
            return ProfileSchema().dump(profile), HTTP_200_ACCEPTED

    def delete(self, profile_id):
        with Session(engine) as session:
            profile = session.get(Profile, profile_id)
            session.delete(profile)
            session.commit()
            return HTTP_204_NO_CONTENT

    def put(self, profile_id):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        name = data['name']
        with Session(engine) as session:
            profile = session.get(Profile, profile_id)
            profile.name = name
            session.commit()
            result = ProfileSchema().dump(session.get(Profile, profile_id))
            return result, HTTP_200_ACCEPTED
