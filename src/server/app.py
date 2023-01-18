from flask import Flask
from src.server.config import config
from src.server.routers import register_endpoints
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, resources={r"/" {"origins": "http://localhost:8080"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object(config)
    register_endpoints(app)
    return app
