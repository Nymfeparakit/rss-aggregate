from datetime import timezone, datetime, timedelta
from unittest.mock import patch

import pytest
from starlette import status

from src.feeds.services import ArticlesParser


@pytest.mark.asyncio
async def test_get_today_feed(override_app_client, sources):
    now = datetime.now(timezone.utc)
    published1 = (now - timedelta(hours=2)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
    published2 = (now - timedelta(hours=3)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
    entry1 = {
            "title": "Title1",
            "link": "https://example.com/link1",
            "published": published1,
            "summary": "Summary1",
    }
    entries_data1 = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">

<channel>
<title>The Simplest Feed</title>
<link>http://example.org/index.html</link>
<description>The Simplest Possible RSS 2.0 Feed</description>

<item>
<title>{entry1["title"]}</title>
<pubDate>{entry1["published"]}</pubDate>
<link>{entry1["link"]}</link>
<summary>{entry1["summary"]}</summary>
</item>
</channel>
</rss>
    """
    entry2 = {
        "title": "Title2",
        "link": "https://example.com/link2",
        "published": published2,
        "summary": "Summary2",
    }
    entries_data2 = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">

<channel>
<title>The Simplest Feed</title>
<link>http://example.org/index.html</link>
<description>The Simplest Possible RSS 2.0 Feed</description>

<item>
<title>{entry2["title"]}</title>
<pubDate>{entry2["published"]}</pubDate>
<link>{entry2["link"]}</link>
<summary>{entry2["summary"]}</summary>
</item>
</channel>
</rss>
        """
    expected_response_data = [
        {"title": entry1["title"], "summary": entry1["summary"], "link": entry1["link"]},
        {"title": entry2["title"], "summary": entry2["summary"], "link": entry2["link"]},
    ]

    with patch("src.feeds.services.fetch_data_by_url") as fetch_patched:
        fetch_patched.side_effect = [entries_data1, entries_data2]
        response = await override_app_client.get("http://test/feeds/today")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_data
