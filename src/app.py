from flask import Flask
from flask_restful import Resource, Api

from dotenv import dotenv_values
from database.connect import create_db_and_tables

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
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host=config.get('HOST'), port=8080, debug=config.get('DEBUG'))
