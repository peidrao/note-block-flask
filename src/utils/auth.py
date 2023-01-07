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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.split(' ')[1]
        if not token:
            return {'message': 'Token is missing'}, HTTP_401_UNAUTHORIZED

        try:
            data = jwt.decode(token, config.get("SECRET_KEY"), "HS256")
            with Session(engine) as session:
                profile = session.get(Profile, data['profile_id'])

        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'}), HTTP_401_UNAUTHORIZED
        # import pdb; pdb.set_trace()
        return f(profile, *args, **kwargs)

    return decorated
