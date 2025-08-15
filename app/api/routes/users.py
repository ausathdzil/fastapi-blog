from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, get_current_user
from app.models.user import User, UsersPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_users_me(current_user: CurrentUser):
    return current_user


@router.get("/", dependencies=[Depends(get_current_user)], response_model=UsersPublic)
async def read_users():
    users = await User.find_all().to_list()
    return UsersPublic(data=users)
