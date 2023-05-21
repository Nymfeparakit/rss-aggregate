import uuid

from fastapi import Depends
from fastapi_users import UUIDIDMixin, BaseUserManager

from src.auth import config
from src.auth.models import User, get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = config.RESET_PWD_SECRET
    verification_token_secret = config.VERIFICATION_TOKEN_SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
