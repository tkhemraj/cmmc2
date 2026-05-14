"""Access Control (AC) domain collector."""

import logging
from typing import List

from .base import CollectorBase
from ..models.assessment import PracticeResult
from ..practices.catalog import get_practice

logger = logging.getLogger(__name__)

_AC = {nist_id: get_practice(nist_id) for nist_id in [
    "3.1.1", "3.1.2", "3.1.3", "3.1.4", "3.1.5", "3.1.6",
    "3.1.7", "3.1.8", "3.1.9", "3.1.10", "3.1.11", "3.1.12",
    "3.1.13", "3.1.14", "3.1.15", "3.1.16", "3.1.17", "3.1.18",
    "3.1.19", "3.1.20", "3.1.21", "3.1.22",
]}


class AccessControlCollector(CollectorBase):
    """Evaluates Access Control (AC) domain practices.

    Automated checks cover account management, session policies, and
    privilege controls using demo data. Non-automatable practices
    (physical controls, documented procedures) are marked NOT_ASSESSED.
    """

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting AC domain...")
        results = []

        # AC.L1-3.1.1 — Authorized Access Control
        # Demo: guest account disabled, named accounts only
        results.append(self.compliant(
            _AC["3.1.1"],
            evidence=["Guest account: Disabled", "Built-in Administrator: Disabled",
                      "All active accounts are named user accounts"],
        ))

        # AC.L1-3.1.2 — Transaction & Function Control
        # Demo: standard users have no admin rights
        results.append(self.compliant(
            _AC["3.1.2"],
            evidence=["Standard user roles enforced via Group Policy",
                      "Admin actions require elevation (UAC enabled)"],
        ))

        # AC.L1-3.1.20 — External Connections
        results.append(self.not_assessed(
            _AC["3.1.20"],
            reason="Manual review required: document and verify all external system connections",
        ))

        # AC.L1-3.1.22 — Control Public Information
        results.append(self.not_assessed(
            _AC["3.1.22"],
            reason="Manual review required: verify CUI is not posted on public-facing systems",
        ))

        # AC.L2-3.1.3 — CUI Flow Control
        results.append(self.not_assessed(
            _AC["3.1.3"],
            reason="Manual review required: verify data flow enforcement mechanisms",
        ))

        # AC.L2-3.1.4 — Separation of Duties
        results.append(self.not_assessed(
            _AC["3.1.4"],
            reason="Manual review required: document separation of duties assignments",
        ))

        # AC.L2-3.1.5 — Least Privilege
        # Demo: privileged accounts inventoried, limited
        results.append(self.compliant(
            _AC["3.1.5"],
            evidence=["Domain Admins group: 2 members (reviewed quarterly)",
                      "Service accounts use minimum required permissions",
                      "No users with unnecessary admin rights detected"],
        ))

        # AC.L2-3.1.6 — Non-Privileged Account Use
        # Demo: admins have separate admin + standard accounts
        results.append(self.compliant(
            _AC["3.1.6"],
            evidence=["Admin personnel have dedicated privileged accounts",
                      "Day-to-day work performed under standard user accounts"],
        ))

        # AC.L2-3.1.7 — Privileged Function Restriction
        # Demo: UAC configured, audit logging of privileged functions
        results.append(self.compliant(
            _AC["3.1.7"],
            evidence=["UAC: Enabled (prompt for all users)",
                      "Privileged function execution logged via Audit Policy"],
        ))

        # AC.L2-3.1.8 — Unsuccessful Logon Attempts
        # Demo: account lockout threshold configured
        results.append(self.compliant(
            _AC["3.1.8"],
            evidence=["Account Lockout Threshold: 5 attempts",
                      "Account Lockout Duration: 30 minutes",
                      "Reset Counter After: 30 minutes"],
        ))

        # AC.L2-3.1.9 — Privacy & Security Notices
        results.append(self.not_assessed(
            _AC["3.1.9"],
            reason="Manual review required: verify logon banner text meets CUI requirements",
        ))

        # AC.L2-3.1.10 — Session Lock
        # Demo: screensaver with password configured via GPO
        results.append(self.compliant(
            _AC["3.1.10"],
            evidence=["Interactive Session Timeout: 15 minutes (Group Policy)",
                      "Screen saver password required: Enabled",
                      "Pattern-hiding screensaver deployed"],
        ))

        # AC.L2-3.1.11 — Session Termination
        # Demo: session timeout policy enforced
        results.append(self.compliant(
            _AC["3.1.11"],
            evidence=["RDP session time limit: 4 hours",
                      "Idle session disconnect: Enabled (15 minutes)"],
        ))

        # AC.L2-3.1.12 — Remote Access Control
        results.append(self.not_assessed(
            _AC["3.1.12"],
            reason="Manual review required: verify remote access monitoring solution",
        ))

        # AC.L2-3.1.13 — Remote Access Confidentiality
        # Demo: VPN with TLS 1.2+ enforced
        results.append(self.compliant(
            _AC["3.1.13"],
            evidence=["VPN: TLS 1.2 minimum enforced",
                      "SSL/TLS weak cipher suites disabled",
                      "Remote Desktop: NLA required"],
        ))

        # AC.L2-3.1.14 — Remote Access Routing
        results.append(self.not_assessed(
            _AC["3.1.14"],
            reason="Manual review required: verify all remote access routes through managed control point",
        ))

        # AC.L2-3.1.15 — Privileged Remote Access
        results.append(self.not_assessed(
            _AC["3.1.15"],
            reason="Manual review required: document operational need for privileged remote access",
        ))

        # AC.L2-3.1.16 — Wireless Access Authorization
        # Demo: 802.1X authentication configured
        results.append(self.compliant(
            _AC["3.1.16"],
            evidence=["WiFi requires 802.1X authentication",
                      "Wireless access restricted to domain-joined devices"],
        ))

        # AC.L2-3.1.17 — Wireless Access Protection
        # Demo: WPA3/WPA2-Enterprise deployed
        results.append(self.compliant(
            _AC["3.1.17"],
            evidence=["Wireless encryption: WPA2-Enterprise (AES)",
                      "802.1X with PEAP-MSCHAPv2 enforced",
                      "Pre-shared key networks prohibited"],
        ))

        # AC.L2-3.1.18 — Mobile Device Control
        results.append(self.not_assessed(
            _AC["3.1.18"],
            reason="Manual review required: verify MDM enrollment and policies for mobile devices",
        ))

        # AC.L2-3.1.19 — Encrypt CUI on Mobile
        # Demo: BitLocker/device encryption enforced
        results.append(self.compliant(
            _AC["3.1.19"],
            evidence=["BitLocker: Enabled on all mobile devices (MDM policy)",
                      "Device encryption enforced via Conditional Access"],
        ))

        # AC.L2-3.1.21 — Portable Storage Use
        # Demo: USB storage restricted via Group Policy
        results.append(self.compliant(
            _AC["3.1.21"],
            evidence=["Removable storage: Restricted via Group Policy",
                      "USB mass storage class: Disabled on endpoints"],
        ))

        logger.info(f"AC domain: {len(results)} results collected")
        return results
