from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    pass


CurrentUser = Annotated[User, Depends(get_current_user)]
