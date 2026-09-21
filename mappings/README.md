# CMMC 2.0 → NIST AI RMF 1.0

This folder is a **practitioner crosswalk**, not a second assessment engine.

`cmmc2` scores the 110 NIST SP 800-171 Rev 2 practices (CMMC Level 2). NIST AI RMF 1.0 is a voluntary framework: GOVERN, MAP, MEASURE, MANAGE (19 categories, 72 subcategories). When an AI system, agent, or vendor LLM can touch CUI, many of those 110 practices already produce evidence an AI-governance program can reuse.

Implementing CMMC is **not** implementing AI RMF.

## Files

| File | Use |
|---|---|
| [cmmc-to-ai-rmf.csv](cmmc-to-ai-rmf.csv) | All 110 practices → primary AI RMF function/category, strength, AI-touch note, leftover gap |
| [ai-rmf-to-cmmc.csv](ai-rmf-to-cmmc.csv) | Reverse: start from an AI RMF category, land on CMMC IDs you can show |

## Strength

- **STRONG** — direct evidence for that AI RMF category when CUI is in scope
- **PARTIAL** — necessary substrate (identity, logs, crypto, change control); does not satisfy the AI-specific outcome alone
- **GAP** — no CMMC analogue (GOVERN 3, GOVERN 5)

Primary-function split (one primary per practice): MANAGE 47 · GOVERN 28 · MEASURE 18 · MAP 17. Strength: 42 STRONG · 68 PARTIAL.

## Hard rule

`AC.L1-3.1.1` already covers **processes acting on behalf of authorized users**. An agent or tool-calling model that reads CUI is that process. There is no AI exemption.

If CUI is in the prompt or the index, `SC.L2-3.13.11` (FIPS-validated cryptography) still applies. Most public SaaS LLMs fail that control.

## How to use with the CLI

1. Run `cmmc2 assess`.
2. Join NOT MET practices to `cmmc-to-ai-rmf.csv` on `CMMC ID`.
3. Filter `Strength = STRONG`. That list is the joint CMMC / AI-governance POA&M.
4. Anything still open on the reverse sheet (`GAP` or “Still missing”) is work AI RMF requires that CMMC will not score.

## What CMMC will not cover

- GOVERN 3 (DEI in AI roles) and GOVERN 5 (stakeholder engagement)
- MAP 1 / 3 / 5 intended purpose, model limits, societal/bias impact
- MEASURE 2 **on the model** (jailbreak, grounding, retrieval-leak tests are not `RA.L2-3.11.2` vuln scans)
- Vendor contract language: no-train, purge, subprocessors

## Sources

NIST AI RMF 1.0 (AI 100-1). NIST SP 800-171 Rev 2. CMMC 2.0 practice IDs. Informational only — not official NIST or DoD guidance.
