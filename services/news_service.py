from typing import List

import httpx

from config import (
    NEWS_API_KEY,
    NEWS_LANGUAGE,
    NEWS_PAGE_SIZE,
    NEWS_QUERY,
    NEWS_SORT_BY,
    REQUEST_TIMEOUT,
)

from models.raw_article import RawArticle


class NewsService:
    """
    Fetches the latest news from NewsAPI.

    Responsibilities:
    -----------------
    • Fetch latest news
    • Validate API response
    • Convert NewsAPI response into RawArticle objects

    It DOES NOT:
    -----------------
    • Perform LLM reasoning
    • Filter relevance
    • Summarize news
    """

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):

        if not NEWS_API_KEY:
            raise ValueError(
                "NEWS_API_KEY not found in environment variables."
            )

        self.api_key = NEWS_API_KEY

    def fetch_latest_news(self) -> List[RawArticle]:

        params = {
            "q": NEWS_QUERY,
            "language": NEWS_LANGUAGE,
            "sortBy": NEWS_SORT_BY,
            "pageSize": NEWS_PAGE_SIZE,
            "apiKey": self.api_key,
        }

        try:

            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:

                response = client.get(
                    self.BASE_URL,
                    params=params,
                )

                response.raise_for_status()

                data = response.json()

            articles = data.get("articles", [])

            return [
                self._normalize(article)
                for article in articles
            ]

        except Exception as e:

            print(f"[NewsAPI Error] {e}")

            return []

    def _normalize(self, article: dict) -> RawArticle:
        """
        Converts a NewsAPI article
        into a RawArticle object.
        """

        return RawArticle(

            title=article.get("title", ""),

            description=article.get("description", ""),

            content=article.get("content"),

            source=article.get("source", {}).get(
                "name",
                "Unknown",
            ),

            url=article.get("url", ""),

            published_at=article.get(
                "publishedAt",
                "",
            ),
        )
if __name__ == "__main__":
    service = NewsService()

    articles = service.fetch_latest_news()

    print(articles)
