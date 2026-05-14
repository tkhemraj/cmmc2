"""Base collector class for CMMC 2.0 domain assessors."""

from abc import ABC, abstractmethod
from typing import List
import logging

from ..models.assessment import PracticeResult, PracticeStatus
from ..practices.catalog import Practice

logger = logging.getLogger(__name__)


class CollectorBase(ABC):
    """Abstract base for all CMMC 2.0 domain collectors.

    Each subclass handles one or more CMMC domains and returns a list of
    PracticeResult objects — one per practice it evaluates.
    """

    @abstractmethod
    def collect(self) -> List[PracticeResult]:
        """Evaluate practices in this domain and return results."""
        pass

    # ------------------------------------------------------------------
    # Helpers for building consistent results
    # ------------------------------------------------------------------

    @staticmethod
    def compliant(practice: Practice, evidence: List[str], notes: str = "") -> PracticeResult:
        return PracticeResult(
            nist_id=practice.nist_id,
            cmmc_id=practice.cmmc_id,
            domain=practice.domain,
            level=practice.level,
            status=PracticeStatus.COMPLIANT,
            evidence=evidence,
            notes=notes,
        )

    @staticmethod
    def non_compliant(
        practice: Practice,
        finding: str,
        remediation: str,
        evidence: List[str] = None,
    ) -> PracticeResult:
        return PracticeResult(
            nist_id=practice.nist_id,
            cmmc_id=practice.cmmc_id,
            domain=practice.domain,
            level=practice.level,
            status=PracticeStatus.NON_COMPLIANT,
            evidence=evidence or [],
            finding=finding,
            remediation=remediation,
        )

    @staticmethod
    def not_assessed(practice: Practice, reason: str = "Manual review required") -> PracticeResult:
        return PracticeResult(
            nist_id=practice.nist_id,
            cmmc_id=practice.cmmc_id,
            domain=practice.domain,
            level=practice.level,
            status=PracticeStatus.NOT_ASSESSED,
            notes=reason,
        )
