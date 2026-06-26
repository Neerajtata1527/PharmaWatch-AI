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

        return event_chain.invoke(
            {
                "title": article.title,

                "description": (article.description or "")[:500],

                "content": (article.content or "")[:1500],

                "source": article.source,

                "published_at": article.published_at,
            }
        )

    except Exception as e:

        print(f"\nEvent Chain Error:\n{e}\n")

        return EventReport(
            relevant=False,
            event_type="Other",
            headline=article.title,
            summary="Failed to classify article.",
            location=None,
            cause=None,
            source=article.source,
            article_url=article.url,
            published_at=article.published_at,
        )