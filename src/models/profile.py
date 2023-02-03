from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.database.database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    username = Column(String(250), unique=True)
    email = Column(String(250), unique=True)
    password = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

