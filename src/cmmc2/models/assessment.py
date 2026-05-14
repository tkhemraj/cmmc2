"""Assessment data models for CMMC 2.0."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class PracticeStatus(str, Enum):
    COMPLIANT = "Compliant"
    NON_COMPLIANT = "Non-Compliant"
    NOT_APPLICABLE = "Not Applicable"
    NOT_ASSESSED = "Not Assessed"


@dataclass
class PracticeResult:
    """Assessment result for a single CMMC 2.0 practice."""

    nist_id: str                      # e.g. "3.1.1"
    cmmc_id: str                      # e.g. "AC.L1-3.1.1"
    domain: str                       # e.g. "AC"
    level: int                        # 1 or 2
    status: PracticeStatus
    evidence: List[str] = field(default_factory=list)
    notes: str = ""
    finding: str = ""                 # specific gap description
    remediation: str = ""             # recommended fix

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nist_id": self.nist_id,
            "cmmc_id": self.cmmc_id,
            "domain": self.domain,
            "level": self.level,
            "status": self.status.value,
            "evidence": self.evidence,
            "notes": self.notes,
            "finding": self.finding,
            "remediation": self.remediation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PracticeResult":
        return cls(
            nist_id=data["nist_id"],
            cmmc_id=data["cmmc_id"],
            domain=data["domain"],
            level=data["level"],
            status=PracticeStatus(data["status"]),
            evidence=data.get("evidence", []),
            notes=data.get("notes", ""),
            finding=data.get("finding", ""),
            remediation=data.get("remediation", ""),
        )


@dataclass
class CMMCAssessment:
    """Complete CMMC 2.0 assessment for an organization."""

    customer: str
    target_level: int                 # 1, 2, or 3
    results: Dict[str, PracticeResult] = field(default_factory=dict)  # keyed by nist_id
    assessment_date: str = field(default_factory=lambda: datetime.now().date().isoformat())
    assessor: str = "Self-Assessment"
    notes: str = ""

    # ------------------------------------------------------------------
    # Convenience filters
    # ------------------------------------------------------------------

    def get_level1_results(self) -> List[PracticeResult]:
        """Return results for Level 1 (basic) practices."""
        return [r for r in self.results.values() if r.level == 1]

    def get_level2_results(self) -> List[PracticeResult]:
        """Return results for all Level 1 + Level 2 practices."""
        return [r for r in self.results.values() if r.level <= 2]

    def get_domain_results(self, domain: str) -> List[PracticeResult]:
        """Return results for a specific domain (e.g. 'AC')."""
        return [r for r in self.results.values() if r.domain == domain]

    def get_non_compliant(self) -> List[PracticeResult]:
        """Return all non-compliant practice results."""
        return [r for r in self.results.values() if r.status == PracticeStatus.NON_COMPLIANT]

    def get_compliant(self) -> List[PracticeResult]:
        return [r for r in self.results.values() if r.status == PracticeStatus.COMPLIANT]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer": self.customer,
            "target_level": self.target_level,
            "assessment_date": self.assessment_date,
            "assessor": self.assessor,
            "notes": self.notes,
            "results": {k: v.to_dict() for k, v in self.results.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CMMCAssessment":
        assessment = cls(
            customer=data["customer"],
            target_level=data["target_level"],
            assessment_date=data.get("assessment_date", ""),
            assessor=data.get("assessor", "Self-Assessment"),
            notes=data.get("notes", ""),
        )
        assessment.results = {
            k: PracticeResult.from_dict(v)
            for k, v in data.get("results", {}).items()
        }
        return assessment
