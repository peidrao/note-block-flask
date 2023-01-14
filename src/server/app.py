from flask import Flask

# from src.database.connect import create_db_and_tables
# from server import make_celery
#
from src.server.config import config
from src.server.routers import register_endpoints

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    # app.config.update(
        # CELERY_BROKER_URL=config.CELERY_BROKER_URL,
        # CELERY_RESULT_BACKEND=config.CELERY_RESULT_BACKEND
    # )
    # celery = make_celery(app)
    # celery.conf.update(app.config)

    register_endpoints(app)
    return app
