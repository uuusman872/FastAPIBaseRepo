from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.models import User
from schema.users import UserCreateModel
from utils.utils import generate_passwd_hash
from fastapi.exceptions import HTTPException
from fastapi import status

class UsersService:
    async def get_user_by(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        users = await result.first()
        if users:
            try:
                users = users[0]
            except Exception as e:
                pass
        return users
    
    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by(email=email, session=session)
        print("[+] The user is ", user)
        return True if user is not None else False

    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data = user_data.model_dump()
        user_data["password"] = generate_passwd_hash(user_data["password"])
        # user_data["hased_password"] = "somehashedvalue"
        user_data = User(**user_data)
        user_data.role = "user"
        session.add(user_data)
        await session.commit()
        return user_data
    
    async def get_user_by_email(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user_data = result.first()
        if user_data:
            user_data = user_data[0]
        return user_data
    
    async def delete_user(self, email: str, session: AsyncSession) -> bool:
        result = await session.execute(select(User).where(User.email == email))
        user = await result.first()

        if user:
            user = user[0]  # Extract user from tuple
            await session.delete(user)
            await session.commit()
            return True  # Successfully deleted
        
        return False  # User not found
