from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from schema.books import Book
from schema.review import ReviewModel

class UserCreateModel(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    password: str


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    firstname: str
    lastname: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    books: List[Book]

class UserBookModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]

class UserLoginModel(BaseModel):
    email: str
    password: str
