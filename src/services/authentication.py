import jwt

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask_restful import Resource
from flask import request
from dotenv import dotenv_values


from database.connect import engine
from models.profile import Profile
from schemas.profile import ProfileSchema, ProfileLoginSchema

from utils.constants import (HTTP_200_ACCEPTED, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
     HTTP_422_UNPROCESSABLE_ENTITY
)

config = dotenv_values(".env")


class ProfileSignupView(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        name = data['name']
        username, email, password = data['username'], data['email'], data['password']

        with Session(engine) as session:
            exists = session.exec(select(Profile).where(
                Profile.email == email,
                Profile.username == username))

            if exists.first():
                return {'message': 'Profile already exists'}, HTTP_400_BAD_REQUEST

            profile = Profile(
                name=name,
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            session.add(profile)
            session.commit()
            result = ProfileSchema().dump(session.get(Profile, profile.id))
            return {'message': result}, HTTP_201_CREATED


class ProfileLoginView(Resource):

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No payload'}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileLoginSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        username, password = data['username'], data['password']
        with Session(engine) as session:
            profile = session.exec(select(Profile).where(
                Profile.username == username
                )).first()

            if profile:
                if check_password_hash(profile.password, password):
                    token = jwt.encode({
                        'profile_id': profile.id,
                        'exp' : datetime.utcnow() + timedelta(minutes = 30)
                    }, config.get('SECRET_KEY'), 'HS256')
                    return {'token': token}, HTTP_200_ACCEPTED

                return {'message': 'passwords do not match'}, HTTP_403_FORBIDDEN
            return {'message': 'profile not found'}, HTTP_404_NOT_FOUND
