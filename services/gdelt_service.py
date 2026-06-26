from typing import List

import httpx

from config import (
    GDELT_BASE_URL,
    GDELT_QUERY,
    GDELT_TIMESPAN,
    GDELT_MAX_RECORDS,
    GDELT_MODE,
    GDELT_FORMAT,
    REQUEST_TIMEOUT,
)

from models.raw_article import RawArticle


class GDELTService:

    """
    Fetch recent articles directly from GDELT.
    """

    def fetch_latest_events(self) -> List[RawArticle]:

        params = {

            "query": GDELT_QUERY,

            "mode": GDELT_MODE,

            "format": GDELT_FORMAT,

            "maxrecords": GDELT_MAX_RECORDS,

            "timespan": GDELT_TIMESPAN,

        }

        try:

            with httpx.Client(timeout=REQUEST_TIMEOUT,follow_redirects=True) as client:

                response = client.get(
                    GDELT_BASE_URL,
                    params=params,
                )

                response.raise_for_status()

                data = response.json()

            articles = data.get("articles", [])

            return [

                self._normalize(article)

                for article in articles

            ]

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                print("⚠️ GDELT rate limit exceeded. Falling back to other news sources.")
            else:
                print(f"GDELT HTTP Error: {e}")
            return []
        except Exception as e:
            print(f"GDELT Unexpected Error: {e}")
            return []

    def _normalize(
        self,
        article: dict,
    ) -> RawArticle:

        return RawArticle(

            title=article.get("title", ""),

            description=article.get("seendate", ""),

            content=None,

            source=article.get("domain", "GDELT"),

            url=article.get("url", ""),

            published_at=article.get(
                "seendate",
                "",
            ),
        )


if __name__ == "__main__":

    service = GDELTService()

    articles = service.fetch_latest_events()

    print(articles)