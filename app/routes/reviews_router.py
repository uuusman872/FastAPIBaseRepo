from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from models.database import get_session
from service.books_service import BookService
from schema.books import Book, BookUpdateModel, BookCreateModel
from typing import List
from dependencies.users import AccessTokenBearer
from dependencies.users import RoleChecker
from models.models import User
from schema.review import ReviewCreatedModel
from service.reviews_service import ReviewService

review_router = APIRouter()

review_service = ReviewService()

@review_router.get("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str, current_user: User, 
    review_data: ReviewCreatedModel, 
    session: AsyncSession=Depends(get_session)
):
    review_service.add_review_to_book(
        user_email=current_user.username,
        review_data=review_data,
        book_uid=book_uid,
        session=session      
    )
    return review_service

