import jwt

from functools import wraps
from flask import request
from dotenv import dotenv_values
from src.database.database import Session

from src.models.profile import Profile
from src.utils import status

config = dotenv_values(".env")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
        if not token:
            return {"message": "Token is missing"}, status.HTTP_401_UNAUTHORIZED

        try:
            data = jwt.decode(token, config.get("SECRET_KEY"), "HS256")

            with Session() as session:
                profile = (
                    session.query(Profile)
                    .filter(Profile.id == data.get("sub"))
                    .one_or_none()
                )

        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError,
        ) as error:
            return {"message": error.args[0]}, status.HTTP_400_BAD_REQUEST
        return f(profile, *args, **kwargs)

    return decorated
