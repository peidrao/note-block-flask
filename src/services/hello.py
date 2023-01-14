from flask import jsonify
from flask.views import MethodView

from src.utils.constants import HTTP_200_ACCEPTED


class HelloWorld(MethodView):
    init_every_request = False
    def get(self):
        # from src.tasks import tasks
        # result = tasks.add_together.delay(1, 1)
        return jsonify({'hello': 'world'}), HTTP_200_ACCEPTED
