import uuid
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publisher_date: Optional[datetime] = None
    page_count: int
    language: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publisher_date: Optional[datetime] = None
    page_count: int
    language: str

    class Config:
        from_attributes = True 

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: Optional[str]
    page_count: Optional[int]
    language: str