from fastapi import APIRouter

from src.auth import fastapi_users
from src.auth.auth_backend import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate

router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend, requires_verification=True))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True))
