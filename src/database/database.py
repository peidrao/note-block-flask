from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.server.config import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    from src.models.profile import Profile
    from src.models.note import Note, Tag
    Base.metadata.create_all(bind=engine)
