from typing import List

from models.alternatives_schema import AlternativesReport
from models.risk_schema import RiskReport

from services.alternatives_service import AlternativesService
from chains.alternatives_chain import find_alternatives

from utils.parallel import run_parallel
from config import MAX_PARALLEL_WORKERS


class AlternativesAgent:
    """
    Drug Alternatives Agent

    Responsibilities
    ----------------
    1. Search live web evidence.
    2. Generate therapeutic alternatives.
    3. Process multiple medicines in parallel.
    """

    def __init__(self):

        self.service = AlternativesService()

    # =====================================================
    # Single Medicine Lookup
    # =====================================================

    def lookup(
        self,
        medicine: str,
    ) -> AlternativesReport:

        evidence = self.service.collect(
            medicine
        )

        return find_alternatives(
            medicine,
            evidence,
        )

    # =====================================================
    # Worker
    # =====================================================

    def _process_single_medicine(
        self,
        medicine: str,
    ) -> AlternativesReport | None:

        try:

            print(f"\nSearching alternatives for: {medicine}")

            report = self.lookup(
                medicine
            )

            print("✓ Alternatives generated")

            return report

        except Exception as e:

            print(
                f"\nAlternative lookup failed\n"
                f"Medicine : {medicine}\n"
                f"Reason   : {e}\n"
            )

            return None

    # =====================================================
    # Process Risk Reports
    # =====================================================

    def suggest_for_risk_reports(
        self,
        reports: List[RiskReport],
        max_medicines: int = 10,
    ) -> List[AlternativesReport]:

        medicines: List[str] = []

        for report in reports:

            for medicine in report.affected_medicines:

                if medicine not in medicines:

                    medicines.append(
                        medicine
                    )

        medicines = medicines[:max_medicines]

        if not medicines:

            return []

        print(
            f"\nRunning {len(medicines)} medicine lookups "
            f"using up to {MAX_PARALLEL_WORKERS} worker threads...\n"
        )

        results = run_parallel(
            items=medicines,
            worker=self._process_single_medicine,
            max_workers=MAX_PARALLEL_WORKERS,
        )

        print(
            f"\n✓ Generated {len(results)} alternatives reports.\n"
        )

        return results


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    agent = AlternativesAgent()

    report = agent.lookup(
        "Paracetamol"
    )

    print(report)