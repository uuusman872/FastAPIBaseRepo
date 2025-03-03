from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from utils.utils import decode_token
from fastapi import status
from models.redis_connection import token_in_blacklist
from models.database import get_session
from service.users_service import UsersService
from typing import List

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(detail="token is invalid", status_code=status.HTTP_403_FORBIDDEN)
        if await token_in_blacklist(token_data["jti"]):
            raise HTTPException(detail="Token revoked", status_code=status.HTTP_403_FORBIDDEN)
        self.verify_token_data(token_data)
        return token_data
    
    def token_valid(self, token: str) -> str:
        token_data = decode_token(token)
        return True if token is not None else False

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please Override this method in child class")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")
        

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide refresh token")


user_service = UsersService()
async def get_current_user(token_details: dict=Depends(AccessTokenBearer()), session=Depends(get_session)):
    username = token_details["user"]["username"]
    user = await user_service.get_user_by_email(username, session)
    return user



class RoleChecker:
    def __init__(self, allowed_list: List[str]):
        self.allowes_roles = allowed_list
    
    def __call__(self, current_user=Depends(get_current_user)):
        if current_user.role in self.allowes_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowd to perform this action"
        )

