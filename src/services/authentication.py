import jwt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from sqlmodel import Session, select
from flask.views import MethodView
from flask import request
from dotenv import dotenv_values


from src.database.connect import engine
from src.models.profile import Profile
from src.schemas.profile import ProfileSchema, ProfileLoginSchema

from src.utils.constants import (
    HTTP_200_ACCEPTED,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

config = dotenv_values(".env")


class ProfileSignupView(MethodView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No payload"}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        name = data["name"]
        username, email, password = data["username"], data["email"], data["password"]

        with Session(engine) as session:
            exists = session.exec(
                select(Profile).where(
                    Profile.email == email, Profile.username == username
                )
            )

            if exists.first():
                return {"message": "Profile already exists"}, HTTP_400_BAD_REQUEST

            profile = Profile(
                name=name,
                username=username,
                email=email,
                password=generate_password_hash(password),
            )
            session.add(profile)
            session.commit()
            result = ProfileSchema().dump(session.get(Profile, profile.id))
            return result, HTTP_201_CREATED


class ProfileLoginView(MethodView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No payload"}, HTTP_400_BAD_REQUEST

        try:
            data = ProfileLoginSchema().load(json_data)
        except ValidationError as err:
            return err.messages, HTTP_422_UNPROCESSABLE_ENTITY

        username, password = data["username"], data["password"]
        with Session(engine) as session:
            profile = session.exec(
                select(Profile).where(Profile.username == username)
            ).first()

            if profile:
                if check_password_hash(profile.password, password):
                    access_token = create_access_token(identity=profile.id)
                    refresh_token = create_refresh_token(profile.id)
                    return {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }, HTTP_200_ACCEPTED

                return {"message": "passwords do not match"}, HTTP_403_FORBIDDEN
            return {"message": "profile not found"}, HTTP_404_NOT_FOUND


class TokenRefresh(MethodView):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
