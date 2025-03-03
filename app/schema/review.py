from typing import Optional
from pydantic import BaseModel, Field
import uuid
import datetime


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

class ReviewCreatedModel:
    rating: int
     

