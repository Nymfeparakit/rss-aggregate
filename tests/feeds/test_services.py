from datetime import timezone, datetime, timedelta

from src.feeds.services import FeedsService, ArticlesParser, Article


class TestFeedsService:
    def test_find_last_article(self):
        now = datetime.now(timezone.utc)
        published1 = (now - timedelta(hours=5)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
        published2 = (now - timedelta(hours=3)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
        entries_data = [
            {
                "title": "Title1",
                "link": "https://example.com/link1",
                "published": published1,
                "summary": "Summary1",
            },
            {
                "title": "Title2",
                "link": "https://example.com/link2",
                "published": published2,
                "summary": "Summary2",
            },
        ]
        rss_data = {"bozo": False, "entries": entries_data}
        expected_result = Article(
            title=entries_data[1]["title"],
            summary=entries_data[1]["summary"],
            link=entries_data[1]["link"],
        )

        result = ArticlesParser().find_last_article(rss_data)
        assert result == expected_result

    def test_find_last_article_no_published_key(self):
        entries_data = [
            {
                "title": "Title1",
                "link": "https://example.com/link1",
                "summary": "Summary1",
            },
            {
                "title": "Title2",
                "link": "https://example.com/link2",
                "summary": "Summary2",
            },
        ]
        rss_data = {"bozo": False, "entries": entries_data}
        expected_result = Article(
            title=entries_data[0]["title"],
            summary=entries_data[0]["summary"],
            link=entries_data[0]["link"],
        )

        result = ArticlesParser().find_last_article(rss_data)
        assert result == expected_result

    def test_find_last_article_published_more_10_hours(self):
        now = datetime.now(timezone.utc)
        published1 = (now - timedelta(hours=12)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
        published2 = (now - timedelta(hours=14)).strftime(ArticlesParser.PUBLISHED_DATETIME_FORMAT)
        entries_data = [
            {
                "title": "Title1",
                "link": "https://example.com/link1",
                "published": published1,
                "summary": "Summary1",
            },
            {
                "title": "Title2",
                "link": "https://example.com/link2",
                "published": published2,
                "summary": "Summary2",
            },
        ]
        rss_data = {"bozo": False, "entries": entries_data}

        result = ArticlesParser().find_last_article(rss_data)
        assert result is None
