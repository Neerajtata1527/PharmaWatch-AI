from typing import List

from models.event_schema import EventReport
from models.research_schema import ResearchReport

from services.research_service import ResearchService
from chains.research_chain import research_event

from utils.parallel import run_parallel

from config import MAX_PARALLEL_WORKERS


class ResearchAgent:
    """
    Research Intelligence Agent

    Responsibilities
    ----------------
    1. Receive verified EventReports.
    2. Collect supporting evidence from Tavily.
    3. Generate structured ResearchReports.
    4. Execute multiple research tasks in parallel.
    """

    def __init__(self):

        self.research_service = ResearchService()

    def _process_single_event(
        self,
        event: EventReport,
    ) -> ResearchReport | None:

        try:

            print("\n" + "=" * 100)
            print(f"Researching : {event.headline}")
            print("=" * 100)

            evidence = self.research_service.collect(event)

            print("✓ Evidence collected")

            report = research_event(
                event,
                evidence,
            )

            print("✓ Research report generated")

            return report

        except Exception as e:

            print(
                f"\nResearch failed\n"
                f"Headline : {event.headline}\n"
                f"Reason   : {e}\n"
            )

            return None

    def process_events(
        self,
        events: List[EventReport],
    ) -> List[ResearchReport]:

        if not events:
            return []

        print(
            f"\nRunning {len(events)} research tasks "
            f"using up to {MAX_PARALLEL_WORKERS} worker threads...\n"
        )

        reports = run_parallel(
            items=events,
            worker=self._process_single_event,
            max_workers=MAX_PARALLEL_WORKERS,
        )

        print(
            f"\n✓ Generated {len(reports)} research reports.\n"
        )

        return reports


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService
    from agents.event_agent import EventAgent

    news_service = NewsService()
    gdelt_service = GDELTService()

    news_articles = news_service.fetch_latest_news()
    gdelt_articles = gdelt_service.fetch_latest_events()

    articles = news_articles + gdelt_articles

    print(f"\nFetched {len(articles)} articles.")

    event_agent = EventAgent()

    events = event_agent.process_articles(articles)

    print(f"\nRelevant Events: {len(events)}")

    if not events:
        raise SystemExit("No relevant events found.")

    research_agent = ResearchAgent()

    reports = research_agent.process_events(events)

    print("\n")
    print("=" * 100)
    print("RESEARCH REPORTS")
    print("=" * 100)

    for i, report in enumerate(reports, start=1):

        print(f"\nResearch Report {i}")
        print("-" * 100)

        print(report)