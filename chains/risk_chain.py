from pydantic import ValidationError

from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm

from prompts.risk_prompt import RISK_ASSESSMENT_PROMPT

from models.research_schema import ResearchReport
from models.risk_schema import RiskReport



# ==========================================================
# Prompt
# ==========================================================

risk_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            RISK_ASSESSMENT_PROMPT,
        ),
        (
            "human",
            """
Research Report

Headline:
{headline}

Event Type:
{event_type}

Location:
{location}

Research Summary:
{research_summary}

Affected Regions:
{affected_regions}

Affected Countries:
{affected_countries}

Affected Trade Routes:
{affected_trade_routes}

Affected Ports:
{affected_ports}

Affected Manufacturers:
{affected_manufacturers}

Affected API Suppliers:
{affected_api_suppliers}

Affected Raw Materials:
{affected_raw_materials}

Evidence:
{evidence}

Confidence:
{confidence}

--------------------------------------------------

Using ONLY this research,
generate the final RiskReport.
""",
        ),
    ]
)


# ==========================================================
# Structured LLM
# ==========================================================

structured_llm = llm.with_structured_output(
    RiskReport
)


# ==========================================================
# Chain
# ==========================================================

risk_chain = (
    risk_prompt
    | structured_llm
)


# ==========================================================
# Helper Function
# ==========================================================

def assess_risk(
    report: ResearchReport,
) -> RiskReport:

    try:

        return risk_chain.invoke(
            {
                "headline": report.headline,
                "event_type": report.event_type,
                "location": report.location,
                "research_summary": report.research_summary,
                "affected_regions": report.affected_regions,
                "affected_countries": report.affected_countries,
                "affected_trade_routes": report.affected_trade_routes,
                "affected_ports": report.affected_ports,
                "affected_manufacturers": report.affected_manufacturers,
                "affected_api_suppliers": report.affected_api_suppliers,
                "affected_raw_materials": report.affected_raw_materials,
                "evidence": report.evidence,
                "confidence": report.confidence,
            }
        )

    except ValidationError:

        return RiskReport(
            headline=report.headline,
            event_type=report.event_type,
            location=report.location,

            overall_risk="LOW",
            risk_score=0,
            confidence=0.0,

            estimated_shortage_time="Unknown",

            affected_medicines=[],
            affected_apis=[],
            affected_regions=[],

            recommended_actions=[],
            recommended_imports=[],
            alternative_suppliers=[],

            hospital_alert="LOW",
            government_actions=[],

            reasoning="Unable to generate risk assessment."
        )


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

    news_service = NewsService()
    gdelt_service = GDELTService()

    articles = (
        news_service.fetch_latest_news()
        +
        gdelt_service.fetch_latest_events()
    )

    # ------------------------------------------------------
    # Event Detection
    # ------------------------------------------------------

    event_agent = EventAgent()

    events = event_agent.process_articles(
        articles
    )

    if not events:

        raise SystemExit("No relevant events found.")

    # ------------------------------------------------------
    # Research
    # ------------------------------------------------------

    research_agent = ResearchAgent()

    research_reports = research_agent.process_events(
        events
    )

    if not research_reports:

        raise SystemExit("No research reports generated.")

    # ------------------------------------------------------
    # Risk Assessment
    # ------------------------------------------------------

    risk_report = assess_risk(
        research_reports[0]
    )

    print("\n")
    print("=" * 100)
    print("RISK REPORT")
    print("=" * 100)

    print(risk_report)