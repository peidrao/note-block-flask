from flask import Flask

from src.database.connect import create_db_and_tables
from src.extensions import make_celery

from src.config import config
from src.routers import register_endpoints


app = Flask(__name__)
app.config.from_object(config)
app.config.update(
    CELERY_BROKER_URL=config.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=config.CELERY_RESULT_BACKEND
)
celery = make_celery(app)
celery.conf.update(app.config)

register_endpoints(app)

if __name__ == '__main__':
    with app.app_context():
        app.logger.info("Creating initial database")
        create_db_and_tables()
        app.logger.info("Initial database created")

    app.run(host=config.HOST, port=8080, debug=config.DEBUG)
