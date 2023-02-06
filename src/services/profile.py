from flask import request
from flask.views import MethodView

from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from src.database import Session
from src.models import Profile
from src.schemas.profile import ProfileSchema
from src.utils.auth import token_required

from src.utils import status


class ProfileListView(MethodView):
    @token_required
    def get(self, _):
        with Session() as session:
            profiles = session.query(Profile).all()
            return ProfileSchema(many=True).dump(profiles)


class ProfileDetailsView(MethodView):
    def get(self, profile_id):
        with Session() as session:
            profile = session.query(Profile).filter(
                Profile.id == profile_id).one_or_none()
            return ProfileSchema().dump(profile), status.HTTP_200_ACCEPTED

    def delete(self, profile_id):
        with Session() as session:
            session.query(Profile).filter(Profile == profile_id).delete()
            return status.HTTP_204_NO_CONTENT

    def put(self, profile_id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No payload"}, status.HTTP_400_BAD_REQUEST

        try:
            data = ProfileSchema().load(json_data)
        except ValidationError as err:
            return err.messages, status.HTTP_422_UNPROCESSABLE_ENTITY

        name = data["name"]
        with Session() as session:
            profile = session.query(Profile).filter(Profile == profile_id).one_or_none()
            profile.name = name
            session.commit()
            result = ProfileSchema().dump(session.get(Profile, profile_id))
            return result, status.HTTP_200_ACCEPTED


class ProfileMeView(MethodView):
    @token_required
    def get(self, _):
        with Session() as session:
            profile = session.query(Profile).filter(Profile.id == self.id).one_or_none()
            result = ProfileSchema().dump(profile)
            return result, status.HTTP_200_ACCEPTED


class ProfileUpdatePasswordView(MethodView):
    @token_required
    def post(self, _):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No password"}, status.HTTP_400_BAD_REQUEST
        password = json_data.get('password')

        with Session() as session:
            profile = session.query(Profile).filter(Profile.id == self.id).one_or_none()
            if profile:
                profile.password = generate_password_hash(password)
                session.commit()
                return {"message": "Password update"}, status.HTTP_200_ACCEPTED

        return {"message": "Profile not found"}, status.HTTP_404_NOT_FOUND
