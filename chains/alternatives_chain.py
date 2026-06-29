from pydantic import ValidationError

from langchain_core.prompts import ChatPromptTemplate

from llm.llm import llm_alternatives

from prompts.alternatives_prompt import ALTERNATIVES_PROMPT

from models.alternatives_schema import AlternativesReport



# ==========================================================
# Prompt
# ==========================================================

alternatives_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            ALTERNATIVES_PROMPT,
        ),
        (
            "human",
            """
Medicine to evaluate:
{medicine_name}

Shortage Context (if any):
{shortage_context}

--------------------------------------------------

Collected Web Evidence

{evidence}

--------------------------------------------------

Using ONLY the evidence above, create a structured
AlternativesReport.
""",
        ),
    ]
)


# ==========================================================
# Structured LLM
#
# Uses the dedicated llm_alternatives instance (separate Groq
# key) so Drug Alternatives calls don't compete with the main
# Event/Research/Risk pipeline for rate-limit headroom.
# ==========================================================

structured_llm = llm_alternatives.with_structured_output(
    AlternativesReport
)


# ==========================================================
# Chain
# ==========================================================

alternatives_chain = (
    alternatives_prompt
    | structured_llm
)


# ==========================================================
# Helper Function
# ==========================================================

def find_alternatives(
    medicine_name: str,
    evidence: str,
    web_sources: list[str] | None = None,
    shortage_context: str | None = None,
) -> AlternativesReport:

    try:

        result = alternatives_chain.invoke(
            {
                "medicine_name": medicine_name,
                "evidence": evidence,
                "shortage_context": shortage_context or "None provided.",
            }
        )

        # ------------------------------------------------
        # Safety checks
        # ------------------------------------------------

        if not result.queried_medicine:
            result.queried_medicine = medicine_name

        if shortage_context and not result.shortage_context:
            result.shortage_context = shortage_context

        if not result.web_sources and web_sources:
            result.web_sources = web_sources

        return result

    except ValidationError as e:

        print(f"\nAlternatives Chain Validation Error:\n{e}\n")

        return AlternativesReport(
            queried_medicine=medicine_name,
            recognized=False,
            therapeutic_class=None,
            alternatives=[],
            shortage_context=shortage_context,
            web_sources=web_sources or [],
            confidence=0.0,
        )

    except Exception as e:

        print(f"\nAlternatives Chain Error:\n{e}\n")

        return AlternativesReport(
            queried_medicine=medicine_name,
            recognized=False,
            therapeutic_class=None,
            alternatives=[],
            shortage_context=shortage_context,
            web_sources=web_sources or [],
            confidence=0.0,
        )


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    from services.alternatives_service import AlternativesService

    service = AlternativesService()

    medicine = "Amoxicillin"

    evidence = service.collect(medicine)

    report = find_alternatives(
        medicine_name=medicine,
        evidence=evidence,
    )

    print("\n")
    print("=" * 80)
    print("ALTERNATIVES REPORT")
    print("=" * 80)

    print(f"Queried Medicine   : {report.queried_medicine}")
    print(f"Recognized         : {report.recognized}")
    print(f"Therapeutic Class  : {report.therapeutic_class}")
    print(f"Confidence         : {report.confidence}")

    print("\nAlternatives")
    for alt in report.alternatives:
        print(f"\n• {alt.name} ({alt.drug_class})")
        print(f"  Notes   : {alt.similarity_notes}")
        print(f"  Caution : {alt.caution}")

    print("\nWeb Sources")
    for s in report.web_sources:
        print(f"- {s}")

    print(f"\nDisclaimer: {report.disclaimer}")