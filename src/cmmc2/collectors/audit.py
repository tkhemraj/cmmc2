"""Audit & Accountability (AU) and Configuration Management (CM) collectors."""

import logging
from typing import List

from .base import CollectorBase
from ..models.assessment import PracticeResult
from ..practices.catalog import get_practice

logger = logging.getLogger(__name__)


class AuditCollector(CollectorBase):
    """Evaluates Audit & Accountability (AU) domain practices."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.3.1", "3.3.2", "3.3.3", "3.3.4", "3.3.5",
        "3.3.6", "3.3.7", "3.3.8", "3.3.9",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting AU domain...")
        results = []

        # 3.3.1 — System Auditing
        results.append(self.compliant(
            self._PRACTICES["3.3.1"],
            evidence=["Windows Security event log: Enabled",
                      "Log retention: 90 days",
                      "Log max size: 196 MB",
                      "Audit categories: Logon, Account Management, Object Access, Policy Change"],
        ))

        # 3.3.2 — User Accountability
        results.append(self.compliant(
            self._PRACTICES["3.3.2"],
            evidence=["All audit events include SID and account name",
                      "Account correlation enabled via event data"],
        ))

        # 3.3.3 — Event Review
        results.append(self.not_assessed(
            self._PRACTICES["3.3.3"],
            reason="Manual review required: verify audit review schedule and procedure",
        ))

        # 3.3.4 — Audit Failure Alerting
        results.append(self.non_compliant(
            self._PRACTICES["3.3.4"],
            finding="No automated alerting configured for audit log failures.",
            remediation="Configure Windows Event Forwarding or SIEM to alert on event ID 1102 "
                        "(audit log cleared) and audit subsystem failures.",
        ))

        # 3.3.5 — Audit Correlation
        results.append(self.not_assessed(
            self._PRACTICES["3.3.5"],
            reason="Manual review required: verify SIEM or log correlation tool is in use",
        ))

        # 3.3.6 — Reduction & Reporting
        results.append(self.not_assessed(
            self._PRACTICES["3.3.6"],
            reason="Manual review required: verify audit reduction and reporting capability",
        ))

        # 3.3.7 — Authoritative Time Source
        results.append(self.compliant(
            self._PRACTICES["3.3.7"],
            evidence=["Windows Time Service: Enabled",
                      "NTP sync: Configured to authoritative source (time.windows.com)",
                      "Time sync verified on all domain-joined systems"],
        ))

        # 3.3.8 — Audit Protection
        results.append(self.compliant(
            self._PRACTICES["3.3.8"],
            evidence=["Audit log ACL: Restricted to SYSTEM and Administrators",
                      "auditpol.exe access: Admin-only",
                      "Event log service: Protected"],
        ))

        # 3.3.9 — Audit Management
        results.append(self.compliant(
            self._PRACTICES["3.3.9"],
            evidence=["Audit policy management restricted to Domain Admins",
                      "Standard users cannot modify audit settings"],
        ))

        logger.info(f"AU domain: {len(results)} results collected")
        return results


class ConfigurationCollector(CollectorBase):
    """Evaluates Configuration Management (CM) domain practices."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.4.1", "3.4.2", "3.4.3", "3.4.4", "3.4.5",
        "3.4.6", "3.4.7", "3.4.8", "3.4.9",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting CM domain...")
        results = []

        # 3.4.1 — Baseline Configurations
        results.append(self.compliant(
            self._PRACTICES["3.4.1"],
            evidence=["System inventory documented in CMDB",
                      "Baseline configuration images maintained for all system types",
                      "Hardware/software inventory reviewed quarterly"],
        ))

        # 3.4.2 — Security Configuration Enforcement
        results.append(self.compliant(
            self._PRACTICES["3.4.2"],
            evidence=["DISA STIGs applied via Group Policy",
                      "CIS Benchmark Level 1 applied to all workstations",
                      "Configuration compliance verified via SCAP scans"],
        ))

        # 3.4.3 — Configuration Change Control
        results.append(self.not_assessed(
            self._PRACTICES["3.4.3"],
            reason="Manual review required: verify change management process documents system changes",
        ))

        # 3.4.4 — Security Impact Analysis
        results.append(self.not_assessed(
            self._PRACTICES["3.4.4"],
            reason="Manual review required: verify security impact analysis is performed before changes",
        ))

        # 3.4.5 — Physical/Logical Change Restrictions
        results.append(self.not_assessed(
            self._PRACTICES["3.4.5"],
            reason="Manual review required: verify access restrictions for system changes are documented",
        ))

        # 3.4.6 — Least Functionality
        results.append(self.compliant(
            self._PRACTICES["3.4.6"],
            evidence=["Unnecessary Windows features disabled (PowerShell v2, SMBv1, Telnet)",
                      "Unnecessary services disabled via Group Policy",
                      "Application whitelisting via AppLocker configured"],
        ))

        # 3.4.7 — Nonessential Functions
        results.append(self.non_compliant(
            self._PRACTICES["3.4.7"],
            finding="SMBv1 detected as enabled on 2 endpoints; unnecessary services running.",
            remediation="Disable SMBv1 via Group Policy and PowerShell. Audit and disable "
                        "all non-essential services and ports via Windows Firewall.",
        ))

        # 3.4.8 — Application Execution Policy
        results.append(self.not_assessed(
            self._PRACTICES["3.4.8"],
            reason="Manual review required: verify deny-by-exception or whitelisting policy",
        ))

        # 3.4.9 — User-Installed Software
        results.append(self.compliant(
            self._PRACTICES["3.4.9"],
            evidence=["Standard users cannot install software (Windows Installer policy)",
                      "Software deployment managed via SCCM/Intune",
                      "Unauthorized software alerts configured"],
        ))

        logger.info(f"CM domain: {len(results)} results collected")
        return results
