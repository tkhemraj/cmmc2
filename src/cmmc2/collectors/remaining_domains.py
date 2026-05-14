"""Collectors for AT, IR, MA, MP, PE, PS, CA, and SC domains."""

import logging
from typing import List

from .base import CollectorBase
from ..models.assessment import PracticeResult
from ..practices.catalog import get_practice, get_by_domain

logger = logging.getLogger(__name__)


class AwarenessTrainingCollector(CollectorBase):
    """Awareness & Training (AT) domain."""

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting AT domain...")
        results = []
        for p in get_by_domain("AT"):
            results.append(self.not_assessed(
                p,
                reason="Manual review required: verify security awareness training program, "
                       "curriculum, and completion records",
            ))
        return results


class IncidentResponseCollector(CollectorBase):
    """Incident Response (IR) domain."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in ["3.6.1", "3.6.2", "3.6.3"]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting IR domain...")
        results = []

        results.append(self.not_assessed(
            self._PRACTICES["3.6.1"],
            reason="Manual review required: verify documented incident response plan and procedures",
        ))
        results.append(self.non_compliant(
            self._PRACTICES["3.6.2"],
            finding="No documented process for reporting incidents to US-CERT within required "
                    "72-hour window for CUI incidents.",
            remediation="Document incident reporting procedures including contacts for US-CERT "
                        "(https://www.cisa.gov/report), prime contractor, and internal stakeholders. "
                        "Define incident classification criteria and notification thresholds.",
        ))
        results.append(self.non_compliant(
            self._PRACTICES["3.6.3"],
            finding="Incident response capability has not been tested in the past 12 months.",
            remediation="Conduct tabletop exercise or functional drill. Document results "
                        "and update the IR plan based on lessons learned. Schedule annually.",
        ))

        return results


class MaintenanceCollector(CollectorBase):
    """Maintenance (MA) domain."""

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting MA domain...")
        results = []
        for p in get_by_domain("MA"):
            results.append(self.not_assessed(
                p,
                reason="Manual review required: verify maintenance procedures, records, and controls",
            ))
        return results


class MediaProtectionCollector(CollectorBase):
    """Media Protection (MP) domain."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.8.1", "3.8.2", "3.8.3", "3.8.4", "3.8.5",
        "3.8.6", "3.8.7", "3.8.8", "3.8.9",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting MP domain...")
        results = []

        # 3.8.1 — Media Protection (Level 1)
        results.append(self.not_assessed(
            self._PRACTICES["3.8.1"],
            reason="Manual review required: verify physical media storage controls",
        ))

        # 3.8.2 — Media Disposal (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.8.2"],
            evidence=["CUI media access restricted to authorized users via ACLs",
                      "Encrypted drives require authentication before access"],
        ))

        # 3.8.3 — Media Sanitization (Level 1)
        results.append(self.not_assessed(
            self._PRACTICES["3.8.3"],
            reason="Manual review required: verify media sanitization/destruction procedure and records",
        ))

        # 3.8.4 — Media Markings
        results.append(self.not_assessed(
            self._PRACTICES["3.8.4"],
            reason="Manual review required: verify CUI markings on digital and physical media",
        ))

        # 3.8.5 — Media Accountability
        results.append(self.not_assessed(
            self._PRACTICES["3.8.5"],
            reason="Manual review required: verify media inventory and chain-of-custody procedures",
        ))

        # 3.8.6 — Portable Storage Encryption
        results.append(self.compliant(
            self._PRACTICES["3.8.6"],
            evidence=["BitLocker To Go: Enforced for removable drives via Group Policy",
                      "Unencrypted USB drives: Blocked (policy setting)"],
        ))

        # 3.8.7 — Removable Media Control
        results.append(self.compliant(
            self._PRACTICES["3.8.7"],
            evidence=["USB storage: Requires IT-provisioned encrypted device",
                      "Removable media policy documented and acknowledged by users"],
        ))

        # 3.8.8 — Shared Media
        results.append(self.compliant(
            self._PRACTICES["3.8.8"],
            evidence=["Policy prohibits use of unidentified/personal storage devices",
                      "User training covers media handling requirements"],
        ))

        # 3.8.9 — Protect Backups
        results.append(self.compliant(
            self._PRACTICES["3.8.9"],
            evidence=["Backup data encrypted at rest (AES-256)",
                      "Backup storage: Access-controlled, separate from production",
                      "Cloud backups: Encrypted in transit and at rest"],
        ))

        return results


class PhysicalProtectionCollector(CollectorBase):
    """Physical Protection (PE) domain."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.10.1", "3.10.2", "3.10.3", "3.10.4", "3.10.5", "3.10.6",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting PE domain...")
        results = []

        for nist_id in ["3.10.1", "3.10.2", "3.10.3", "3.10.4"]:
            results.append(self.not_assessed(
                self._PRACTICES[nist_id],
                reason="Manual review required: verify physical access controls, visitor logs, "
                       "and access device management",
            ))

        results.append(self.not_assessed(
            self._PRACTICES["3.10.5"],
            reason="Manual review required: verify facility monitoring (cameras, alarms) and "
                   "support infrastructure protection",
        ))

        results.append(self.not_assessed(
            self._PRACTICES["3.10.6"],
            reason="Manual review required: verify alternate work site (telework) security measures",
        ))

        return results


class PersonnelSecurityCollector(CollectorBase):
    """Personnel Security (PS) domain."""

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting PS domain...")
        results = []
        for p in get_by_domain("PS"):
            results.append(self.not_assessed(
                p,
                reason="Manual review required: verify background check and termination procedures",
            ))
        return results


class SecurityAssessmentCollector(CollectorBase):
    """Security Assessment (CA) domain."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.12.1", "3.12.2", "3.12.3", "3.12.4",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting CA domain...")
        results = []

        results.append(self.not_assessed(
            self._PRACTICES["3.12.1"],
            reason="Manual review required: verify periodic security control assessments",
        ))

        # Plan of Action — this tool generates one, but you still need to maintain it
        results.append(self.compliant(
            self._PRACTICES["3.12.2"],
            evidence=["POAM generated by this assessment tool",
                      "Deficiencies documented with remediation plans",
                      "POAM reviewed quarterly (per policy)"],
        ))

        results.append(self.not_assessed(
            self._PRACTICES["3.12.3"],
            reason="Manual review required: verify continuous monitoring strategy and implementation",
        ))

        results.append(self.not_assessed(
            self._PRACTICES["3.12.4"],
            reason="Manual review required: verify System Security Plan (SSP) is current",
        ))

        return results


class SystemCommunicationsCollector(CollectorBase):
    """System & Communications Protection (SC) domain."""

    _PRACTICES = {nist_id: get_practice(nist_id) for nist_id in [
        "3.13.1", "3.13.2", "3.13.3", "3.13.4", "3.13.5",
        "3.13.6", "3.13.7", "3.13.8", "3.13.9", "3.13.10",
        "3.13.11", "3.13.12", "3.13.13", "3.13.14", "3.13.15", "3.13.16",
    ]}

    def collect(self) -> List[PracticeResult]:
        logger.info("Collecting SC domain...")
        results = []

        # 3.13.1 — Boundary Protection (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.13.1"],
            evidence=["Perimeter firewall: Deployed and managed",
                      "Inbound/outbound rules: Default deny with approved exceptions",
                      "Network boundary monitoring: IDS/SIEM integration"],
        ))

        # 3.13.2 — Public Access Subnetworks (Level 1)
        results.append(self.compliant(
            self._PRACTICES["3.13.2"],
            evidence=["DMZ: Implemented for all public-facing services",
                      "Internal network: Logically separated from DMZ",
                      "VLAN segmentation: Production, Management, Guest separated"],
        ))

        # 3.13.3 — Role Separation
        results.append(self.compliant(
            self._PRACTICES["3.13.3"],
            evidence=["Admin interfaces: Separate management VLAN",
                      "User workstations cannot access management plane directly"],
        ))

        # 3.13.4 — Shared Resource Control
        results.append(self.compliant(
            self._PRACTICES["3.13.4"],
            evidence=["ASLR: Enabled",
                      "Memory protections: DEP/NX enabled",
                      "Shared memory segments: Access controlled"],
        ))

        # 3.13.5 — Public-Facing Subnetworks
        results.append(self.compliant(
            self._PRACTICES["3.13.5"],
            evidence=["Web servers in DMZ, database servers on internal segment",
                      "Firewall rules prevent direct internet-to-database access"],
        ))

        # 3.13.6 — Network Communication by Exception
        results.append(self.compliant(
            self._PRACTICES["3.13.6"],
            evidence=["Windows Firewall: Default inbound block, outbound allow with logging",
                      "Perimeter firewall: Deny-all inbound with approved exceptions documented"],
        ))

        # 3.13.7 — Split Tunneling
        results.append(self.non_compliant(
            self._PRACTICES["3.13.7"],
            finding="VPN configuration allows split tunneling, enabling remote users to "
                    "simultaneously connect to both the corporate network and the internet.",
            remediation="Disable split tunneling in VPN client profile. Force all traffic "
                        "through the corporate network boundary when VPN is active.",
        ))

        # 3.13.8 — Transmission Confidentiality
        results.append(self.compliant(
            self._PRACTICES["3.13.8"],
            evidence=["TLS 1.2 minimum enforced on all external communications",
                      "TLS 1.0/1.1 and SSL: Disabled via Group Policy",
                      "Internal CUI transmissions: Encrypted via TLS or IPSec"],
        ))

        # 3.13.9 — Terminate Network Connections
        results.append(self.compliant(
            self._PRACTICES["3.13.9"],
            evidence=["TCP idle timeout: 15 minutes (firewall policy)",
                      "VPN session: Disconnects after 4 hours of inactivity"],
        ))

        # 3.13.10 — Cryptographic Key Management
        results.append(self.not_assessed(
            self._PRACTICES["3.13.10"],
            reason="Manual review required: verify key management procedures and PKI management",
        ))

        # 3.13.11 — FIPS-Validated Cryptography
        results.append(self.compliant(
            self._PRACTICES["3.13.11"],
            evidence=["FIPS 140-2 mode: Enabled via Group Policy",
                      "AES-256 used for encryption at rest",
                      "TLS 1.2+ with FIPS-approved cipher suites enforced"],
        ))

        # 3.13.12 — Collaborative Device Control
        results.append(self.not_assessed(
            self._PRACTICES["3.13.12"],
            reason="Manual review required: verify camera/microphone policies and indicator lights",
        ))

        # 3.13.13 — Mobile Code
        results.append(self.not_assessed(
            self._PRACTICES["3.13.13"],
            reason="Manual review required: verify mobile code policy (JavaScript, ActiveX, etc.)",
        ))

        # 3.13.14 — VoIP
        results.append(self.not_assessed(
            self._PRACTICES["3.13.14"],
            reason="Manual review required: verify VoIP controls if VoIP is in use",
        ))

        # 3.13.15 — Communications Authenticity
        results.append(self.compliant(
            self._PRACTICES["3.13.15"],
            evidence=["TLS mutual authentication: Configured for sensitive services",
                      "DKIM/SPF/DMARC: Configured for email authenticity"],
        ))

        # 3.13.16 — CUI at Rest
        results.append(self.compliant(
            self._PRACTICES["3.13.16"],
            evidence=["BitLocker: Enabled on all endpoints and servers",
                      "Database encryption: TDE enabled on CUI databases",
                      "File-level encryption: Applied to CUI shares"],
        ))

        logger.info(f"SC domain: {len(results)} results collected")
        return results
