from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import authenticate, create_access_token, get_password_hash
from app.models.token import Token
from app.models.user import User, UserPublic, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_db = await authenticate(form_data.username, form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        sub=user_db.username, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/register", response_model=UserPublic)
async def register_user(user_in: UserRegister):
    existing_user = await User.find_one(User.username == user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = await User.find_one(User.email == user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )

    await user.insert()
    return user
