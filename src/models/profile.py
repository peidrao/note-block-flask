from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    email: str
    password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
