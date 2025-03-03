from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from models.database import get_session
from service.books_service import BookService
from schema.books import Book, BookUpdateModel, BookCreateModel
from typing import List
from dependencies.users import AccessTokenBearer
from dependencies.users import RoleChecker

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_list=["admin", "user"]))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_access = Depends(access_token_bearer)):
    print("[+] The user data is ", user_access)
    books = await book_service.get_all_books(session)
    return books

@router.get("/user")
async def get_book_by_user(session: AsyncSession=Depends(get_session), user_access=Depends(access_token_bearer)):
    uid = user_access["user"]["user_uid"]
    books = await book_service.get_users_books(uid=uid, session=session)
    return books

@router.post("/", status_code=status.HTTP_200_OK, response_model=BookCreateModel, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), user_access = Depends(access_token_bearer)):
    user_id = user_access["user"]["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid=user_id, session=session)
    return new_book

@router.get("/{book_uid}", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def get_book(book_uid: int, session: AsyncSession = Depends(get_session), user_access = Depends(access_token_bearer)):
    book = await book_service.get_books(book_uid, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_201_CREATED)

@router.patch("/{book_uid}", status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), user_access = Depends(access_token_bearer)):
    update_book = await book_service.update_book(book_uid, book_update_data, session)
    if update_book:
        return update_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid, session: AsyncSession = Depends(get_session), user_access = Depends(access_token_bearer)):
    await book_service.delete_book(book_uid, session)
