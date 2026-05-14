"""POAM (Plan of Action & Milestones) exporter.

Generates a DoD-style POAM document listing all non-compliant and
not-assessed practices with scheduled milestones for remediation.
"""

import csv
import logging
from datetime import datetime, timedelta
from .base import ExporterBase
from ..models.assessment import PracticeStatus
from ..practices.catalog import get_practice

logger = logging.getLogger(__name__)

# Default milestone schedule (days from assessment date)
_MILESTONE_DAYS = {
    "Identify root cause": 14,
    "Develop remediation plan": 30,
    "Begin implementation": 45,
    "Complete implementation": 90,
    "Validate / re-assess": 120,
}


def _milestone_dates(base_date: datetime) -> dict:
    return {
        task: (base_date + timedelta(days=days)).strftime("%Y-%m-%d")
        for task, days in _MILESTONE_DAYS.items()
    }


class POAMExporter(ExporterBase):
    """Exports a POAM as both HTML and CSV for DoD reporting."""

    def export(self, assessment, scorecard, output_path: str, **_) -> bool:
        try:
            base_date = datetime.fromisoformat(assessment.assessment_date)
        except (ValueError, TypeError):
            base_date = datetime.now()

        gaps = [
            r for r in assessment.results.values()
            if r.status in (PracticeStatus.NON_COMPLIANT, PracticeStatus.NOT_ASSESSED)
        ]

        if output_path.endswith(".csv"):
            return self._export_csv(gaps, base_date, assessment, output_path)
        return self._export_html(gaps, base_date, assessment, scorecard, output_path)

    # ------------------------------------------------------------------

    def _export_csv(self, gaps, base_date, assessment, output_path) -> bool:
        try:
            milestones = _milestone_dates(base_date)
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "POAM Item #", "CMMC ID", "NIST ID", "Domain", "Level",
                    "Status", "Weakness/Finding", "Recommended Remediation",
                    "Point of Contact", "Resources Required",
                ] + list(milestones.keys()) + ["Completion Date"])

                for i, result in enumerate(sorted(gaps, key=lambda r: r.nist_id), start=1):
                    practice = get_practice(result.nist_id)
                    writer.writerow([
                        f"POAM-{i:03d}",
                        result.cmmc_id,
                        result.nist_id,
                        result.domain,
                        result.level,
                        result.status.value,
                        result.finding or result.notes or "Not assessed — manual review required",
                        result.remediation or "Contact IT Security for assessment",
                        "IT Security Team",
                        "Internal Staff",
                    ] + list(milestones.values()) + [milestones["Complete implementation"]])

            logger.info(f"Exported POAM CSV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"POAM CSV export failed: {e}")
            return False

    def _export_html(self, gaps, base_date, assessment, scorecard, output_path) -> bool:
        try:
            milestones = _milestone_dates(base_date)
            rows = ""
            for i, result in enumerate(sorted(gaps, key=lambda r: r.nist_id), start=1):
                bg = "#ffebee" if result.status == PracticeStatus.NON_COMPLIANT else "#fff3e0"
                status_color = "#f44336" if result.status == PracticeStatus.NON_COMPLIANT else "#ff9800"
                finding = result.finding or result.notes or "Not assessed — manual review required"
                remediation = result.remediation or "Contact IT Security for assessment"
                milestone_cells = "".join(
                    f"<td>{date}</td>" for date in milestones.values()
                )
                rows += f"""
                <tr style="background:{bg}">
                  <td style="font-weight:bold">POAM-{i:03d}</td>
                  <td style="font-weight:bold; white-space:nowrap">{result.cmmc_id}</td>
                  <td>{result.domain}</td>
                  <td>L{result.level}</td>
                  <td style="color:{status_color}; font-weight:bold">{result.status.value}</td>
                  <td>{finding}</td>
                  <td>{remediation}</td>
                  <td>IT Security Team</td>
                  {milestone_cells}
                </tr>"""

            milestone_headers = "".join(f"<th>{m}</th>" for m in milestones)

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>POAM — {assessment.customer}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f0f2f5; }}
  .header {{ background: #b71c1c; color: white; padding: 28px 40px; }}
  .header h1 {{ font-size: 1.6em; }}
  .header .meta {{ opacity: 0.85; font-size: 0.88em; margin-top: 6px; }}
  .content {{ max-width: 1400px; margin: 24px auto; padding: 0 20px; }}
  .summary {{ background: white; border-radius: 8px; padding: 20px 24px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px;
              display: flex; gap: 40px; flex-wrap: wrap; }}
  .summary div {{ min-width: 160px; }}
  .summary .num {{ font-size: 2em; font-weight: 700; color: #b71c1c; }}
  .summary .lbl {{ color: #666; font-size: 0.82em; }}
  .section {{ background: white; border-radius: 8px; padding: 20px 24px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow-x: auto; }}
  .section h2 {{ color: #b71c1c; border-bottom: 2px solid #ffcdd2;
                  padding-bottom: 8px; margin-bottom: 14px; font-size: 1.05em; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.82em; min-width: 1200px; }}
  th {{ background: #ffcdd2; padding: 9px 10px; text-align: left;
        font-size: 0.78em; text-transform: uppercase; white-space: nowrap; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid #f5f5f5; vertical-align: top; }}
  .footer {{ text-align:center; color:#999; font-size:0.78em; padding:20px; }}
</style>
</head>
<body>
<div class="header">
  <h1>Plan of Action &amp; Milestones (POAM)</h1>
  <div class="meta">
    Customer: <strong>{assessment.customer}</strong> &nbsp;|&nbsp;
    Assessment Date: <strong>{assessment.assessment_date}</strong> &nbsp;|&nbsp;
    SPRS Score: <strong>{scorecard['sprs_score']}</strong> &nbsp;|&nbsp;
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </div>
</div>
<div class="content">
  <div class="summary">
    <div><div class="num">{len(gaps)}</div><div class="lbl">Total POAM Items</div></div>
    <div><div class="num" style="color:#f44336">{sum(1 for r in gaps if r.status == PracticeStatus.NON_COMPLIANT)}</div><div class="lbl">Non-Compliant</div></div>
    <div><div class="num" style="color:#ff9800">{sum(1 for r in gaps if r.status == PracticeStatus.NOT_ASSESSED)}</div><div class="lbl">Not Assessed</div></div>
    <div><div class="num">{scorecard['sprs_score']}</div><div class="lbl">SPRS Score</div></div>
  </div>
  <div class="section">
    <h2>POAM Items ({len(gaps)} open items)</h2>
    <table>
      <thead>
        <tr>
          <th>POAM #</th><th>CMMC ID</th><th>Domain</th><th>Lvl</th><th>Status</th>
          <th>Weakness / Finding</th><th>Recommended Remediation</th><th>Owner</th>
          {milestone_headers}
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
<div class="footer">
  This POAM was generated from a CMMC 2.0 self-assessment. Items must be tracked to closure.
  A current POAM is required for CMMC Level 2 certification (CA.L2-3.12.2).
</div>
</body>
</html>"""

            with open(output_path, 'w') as f:
                f.write(html)
            logger.info(f"Exported POAM HTML: {output_path}")
            return True
        except Exception as e:
            logger.error(f"POAM HTML export failed: {e}")
            return False
