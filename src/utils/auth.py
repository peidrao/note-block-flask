import jwt

from sqlmodel import Session
from functools import wraps
from flask import request
from dotenv import dotenv_values

from models.profile import Profile
from database.connect import engine
from utils.constants import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

config = dotenv_values(".env")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.split(' ')[1]
        if not token:
            return {'message': 'Token is missing'}, HTTP_401_UNAUTHORIZED

        try:
            data = jwt.decode(token, config.get("SECRET_KEY"), "HS256")
            with Session(engine) as session:
                profile = session.get(Profile, data['profile_id'])

        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError) as error:
            return {'message': error.args[0]}, HTTP_400_BAD_REQUEST
        return f(profile, *args, **kwargs)

    return decorated
