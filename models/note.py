from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    profile_id: Optional[int] = Field(default=None, foreign_key='profile.id')
