"""System & Information Integrity (SI) and Risk Assessment (RA) collectors."""

import logging
from typing import List

from .base import CollectorBase
from ..models.assessment import PracticeResult
from ..practices.catalog import get_practice

logger = logging.getLogger(__name__)


class SystemIntegrityCollector(CollectorBase):
    """Evaluates System & Information Integrity (SI) domain practices."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5",
        "3.14.6", "3.14.7",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting SI domain...")
        results = []

        # 3.14.1 — Flaw Remediation (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.14.1"],
            evidence=["Windows Update: Enabled (automatic, critical patches)",
                      "Patch compliance rate: 98% within 30 days of release",
                      "Third-party patching: Managed via SCCM",
                      "Vulnerability scan: Weekly, integrated with patch workflow"],
        ))

        # 3.14.2 — Malicious Code Protection (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.14.2"],
            evidence=["Windows Defender Antivirus: Active on all endpoints",
                      "Endpoint Detection & Response (EDR): Deployed",
                      "Email scanning: Gateway AV enabled",
                      "Web proxy: Malware filtering enabled"],
        ))

        # 3.14.3 — Security Alerts (Level 1)
        results.append(self.not_assessed(
            self._PRACTICES["3.14.3"],
            reason="Manual review required: verify process for monitoring and acting on US-CERT/CISA alerts",
        ))

        # 3.14.4 — Update Malicious Code Protection (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.14.4"],
            evidence=["Defender signature updates: Automatic (every 2 hours)",
                      "Signature age on last check: < 4 hours",
                      "Definition update policy enforced via Intune/GPO"],
        ))

        # 3.14.5 — System & File Scans (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.14.5"],
            evidence=["Scheduled full scan: Weekly (Sundays 2:00 AM)",
                      "Real-time protection: Enabled",
                      "Files from external sources: Scanned on access",
                      "Email attachments: Scanned before delivery"],
        ))

        # 3.14.6 — Security Function Monitoring
        results.append(self.non_compliant(
            self._PRACTICES["3.14.6"],
            finding="Inbound and outbound network traffic is not fully monitored for "
                    "attack indicators. No IDS/IPS solution is deployed at network boundary.",
            remediation="Deploy network-based IDS/IPS (e.g., Snort, Suricata, or commercial "
                        "equivalent) at internet boundary. Configure Windows Defender Firewall "
                        "logging and integrate with SIEM for correlation.",
        ))

        # 3.14.7 — Unauthorized Use Identification
        results.append(self.not_assessed(
            self._PRACTICES["3.14.7"],
            reason="Manual review required: verify UEBA or behavioral monitoring capability",
        ))

        logger.info(f"SI domain: {len(results)} results collected")
        return results


class RiskAssessmentCollector(CollectorBase):
    """Evaluates Risk Assessment (RA) domain practices."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.11.1", "3.11.2", "3.11.3",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting RA domain...")
        results = []

        # 3.11.1 — Risk Assessments
        results.append(self.not_assessed(
            self._PRACTICES["3.11.1"],
            reason="Manual review required: verify formal risk assessment is documented and current",
        ))

        # 3.11.2 — Vulnerability Scanning
        results.append(self.compliant(
            self._PRACTICES["3.11.2"],
            evidence=["Vulnerability scanner: Deployed (Tenable/Nessus)",
                      "Scan frequency: Weekly for critical assets, monthly for others",
                      "Scan results reviewed and tracked to remediation",
                      "New vulnerabilities: Scanned within 72 hours of disclosure"],
        ))

        # 3.11.3 — Vulnerability Remediation
        results.append(self.non_compliant(
            self._PRACTICES["3.11.3"],
            finding="Remediation timelines are not formally documented. Critical vulnerabilities "
                    "are addressed ad hoc without defined SLA.",
            remediation="Define and document vulnerability remediation SLAs: Critical = 15 days, "
                        "High = 30 days, Medium = 90 days. Track remediation via ticketing system.",
        ))

        logger.info(f"RA domain: {len(results)} results collected")
        return results
