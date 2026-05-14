"""CMMC 2.0 assessment exporters."""

from .json_exporter import JSONExporter
from .html_exporter import HTMLExporter
from .poam_exporter import POAMExporter

EXPORTERS = {
    "json": JSONExporter,
    "html": HTMLExporter,
    "poam": POAMExporter,
    "poam_csv": POAMExporter,
}


def create_exporter(format_type: str):
    """Return an exporter for the given format name, or None if unknown."""
    cls = EXPORTERS.get(format_type.lower())
    return cls() if cls else None


__all__ = ["JSONExporter", "HTMLExporter", "POAMExporter", "EXPORTERS", "create_exporter"]
