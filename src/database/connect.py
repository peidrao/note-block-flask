from dotenv import dotenv_values
from pydantic import PostgresDsn
from sqlmodel import create_engine, SQLModel

config = dotenv_values(".env")


DATABASE_URI: str = PostgresDsn.build(
    scheme='postgresql+psycopg2',
    path='/flask_db',
    user=config.get('DATABASE_USER'),
    password=config.get('DATABASE_PASS'),
    host=config.get('HOST'),
    port=config.get('DATABASE_PORT'))

engine = create_engine(DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
