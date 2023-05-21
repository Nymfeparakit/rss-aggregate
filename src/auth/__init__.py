import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.auth.auth_backend import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate, UserUpdate


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True, verified=True)
