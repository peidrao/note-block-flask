from sqlmodel import create_engine, SQLModel
from src.server.config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)
