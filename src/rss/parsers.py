import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

import aiofiles
import aiohttp
import feedparser
from feedparser import FeedParserDict
from loguru import logger
from starlette import status

from src.config import global_settings
from src.feeds.schemas import Article
from src.rss.exceptions import InvalidRSSURL


class ArticlesParser:
    PUBLISHED_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"

    def find_last_article(self, parsed_rss_data: Dict[str, Any]) -> Optional[Article]:
        # get latest article in last 10 hours
        try:
            entries = parsed_rss_data["entries"]

            # if there is a published date in entries, sort them by this dates
            entries_have_date = False
            if entries[0].get("published"):
                entries_have_date = True

            if entries_have_date:
                entries = sorted(
                    entries,
                    key=self._get_entry_datetime,
                    reverse=True,
                )

            # get first entry and return its data
            first_entry = entries[0]
            if entries_have_date:
                # check that the article was published no more than 10 hours ago
                h_10_ago = datetime.now(timezone.utc) - timedelta(hours=10)
                article_published_dt = self._get_entry_datetime(first_entry)
                if article_published_dt < h_10_ago:
                    return None

            last_article = Article(
                title=first_entry["title"],
                summary=first_entry["summary"],
                link=first_entry["link"],
            )

            return last_article

        except KeyError:
            logger.error("Failed to find last article, data parsing error")

    def _get_entry_datetime(self, entry: Dict[str, Any]) -> datetime:
        return datetime.strptime(
            entry["published"], self.PUBLISHED_DATETIME_FORMAT
        )


class RSSFeedParser:
    BOZO_KEY = "bozo"

    async def try_parse_rss(self, url: str) -> FeedParserDict:
        # todo: move parsing to separate service?
        # проверяем, что ссылка на rss валидна
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != status.HTTP_200_OK:
                    raise InvalidRSSURL
                resp_text = await resp.text()

        parsed_data = feedparser.parse(resp_text)
        if parsed_data[self.BOZO_KEY] == 1:
            raise InvalidRSSURL

        return parsed_data


class CanNotFetchImage(Exception):
    pass


class ImageSavingService:
    async def save_image(self, parsed_rss_data: FeedParserDict, folder_name: str, file_name: str) -> str:
        print("trying to save an image")
        image_data = parsed_rss_data.feed.image
        async with aiohttp.ClientSession() as session:
            async with session.get(image_data.href) as resp:
                if resp.status != status.HTTP_200_OK:
                    raise CanNotFetchImage

                print("got response successfully")
                feed_dir_path = os.path.join(global_settings.icons_path, folder_name)
                dir_exists = os.path.exists(feed_dir_path)
                if not dir_exists:
                    os.makedirs(feed_dir_path)
                file_path = os.path.join(feed_dir_path, file_name)
                # todo: продумать логику на случай файлов с одинаковыми именами
                print(f"will save image at: {file_path}")
                async with aiofiles.open(file_path, mode='wb') as f:
                    await f.write(await resp.read())

        return os.path.join(folder_name, file_name)
