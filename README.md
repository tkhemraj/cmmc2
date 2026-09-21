# CMMC 2.0 Compliance Assessment Tool

> **Stop guessing. Start scoring.**
> Open-source CMMC 2.0 self-assessment: official DoD SPRS score and a ready-to-submit POAM in under 10 seconds.
>
> Optional NIST AI RMF map for guardrails on private and public LLMs. Exempt it when AI is not in the mix.

**Docs:** [docs/](docs/) · **AI map:** [mappings/](mappings/) · **Guardrails:** [docs/guardrails.md](docs/guardrails.md) · **When to skip AI:** [docs/scope-and-exemption.md](docs/scope-and-exemption.md)

---

## Why This Exists

CMMC 2.0 is not optional for DoD contractors who handle **Controlled Unclassified Information (CUI)**. You need all 110 practices from **NIST SP 800-171 Rev 2** or you lose eligibility.

Most organizations spend weeks in spreadsheets mapping 14 domains, guessing an SPRS score, and writing a POAM an auditor will reject.

This tool does that work. Clients then asked the next question: *how do we constrain private models and public LLMs with the same control language, without standing up a second GRC program?* The [mappings/](mappings/) and [docs/](docs/) tree is that answer. It is guidance reused from the 110 — not a second score. If the client has no AI, mark the layer N/A and move on.

Same controls also travel. Aerospace shops that sit between DoD programs and civilian product lines, and civilian companies that will never see a C3PAO, can use the STRONG rows as LLM guardrails without pretending they are in the DIB.

---

## What It Does

| Feature | Details |
|---|---|
| **Full Practice Catalog** | All 110 NIST SP 800-171 Rev 2 practices across 14 CMMC domains, official CMMC IDs (e.g. `AC.L1-3.1.1`) |
| **SPRS Score** | Official DoD Supplier Performance Risk System score (-203 to 110) using DoD Assessment Methodology weights |
| **Level Determination** | Level 0 / 1 / 2 vs target |
| **POAM Generation** | DoD-style Plan of Action & Milestones with milestone dates — HTML and CSV |
| **HTML Dashboard** | Domain score bars, color-coded findings, evidence table |
| **Per-Domain Scoring** | AC, AT, AU, CM, IA, IR, MA, MP, PE, PS, RA, CA, SC, SI |
| **Evidence Tracking** | Automated checks log evidence for the auditor walkthrough |
| **JSON Round-Trip** | Save and reload assessments |
| **Optional AI RMF layer** | 110 practices mapped to GOVERN / MAP / MEASURE / MANAGE for private and public LLM guardrails. Exempt if AI is not in scope. |

---

## Optional: CMMC → NIST AI RMF (LLM guardrails)

This tool **scores CMMC**. It does not score AI RMF.

When a private model, public LLM, Copilot-class assistant, or agent can see CUI, FCI, or other sensitive data, the same 110 practices are the guardrails:

- the model is a **process** (`AC.L1-3.1.1`)
- the vendor is an **external system** (`AC.L1-3.1.20`)
- the agent needs an **identity** (`IA.L1-3.5.1`)
- calls need **logs** (`AU.L2-3.3.1`)
- CUI still needs **FIPS crypto** (`SC.L2-3.13.11`)
- the model belongs in the **SSP and POAM** (`CA.L2-3.12.4`, `CA.L2-3.12.2`)

If there is no AI in the authorization boundary, **exempt the layer**. Write one SSP sentence and test that staff cannot paste CUI into a browser chatbot. Do not invent an AI program.

- [mappings/README.md](mappings/README.md) — how to read the map
- [mappings/cmmc-to-ai-rmf.csv](mappings/cmmc-to-ai-rmf.csv) — 110 → AI RMF
- [mappings/ai-rmf-to-cmmc.csv](mappings/ai-rmf-to-cmmc.csv) — reverse
- [mappings/additional-controls.md](mappings/additional-controls.md) — extras CMMC will not emit
- [docs/guardrails.md](docs/guardrails.md) — public vs private LLM
- [docs/scope-and-exemption.md](docs/scope-and-exemption.md) — N/A rules

Join a `cmmc2` NOT MET list to the practice CSV and filter `Strength = STRONG`. That is the joint POA&M.

---

## The Output

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
============================================================

  ✓ json:  reports/acme_corp_cmmc2.json
  ✓ html:  reports/acme_corp_cmmc2.html
  ✓ poam:  reports/acme_corp_cmmc2.poam.html
```

- **`report.html`** — dashboard executives and auditors can read
- **`poam.html`** — findings, remediation, milestones
- **`assessment.json`** — reload into downstream tooling

---

## Time Savings

| Task | Manual | This tool |
|---|---|---|
| Map controls to NIST 800-171 | 2–3 days | Instant |
| Calculate SPRS score | 4–8 hours | < 1 second |
| Write POAM | 1–2 days | Instant |
| Compliance dashboard | Custom report | Auto HTML |
| Re-assess after remediation | Start over | Reload JSON |
| **Total per assessment** | **~1–2 weeks** | **< 10 seconds** |

For MSPs with 10+ clients, that is compliance as a workstream instead of a time sink.

---

## Installation

```bash
git clone https://github.com/tkhemraj/cmmc2.git
cd cmmc2
pip install -e .
```

No external dependencies. Pure Python 3.9+.

---

## Usage

```bash
cmmc2 assess --customer "Your Company" --level 2 --all --output-dir ./reports
cmmc2 assess --customer "Your Company" --format html --output report.html
cmmc2 report --input assessment.json --format poam --output poam.html
```

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

## The 14 CMMC Domains

| Domain | Practices | Key controls |
|---|---|---|
| **AC** Access Control | 22 | Least privilege, remote access, CUI flow |
| **AT** Awareness & Training | 3 | Awareness, role training, insider threat |
| **AU** Audit & Accountability | 9 | Logs, review, time sync |
| **CM** Configuration Management | 9 | Inventory, change control, least functionality |
| **IA** Identification & Authentication | 11 | Identity, MFA, authenticators |
| **IR** Incident Response | 3 | Capability, reporting, tests |
| **MA** Maintenance | 6 | Controlled and remote maintenance |
| **MP** Media Protection | 9 | Sanitize, encrypt, removable media |
| **PE** Physical Protection | 6 | Facility and alternate sites |
| **PS** Personnel Security | 2 | Screening, termination |
| **RA** Risk Assessment | 3 | Assess, scan, remediate |
| **CA** Security Assessment | 4 | Assess, POAM, monitor, SSP |
| **SC** System & Communications | 16 | Boundary, TLS, FIPS, at rest |
| **SI** System & Information Integrity | 7 | Patch, malware, monitor, unauthorized use |

---

## Need Help

The tool is the foundation. Implementation is where organizations get stuck.

**Tarique Khemraj** — MSP compliance work for defense contractors and providers getting to CMMC Level 2: assessment against the real environment, remediation, SSP, POAM, C3PAO prep, and optional LLM guardrail scope for dual-use and civilian shops.

📧 **t.khemraj@gmail.com**
🐙 **github.com/tkhemraj/cmmc2**

---

## License

MIT — use it, fork it, build on it.

---

*NIST SP 800-171 Rev 2. CMMC 2.0. DoD Assessment Methodology. NIST AI RMF 1.0 map is optional guidance, not a substitute for either framework.*
