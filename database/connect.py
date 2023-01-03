from pydantic import PostgresDsn

from models.note import Note

from models.profile import Profile


from sqlmodel import create_engine, SQLModel

DATABASE_URI: str = PostgresDsn.build(
    scheme='postgresql+psycopg2',
    path='/flask_db',
    user='flask',
    password='flask',
    host='localhost',
    port='5434')

engine = create_engine(DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
