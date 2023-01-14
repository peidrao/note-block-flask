from flask.cli import FlaskGroup

from src.server.app import create_app
from src.server.config import config
from src.database.connect import create_db_and_tables

app = create_app()


if __name__ == '__main__':
    with app.app_context():
        app.logger.info("Creating initial database")
        create_db_and_tables()
        app.logger.info("Initial database created")

    app.run(host=config.HOST, port=8080, debug=config.DEBUG)
