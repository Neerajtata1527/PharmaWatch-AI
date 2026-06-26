from typing import List

from models.event_schema import EventReport
from models.research_schema import ResearchReport

from services.research_service import ResearchService
from chains.research_chain import research_event


class ResearchAgent:
    """
    Research Intelligence Agent

    Responsibilities
    ----------------
    1. Receive verified EventReports.
    2. Collect supporting evidence from Tavily.
    3. Generate structured ResearchReports.
    4. Return all research reports.
    """

    def __init__(self):

        self.research_service = ResearchService()

    def process_events(
        self,
        events: List[EventReport],
    ) -> List[ResearchReport]:

        reports: List[ResearchReport] = []

        if not events:
            return reports

        total = len(events)

        for index, event in enumerate(events, start=1):

            print("\n" + "=" * 100)
            print(f"[{index}/{total}] Researching Event")
            print("=" * 100)

            print(f"Headline : {event.headline}")
            print(f"Type     : {event.event_type}")
            print(f"Location : {event.location}")
            print()

            try:

                # ----------------------------------------
                # Retrieve supporting evidence
                # ----------------------------------------

                evidence = self.research_service.collect(event)

                print("✓ Evidence collected")

                # ----------------------------------------
                # Generate Research Report
                # ----------------------------------------

                report = research_event(
                    event,
                    evidence,
                )

                reports.append(report)

                print("✓ Research report generated")

            except Exception as e:

                print(
                    f"\nResearch failed:\n"
                    f"{event.headline}\n"
                    f"Reason: {e}\n"
                )

        return reports


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService

    from agents.event_agent import EventAgent

    # ------------------------------------------------------
    # Fetch News
    # ------------------------------------------------------

    news_service = NewsService()
    gdelt_service = GDELTService()

    news_articles = news_service.fetch_latest_news()
    gdelt_articles = gdelt_service.fetch_latest_events()

    articles = news_articles + gdelt_articles

    print(f"\nFetched {len(articles)} articles.")

    # ------------------------------------------------------
    # Event Detection
    # ------------------------------------------------------

    event_agent = EventAgent()

    events = event_agent.process_articles(articles)

    print(f"\nRelevant Events: {len(events)}")

    if not events:
        raise SystemExit("No relevant events found.")

    # ------------------------------------------------------
    # Research Agent
    # ------------------------------------------------------

    research_agent = ResearchAgent()

    reports = research_agent.process_events(events)

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    print("\n")
    print("=" * 100)
    print("RESEARCH REPORTS")
    print("=" * 100)

    for i, report in enumerate(reports, start=1):

        print(f"\nResearch Report {i}")
        print("-" * 100)

        print(report)