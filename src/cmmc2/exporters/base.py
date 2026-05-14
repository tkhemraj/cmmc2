"""Base exporter for CMMC 2.0 assessment results."""

from abc import ABC, abstractmethod
from typing import Any


class ExporterBase(ABC):
    """Abstract base for all assessment exporters."""

    @abstractmethod
    def export(self, assessment: Any, scorecard: Any, output_path: str, **kwargs) -> bool:
        """Write the assessment to output_path. Returns True on success."""
        pass
