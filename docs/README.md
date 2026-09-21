# Documentation

`cmmc2` scores **CMMC 2.0 / NIST SP 800-171 Rev 2** (110 practices, SPRS, POAM).

An optional **NIST AI RMF 1.0** layer sits next to that score. Use it when the client has private models, public LLMs, agents, or Copilot-class tools that can see CUI, FCI, or other sensitive data. **Exempt it** when AI is truly not in the mix — do not invent an AI program for a shop that does not have one.

## Start here

| Doc | What it is |
|---|---|
| [../README.md](../README.md) | Install, assess, SPRS, POAM |
| [../mappings/README.md](../mappings/README.md) | How the CMMC ↔ AI RMF crosswalk works, when to skip it |
| [../mappings/cmmc-to-ai-rmf.csv](../mappings/cmmc-to-ai-rmf.csv) | All 110 practices → AI RMF function / strength |
| [../mappings/ai-rmf-to-cmmc.csv](../mappings/ai-rmf-to-cmmc.csv) | Start from GOVERN / MAP / MEASURE / MANAGE |
| [../mappings/additional-controls.md](../mappings/additional-controls.md) | Controls CMMC will not score, and why they matter |
| [guardrails.md](guardrails.md) | Private vs public LLM guardrails built from the same 110 |
| [scope-and-exemption.md](scope-and-exemption.md) | Who this is for, when to mark AI N/A |
| [templates/unsupervised-deployment.md](templates/unsupervised-deployment.md) | Site template when there is no assessor |
| [article-cmmc-basis-800-53-template.md](article-cmmc-basis-800-53-template.md) | Why CMMC is the basis, 800-53 as translation |

## Who this is for

- DoD contractors and MSPs already on a CMMC path
- Adjacent aerospace (Long Beach / LA basin and like it): DoD-aligned companies that do **not** require TS or Secret for most staff, but sell next to cleared primes. Aligning to counterpart controls helps civilian products and services land.
- Dual-use shops that sit between DoD work and civilian product lines
- Civilian companies that will never see a C3PAO but still need a control language that is not a 200-page consulting deck
- Sites deployed without oversight — control and cost

CMMC remains the scored framework. AI RMF is guidance reused from those controls, plus a short list of extras (policy, owners, purpose, model tests, vendor clauses).
