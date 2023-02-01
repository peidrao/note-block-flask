from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from datetime import datetime

from src.database.database import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", backref=backref("profiles_tags", uselist=False))


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    text = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", backref=backref("profiles", uselist=False))

    tag_id = Column(Integer, ForeignKey("tags.id"))
    tag = relationship("Tag", backref=backref("tags", uselist=False))
