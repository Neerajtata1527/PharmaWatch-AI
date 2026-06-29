from typing import List

from models.raw_article import RawArticle
from models.event_schema import EventReport

from chains.event_chain import classify_article
from utils.noise_filter import filter_articles
from utils.parallel import run_parallel

from config import MAX_PARALLEL_WORKERS


class EventAgent:
    """
    Event Intelligence Agent

    Responsibilities
    ----------------
    1. Receive raw news articles.
    2. Remove obvious noise.
    3. Classify remaining articles using the LLM.
    4. Filter irrelevant events.
    5. Execute classifications in parallel.
    """

    def _process_single_article(
        self,
        article: RawArticle,
    ) -> EventReport | None:

        try:

            print(f"\nProcessing : {article.title}")

            event = classify_article(article)

            if event.relevant:

                print("✓ Relevant")
                return event

            print("✗ Not Relevant")
            return None

        except Exception as e:

            print(
                f"\nFailed to classify article\n"
                f"Title  : {article.title}\n"
                f"Reason : {e}\n"
            )

            return None

    def process_articles(
        self,
        articles: List[RawArticle],
    ) -> List[EventReport]:

        articles = filter_articles(articles)

        print(f"\nArticles after Noise Filter: {len(articles)}")

        if not articles:
            return []

        print(
            f"\nRunning {len(articles)} article classifications "
            f"using up to {MAX_PARALLEL_WORKERS} worker threads...\n"
        )

        relevant_events = run_parallel(
            items=articles,
            worker=self._process_single_article,
            max_workers=MAX_PARALLEL_WORKERS,
        )

        print(
            f"\n✓ Event Agent completed."
            f"\nRelevant Events Found : {len(relevant_events)}\n"
        )

        return relevant_events


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService

    news_service = NewsService()
    gdelt_service = GDELTService()

    print("\nFetching NewsAPI articles...")
    news_articles = news_service.fetch_latest_news()

    print(f"Fetched {len(news_articles)} NewsAPI articles.")

    print("\nFetching GDELT articles...")
    gdelt_articles = gdelt_service.fetch_latest_events()

    print(f"Fetched {len(gdelt_articles)} GDELT articles.")

    all_articles = news_articles + gdelt_articles

    print(f"\nTotal Articles Fetched: {len(all_articles)}")

    agent = EventAgent()

    events = agent.process_articles(all_articles)

    print("\n" + "=" * 80)
    print(f"Relevant Events Found: {len(events)}")
    print("=" * 80)

    for i, event in enumerate(events, start=1):

        print(f"\nEvent {i}")
        print("-" * 80)
        print(event)