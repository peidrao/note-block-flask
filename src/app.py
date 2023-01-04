from flask import Flask
from flask_restful import Resource, Api

from dotenv import dotenv_values
from database.connect import create_db_and_tables
from utils.constants import HTTP_200_ACCEPTED
from services.profile import ProfileListView

config = dotenv_values(".env")


app = Flask(__name__)
api = Api(app)


@app.before_first_request
def create_db():
    app.logger.info("Creating initial database")
    create_db_and_tables()
    app.logger.info("Initial database created")


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, HTTP_200_ACCEPTED


api.add_resource(HelloWorld, '/')
api.add_resource(ProfileListView, '/profile')

if __name__ == '__main__':
    app.run(host=config.get('HOST'), port=8080, debug=config.get('DEBUG'))
