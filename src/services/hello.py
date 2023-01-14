from flask import jsonify
from flask.views import MethodView

from utils.constants import HTTP_200_ACCEPTED


class HelloWorld(MethodView):
    init_every_request = False
    def get(self):
        from tasks import tasks
        result = tasks.add_together.delay(1, 1)
        print(result)
        print("PEDRO")
        return jsonify({'hello': 'world'}), HTTP_200_ACCEPTED
