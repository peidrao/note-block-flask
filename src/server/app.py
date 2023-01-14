from flask import Flask
from src.server.config import config
from src.server.routers import register_endpoints

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    register_endpoints(app)
    return app
