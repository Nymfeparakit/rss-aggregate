import asyncio
from typing import Dict, Any, List

import feedparser
from aiohttp import ClientSession, ClientTimeout
from fastapi import Depends
from loguru import logger

from src.auth import User
from src.feeds.exceptions import CanNotFetchRSSByURL
from src.feeds.schemas import Article
from src.rss.parsers import ArticlesParser
from src.sources.services import get_sources_service, SourceService


async def fetch_data_by_url(session: ClientSession, url: str) -> Dict[str, Any]:
    """Try to fetch data from urls using async session."""
    request_timeout = ClientTimeout(2)
    async with session.get(url, timeout=request_timeout) as response:
        try:
            data = await response.text()
            status = response.status
            if status != 200:
                raise CanNotFetchRSSByURL(
                    f"Failed to fetch data by url: {url}, response - {data}, status - {status}"
                )
            logger.info(f"got feed data from {url}")
            return data
        except asyncio.TimeoutError:
            CanNotFetchRSSByURL(
                f"Failed to fetch data by url: {url}, timeout error"
            )


class FeedsService:
    def __init__(self, sources_service: SourceService):
        self.feed_parser = ArticlesParser()
        self.sources_service = sources_service

    async def get_today_feed(self, user: User) -> List[Article]:
        """Find sources from all user folders.
        From each of these resources, take the most recently published article.
        """
        # get all sources from all user folders
        user_sources = await self.sources_service.find_sources_by_user(user)
        # for each source get latest news (for last 10 hours)
        async with ClientSession() as session:
            fetchers = [
                fetch_data_by_url(session, source.url) for source in user_sources
            ]
            articles = []

            for finished_task in asyncio.as_completed(fetchers):
                try:
                    rss_data = await finished_task

                    parsed_data = feedparser.parse(rss_data)
                    article = self.feed_parser.find_last_article(parsed_data)
                    if article is not None:
                        articles.append(article)

                except CanNotFetchRSSByURL as e:
                    logger.error(str(e))

        return articles


def get_feeds_service(sources_service=Depends(get_sources_service)) -> FeedsService:
    return FeedsService(sources_service)
