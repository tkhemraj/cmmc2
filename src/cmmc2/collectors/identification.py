"""Identification & Authentication (IA) collector."""

import logging
from typing import List

from .base import CollectorBase
from ..models.assessment import PracticeResult
from ..practices.catalog import get_practice

logger = logging.getLogger(__name__)


class IdentificationCollector(CollectorBase):
    """Evaluates Identification & Authentication (IA) domain practices."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.5.1", "3.5.2", "3.5.3", "3.5.4", "3.5.5",
        "3.5.6", "3.5.7", "3.5.8", "3.5.9", "3.5.10", "3.5.11",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting IA domain...")
        results = []

        # 3.5.1 — Identify System Users (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.5.1"],
            evidence=["All accounts are named individual accounts",
                      "Shared/generic accounts: None active",
                      "Service accounts: Identified and documented",
                      "Device accounts: Managed via AD computer objects"],
        ))

        # 3.5.2 — Authenticate System Users (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.5.2"],
            evidence=["Windows authentication required for all logons",
                      "Kerberos authentication enforced on domain",
                      "Local account authentication restricted to emergency access"],
        ))

        # 3.5.3 — Multi-Factor Authentication
        # Demo: MFA not enabled for non-privileged accounts
        results.append(self.non_compliant(
            self._PRACTICES["3.5.3"],
            finding="MFA is enforced for privileged accounts but NOT for all network-access "
                    "non-privileged accounts. Remote access users without admin rights can "
                    "authenticate with password only.",
            remediation="Enforce MFA for all accounts accessing the network remotely via "
                        "Azure AD Conditional Access, Duo, or equivalent. Minimum: hardware "
                        "token or authenticator app. Target: all network-access accounts.",
        ))

        # 3.5.4 — Replay-Resistant Authentication
        results.append(self.compliant(
            self._PRACTICES["3.5.4"],
            evidence=["Kerberos: In use (replay-resistant by design)",
                      "NTLMv1: Disabled via Security Policy",
                      "NTLMv2: Enforced where NTLM is required"],
        ))

        # 3.5.5 — Identifier Reuse
        results.append(self.compliant(
            self._PRACTICES["3.5.5"],
            evidence=["SID-based identity prevents reuse of usernames for different users",
                      "Account naming convention enforces unique identifiers",
                      "Terminated account SIDs never reassigned"],
        ))

        # 3.5.6 — Identifier Handling (inactive accounts)
        results.append(self.non_compliant(
            self._PRACTICES["3.5.6"],
            finding="No automated process to disable accounts after inactivity period. "
                    "3 accounts identified with last logon > 90 days still active.",
            remediation="Implement an automated process (PowerShell/Entra ID) to disable "
                        "accounts inactive for more than 90 days. Review and disable the "
                        "3 identified stale accounts immediately.",
            evidence=["Stale account audit performed: 3 accounts found inactive > 90 days"],
        ))

        # 3.5.7 — Password Complexity
        results.append(self.compliant(
            self._PRACTICES["3.5.7"],
            evidence=["Minimum password length: 14 characters",
                      "Complexity requirements: Enabled (upper, lower, digit, symbol)",
                      "Password change enforced: 90-day maximum age",
                      "Fine-grained password policy: Applied to admin accounts (20+ chars)"],
        ))

        # 3.5.8 — Password Reuse
        results.append(self.compliant(
            self._PRACTICES["3.5.8"],
            evidence=["Password history: 24 passwords remembered",
                      "Minimum password age: 1 day (prevents rapid cycling)"],
        ))

        # 3.5.9 — Temporary Passwords
        results.append(self.compliant(
            self._PRACTICES["3.5.9"],
            evidence=["Temporary passwords expire on first logon (AD setting)",
                      "IT uses 'User must change password at next logon' for all resets"],
        ))

        # 3.5.10 — Cryptographically Protected Passwords
        results.append(self.compliant(
            self._PRACTICES["3.5.10"],
            evidence=["LM hash storage: Disabled",
                      "Reversible encryption for passwords: Disabled",
                      "Credential Guard: Enabled on supported hardware"],
        ))

        # 3.5.11 — Obscure Feedback
        results.append(self.compliant(
            self._PRACTICES["3.5.11"],
            evidence=["Password input fields: Masked (OS default)",
                      "Authentication failure messages: Generic (no enumeration)"],
        ))

        logger.info(f"IA domain: {len(results)} results collected")
        return results
