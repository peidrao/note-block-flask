from flask import jsonify
from flask.views import MethodView
from src.tasks import tasks
from src.utils.constants import HTTP_200_ACCEPTED


class HelloWorld(MethodView):
    init_every_request = False

    def get(self):
        # result = tasks.add_together.delay(1, 2)
        return jsonify({"hello": "world"}), HTTP_200_ACCEPTED
