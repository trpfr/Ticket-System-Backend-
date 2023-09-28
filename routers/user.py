import uuid

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.mananger import get_user_manager
from database import get_async_session
from models.user import User
from dto import user as user_dto

#  This is the router object. It is used to create the routes.
router = APIRouter()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)


async def async_wrapper(func, *args, **kwargs):
    return await func(*args, **kwargs)


@router.get("/",
            response_model=user_dto.UserRead,
            tags=["user"],
            dependencies=[Depends(current_active_user)])
async def get_current_user(user: User = Depends(current_active_user)):
    """Get the current user"""
    return user


