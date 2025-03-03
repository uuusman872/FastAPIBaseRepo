from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from models.database import get_session
from service.books_service import BookService
from schema.books import Book, BookUpdateModel, BookCreateModel
from typing import List
from dependencies.users import AccessTokenBearer
from dependencies.users import RoleChecker
from models.models import User
from schema.review import ReviewCreatedModel, ReviewModel
from service.reviews_service import ReviewService
from dependencies.users import get_current_user

router = APIRouter()

review_service = ReviewService()

@router.post("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str, review_data: ReviewCreatedModel, 
    current_user: User=Depends(get_current_user),
    session: AsyncSession=Depends(get_session)
):
    username = current_user.username
    new_review = await review_service.add_review_to_book(
        username="uuusman872",
        review_date=review_data,
        book_uid=book_uid,
        session=session      
    )
    return new_review

