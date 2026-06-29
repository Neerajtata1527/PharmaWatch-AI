from tavily import TavilyClient

from config import TAVILY_API_KEY
from models.event_schema import EventReport


class ResearchService:
    """
    Collects pharmaceutical supply-chain evidence
    for a given EventReport.
    """

    MIN_SCORE = 0.30
    MAX_RESULTS = 10
    MAX_CONTENT_LENGTH = 800

    def __init__(self):

        self.client = TavilyClient(
            api_key=TAVILY_API_KEY
        )

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def collect(
        self,
        event: EventReport,
    ) -> str:
        """
        Complete retrieval pipeline.

        Event
            ↓
        Tavily Search
            ↓
        Filter
            ↓
        Sort
            ↓
        Format

        Returns formatted evidence ready for the LLM.
        """

        results = self.search(event)

        return self.format_results(results)

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        event: EventReport,
    ) -> list[dict]:

        query = self._build_query(event)

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=self.MAX_RESULTS,
            include_answer=False,
        )

        results = response.get("results", [])

        return self._filter_results(results)

    # ==========================================================
    # QUERY BUILDER
    # ==========================================================
    def _build_query(
    self,
    event: EventReport,
) -> str:
        headline = (event.headline or "").strip()
        location = (event.location or "").strip()
        event_type = event.event_type or ""
        event_keywords = {

        "Shipping Disruption":
            "shipping ports logistics API imports",

        "Natural Disaster":
            "pharmaceutical factories manufacturing logistics",

        "Trade Restriction":
            "drug exports API imports sanctions",

        "Manufacturing Disruption":
            "API manufacturers pharmaceutical production",

        "Public Health Event":
            "medicine demand drug manufacturing",

        "Infrastructure Failure":
            "ports airports logistics transport",

        "Regulatory Action":
            "FDA WHO pharmaceutical regulation",

        "Economic Disruption":
            "fuel prices pharmaceutical supply chain",

        "Geopolitical Conflict":
            "Strait of Hormuz sanctions shipping API supply chain",

    }
        keywords = event_keywords.get(
        event_type,
        "pharmaceutical supply chain",
    )
        query_parts = [
        headline,
        location,
        keywords,
        "medicine shortages",
    ]
        query = " ".join(
        part for part in query_parts if part
    )
        return query[:350]
    # ==========================================================
    # FILTER RESULTS
    # ==========================================================

    def _filter_results(
        self,
        results: list[dict],
    ) -> list[dict]:

        filtered = []

        for result in results:

            score = result.get("score", 0)

            if score < self.MIN_SCORE:
                continue

            filtered.append(
                {
                    "title": result.get("title", ""),

                    "url": result.get("url", ""),

                    "score": score,

                    "content": result.get(
                        "content",
                        ""
                    )[: self.MAX_CONTENT_LENGTH],
                }
            )

        filtered.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return filtered

    # ==========================================================
    # FORMAT RESULTS
    # ==========================================================

    def format_results(
        self,
        results: list[dict],
    ) -> str:

        if not results:

            return (
                "No reliable pharmaceutical "
                "evidence found."
            )

        formatted = []

        for i, result in enumerate(
            results[:5],
            start=1,
        ):

            formatted.append(
                f"""
================ SOURCE {i} ================

Title:
{result['title']}

Content:
{result['content']}

Source:
{result['url']}

Relevance Score:
{result['score']:.2f}
"""
            )

        return "\n".join(formatted)