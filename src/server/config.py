import os
from dotenv import dotenv_values
from pydantic import PostgresDsn

config = dotenv_values(".env")

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    DEBUG = True


class TestConfig(Config):
    """Testing configuration options."""
    ENV_PREFIX = 'APP_'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory.db'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = PostgresDsn.build(
        scheme='postgresql+psycopg2',
        path='/flask_db',
        user=config.get('DATABASE_USER'),
        password=config.get('DATABASE_PASS'),
        host=config.get('HOST'),
        port=config.get('DATABASE_PORT')
    )
    HOST = config.get('HOST')

    CELERY_BROKER_URL = config.get('CELERY_BROKER')
    CELERY_RESULT_BACKEND = config.get('CELERY_RESULT')


available_configs = dict(development=DevelopmentConfig, test=TestConfig)
selected_config = os.environ.get("FLASK_DEBUG")
config = available_configs.get(selected_config)
