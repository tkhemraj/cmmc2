# CMMC 2.0 → NIST AI RMF 1.0

Optional layer. Not a second scoring engine.

`cmmc2` scores the 110 NIST SP 800-171 Rev 2 practices. This folder maps those practices to NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE) so you can build guardrails on **private and public LLMs** from controls you already owe.

**Exempt this layer** when AI is not in the environment. See [docs/scope-and-exemption.md](../docs/scope-and-exemption.md).

Implementing CMMC is **not** implementing AI RMF. A MET SPRS score does not mean the model is governed.

## Files

| File | Use |
|---|---|
| [cmmc-to-ai-rmf.csv](cmmc-to-ai-rmf.csv) | All 110 practices → primary AI RMF function, category, strength |
| [ai-rmf-to-cmmc.csv](ai-rmf-to-cmmc.csv) | Reverse: start from an AI RMF category |
| [additional-controls.md](additional-controls.md) | What CMMC will not score, and why it still matters |

Related:

- [docs/guardrails.md](../docs/guardrails.md) — private vs public LLM guardrails
- [docs/scope-and-exemption.md](../docs/scope-and-exemption.md) — when to mark N/A
- [docs/README.md](../docs/README.md) — documentation index

## Strength

- **STRONG** — direct evidence for that AI RMF category when sensitive data is in scope
- **PARTIAL** — substrate (identity, logs, crypto, change control); not the AI-specific outcome by itself
- **GAP** — no CMMC analogue (GOVERN 3, GOVERN 5)

Primary-function split: MANAGE 47 · GOVERN 28 · MEASURE 18 · MAP 17. Strength: 42 STRONG · 68 PARTIAL.

## Hard rules

`AC.L1-3.1.1` already covers **processes acting on behalf of authorized users**. An agent that reads CUI is that process. There is no “it is just AI” exemption for that practice.

If CUI is in the prompt or the index, `SC.L2-3.13.11` still applies. Most public SaaS LLMs fail FIPS. That is a CMMC fail, not an AI-policy debate.

The *layer* can be N/A. The practices cannot be N/A if the model exists.

## How to use with the CLI

1. Decide scope ([docs/scope-and-exemption.md](../docs/scope-and-exemption.md)). If no AI, stop after the CMMC assess.
2. `cmmc2 assess`.
3. Join NOT MET practices to `cmmc-to-ai-rmf.csv` on `CMMC ID`.
4. Filter `Strength = STRONG`. That is the joint POA&M for DIB, aerospace dual-use, or civilian LLM guardrails.
5. Read [additional-controls.md](additional-controls.md) for policy, owners, purpose, model tests, and vendor clauses CMMC will not emit.

## Who uses this besides DoD contractors

- Aerospace and other dual-use shops: one engineering system, DoD CUI on one program, commercial data on another. Same identities, logs, and crypto. Different authorization boundary language.
- Civilian companies with no C3PAO in their future: treat STRONG rows as the control list for LLM guardrails. Ignore SPRS if you do not report it. Keep one gap list.

## Sources

NIST AI RMF 1.0 (AI 100-1). NIST SP 800-171 Rev 2. CMMC 2.0 practice IDs. Informational — not official NIST or DoD guidance.
