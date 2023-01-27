from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from datetime import datetime

from src.database.database import Base


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    text = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", backref=backref("profiles", uselist=False))
