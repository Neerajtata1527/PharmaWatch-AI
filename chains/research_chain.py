from pydantic import ValidationError

from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm

from prompts.research_prompt import RESEARCH_PROMPT

from models.event_schema import EventReport
from models.research_schema import ResearchReport


# ==========================================================
# Prompt
# ==========================================================

research_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            RESEARCH_PROMPT,
        ),
        (
            "human",
            """
Verified Event

Headline:
{headline}

Event Type:
{event_type}

Location:
{location}

Original Summary:
{summary}


--------------------------------------------------

Collected Web Evidence

{evidence}


--------------------------------------------------

Using ONLY the evidence above, create a structured
ResearchReport.
""",
        ),
    ]
)

# ==========================================================
# Structured LLM
# ==========================================================

structured_llm = llm.with_structured_output(
    ResearchReport
)

# ==========================================================
# Chain
# ==========================================================

research_chain = (
    research_prompt
    | structured_llm
)


# ==========================================================
# Helper Function
# ==========================================================

def research_event(
    event: EventReport,
    evidence: str,
) -> ResearchReport:

    try:

        report = research_chain.invoke(
            {
                "headline": event.headline,
                "event_type": event.event_type,
                "location": event.location,
                "summary": event.summary,
                "event": event,
                "evidence": evidence,
            }
        )

        return report

    except ValidationError:

        return ResearchReport(
            event=event,

            summary="Unable to generate research report.",

            affected_regions=[],

            affected_countries=[],

            affected_trade_routes=[],

            affected_ports=[],

            affected_manufacturers=[],

            affected_api_suppliers=[],

            affected_raw_materials=[],

            evidence=[],

            web_sources=[],

            confidence=0.0,
        )


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService

    from agents.event_agent import EventAgent

    from services.research_service import ResearchService

    # ----------------------------
    # Fetch News
    # ----------------------------

    news_service = NewsService()
    gdelt_service = GDELTService()

    articles = (
        news_service.fetch_latest_news()
        +
        gdelt_service.fetch_latest_events()
    )

    # ----------------------------
    # Event Detection
    # ----------------------------

    event_agent = EventAgent()

    events = event_agent.process_articles(
        articles
    )

    if not events:

        raise SystemExit("No events found.")

    # ----------------------------
    # Research
    # ----------------------------

    research_service = ResearchService()

    event = events[0]

    evidence = research_service.collect(
        event
    )

    report = research_event(
        event,
        evidence,
    )

    print("\n")
    print("=" * 80)
    print("RESEARCH REPORT")
    print("=" * 80)

    print(report)