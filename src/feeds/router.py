from typing import List

from fastapi import APIRouter, Depends

from src.auth import User, current_user
from src.feeds.schemas import Article
from src.feeds.services import FeedsService, get_feeds_service

feeds_router = APIRouter()


@feeds_router.get("/today", response_model=List[Article])
async def get_today_feed(user: User = Depends(current_user), feeds_service: FeedsService = Depends(get_feeds_service)):
    return await feeds_service.get_today_feed(user)
