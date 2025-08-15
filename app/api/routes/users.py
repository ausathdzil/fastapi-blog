from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.models.user import User, UsersPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_users_me(current_user: CurrentUser):
    return current_user


@router.get("/", response_model=UsersPublic)
async def read_users():
    users = await User.find_all().to_list()
    return UsersPublic(data=users)
