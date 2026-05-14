"""CMMC 2.0 compliance scoring.

Implements:
  - Level 1 / Level 2 percentage scores
  - SPRS score (-203 to 110) per DoD Assessment Methodology
  - Per-domain scores
  - Achieved CMMC level determination
"""

from typing import Dict, Tuple
from ..models.assessment import CMMCAssessment, PracticeStatus
from ..practices.catalog import (
    get_practice, LEVEL1_PRACTICES, LEVEL2_PRACTICES,
    get_by_domain, DOMAINS, MAX_SPRS_SCORE,
)


class CMMCScorer:
    """Calculates CMMC 2.0 compliance scores from a CMMCAssessment."""

    # SPRS starts at 110; we deduct the practice's sprs_weight for each
    # non-compliant practice.  Practices that are NOT_ASSESSED are counted
    # as non-compliant for conservative scoring (DoD methodology intent).
    SPRS_MAX = 110

    @classmethod
    def calculate_sprs_score(cls, assessment: CMMCAssessment) -> int:
        """Return the SPRS self-assessment score (range: -203 to 110).

        Non-compliant and not-assessed practices both deduct from 110.
        Compliant and not-applicable practices do not deduct.
        """
        deductions = 0
        for result in assessment.get_level2_results():
            if result.status in (PracticeStatus.NON_COMPLIANT, PracticeStatus.NOT_ASSESSED):
                practice = get_practice(result.nist_id)
                if practice:
                    deductions += practice.sprs_weight
        return cls.SPRS_MAX - deductions

    @classmethod
    def calculate_level1_score(cls, assessment: CMMCAssessment) -> Tuple[int, int, float]:
        """Return (compliant_count, total_count, percentage) for Level 1 practices."""
        l1_ids = {p.nist_id for p in LEVEL1_PRACTICES}
        l1_results = [r for r in assessment.results.values() if r.nist_id in l1_ids]
        if not l1_results:
            return 0, len(LEVEL1_PRACTICES), 0.0
        compliant = sum(
            1 for r in l1_results if r.status == PracticeStatus.COMPLIANT
        )
        return compliant, len(l1_results), round(compliant / len(l1_results) * 100, 1)

    @classmethod
    def calculate_level2_score(cls, assessment: CMMCAssessment) -> Tuple[int, int, float]:
        """Return (compliant_count, total_count, percentage) for all Level 2 practices."""
        l2_results = assessment.get_level2_results()
        if not l2_results:
            return 0, len(LEVEL2_PRACTICES), 0.0
        compliant = sum(
            1 for r in l2_results if r.status == PracticeStatus.COMPLIANT
        )
        return compliant, len(l2_results), round(compliant / len(l2_results) * 100, 1)

    @classmethod
    def calculate_domain_scores(cls, assessment: CMMCAssessment) -> Dict[str, Dict]:
        """Return per-domain scores.

        Returns a dict keyed by domain abbreviation, each with:
          compliant, total, percentage, non_compliant_ids
        """
        domain_scores = {}
        for domain in DOMAINS:
            domain_results = assessment.get_domain_results(domain)
            if not domain_results:
                continue
            compliant = sum(1 for r in domain_results if r.status == PracticeStatus.COMPLIANT)
            non_compliant_ids = [
                r.cmmc_id for r in domain_results
                if r.status == PracticeStatus.NON_COMPLIANT
            ]
            domain_scores[domain] = {
                "compliant": compliant,
                "total": len(domain_results),
                "percentage": round(compliant / len(domain_results) * 100, 1),
                "non_compliant_ids": non_compliant_ids,
            }
        return domain_scores

    @classmethod
    def determine_achieved_level(cls, assessment: CMMCAssessment) -> int:
        """Return the highest CMMC level fully achieved (0, 1, or 2).

        Level N is achieved when ALL Level N practices (and below) are
        either Compliant or Not Applicable.  Not-assessed practices
        prevent level achievement.
        """
        non_passing = {PracticeStatus.NON_COMPLIANT, PracticeStatus.NOT_ASSESSED}

        l1_ids = {p.nist_id for p in LEVEL1_PRACTICES}
        l1_results = [r for r in assessment.results.values() if r.nist_id in l1_ids]
        l1_achieved = all(r.status not in non_passing for r in l1_results)
        if not l1_achieved:
            return 0

        l2_results = assessment.get_level2_results()
        l2_achieved = all(r.status not in non_passing for r in l2_results)
        return 2 if l2_achieved else 1

    @classmethod
    def full_scorecard(cls, assessment: CMMCAssessment) -> Dict:
        """Return a complete scorecard dict for reporting."""
        l1_compliant, l1_total, l1_pct = cls.calculate_level1_score(assessment)
        l2_compliant, l2_total, l2_pct = cls.calculate_level2_score(assessment)
        sprs = cls.calculate_sprs_score(assessment)
        achieved = cls.determine_achieved_level(assessment)
        domain_scores = cls.calculate_domain_scores(assessment)
        non_compliant = assessment.get_non_compliant()

        return {
            "sprs_score": sprs,
            "sprs_max": cls.SPRS_MAX,
            "achieved_level": achieved,
            "target_level": assessment.target_level,
            "level1": {"compliant": l1_compliant, "total": l1_total, "percentage": l1_pct},
            "level2": {"compliant": l2_compliant, "total": l2_total, "percentage": l2_pct},
            "domains": domain_scores,
            "non_compliant_count": len(non_compliant),
            "non_compliant_ids": [r.cmmc_id for r in non_compliant],
        }
