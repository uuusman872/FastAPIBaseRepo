from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    __tablename__ = "user"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, 
            primary_key=True, 
            default=uuid.uuid4()
        )
    )
    email: str
    username: str
    password: str = Field(exclude=True)
    firstname: str
    lastname: str
    is_verified: bool = Field(sa_column=Column(pg.BOOLEAN, default=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=True, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=True, default=datetime.now))

    def __repr__(self):
        return f"<User {self.username} >"
    