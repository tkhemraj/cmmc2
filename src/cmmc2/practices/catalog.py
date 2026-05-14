"""CMMC 2.0 practice catalog — all Level 1 and Level 2 practices.

Practice IDs follow the NIST SP 800-171 Rev 2 numbering (e.g. "3.1.1").
CMMC IDs follow the DoD format (e.g. "AC.L1-3.1.1").
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Practice:
    nist_id: str          # e.g. "3.1.1"
    cmmc_id: str          # e.g. "AC.L1-3.1.1"
    domain: str           # e.g. "AC"
    level: int            # 1, 2, or 3
    title: str
    description: str
    sprs_weight: int = 1  # point value for SPRS scoring (simplified)
    automated: bool = False  # True if this tool can check it automatically


# ---------------------------------------------------------------------------
# Full CMMC 2.0 practice catalog
# Level 1: 17 practices (FAR 52.204-21 / FCI basic safeguarding)
# Level 2: 110 practices (NIST SP 800-171 Rev 2 / CUI protection)
# ---------------------------------------------------------------------------

PRACTICES: List[Practice] = [

    # ── Access Control (AC) ────────────────────────────────────────────────
    Practice("3.1.1",  "AC.L1-3.1.1",  "AC", 1,
        "Authorized Access Control",
        "Limit system access to authorized users, processes acting on behalf of "
        "authorized users, and devices (including other systems).",
        sprs_weight=5, automated=True),

    Practice("3.1.2",  "AC.L1-3.1.2",  "AC", 1,
        "Transaction & Function Control",
        "Limit system access to the types of transactions and functions that "
        "authorized users are permitted to execute.",
        sprs_weight=5, automated=True),

    Practice("3.1.20", "AC.L1-3.1.20", "AC", 1,
        "External Connections",
        "Verify and control/limit connections to external systems.",
        sprs_weight=3, automated=False),

    Practice("3.1.22", "AC.L1-3.1.22", "AC", 1,
        "Control Public Information",
        "Control CUI posted or processed on publicly accessible systems.",
        sprs_weight=3, automated=False),

    Practice("3.1.3",  "AC.L2-3.1.3",  "AC", 2,
        "Control CUI Flow",
        "Control the flow of CUI in accordance with approved authorizations.",
        sprs_weight=3),

    Practice("3.1.4",  "AC.L2-3.1.4",  "AC", 2,
        "Separation of Duties",
        "Separate the duties of individuals to reduce the risk of malevolent "
        "activity without collusion.",
        sprs_weight=3),

    Practice("3.1.5",  "AC.L2-3.1.5",  "AC", 2,
        "Least Privilege",
        "Employ the principle of least privilege, including for specific security "
        "functions and privileged accounts.",
        sprs_weight=5, automated=True),

    Practice("3.1.6",  "AC.L2-3.1.6",  "AC", 2,
        "Non-Privileged Account Use",
        "Use non-privileged accounts or roles when accessing non-security functions.",
        sprs_weight=3, automated=True),

    Practice("3.1.7",  "AC.L2-3.1.7",  "AC", 2,
        "Privileged Function Restriction",
        "Prevent non-privileged users from executing privileged functions and "
        "capture the execution of such functions in audit logs.",
        sprs_weight=5, automated=True),

    Practice("3.1.8",  "AC.L2-3.1.8",  "AC", 2,
        "Unsuccessful Logon Attempts",
        "Limit unsuccessful logon attempts.",
        sprs_weight=3, automated=True),

    Practice("3.1.9",  "AC.L2-3.1.9",  "AC", 2,
        "Privacy & Security Notices",
        "Provide privacy and security notices consistent with CUI rules.",
        sprs_weight=1),

    Practice("3.1.10", "AC.L2-3.1.10", "AC", 2,
        "Session Lock",
        "Use session lock with pattern-hiding displays after a period of inactivity.",
        sprs_weight=3, automated=True),

    Practice("3.1.11", "AC.L2-3.1.11", "AC", 2,
        "Session Termination",
        "Terminate (automatically) a user session after a defined condition.",
        sprs_weight=3, automated=True),

    Practice("3.1.12", "AC.L2-3.1.12", "AC", 2,
        "Remote Access Control",
        "Monitor and control remote access sessions.",
        sprs_weight=3),

    Practice("3.1.13", "AC.L2-3.1.13", "AC", 2,
        "Remote Access Confidentiality",
        "Employ cryptographic mechanisms to protect the confidentiality of remote "
        "access sessions.",
        sprs_weight=5, automated=True),

    Practice("3.1.14", "AC.L2-3.1.14", "AC", 2,
        "Remote Access Routing",
        "Route remote access via managed access control points.",
        sprs_weight=3),

    Practice("3.1.15", "AC.L2-3.1.15", "AC", 2,
        "Privileged Remote Access",
        "Authorize remote execution of privileged commands and access to "
        "security-relevant information via remote access only for documented "
        "operational needs.",
        sprs_weight=3),

    Practice("3.1.16", "AC.L2-3.1.16", "AC", 2,
        "Wireless Access Authorization",
        "Authorize wireless access prior to allowing such connections.",
        sprs_weight=3),

    Practice("3.1.17", "AC.L2-3.1.17", "AC", 2,
        "Wireless Access Protection",
        "Protect wireless access using authentication and encryption.",
        sprs_weight=5),

    Practice("3.1.18", "AC.L2-3.1.18", "AC", 2,
        "Mobile Device Control",
        "Control connection of mobile devices.",
        sprs_weight=3),

    Practice("3.1.19", "AC.L2-3.1.19", "AC", 2,
        "Encrypt CUI on Mobile",
        "Encrypt CUI on mobile devices and mobile computing platforms.",
        sprs_weight=5),

    Practice("3.1.21", "AC.L2-3.1.21", "AC", 2,
        "Portable Storage Use",
        "Limit use of portable storage devices on external systems.",
        sprs_weight=3),

    # ── Awareness & Training (AT) ──────────────────────────────────────────
    Practice("3.2.1",  "AT.L2-3.2.1",  "AT", 2,
        "Role-Based Risk Awareness",
        "Ensure that managers, systems administrators, and users of organizational "
        "systems are made aware of the security risks associated with their activities.",
        sprs_weight=3),

    Practice("3.2.2",  "AT.L2-3.2.2",  "AT", 2,
        "Role-Based Training",
        "Ensure that organizational personnel are adequately trained to carry out "
        "their assigned information security-related duties and responsibilities.",
        sprs_weight=3),

    Practice("3.2.3",  "AT.L2-3.2.3",  "AT", 2,
        "Insider Threat Awareness",
        "Provide security awareness training on recognizing and reporting potential "
        "indicators of insider threat.",
        sprs_weight=3),

    # ── Audit & Accountability (AU) ────────────────────────────────────────
    Practice("3.3.1",  "AU.L2-3.3.1",  "AU", 2,
        "System Auditing",
        "Create and retain system audit logs and records to the extent needed to "
        "enable the monitoring, analysis, investigation, and reporting of unlawful "
        "or unauthorized system activity.",
        sprs_weight=5, automated=True),

    Practice("3.3.2",  "AU.L2-3.3.2",  "AU", 2,
        "User Accountability",
        "Ensure that the actions of individual system users can be traced to those "
        "users so they can be held accountable for their actions.",
        sprs_weight=5, automated=True),

    Practice("3.3.3",  "AU.L2-3.3.3",  "AU", 2,
        "Event Review",
        "Review and update logged events.",
        sprs_weight=3),

    Practice("3.3.4",  "AU.L2-3.3.4",  "AU", 2,
        "Audit Failure Alerting",
        "Alert in the event of an audit logging process failure.",
        sprs_weight=3),

    Practice("3.3.5",  "AU.L2-3.3.5",  "AU", 2,
        "Audit Correlation",
        "Correlate audit record review, analysis, and reporting processes for "
        "investigation and response to indications of unlawful, unauthorized, "
        "suspicious, or unusual activity.",
        sprs_weight=3),

    Practice("3.3.6",  "AU.L2-3.3.6",  "AU", 2,
        "Reduction & Reporting",
        "Provide audit record reduction and report generation to support on-demand "
        "analysis and reporting.",
        sprs_weight=3),

    Practice("3.3.7",  "AU.L2-3.3.7",  "AU", 2,
        "Authoritative Time Source",
        "Provide a system capability that compares and synchronizes internal system "
        "clocks with an authoritative source to generate time stamps for audit records.",
        sprs_weight=1, automated=True),

    Practice("3.3.8",  "AU.L2-3.3.8",  "AU", 2,
        "Audit Protection",
        "Protect audit information and audit tools from unauthorized access, "
        "modification, and deletion.",
        sprs_weight=3),

    Practice("3.3.9",  "AU.L2-3.3.9",  "AU", 2,
        "Audit Management",
        "Limit management of audit logging to a subset of privileged users.",
        sprs_weight=3),

    # ── Configuration Management (CM) ─────────────────────────────────────
    Practice("3.4.1",  "CM.L2-3.4.1",  "CM", 2,
        "Baseline Configurations",
        "Establish and maintain baseline configurations and inventories of "
        "organizational systems (including hardware, software, firmware, and "
        "documentation) throughout the respective system development life cycles.",
        sprs_weight=3, automated=True),

    Practice("3.4.2",  "CM.L2-3.4.2",  "CM", 2,
        "Security Configuration Enforcement",
        "Establish and enforce security configuration settings for information "
        "technology products employed in organizational systems.",
        sprs_weight=3, automated=True),

    Practice("3.4.3",  "CM.L2-3.4.3",  "CM", 2,
        "Configuration Change Control",
        "Track, review, approve, and log changes to organizational systems.",
        sprs_weight=3),

    Practice("3.4.4",  "CM.L2-3.4.4",  "CM", 2,
        "Security Impact Analysis",
        "Analyze the security impact of changes prior to implementation.",
        sprs_weight=3),

    Practice("3.4.5",  "CM.L2-3.4.5",  "CM", 2,
        "Least Functionality",
        "Define, document, approve, and enforce physical and logical access "
        "restrictions associated with changes to organizational systems.",
        sprs_weight=3),

    Practice("3.4.6",  "CM.L2-3.4.6",  "CM", 2,
        "Least Functionality — Software",
        "Employ the principle of least functionality by configuring organizational "
        "systems to provide only essential capabilities.",
        sprs_weight=3, automated=True),

    Practice("3.4.7",  "CM.L2-3.4.7",  "CM", 2,
        "Nonessential Functions",
        "Restrict, disable, or prevent the use of nonessential programs, functions, "
        "ports, protocols, and services.",
        sprs_weight=3),

    Practice("3.4.8",  "CM.L2-3.4.8",  "CM", 2,
        "Application Execution Policy",
        "Apply deny-by-exception (blacklisting) policy to prevent the use of "
        "unauthorized software or deny-all, permit-by-exception (whitelisting) "
        "policy to allow the execution of authorized software.",
        sprs_weight=5),

    Practice("3.4.9",  "CM.L2-3.4.9",  "CM", 2,
        "User-Installed Software",
        "Control and monitor user-installed software.",
        sprs_weight=3),

    # ── Identification & Authentication (IA) ──────────────────────────────
    Practice("3.5.1",  "IA.L1-3.5.1",  "IA", 1,
        "Identify System Users",
        "Identify information system users, processes acting on behalf of users, "
        "and devices.",
        sprs_weight=5, automated=True),

    Practice("3.5.2",  "IA.L1-3.5.2",  "IA", 1,
        "Authenticate System Users",
        "Authenticate (or verify) the identities of those users, processes, or "
        "devices, as a prerequisite to allowing access to organizational systems.",
        sprs_weight=5, automated=True),

    Practice("3.5.3",  "IA.L2-3.5.3",  "IA", 2,
        "Multi-Factor Authentication",
        "Use multifactor authentication for local and network access to privileged "
        "accounts and for network access to non-privileged accounts.",
        sprs_weight=5, automated=True),

    Practice("3.5.4",  "IA.L2-3.5.4",  "IA", 2,
        "Replay-Resistant Authentication",
        "Employ replay-resistant authentication mechanisms for network access to "
        "privileged and non-privileged accounts.",
        sprs_weight=3),

    Practice("3.5.5",  "IA.L2-3.5.5",  "IA", 2,
        "Identifier Reuse",
        "Employ identifier management practices that prevent reuse of identifiers.",
        sprs_weight=1),

    Practice("3.5.6",  "IA.L2-3.5.6",  "IA", 2,
        "Identifier Handling",
        "Disable identifiers after a defined inactivity period.",
        sprs_weight=3, automated=True),

    Practice("3.5.7",  "IA.L2-3.5.7",  "IA", 2,
        "Password Complexity",
        "Enforce a minimum password complexity and change of characters when new "
        "passwords are created.",
        sprs_weight=5, automated=True),

    Practice("3.5.8",  "IA.L2-3.5.8",  "IA", 2,
        "Password Reuse",
        "Prohibit password reuse for a specified number of generations.",
        sprs_weight=3, automated=True),

    Practice("3.5.9",  "IA.L2-3.5.9",  "IA", 2,
        "Temporary Passwords",
        "Allow temporary password use for system logons with an immediate change "
        "to a permanent password.",
        sprs_weight=1),

    Practice("3.5.10", "IA.L2-3.5.10", "IA", 2,
        "Cryptographically Protected Passwords",
        "Store and transmit only cryptographically-protected passwords.",
        sprs_weight=5, automated=True),

    Practice("3.5.11", "IA.L2-3.5.11", "IA", 2,
        "Obscure Feedback",
        "Obscure feedback of authentication information.",
        sprs_weight=1),

    # ── Incident Response (IR) ────────────────────────────────────────────
    Practice("3.6.1",  "IR.L2-3.6.1",  "IR", 2,
        "Incident Handling",
        "Establish an operational incident-handling capability for organizational "
        "systems that includes preparation, detection, analysis, containment, "
        "recovery, and user response activities.",
        sprs_weight=5),

    Practice("3.6.2",  "IR.L2-3.6.2",  "IR", 2,
        "Incident Reporting",
        "Track, document, and report incidents to designated officials and/or "
        "authorities both internal and external to the organization.",
        sprs_weight=3),

    Practice("3.6.3",  "IR.L2-3.6.3",  "IR", 2,
        "Incident Response Testing",
        "Test the organizational incident response capability.",
        sprs_weight=3),

    # ── Maintenance (MA) ──────────────────────────────────────────────────
    Practice("3.7.1",  "MA.L2-3.7.1",  "MA", 2,
        "Manage Maintenance",
        "Perform maintenance on organizational systems.",
        sprs_weight=1),

    Practice("3.7.2",  "MA.L2-3.7.2",  "MA", 2,
        "Controlled Maintenance",
        "Provide controls on the tools, techniques, mechanisms, and personnel "
        "that perform system maintenance.",
        sprs_weight=3),

    Practice("3.7.3",  "MA.L2-3.7.3",  "MA", 2,
        "Equipment Sanitization",
        "Ensure equipment removed for maintenance is sanitized with respect to "
        "all CUI.",
        sprs_weight=3),

    Practice("3.7.4",  "MA.L2-3.7.4",  "MA", 2,
        "Media Inspection",
        "Check media containing diagnostic and test programs for malicious code "
        "before the media are used in organizational systems.",
        sprs_weight=3),

    Practice("3.7.5",  "MA.L2-3.7.5",  "MA", 2,
        "Multi-Factor Authentication for Maintenance",
        "Require MFA to establish nonlocal maintenance sessions via external "
        "networks and terminate such connections when nonlocal maintenance is "
        "complete.",
        sprs_weight=5),

    Practice("3.7.6",  "MA.L2-3.7.6",  "MA", 2,
        "Remote Maintenance Supervision",
        "Supervise the maintenance activities of maintenance personnel without "
        "required access authorization.",
        sprs_weight=3),

    # ── Media Protection (MP) ─────────────────────────────────────────────
    Practice("3.8.1",  "MP.L2-3.8.1",  "MP", 2,
        "Media Protection",
        "Protect (i.e., physically control and securely store) system media "
        "containing Federal Contract Information (FCI), both paper and digital.",
        sprs_weight=3),

    Practice("3.8.2",  "MP.L2-3.8.2",  "MP", 2,
        "Media Access",
        "Limit access to CUI on system media to authorized users.",
        sprs_weight=3),

    Practice("3.8.3",  "MP.L1-3.8.3",  "MP", 1,
        "Media Sanitization",
        "Sanitize or destroy system media before disposal or reuse.",
        sprs_weight=5, automated=False),

    Practice("3.8.4",  "MP.L2-3.8.4",  "MP", 2,
        "Media Markings",
        "Mark media with necessary CUI markings and distribution limitations.",
        sprs_weight=1),

    Practice("3.8.5",  "MP.L2-3.8.5",  "MP", 2,
        "Media Accountability",
        "Control access to media containing CUI and maintain accountability for "
        "media during transport.",
        sprs_weight=3),

    Practice("3.8.6",  "MP.L2-3.8.6",  "MP", 2,
        "Portable Storage Encryption",
        "Implement cryptographic mechanisms to protect the confidentiality of CUI "
        "during transport unless otherwise protected by alternative physical "
        "safeguards.",
        sprs_weight=5),

    Practice("3.8.7",  "MP.L2-3.8.7",  "MP", 2,
        "Removable Media Control",
        "Control the use of removable media on system components.",
        sprs_weight=3),

    Practice("3.8.8",  "MP.L2-3.8.8",  "MP", 2,
        "Shared Media",
        "Prohibit the use of portable storage devices when such devices have no "
        "identifiable owner.",
        sprs_weight=1),

    Practice("3.8.9",  "MP.L2-3.8.9",  "MP", 2,
        "Protect Backups",
        "Protect the confidentiality of backup CUI at storage locations.",
        sprs_weight=3),

    # ── Personnel Security (PS) ───────────────────────────────────────────
    Practice("3.9.1",  "PS.L2-3.9.1",  "PS", 2,
        "Screen Individuals",
        "Screen individuals prior to authorizing access to organizational systems "
        "containing CUI.",
        sprs_weight=3),

    Practice("3.9.2",  "PS.L2-3.9.2",  "PS", 2,
        "Termination & Transfer",
        "Ensure that organizational systems containing CUI are protected during "
        "and after personnel actions such as terminations and transfers.",
        sprs_weight=3),

    # ── Physical Protection (PE) ──────────────────────────────────────────
    Practice("3.10.1", "PE.L1-3.10.1", "PE", 1,
        "Limit Physical Access",
        "Limit physical access to organizational systems to authorized individuals.",
        sprs_weight=3),

    Practice("3.10.2", "PE.L1-3.10.2", "PE", 1,
        "Escort Visitors",
        "Escort visitors and monitor visitor activity.",
        sprs_weight=1),

    Practice("3.10.3", "PE.L1-3.10.3", "PE", 1,
        "Physical Access Logs",
        "Maintain audit logs of physical access.",
        sprs_weight=1),

    Practice("3.10.4", "PE.L1-3.10.4", "PE", 1,
        "Manage Physical Access Devices",
        "Control and manage physical access devices.",
        sprs_weight=1),

    Practice("3.10.5", "PE.L2-3.10.5", "PE", 2,
        "Physical Access Protection",
        "Protect and monitor the physical facility and support infrastructure "
        "for organizational systems.",
        sprs_weight=3),

    Practice("3.10.6", "PE.L2-3.10.6", "PE", 2,
        "Alternative Work Sites",
        "Enforce safeguarding measures for CUI at alternate work sites.",
        sprs_weight=3),

    # ── Risk Assessment (RA) ──────────────────────────────────────────────
    Practice("3.11.1", "RA.L2-3.11.1", "RA", 2,
        "Risk Assessments",
        "Periodically assess the risk to organizational operations, assets, and "
        "individuals resulting from the operation of organizational systems and "
        "the associated processing, storage, or transmission of CUI.",
        sprs_weight=3),

    Practice("3.11.2", "RA.L2-3.11.2", "RA", 2,
        "Vulnerability Scanning",
        "Scan for vulnerabilities in organizational systems and applications "
        "periodically and when new vulnerabilities affecting those systems and "
        "applications are identified.",
        sprs_weight=5, automated=True),

    Practice("3.11.3", "RA.L2-3.11.3", "RA", 2,
        "Vulnerability Remediation",
        "Remediate vulnerabilities in accordance with risk assessments.",
        sprs_weight=5),

    # ── Security Assessment (CA) ──────────────────────────────────────────
    Practice("3.12.1", "CA.L2-3.12.1", "CA", 2,
        "Security Control Assessments",
        "Periodically assess the security controls in organizational systems to "
        "determine if the controls are effective in their application.",
        sprs_weight=3),

    Practice("3.12.2", "CA.L2-3.12.2", "CA", 2,
        "Plan of Action",
        "Develop and implement plans of action designed to correct deficiencies "
        "and reduce or eliminate vulnerabilities in organizational systems.",
        sprs_weight=5),

    Practice("3.12.3", "CA.L2-3.12.3", "CA", 2,
        "Continuous Monitoring",
        "Monitor security controls on an ongoing basis to ensure the continued "
        "effectiveness of the controls.",
        sprs_weight=3),

    Practice("3.12.4", "CA.L2-3.12.4", "CA", 2,
        "System Security Plan",
        "Develop, document, and periodically update system security plans that "
        "describe system boundaries, system environments of operation, how security "
        "requirements are implemented, and the relationships with or connections to "
        "other systems.",
        sprs_weight=3),

    # ── System & Communications Protection (SC) ───────────────────────────
    Practice("3.13.1", "SC.L1-3.13.1", "SC", 1,
        "Boundary Protection",
        "Monitor, control, and protect communications at the external boundaries "
        "and key internal boundaries of organizational systems.",
        sprs_weight=5, automated=True),

    Practice("3.13.2", "SC.L1-3.13.2", "SC", 1,
        "Public Access Subnetworks",
        "Implement subnetworks for publicly accessible system components that are "
        "physically or logically separated from internal networks.",
        sprs_weight=3),

    Practice("3.13.3", "SC.L2-3.13.3", "SC", 2,
        "Role Separation",
        "Separate user functionality from system management functionality.",
        sprs_weight=3),

    Practice("3.13.4", "SC.L2-3.13.4", "SC", 2,
        "Shared Resource Control",
        "Prevent unauthorized and unintended information transfer via shared "
        "system resources.",
        sprs_weight=3),

    Practice("3.13.5", "SC.L2-3.13.5", "SC", 2,
        "Public-Facing Subnetworks",
        "Implement subnetworks for publicly accessible system components that are "
        "physically or logically separated from internal networks.",
        sprs_weight=5),

    Practice("3.13.6", "SC.L2-3.13.6", "SC", 2,
        "Network Communication by Exception",
        "Deny network communications traffic by default and allow network "
        "communications traffic by exception (i.e., deny all, permit by exception).",
        sprs_weight=5, automated=True),

    Practice("3.13.7", "SC.L2-3.13.7", "SC", 2,
        "Split Tunneling",
        "Prevent remote devices from simultaneously establishing remote connections "
        "with the system and communicating via some other connection to resources "
        "in other networks (i.e., split tunneling).",
        sprs_weight=3),

    Practice("3.13.8", "SC.L2-3.13.8", "SC", 2,
        "Transmission Confidentiality",
        "Implement cryptographic mechanisms to prevent unauthorized disclosure of "
        "CUI during transmission unless otherwise protected by alternative physical "
        "safeguards.",
        sprs_weight=5, automated=True),

    Practice("3.13.9", "SC.L2-3.13.9", "SC", 2,
        "Terminate Network Connections",
        "Terminate network connections associated with communications sessions "
        "after a defined period of inactivity.",
        sprs_weight=3),

    Practice("3.13.10", "SC.L2-3.13.10", "SC", 2,
        "Cryptographic Key Management",
        "Establish and manage cryptographic keys for cryptography employed in "
        "organizational systems.",
        sprs_weight=3),

    Practice("3.13.11", "SC.L2-3.13.11", "SC", 2,
        "FIPS-Validated Cryptography",
        "Employ FIPS-validated cryptography when used to protect the "
        "confidentiality of CUI.",
        sprs_weight=5, automated=True),

    Practice("3.13.12", "SC.L2-3.13.12", "SC", 2,
        "Collaborative Device Control",
        "Prohibit remote activation of collaborative computing devices and provide "
        "indication of use to present users.",
        sprs_weight=3),

    Practice("3.13.13", "SC.L2-3.13.13", "SC", 2,
        "Mobile Code",
        "Control and monitor the use of mobile code.",
        sprs_weight=3),

    Practice("3.13.14", "SC.L2-3.13.14", "SC", 2,
        "VoIP",
        "Control and monitor the use of VoIP technologies.",
        sprs_weight=1),

    Practice("3.13.15", "SC.L2-3.13.15", "SC", 2,
        "Communications Authenticity",
        "Protect the authenticity of communications sessions.",
        sprs_weight=3),

    Practice("3.13.16", "SC.L2-3.13.16", "SC", 2,
        "CUI at Rest",
        "Protect the confidentiality of CUI at rest.",
        sprs_weight=5, automated=True),

    # ── System & Information Integrity (SI) ───────────────────────────────
    Practice("3.14.1", "SI.L1-3.14.1", "SI", 1,
        "Flaw Remediation",
        "Identify, report, and correct information and system flaws in a timely "
        "manner.",
        sprs_weight=5, automated=True),

    Practice("3.14.2", "SI.L1-3.14.2", "SI", 1,
        "Malicious Code Protection",
        "Provide protection from malicious code at appropriate locations within "
        "organizational systems.",
        sprs_weight=5, automated=True),

    Practice("3.14.3", "SI.L2-3.14.3", "SI", 2,
        "Security Alerts",
        "Monitor system security alerts and advisories and take action in response.",
        sprs_weight=3),

    Practice("3.14.4", "SI.L1-3.14.4", "SI", 1,
        "Update Malicious Code Protection",
        "Update malicious code protection mechanisms when new releases are "
        "available.",
        sprs_weight=5, automated=True),

    Practice("3.14.5", "SI.L1-3.14.5", "SI", 1,
        "System & File Scans",
        "Perform periodic scans of organizational systems and real-time scans of "
        "files from external sources.",
        sprs_weight=5, automated=True),

    Practice("3.14.6", "SI.L2-3.14.6", "SI", 2,
        "Security Function Monitoring",
        "Monitor organizational systems, including inbound and outbound "
        "communications traffic, to detect attacks and indicators of potential "
        "attacks.",
        sprs_weight=5, automated=True),

    Practice("3.14.7", "SI.L2-3.14.7", "SI", 2,
        "Unauthorized Use Identification",
        "Identify unauthorized use of organizational systems.",
        sprs_weight=5),
]

# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

_BY_NIST_ID: dict = {p.nist_id: p for p in PRACTICES}
_BY_CMMC_ID: dict = {p.cmmc_id: p for p in PRACTICES}


def get_practice(nist_id: str) -> Optional[Practice]:
    """Return a Practice by its NIST SP 800-171 ID (e.g. '3.1.1')."""
    return _BY_NIST_ID.get(nist_id)


def get_by_cmmc_id(cmmc_id: str) -> Optional[Practice]:
    """Return a Practice by its CMMC 2.0 ID (e.g. 'AC.L1-3.1.1')."""
    return _BY_CMMC_ID.get(cmmc_id)


def get_by_level(level: int) -> List[Practice]:
    """Return all practices at or below the given CMMC level."""
    return [p for p in PRACTICES if p.level <= level]


def get_by_domain(domain: str) -> List[Practice]:
    """Return all practices in the given domain (e.g. 'AC')."""
    return [p for p in PRACTICES if p.domain == domain]


DOMAINS = sorted({p.domain for p in PRACTICES})
LEVEL1_PRACTICES = get_by_level(1)
LEVEL2_PRACTICES = get_by_level(2)

MAX_SPRS_SCORE = 110  # SPRS score when all Level 2 practices are compliant
