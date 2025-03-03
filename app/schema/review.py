from typing import Optional
from pydantic import BaseModel, Field
import uuid
from datetime import date, datetime



class ReviewModel(BaseModel):
    uid: uuid.UUID
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

class ReviewCreatedModel(BaseModel):
    rating: int
    review_text: str


