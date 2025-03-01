from pydantic import BaseModel, Field
import uuid
from datetime import datetime

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
    is_verified: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserLoginModel(BaseModel):
    email: str
    password: str
