"""CMMC 2.0 Compliance Assessment Tool.

Covers all 110 NIST SP 800-171 Rev 2 practices across 14 domains.
Produces SPRS score, per-domain scoring, HTML compliance dashboard, and POAM.
"""

__version__ = "1.0.0"

from .assessor import CMMCAssessor

__all__ = ["CMMCAssessor"]
