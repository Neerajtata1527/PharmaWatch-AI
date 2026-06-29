from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm

from prompts.event_prompt import EVENT_CLASSIFICATION_PROMPT

from models.raw_article import RawArticle
from models.event_schema import EventReport




# =====================================================
# Prompt Template
# =====================================================

event_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            EVENT_CLASSIFICATION_PROMPT,
        ),
        (
            "human",
            """
Analyze the following news article.

Title:
{title}

Description:
{description}

Content:
{content}

Source:
{source}

Published At:
{published_at}
""",
        ),
    ]
)


# =====================================================
# Structured LLM
# =====================================================

structured_llm = llm.with_structured_output(
    EventReport
)


# =====================================================
# Event Classification Chain
# =====================================================

event_chain = (
    event_prompt
    | structured_llm
)


# =====================================================
# Helper Function
# =====================================================

def classify_article(
    article: RawArticle,
) -> EventReport:
    """
    Classify a single RawArticle into an EventReport.
    """

    try:

        result = event_chain.invoke(
            {
                "title": article.title,
                "description": (article.description or "")[:500],
                "content": (article.content or "")[:1500],
                "source": article.source,
                "published_at": article.published_at,
            }
        )

        # ------------------------------------------------
        # Safety checks
        # ------------------------------------------------

        if isinstance(result.relevant, str):
            result.relevant = (
                result.relevant.strip().lower() == "true"
            )

        if not result.headline:
            result.headline = article.title

        if not result.source:
            result.source = article.source

        if not result.article_url:
            result.article_url = article.url

        if not result.published_at:
            result.published_at = article.published_at

        if not result.summary:
            result.summary = (
                article.description
                or "No summary available."
            )

        return result

    except Exception as e:

        print("=" * 80)
        print("EVENT CHAIN ERROR")
        print("=" * 80)
        print(e)
        print("=" * 80)

        return EventReport(
            relevant=False,
            event_type="Other",
            headline=article.title,
            summary=article.description
            or "Unable to classify article.",
            location=None,
            cause=None,
            source=article.source,
            article_url=article.url,
            published_at=article.published_at,
        )


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    from services.news_service import NewsService
    from services.gdelt_service import GDELTService

    news_service = NewsService()
    gdelt_service = GDELTService()

    news_articles = news_service.fetch_latest_news()
    gdelt_articles = gdelt_service.fetch_latest_events()

    articles = news_articles + gdelt_articles

    print(f"\nFetched {len(articles)} articles.\n")

    if not articles:
        raise SystemExit("No articles found.")

    article = articles[0]

    report = classify_article(article)

    print("\n")
    print("=" * 80)
    print("EVENT REPORT")
    print("=" * 80)
    print(report)
