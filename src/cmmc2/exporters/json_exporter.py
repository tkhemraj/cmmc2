"""JSON exporter for CMMC 2.0 assessments."""

import json
import logging
from .base import ExporterBase

logger = logging.getLogger(__name__)


class JSONExporter(ExporterBase):
    """Exports full assessment + scorecard as JSON."""

    def export(self, assessment, scorecard, output_path: str, **_) -> bool:
        try:
            payload = {
                "assessment": assessment.to_dict(),
                "scorecard": scorecard,
            }
            with open(output_path, 'w') as f:
                json.dump(payload, f, indent=2, default=str)
            logger.info(f"Exported JSON: {output_path}")
            return True
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return False
