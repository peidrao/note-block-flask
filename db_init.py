# from src.database.connect import create_db_and_tables, drop_db_and_tables
from sqlmodel import SQLModel
from src.database.connect import engine
from src.models import Note, Profile


def start_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


start_db()
