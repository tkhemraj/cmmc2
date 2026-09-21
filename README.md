# CMMC 2.0 Compliance Assessment Tool

> **Stop guessing. Start scoring.**
> Open-source CMMC 2.0 self-assessment: official DoD SPRS score and a ready-to-submit POAM in under 10 seconds.
>
> Optional NIST AI RMF map for guardrails on private and public LLMs. Exempt it when AI is not in the mix.

**Docs:** [docs/](docs/) · **AI map:** [mappings/](mappings/) · **Guardrails:** [docs/guardrails.md](docs/guardrails.md) · **When to skip AI:** [docs/scope-and-exemption.md](docs/scope-and-exemption.md) · **Unsupervised template:** [docs/templates/unsupervised-deployment.md](docs/templates/unsupervised-deployment.md)

---

## Why This Exists

CMMC 2.0 is not optional for DoD contractors who handle **Controlled Unclassified Information (CUI)**. You need all 110 practices from **NIST SP 800-171 Rev 2** or you lose eligibility.

Most organizations spend weeks in spreadsheets mapping 14 domains, guessing an SPRS score, and writing a POAM an auditor will reject.

This tool does that work. Clients then asked the next question: *how do we constrain private models and public LLMs with the same control language, without standing up a second GRC program?* The [mappings/](mappings/) and [docs/](docs/) tree is that answer. It is guidance reused from the 110 — not a second score. If the client has no AI, mark the layer N/A and move on.

Same controls also travel. Built from work in Long Beach with DoD-aligned aerospace that is **adjacent**, not fully cleared — no TS or Secret required for most employees — and still selling civilian products and services next to primes who *do* run 800-171 and 800-53. Knowing those counterpart controls, and lining up to them, is how an uncleared shop stays in the deal without pretending it is a SAP program. Civilian companies that will never see a C3PAO can use the same STRONG rows as LLM guardrails without pretending they are in the DIB.

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
- [docs/templates/unsupervised-deployment.md](docs/templates/unsupervised-deployment.md) — no-assessor template

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

---

## Installation

```bash
git clone https://github.com/tkhemraj/cmmc2.git
cd cmmc2
pip install -e .
```

No external dependencies. Pure Python 3.9+.

---

## Need Help

The tool is the foundation. Implementation is where organizations get stuck.

**Tarique Khemraj** (Long Beach, CA) — CMMC and control alignment for defense contractors **and** adjacent aerospace that is DoD-aligned without being a cleared program: no TS/Secret required for most staff, civilian products and services next to primes who already speak 800-171 / 800-53. Assessment against the real environment, remediation, SSP, POAM, C3PAO prep, optional LLM guardrail scope.

📧 **t.khemraj@gmail.com**
🐙 **github.com/tkhemraj/cmmc2**

---

## License

MIT — use it, fork it, build on it.

---

*NIST SP 800-171 Rev 2. CMMC 2.0. DoD Assessment Methodology. NIST AI RMF 1.0 map is optional guidance, not a substitute for either framework.*
