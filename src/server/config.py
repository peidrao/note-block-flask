from dotenv import dotenv_values

config = dotenv_values(".env")


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    DEBUG = True

    DATABASE_USER = config.get('DATABASE_USER')
    DATABASE_DB = config.get('DATABASE_DATA')
    DATABASE_PASSWORD = config.get('DATABASE_PASS')
    DATABASE_PORT = config.get('DATABASE_PORT')

    HOST = config.get('HOST')

    CELERY_BROKER_URL = config.get('CELERY_BROKER')
    CELERY_RESULT_BACKEND = config.get('CELERY_RESULT')



class TestConfig(Config):
    """Testing configuration options."""
    ENV_PREFIX = 'APP_'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory'


config = Config()
test_config = TestConfig()
