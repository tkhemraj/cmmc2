# CMMC 2.0 Compliance Assessment Tool

> **Stop guessing. Start scoring.**
> The only open-source tool that runs a full CMMC 2.0 self-assessment, calculates your official DoD SPRS score, and generates a ready-to-submit POAM — in under 10 seconds.

---

## Why This Exists

CMMC 2.0 certification is no longer optional for DoD contractors. If you handle **Controlled Unclassified Information (CUI)**, you need to demonstrate compliance with all 110 practices from **NIST SP 800-171 Rev 2** — or lose your contract eligibility.

The problem? Most organizations spend **weeks** manually working through spreadsheets, trying to map their controls to 14 domains, calculate a SPRS score they have no idea how to compute, and produce a POAM that satisfies an auditor.

This tool does all of that automatically.

---

## What It Does

| Feature | Details |
|---|---|
| **Full Practice Catalog** | All 110 NIST SP 800-171 Rev 2 practices across all 14 CMMC domains, with official CMMC IDs (e.g. `AC.L1-3.1.1`) |
| **SPRS Score** | Calculates your official DoD Supplier Performance Risk System score (-203 to 110) using the DoD Assessment Methodology weights |
| **Level Determination** | Tells you exactly which CMMC level you've achieved (0, 1, or 2) vs. your target |
| **POAM Generation** | Produces a DoD-style Plan of Action & Milestones with auto-calculated milestone dates — HTML and CSV |
| **HTML Dashboard** | Executive-ready compliance dashboard with domain score bars, color-coded findings, and full evidence table |
| **Per-Domain Scoring** | Breakdown across all 14 domains: AC, AT, AU, CM, IA, IR, MA, MP, PE, PS, RA, CA, SC, SI |
| **Evidence Tracking** | Every automated check logs its evidence so you can walk an auditor through exactly how you're compliant |
| **JSON Round-Trip** | Save and reload assessments — re-generate any report format from a stored assessment file |

---

## The Output

One command gives you three deliverables:

```
cmmc2 assess --customer "Acme Corp" --all --output-dir ./reports/
```

```
============================================================
  CMMC 2.0 Assessment — Acme Corp
============================================================
  SPRS Score:        87  (max 110)
  Achieved Level:  Level 1  (target: Level 2)
  Level 1:         17/17 (100.0%)
  Level 2:         74/110 (67.3%)
  Non-Compliant:   8 practice(s)

  Domain Scores:
    AC  [████████████████░░░░]  82.6%  (19/22)
    AU  [███████████████████░]  88.9%  (8/9)
    CM  [████████████░░░░░░░░]  55.6%  (5/9)
    IA  [████████████████████]  100.0% (11/11)
    IR  [████░░░░░░░░░░░░░░░░]  0.0%   (0/3)
    SC  [████████████████░░░░]  75.0%  (12/16)
    SI  [████████████████████]  100.0% (7/7)
    ...
============================================================

  ✓ json:  reports/acme_corp_cmmc2.json
  ✓ html:  reports/acme_corp_cmmc2.html
  ✓ poam:  reports/acme_corp_cmmc2.poam.html
```

- **`report.html`** — Full compliance dashboard your executives and auditors can actually read
- **`poam.html`** — Ready-to-use POAM with findings, remediation steps, and milestone schedule
- **`assessment.json`** — Machine-readable results you can load into any downstream tooling

---

## Time Savings

| Task | Manual Approach | This Tool |
|---|---|---|
| Map controls to NIST 800-171 | 2–3 days | Instant — catalog is built in |
| Calculate SPRS score | 4–8 hours + spreadsheet errors | < 1 second |
| Write POAM for gaps | 1–2 days per assessment | Instant, with milestone dates |
| Build compliance dashboard | Custom report, hours of work | Auto-generated HTML |
| Re-assess after remediation | Start over | Reload JSON, re-run |
| **Total per assessment** | **~1–2 weeks** | **< 10 seconds** |

For MSPs managing 10+ clients, that's the difference between compliance being a revenue stream and a time sink.

---

## Installation

```bash
git clone https://github.com/tkhemraj/cmmc2.git
cd cmmc2
pip install -e .
```

No external dependencies. Pure Python 3.9+. Runs on any machine.

---

## Usage

### Run a full assessment
```bash
cmmc2 assess --customer "Your Company" --level 2 --all --output-dir ./reports
```

### Single format
```bash
cmmc2 assess --customer "Your Company" --format html --output report.html
```

### Re-generate reports from a saved assessment
```bash
cmmc2 report --input assessment.json --format poam --output poam.html
cmmc2 report --input assessment.json --format html --output dashboard.html
```

### From Python
```python
from cmmc2 import CMMCAssessor

assessor = CMMCAssessor("Acme Corp", target_level=2)
assessment = assessor.assess()
assessor.print_summary()

assessor.export("html", "dashboard.html")
assessor.export("poam", "poam.html")
assessor.export("json", "assessment.json")
```

---

## The 14 CMMC Domains Covered

| Domain | Practices | Key Controls |
|---|---|---|
| **AC** — Access Control | 22 | Least privilege, MFA, remote access, session management |
| **AT** — Awareness & Training | 3 | Security awareness, role-based training, insider threat |
| **AU** — Audit & Accountability | 9 | Event logging, audit review, time sync, log protection |
| **CM** — Configuration Management | 9 | Baseline configs, change control, least functionality |
| **IA** — Identification & Authentication | 11 | MFA, password policy, account management, FIPS crypto |
| **IR** — Incident Response | 3 | IR capability, incident reporting, IR testing |
| **MA** — Maintenance | 6 | Controlled maintenance, remote maintenance MFA |
| **MP** — Media Protection | 9 | Media sanitization, encryption, removable storage |
| **PE** — Physical Protection | 6 | Physical access, visitor control, alternate work sites |
| **PS** — Personnel Security | 2 | Background checks, termination procedures |
| **RA** — Risk Assessment | 3 | Risk assessments, vulnerability scanning, remediation |
| **CA** — Security Assessment | 4 | Control assessments, POAM, continuous monitoring, SSP |
| **SC** — System & Communications | 16 | Boundary protection, encryption in transit, FIPS crypto |
| **SI** — System & Information Integrity | 7 | Patching, AV/EDR, vulnerability scanning, monitoring |

---

## What Makes This Different

**Other tools** give you a spreadsheet, a checklist, or a $50k consulting engagement.

**This tool** gives you:
- A running score you can track over time as you remediate gaps
- Evidence capture baked into every automated check
- A POAM your C3PAO auditor will actually respect
- The exact SPRS number you need to self-report to the DoD's SPRS system
- All of it in under 10 seconds, repeatable on every assessment cycle

---

## Need Help With Your CMMC Compliance?

This tool is the foundation. The implementation is where organizations get stuck.

**Tarique Khemraj** is an MSP compliance specialist who helps defense contractors and their managed service providers get to CMMC Level 2 certification — from initial assessment through remediation, documentation, and C3PAO audit preparation.

**What I can help with:**
- Running this assessment against your actual environment (not demo data)
- Remediating the gaps the tool finds — technically and procedurally
- Building your System Security Plan (SSP)
- Preparing your POAM and tracking it to closure
- Getting ready for your C3PAO third-party assessment
- Ongoing compliance management for MSPs managing multiple DoD clients

📧 **t.khemraj@gmail.com**
🐙 **github.com/tkhemraj**

> If your MSP is managing DoD contractor clients and CMMC is on the roadmap — reach out. This is what I do.

---

## License

MIT — use it, fork it, build on it.

---

*Built for the defense industrial base. NIST SP 800-171 Rev 2. CMMC 2.0 Model. DoD Assessment Methodology.*
