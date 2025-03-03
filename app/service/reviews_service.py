from schema.review import ReviewCreatedModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from service.books_service import BookService
from service.users_service import UsersService
from models.models import Review
from fastapi import status

book_service = BookService()
user_service = UsersService()
class ReviewService:
    async def add_review_to_book(
            self,
            username: str,
            book_uid: str,
            review_date: ReviewCreatedModel,
            session: AsyncSession
    ):
        try:
            book = await book_service.get_books(
                book_uid=book_uid,
                session=session
            )
            user = await user_service.get_user_by_email(
                username=username,
                session=session
            )
            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            review_data_dict = review_date.model_dump()
            
            new_review = Review(
                **review_data_dict
            )
            new_review.user = user
            new_review.book = book[0]
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review
        except Exception as e:
            raise HTTPException(status_code=500, detail="Ops something went wrong")