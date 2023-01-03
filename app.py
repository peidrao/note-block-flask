from flask import Flask
import logging

from database.connect import create_db_and_tables

logger = logging.getLogger(__name__)


app = Flask(__name__)

@app.before_first_request
def create_db():
    logger.info("Creating initial database")
    create_db_and_tables()
    logger.info("Initial database created")


@app.route('/')
def index():
    return 'Hello, World!'
