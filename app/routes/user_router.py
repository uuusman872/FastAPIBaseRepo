from fastapi import APIRouter, status, Depends, HTTPException
from schema.users import UserCreateModel, UserLoginModel, UserModel, UserBookModel
from sqlmodel.ext.asyncio.session import AsyncSession
from service.users_service import UsersService
from models.database import get_session
from utils.utils import verify_password, generate_access_token
from datetime import timedelta
from fastapi.responses import JSONResponse
from dependencies.users import RefreshTokenBearer
from datetime import datetime
from utils.utils import generate_access_token
from dependencies.users import AccessTokenBearer
from models.redis_connection import add_jti_to_blocklist
from dependencies.users import get_current_user
from dependencies.users import RoleChecker

router = APIRouter()
service = UsersService()
role_checker = RoleChecker(allowed_list=["admin", "user"])


@router.post("/signup")
async def create_user_account(user_data: UserCreateModel,
                            session: AsyncSession = Depends(get_session)):
    
    email = user_data.email
    print("Fuck")
    exists = await service.user_exists(email, session=session)
    print("[+] The user is ", exists)
    if exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Already exist's")
    new_user = await service.create_user(user_data, session=session)
    return new_user


@router.post("/login")
async def login_users(login_form: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_form.email
    password = login_form.password
    user = await service.get_user_by(email=email, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Does not exist's")
    password_valid = verify_password(password, user.password)
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token = generate_access_token(user_data={"username": user.username, "user_uid": str(user.uid), "role": user.role})
    refresh_token = generate_access_token(user_data={"username": user.username, "user_uid": str(user.uid), "role": user.role}, refresh=True, expiry=timedelta(days=2))
    
    return JSONResponse(content={
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "username": user.username,
            "uid": str(user.uid)
        }
    })

@router.get("/refresh")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_date = token_details["exp"]
    if datetime.fromtimestamp(expiry_date) > datetime.now():
        new_access_token = generate_access_token(user_data=token_details["user"])
        new_refresh_token = generate_access_token(user_data=token_details["user"], refresh=True, expiry=timedelta(days=2))
        return JSONResponse(content={
        "message": "Login Successful",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "user": token_details["user"]
    })
    raise HTTPException(detail="refresh token is expired", status_code=status.HTTP_403_FORBIDDEN)


@router.get("/me", response_model=UserBookModel)
async def get_current_user(user=Depends(get_current_user), _:bool=Depends(RoleChecker(allowed_list=["admin", "user"]))):
    return user


@router.get("/logout")
async def logout(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details.get("jti")
    await add_jti_to_blocklist(jti)
    return JSONResponse(content={
        "message": "Logged Out Complete",
    }, status_code=status.HTTP_200_OK)