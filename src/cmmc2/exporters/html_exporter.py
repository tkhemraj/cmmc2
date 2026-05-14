"""HTML compliance dashboard exporter for CMMC 2.0."""

import logging
from datetime import datetime
from .base import ExporterBase
from ..models.assessment import PracticeStatus

logger = logging.getLogger(__name__)

_STATUS_COLOR = {
    PracticeStatus.COMPLIANT:     "#4caf50",
    PracticeStatus.NON_COMPLIANT: "#f44336",
    PracticeStatus.NOT_ASSESSED:  "#ff9800",
    PracticeStatus.NOT_APPLICABLE: "#9e9e9e",
}
_STATUS_BG = {
    PracticeStatus.COMPLIANT:     "#e8f5e9",
    PracticeStatus.NON_COMPLIANT: "#ffebee",
    PracticeStatus.NOT_ASSESSED:  "#fff3e0",
    PracticeStatus.NOT_APPLICABLE: "#f5f5f5",
}


class HTMLExporter(ExporterBase):
    """Exports an HTML compliance dashboard showing SPRS score, domain breakdown, and findings."""

    def export(self, assessment, scorecard, output_path: str, **_) -> bool:
        try:
            with open(output_path, 'w') as f:
                f.write(self._generate(assessment, scorecard))
            logger.info(f"Exported HTML: {output_path}")
            return True
        except Exception as e:
            logger.error(f"HTML export failed: {e}")
            return False

    def _generate(self, assessment, scorecard) -> str:
        sprs = scorecard["sprs_score"]
        achieved = scorecard["achieved_level"]
        target = scorecard["target_level"]
        l1 = scorecard["level1"]
        l2 = scorecard["level2"]
        domains = scorecard["domains"]

        sprs_color = "#4caf50" if sprs >= 88 else ("#ff9800" if sprs >= 70 else "#f44336")
        level_color = "#4caf50" if achieved >= target else "#f44336"

        # Domain score bars
        domain_bars = ""
        for domain, ds in domains.items():
            pct = ds["percentage"]
            bar_color = "#4caf50" if pct >= 80 else ("#ff9800" if pct >= 50 else "#f44336")
            domain_bars += f"""
            <div class="domain-row">
                <div class="domain-label">{domain}</div>
                <div class="domain-bar-bg">
                    <div class="domain-bar" style="width:{pct}%; background:{bar_color}"></div>
                </div>
                <div class="domain-pct">{pct}%
                    <span class="domain-counts">({ds['compliant']}/{ds['total']})</span>
                </div>
            </div>"""

        # Findings table (non-compliant + not-assessed)
        findings_rows = ""
        for result in sorted(assessment.results.values(), key=lambda r: (r.domain, r.nist_id)):
            if result.status in (PracticeStatus.NON_COMPLIANT, PracticeStatus.NOT_ASSESSED):
                bg = _STATUS_BG[result.status]
                color = _STATUS_COLOR[result.status]
                finding_text = result.finding or result.notes or "—"
                remediation_text = result.remediation or "Manual review required"
                findings_rows += f"""
                <tr style="background:{bg}">
                    <td style="color:{color}; font-weight:bold; white-space:nowrap">{result.cmmc_id}</td>
                    <td>{result.domain}</td>
                    <td style="color:{color}">{result.status.value}</td>
                    <td>{finding_text}</td>
                    <td>{remediation_text}</td>
                </tr>"""

        # Practice detail table
        detail_rows = ""
        for domain in sorted(set(r.domain for r in assessment.results.values())):
            domain_results = sorted(
                assessment.get_domain_results(domain), key=lambda r: r.nist_id
            )
            for result in domain_results:
                color = _STATUS_COLOR[result.status]
                bg = _STATUS_BG[result.status]
                evidence = "; ".join(result.evidence) if result.evidence else "—"
                detail_rows += f"""
                <tr style="background:{bg}">
                    <td style="white-space:nowrap">{result.cmmc_id}</td>
                    <td>{result.domain}</td>
                    <td>L{result.level}</td>
                    <td style="color:{color}; font-weight:bold">{result.status.value}</td>
                    <td style="font-size:0.85em">{evidence}</td>
                </tr>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CMMC 2.0 Assessment — {assessment.customer}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; color: #333; }}
  .header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
             color: white; padding: 32px 40px; }}
  .header h1 {{ font-size: 1.8em; }}
  .header .meta {{ opacity: 0.8; margin-top: 6px; font-size: 0.9em; }}
  .content {{ max-width: 1100px; margin: 0 auto; padding: 30px 20px; }}
  .cards {{ display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }}
  .card {{ background: white; border-radius: 8px; padding: 24px;
           box-shadow: 0 2px 8px rgba(0,0,0,0.08); flex: 1; min-width: 180px; }}
  .card .number {{ font-size: 2.8em; font-weight: 700; line-height: 1; }}
  .card .label {{ color: #666; font-size: 0.85em; margin-top: 4px; }}
  .section {{ background: white; border-radius: 8px; padding: 24px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 24px; }}
  .section h2 {{ font-size: 1.1em; color: #1a237e; border-bottom: 2px solid #e8eaf6;
                 padding-bottom: 10px; margin-bottom: 16px; }}
  .domain-row {{ display: flex; align-items: center; gap: 12px; margin: 8px 0; }}
  .domain-label {{ width: 32px; font-weight: bold; font-size: 0.85em; color: #555; }}
  .domain-bar-bg {{ flex: 1; height: 18px; background: #eee; border-radius: 9px; overflow: hidden; }}
  .domain-bar {{ height: 100%; border-radius: 9px; transition: width 0.3s; }}
  .domain-pct {{ width: 70px; font-size: 0.85em; font-weight: bold; }}
  .domain-counts {{ color: #999; font-weight: normal; font-size: 0.85em; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88em; }}
  th {{ background: #e8eaf6; padding: 10px 12px; text-align: left;
        font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
  tr:hover td {{ background: rgba(0,0,0,0.02); }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px;
             font-size: 0.8em; font-weight: bold; }}
  .footer {{ text-align: center; color: #999; font-size: 0.8em; margin-top: 20px; padding: 20px; }}
</style>
</head>
<body>
<div class="header">
  <h1>CMMC 2.0 Compliance Assessment</h1>
  <div class="meta">
    Customer: <strong>{assessment.customer}</strong> &nbsp;|&nbsp;
    Assessment Date: <strong>{assessment.assessment_date}</strong> &nbsp;|&nbsp;
    Target Level: <strong>Level {target}</strong> &nbsp;|&nbsp;
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </div>
</div>

<div class="content">

  <!-- Score Cards -->
  <div class="cards">
    <div class="card">
      <div class="number" style="color:{sprs_color}">{sprs}</div>
      <div class="label">SPRS Score (max 110)</div>
    </div>
    <div class="card">
      <div class="number" style="color:{level_color}">L{achieved}</div>
      <div class="label">Achieved Level (target L{target})</div>
    </div>
    <div class="card">
      <div class="number" style="color:#1a237e">{l1['percentage']}%</div>
      <div class="label">Level 1 ({l1['compliant']}/{l1['total']} practices)</div>
    </div>
    <div class="card">
      <div class="number" style="color:#283593">{l2['percentage']}%</div>
      <div class="label">Level 2 ({l2['compliant']}/{l2['total']} practices)</div>
    </div>
    <div class="card">
      <div class="number" style="color:#f44336">{scorecard['non_compliant_count']}</div>
      <div class="label">Non-Compliant Practices</div>
    </div>
  </div>

  <!-- Domain Scores -->
  <div class="section">
    <h2>Domain Scores</h2>
    {domain_bars}
  </div>

  <!-- Findings & Remediation -->
  <div class="section">
    <h2>Findings &amp; Remediation ({scorecard['non_compliant_count']} items)</h2>
    <table>
      <thead>
        <tr>
          <th>CMMC ID</th><th>Domain</th><th>Status</th>
          <th>Finding</th><th>Recommended Remediation</th>
        </tr>
      </thead>
      <tbody>{findings_rows}</tbody>
    </table>
  </div>

  <!-- Full Practice Detail -->
  <div class="section">
    <h2>All Practices — Detail</h2>
    <table>
      <thead>
        <tr>
          <th>CMMC ID</th><th>Domain</th><th>Lvl</th><th>Status</th><th>Evidence / Notes</th>
        </tr>
      </thead>
      <tbody>{detail_rows}</tbody>
    </table>
  </div>

</div>
<div class="footer">
  CMMC 2.0 Assessment Tool &nbsp;|&nbsp; NIST SP 800-171 Rev 2 &nbsp;|&nbsp;
  This is a self-assessment. Third-party C3PAO assessment required for Level 2 certification.
</div>
</body>
</html>"""
