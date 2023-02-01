from flask.views import MethodView
from src.utils import status


class HelloWorld(MethodView):
    init_every_request = False

    def get(self):
        return {"hello": "world"}, status.HTTP_200_ACCEPTED
