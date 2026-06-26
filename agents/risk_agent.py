from typing import List

from models.research_schema import ResearchReport
from models.risk_schema import RiskReport

from chains.risk_chain import assess_risk


class RiskAgent:
    """
    Pharmaceutical Risk Assessment Agent

    Responsibilities
    ----------------
    1. Receive ResearchReports.
    2. Perform pharmaceutical risk assessment.
    3. Generate actionable recommendations.
    4. Return structured RiskReports.
    """

    def process_reports(
        self,
        reports: List[ResearchReport],
    ) -> List[RiskReport]:

        risk_reports: List[RiskReport] = []

        if not reports:
            return risk_reports

        total = len(reports)

        for index, report in enumerate(reports, start=1):

            print("\n" + "=" * 100)
            print(f"[{index}/{total}] Assessing Risk")
            print("=" * 100)

            print(f"Headline : {report.headline}")
            print(f"Event Type : {report.event_type}")
            print()

            try:

                risk_report = assess_risk(report)

                risk_reports.append(risk_report)

                print("✓ Risk assessment completed")

            except Exception as e:

                print(
                    f"\nRisk Assessment Failed\n"
                    f"Headline : {report.headline}\n"
                    f"Reason : {e}\n"
                )

        return risk_reports


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService

    from agents.event_agent import EventAgent
    from agents.research_agent import ResearchAgent

    # ------------------------------------------------------
    # Fetch News
    # ------------------------------------------------------

    print("\nFetching latest news...\n")

    news_service = NewsService()
    gdelt_service = GDELTService()

    news_articles = news_service.fetch_latest_news()
    gdelt_articles = gdelt_service.fetch_latest_events()

    articles = news_articles + gdelt_articles

    print(f"Fetched {len(articles)} articles.\n")

    # ------------------------------------------------------
    # Event Detection
    # ------------------------------------------------------

    event_agent = EventAgent()

    events = event_agent.process_articles(articles)

    print(f"\nRelevant Events : {len(events)}")

    if not events:
        raise SystemExit("No relevant events found.")

    # ------------------------------------------------------
    # Research Agent
    # ------------------------------------------------------

    research_agent = ResearchAgent()

    research_reports = research_agent.process_events(events)

    print(f"\nResearch Reports : {len(research_reports)}")

    if not research_reports:
        raise SystemExit("No research reports generated.")

    # ------------------------------------------------------
    # Risk Agent
    # ------------------------------------------------------

    risk_agent = RiskAgent()

    risk_reports = risk_agent.process_reports(
        research_reports
    )

    # ------------------------------------------------------
    # Display Final Reports
    # ------------------------------------------------------

    print("\n")
    print("=" * 100)
    print("FINAL PHARMACEUTICAL RISK REPORTS")
    print("=" * 100)

    for i, report in enumerate(risk_reports, start=1):

        print(f"\nRisk Report {i}")
        print("-" * 100)

        print(f"Headline              : {report.headline}")
        print(f"Risk Level            : {report.overall_risk}")
        print(f"Risk Score            : {report.risk_score}")
        print(f"Confidence            : {report.confidence}")

        print(f"\nEstimated Shortage    : {report.estimated_shortage_time}")

        print("\nAffected Medicines")
        for med in report.affected_medicines:
            print(f"• {med}")

        print("\nAffected APIs")
        for api in report.affected_apis:
            print(f"• {api}")

        print("\nAffected Regions")
        for region in report.affected_regions:
            print(f"• {region}")

        print("\nRecommended Actions")
        for action in report.recommended_actions:
            print(f"✓ {action}")

        print("\nRecommended Imports")
        for item in report.recommended_imports:
            print(f"✓ {item}")

        print("\nAlternative Suppliers")
        for supplier in report.alternative_suppliers:
            print(f"• {supplier}")

        print(f"\nHospital Alert : {report.hospital_alert}")

        print("\nGovernment Actions")
        for action in report.government_actions:
            print(f"✓ {action}")

        print("\nReasoning")
        print(report.reasoning)

        print("\n" + "=" * 100)