# Template: deployed without oversight

Use this when there is no C3PAO, no in-house GRC team, and no budget for a second platform. CMMC 2.0 / NIST SP 800-171 Rev 2 is the worklist. NIST SP 800-53 families are the translation layer when a prime or civilian CISO does not speak CMMC IDs. NIST AI RMF is optional — exempt it if there is no model.

Print this. Fill the last two columns. Park gaps on the same POA&M the tool already emits.

## How to spend

| Do | Do not |
|---|---|
| Evidence a CMMC ID with a config, log, screenshot, or clause | Buy a tool that only produces a slide |
| Reuse the IdP, firewall, and log pipe you already run | Stand up a SIEM you cannot staff |
| Spreadsheet CMDB + SSP attachment | $40k GRC seat for one site |
| Allowlist + policy for public LLMs | Prompt-security broker in front of an endpoint you should not use |
| One POA&M | A second "AI tracker" |

## Pass order (control and cost)

Do these families first. They close the most leak paths per hour.

| Order | CMMC families | 800-53 families | Unsupervised "good" | Cheap evidence |
|---|---|---|---|---|
| 1 | IA, AC | IA, AC | Unique IDs for people **and** processes; MFA on data and model admin; vaulted API keys; least privilege on any corpus a model can retrieve | IdP reports, group membership, key vault ACL, no shared `chatgpt` account |
| 2 | SC, AC (flow / external systems) | SC, AC | Default-deny outbound to random model hosts; CUI does not ride a public LLM unless FIPS + no-train are real; private model stays in an enclave | Firewall allowlist, proxy logs, architecture diagram, vendor contract page |
| 3 | AU | AU | You can say who called which model, when, toward which dest. Prompt bodies are CUI — metadata first | Existing SIEM/log store + gateway fields (principal, model ID, dest) |
| 4 | CM, CA | CM, CA | Model, corpus, system prompt, plugins are inventory items and sit in the SSP | Spreadsheet CMDB, SSP section, change ticket on prompt/corpus edits |
| 5 | RA, IR, SI | RA, IR, SI, SR | Risk assessment names AI uses; IR has a row for CUI in a vendor log; watch unauthorized / shadow use | Updated RA page, IR playbook row, egress report |

Then AT, PS, MP, MA, PE as the site already owes them. Do not skip PS offboarding of API keys.

## 800-171 → 800-53 family crib (so you can talk to both rooms)

This is a crib, not a complete overlay. 800-171 requirements derive from 800-53; primes who say "moderate baseline" mean the parent family.

| 800-171 family | Speak this 800-53 family | Notes for unsupervised sites |
|---|---|---|
| 3.1 AC | AC | `3.1.1` ≈ AC-2 / AC-3 — processes count. `3.1.20` ≈ CA-3 / AC-20 — the public LLM is an external system |
| 3.2 AT | AT | Role training for anyone who prompts or administers a model |
| 3.3 AU | AU | AU-2 / AU-3 / AU-12 — attributable inference events |
| 3.4 CM | CM | CM-2 / CM-3 / CM-8 — inventory the model |
| 3.5 IA | IA | IA-2 / IA-4 / IA-5 — keys are authenticators |
| 3.6 IR | IR | IR-4 / IR-6 — CUI in a prompt log is still an incident |
| 3.7 MA | MA | Vendor on your GPU box is maintenance |
| 3.8 MP | MP | Indexes, checkpoints, prompt stores are media |
| 3.9 PS | PS | Kill model and API access the day they leave |
| 3.10 PE | PE | Only if you host inference on-prem |
| 3.11 RA | RA | RA-3 / RA-5 — name AI uses; scans ≠ model tests |
| 3.12 CA | CA | CA-2 / CA-5 / CA-7 — SSP + POA&M + monitor |
| 3.13 SC | SC | SC-7 / SC-8 / SC-13 / SC-28 — boundary, transit, FIPS, at rest |
| 3.14 SI | SI | SI-4 unauthorized use = shadow AI |

## Site header (fill once)

```
Site / program:
Authorization boundary (one paragraph):
CUI / FCI / other sensitive data in scope?  Y/N
AI in scope?  Y / N / revisit date:
If N, SSP sentence: "No AI systems in the authorization boundary. Public LLM use prohibited for sensitive data. Revisit at next SSP update."
If Y, systems (name, private/public, owner, purpose, data it may see):
1.
2.
IdP / logging / firewall already in place:
Budget cap this quarter (tools + time):
POA&M owner:
```

## Extras CMMC will not score (still do them if AI is in scope)

- [ ] One page: approved AI, banned AI, exception path
- [ ] Named owner per system
- [ ] Purpose and tier (CUI-touch vs public copy)
- [ ] One test: can the model retrieve data the caller cannot open?
- [ ] Vendor: no-train, purge, subprocessor list, notice on model change

Same POA&M as the 110. Not a second list.

## Done looks like

- `cmmc2 assess` has been run against this site
- NOT MET rows are on one POA&M with dates
- If AI is N/A, the SSP sentence exists and outbound to consumer LLM hosts is blocked or monitored
- If AI is in scope, every system has an owner and is named in the SSP
- No tool on the invoice that cannot attach to a CMMC ID
