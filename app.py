from flask import Flask

from dotenv import dotenv_values
from database.connect import create_db_and_tables

config = dotenv_values(".env")


app = Flask(__name__)

@app.before_first_request
def create_db():
    app.logger.info("Creating initial database")
    create_db_and_tables()
    app.logger.info("Initial database created")



@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host=config.get('HOST'), port=8080, debug=config.get('DEBUG'))
