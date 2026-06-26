from tavily import TavilyClient

from config import TAVILY_API_KEY
from models.event_schema import EventReport


class ResearchService:
    """
    Collects pharmaceutical supply-chain evidence
    for a given EventReport.
    """

    MIN_SCORE = 0.35
    MAX_RESULTS = 8
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

        headline = event.headline or ""
        location = event.location or ""

        match event.event_type:

            case "Shipping Disruption":

                keywords = (
                    "pharma supply chain "
                    "shipping routes "
                    "API imports "
                    "logistics"
                )

            case "Natural Disaster":

                keywords = (
                    "pharma manufacturing "
                    "drug factories "
                    "logistics "
                    "transport"
                )

            case "Trade Restriction":

                keywords = (
                    "drug imports "
                    "medicine exports "
                    "API supply chain "
                    "trade sanctions"
                )

            case "Manufacturing Disruption":

                keywords = (
                    "API manufacturers "
                    "drug production "
                    "factory shutdown"
                )

            case "Public Health Event":

                keywords = (
                    "medicine demand "
                    "drug manufacturing "
                    "healthcare supply chain"
                )

            case "Infrastructure Failure":

                keywords = (
                    "ports "
                    "airports "
                    "transport "
                    "pharma logistics"
                )

            case "Regulatory Action":

                keywords = (
                    "FDA "
                    "WHO "
                    "drug regulation "
                    "pharmaceutical industry"
                )

            case "Economic Disruption":

                keywords = (
                    "pharmaceutical trade "
                    "medicine supply chain "
                    "manufacturing"
                )

            case "Geopolitical Conflict":

                keywords = (
                    "pharmaceutical supply chain "
                    "API imports "
                    "shipping routes "
                    "trade impact"
                )

            case _:

                keywords = "pharmaceutical supply chain"

        return f"{headline} {location} {keywords}"

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
            results,
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