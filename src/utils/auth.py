from sqlmodel import Session
from models import Profile
from flask import jsonify, request
import jwt
from functools import wraps
from database.connect import engine

from dotenv import dotenv_values
from werkzeug.security import generate_password_hash, check_password_hash

from utils.constants import HTTP_401_UNAUTHORIZED

config = dotenv_values(".env")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, HTTP_401_UNAUTHORIZED

        try:
            data = jwt.decode(token, config.get("SECRET_KEY"))
            with Session(engine) as session:
                profile = session.get(Profile, data['id'])
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'}), HTTP_401_UNAUTHORIZED

        return f(profile, *args, **kwargs)

    return decorated
