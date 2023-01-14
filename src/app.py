from flask import Flask
# from flask_restful import Resource, Api

# from dotenv import dotenv_values
from database import connect
# froQm services import ProfileMeView, ProfileMeNotes
# from services.hello import HelloWorld
from extensions import make_celery

# from src.utils.constants import HTTP_200_ACCEPTED

# from services import (NoteListView, ProfileDetailsView, ProfileListView,
#     ProfileSignupView, ProfileLoginView)
from config import config
from routers import register_endpoints


app = Flask(__name__)
app.config.from_object(config)
app.config.update(
    CELERY_BROKER_URL=config.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=config.CELERY_RESULT_BACKEND
)
celery = make_celery(app)
celery.conf.update(app.config)

register_endpoints(app)


@app.before_first_request
def create_db():
    app.logger.info("Creating initial database")
    connect.create_db_and_tables()
    app.logger.info("Initial database created")


# def create_app():
#     app = Flask(__name__)
#    onfig)
#     return app app.logger.info("Creating initial database")
#     connect.create_db_and_tables()
#     app.logger.info("Initial database created")
#     # app.config["CELERY_BROKER_URL"] = "redis://localhost:6378"
#     # app.config['TESTING'] = False
#     # app.config['CELERY_REDIS_USE_SSL'] = False
#     app.config.from_object(c

#     # celery = celery_app.create_celery_app(app)
#     # celery_app.celery = celery
#     # return app

# # app = create_app()
# # api = Api(app)

# def create_worker():
#     app = Flask(__name__)
#     app.config.from_object(config)
#     register_extensions(app, worker=True)

#     return app



if __name__ == '__main__':
    # create_worker()
    app.run(host=config.HOST, port=8080, debug=config.DEBUG)
