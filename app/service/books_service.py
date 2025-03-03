from sqlalchemy.ext.asyncio.session import AsyncSession
from schema.books import BookCreateModel, BookUpdateModel
from models.models import Book
from sqlmodel import select, desc


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        results = result.scalars().all()
        return results
    
    async def get_users_books(self, uid, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == uid).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        results = result.scalars().all()
        return results
    
    async def get_books(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uuid == book_uid)
        result = await session.execute(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, user_uid, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        update_data_dict = update_data.model_dump()
        book_to_update = self.get_books(book_uid)
        if book_to_update:
            for k, v in update_data_dict:
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update
        return book_to_update
    
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = self.get_books(book_uid)
        if book_to_delete is None:
            return None
        await session.delete(book_to_delete)
        await session.commit()