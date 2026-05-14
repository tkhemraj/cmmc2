"""Command-line interface for CMMC 2.0 assessor."""

import argparse
import json
import logging
import sys
from pathlib import Path

from .assessor import CMMCAssessor
from .models.assessment import CMMCAssessment
from .scoring.scorer import CMMCScorer
from .exporters import create_exporter

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="CMMC 2.0 Compliance Assessment Tool")
    subparsers = parser.add_subparsers(dest="command")

    # assess
    ap = subparsers.add_parser("assess", help="Run a CMMC 2.0 assessment")
    ap.add_argument("--customer", "-c", required=True, help="Organization / customer name")
    ap.add_argument("--level", "-l", type=int, choices=[1, 2], default=2,
                    help="Target CMMC level (default: 2)")
    ap.add_argument("--output", "-o", default="assessment.json",
                    help="Output file (default: assessment.json)")
    ap.add_argument("--format", "-f", choices=["json", "html", "poam", "poam_csv"],
                    default="json", help="Output format (default: json)")
    ap.add_argument("--all", "-a", action="store_true",
                    help="Export all formats (json, html, poam) to --output-dir")
    ap.add_argument("--output-dir", "-d", default=".", help="Output directory (used with --all)")

    # report
    rp = subparsers.add_parser("report", help="Generate report from saved JSON assessment")
    rp.add_argument("--input", "-i", required=True, help="Input JSON assessment file")
    rp.add_argument("--format", "-f", choices=["html", "poam", "poam_csv"], default="html")
    rp.add_argument("--output", "-o", default="report.html")

    args = parser.parse_args()

    if args.command == "assess":
        return _assess(args)
    elif args.command == "report":
        return _report(args)
    else:
        parser.print_help()
        return 0


def _assess(args) -> int:
    assessor = CMMCAssessor(customer=args.customer, target_level=args.level)
    assessor.assess()
    assessor.print_summary()

    if args.all:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        slug = args.customer.replace(" ", "_").lower()
        results = {}
        for fmt, ext in [("json", "json"), ("html", "html"), ("poam", "poam.html")]:
            path = str(out_dir / f"{slug}_cmmc2.{ext}")
            results[fmt] = assessor.export(fmt, path)
            print(f"  {'✓' if results[fmt] else '✗'} {fmt}: {path}")
    else:
        success = assessor.export(args.format, args.output)
        print(f"{'✓' if success else '✗'} Exported {args.format}: {args.output}")

    return 0


def _report(args) -> int:
    try:
        with open(args.input) as f:
            data = json.load(f)
        assessment = CMMCAssessment.from_dict(data.get("assessment", data))
        scorecard = CMMCScorer.full_scorecard(assessment)
        exporter = create_exporter(args.format)
        if not exporter:
            logger.error(f"Unknown format: {args.format}")
            return 1
        success = exporter.export(assessment, scorecard, args.output)
        print(f"{'✓' if success else '✗'} Exported {args.format}: {args.output}")
        return 0 if success else 1
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
