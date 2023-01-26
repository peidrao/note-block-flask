from flask import jsonify
from flask.views import MethodView
from src.utils.constants import HTTP_200_ACCEPTED


class HelloWorld(MethodView):
    init_every_request = False

    def get(self):
        return jsonify({"hello": "world"}), HTTP_200_ACCEPTED
