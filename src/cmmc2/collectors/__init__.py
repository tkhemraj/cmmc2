"""CMMC 2.0 domain collectors."""

from .access_control import AccessControlCollector
from .audit import AuditCollector, ConfigurationCollector
from .identification import IdentificationCollector
from .system_integrity import SystemIntegrityCollector, RiskAssessmentCollector
from .remaining_domains import (
    AwarenessTrainingCollector,
    IncidentResponseCollector,
    MaintenanceCollector,
    MediaProtectionCollector,
    PhysicalProtectionCollector,
    PersonnelSecurityCollector,
    SecurityAssessmentCollector,
    SystemCommunicationsCollector,
)

ALL_COLLECTORS = [
    AccessControlCollector,
    AuditCollector,
    ConfigurationCollector,
    IdentificationCollector,
    SystemIntegrityCollector,
    RiskAssessmentCollector,
    AwarenessTrainingCollector,
    IncidentResponseCollector,
    MaintenanceCollector,
    MediaProtectionCollector,
    PhysicalProtectionCollector,
    PersonnelSecurityCollector,
    SecurityAssessmentCollector,
    SystemCommunicationsCollector,
]

__all__ = [
    "AccessControlCollector", "AuditCollector", "ConfigurationCollector",
    "IdentificationCollector", "SystemIntegrityCollector", "RiskAssessmentCollector",
    "AwarenessTrainingCollector", "IncidentResponseCollector", "MaintenanceCollector",
    "MediaProtectionCollector", "PhysicalProtectionCollector", "PersonnelSecurityCollector",
    "SecurityAssessmentCollector", "SystemCommunicationsCollector",
    "ALL_COLLECTORS",
]
