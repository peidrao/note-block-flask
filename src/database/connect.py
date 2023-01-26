from sqlmodel import create_engine
from src.server.config import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
