"""Main CMMC 2.0 assessment orchestrator."""

import logging
from typing import Dict, List, Optional

from .collectors import ALL_COLLECTORS
from .models.assessment import CMMCAssessment, PracticeResult
from .scoring.scorer import CMMCScorer
from .exporters import create_exporter

logger = logging.getLogger(__name__)


class CMMCAssessor:
    """Orchestrates a full CMMC 2.0 compliance assessment.

    Usage:
        assessor = CMMCAssessor("Acme Corp", target_level=2)
        assessment = assessor.assess()
        assessor.export("html", "report.html")
        assessor.export("poam", "poam.html")
    """

    def __init__(
        self,
        customer: str,
        target_level: int = 2,
        assessor_name: str = "Self-Assessment",
    ):
        self.customer = customer
        self.target_level = target_level
        self.assessor_name = assessor_name
        self._assessment: Optional[CMMCAssessment] = None
        self._scorecard: Optional[Dict] = None

    def assess(self) -> CMMCAssessment:
        """Run all domain collectors and build the assessment."""
        logger.info(f"Starting CMMC 2.0 Level {self.target_level} assessment for {self.customer}")

        assessment = CMMCAssessment(
            customer=self.customer,
            target_level=self.target_level,
            assessor=self.assessor_name,
        )

        all_results: List[PracticeResult] = []
        for collector_class in ALL_COLLECTORS:
            collector = collector_class()
            try:
                results = collector.collect()
                all_results.extend(results)
            except Exception as e:
                logger.error(f"{collector_class.__name__} failed: {e}")

        assessment.results = {r.nist_id: r for r in all_results}
        self._assessment = assessment
        self._scorecard = CMMCScorer.full_scorecard(assessment)

        logger.info(
            f"Assessment complete — SPRS: {self._scorecard['sprs_score']}, "
            f"Achieved Level: {self._scorecard['achieved_level']}, "
            f"Non-compliant: {self._scorecard['non_compliant_count']}"
        )
        return assessment

    @property
    def scorecard(self) -> Optional[Dict]:
        """Return the scorecard from the last assess() call."""
        return self._scorecard

    def export(self, format_type: str, output_path: str) -> bool:
        """Export the assessment to the given format.

        Args:
            format_type: 'json', 'html', 'poam', or 'poam_csv'
            output_path: File path to write

        Returns:
            True on success, False on failure.
        """
        if self._assessment is None:
            logger.error("No assessment to export — call assess() first")
            return False

        exporter = create_exporter(format_type)
        if not exporter:
            logger.error(f"Unknown export format: {format_type}")
            return False

        return exporter.export(self._assessment, self._scorecard, output_path)

    def print_summary(self) -> None:
        """Print a text summary of the assessment to stdout."""
        if not self._scorecard:
            print("No assessment completed.")
            return

        sc = self._scorecard
        print(f"\n{'=' * 60}")
        print(f"  CMMC 2.0 Assessment — {self.customer}")
        print(f"{'=' * 60}")
        print(f"  SPRS Score:      {sc['sprs_score']:>4}  (max 110)")
        print(f"  Achieved Level:  Level {sc['achieved_level']}  (target: Level {sc['target_level']})")
        print(f"  Level 1:         {sc['level1']['compliant']}/{sc['level1']['total']} "
              f"({sc['level1']['percentage']}%)")
        print(f"  Level 2:         {sc['level2']['compliant']}/{sc['level2']['total']} "
              f"({sc['level2']['percentage']}%)")
        print(f"  Non-Compliant:   {sc['non_compliant_count']} practice(s)")
        print(f"\n  Domain Scores:")
        for domain, ds in sc['domains'].items():
            bar_fill = int(ds['percentage'] / 5)
            bar = '█' * bar_fill + '░' * (20 - bar_fill)
            print(f"    {domain:2s}  [{bar}] {ds['percentage']:5.1f}%  "
                  f"({ds['compliant']}/{ds['total']})")

        if sc['non_compliant_ids']:
            print(f"\n  Non-Compliant Practices:")
            for cmmc_id in sc['non_compliant_ids']:
                print(f"    ✗ {cmmc_id}")
        print(f"{'=' * 60}\n")
