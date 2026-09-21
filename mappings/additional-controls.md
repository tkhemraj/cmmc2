# The controls CMMC does not score — and why they matter when AI can see CUI

CMMC Level 2 is 110 NIST SP 800-171 Rev 2 practices. That catalog protects Federal Contract Information and Controlled Unclassified Information on contractor systems. It is necessary. It is not an AI governance program.

NIST AI RMF 1.0 asks four questions CMMC never asks in those words: who owns model risk, what is this system *for*, how do you *measure* the model, and what do you do when the model is the incident. The `cmmc2` tool will give you an SPRS score and a POA&M. It will not invent those answers.

This article is about the **additional** work — the AI RMF outcomes you still owe after every CMMC practice is MET — and why skipping them is how CUI leaves through a prompt instead of a USB stick.

The machine-readable map lives in [`mappings/`](.). Use that to join a NOT MET list to GOVERN / MAP / MEASURE / MANAGE. Use this to decide what to write that CMMC will never grade.

---

## First: what you already have

Do not rebuild identity, logging, crypto, and change control under an “AI” label. You already score them.

| If the model or agent can touch CUI | CMMC practice you already owe |
|---|---|
| The agent is a process acting on behalf of a user | `AC.L1-3.1.1` |
| The commercial LLM is an external system | `AC.L1-3.1.20` |
| CUI moves in a prompt, completion, or retrieval | `AC.L2-3.1.3` |
| The agent needs an identity, not a shared “chatgpt” account | `IA.L1-3.5.1` |
| API keys are authenticators | `IA.L2-3.5.10` |
| You can reconstruct who asked what, of which model | `AU.L2-3.3.1`, `AU.L2-3.3.2` |
| Models, plugins, and vector stores are in inventory | `CM.L2-3.4.1` |
| System prompt, corpus, and tool schema are change-controlled | `CM.L2-3.4.3` |
| CUI in transit or at rest still needs FIPS-validated crypto | `SC.L2-3.13.8`, `SC.L2-3.13.11`, `SC.L2-3.13.16` |
| The SSP names the model and the vendor | `CA.L2-3.12.4` |
| Gaps go on the same POA&M | `CA.L2-3.12.2` |

If those are NOT MET, stop. You do not have an AI problem. You have a CMMC problem that an LLM will make louder.

`SC.L2-3.13.11` is the hard stop most people want to talk around. If CUI is in the prompt or the index, FIPS-validated cryptography still applies. Most public SaaS models fail that control. That is a CMMC fail. Calling the same system “an AI pilot” does not change the assessment objective.

---

## What “additional” actually means

AI RMF is voluntary. CMMC, for covered contracts, is not. The extra controls are additional in the sense that **a perfect SPRS score can still leave you unable to answer a board, a prime, or a customer who asks how you govern the model.**

They cluster in five places.

### 1. An AI-use policy is not an SSP

**AI RMF:** GOVERN 1 — policies and processes for mapping, measuring, and managing *AI* risk.

**What CMMC gives you:** `CA.L2-3.12.4` wants a System Security Plan. That plan describes the authorization boundary, the CUI flow, and the 110 practices.

**What it does not give you:** a written decision about which models exist, who may put CUI in a prompt, which tools the model is allowed to call, and what is banned (public chatbots, training on your data, shadow Copilot tenants).

Why it matters: assessors and customers will ask “is this allowed?” before they ask “is TLS on?” Without a policy, every engineer invents an answer. That is how drawings land in a consumer chatbot on a Sunday night. The SSP can *attach* the AI-use policy. It cannot replace it.

Write, at minimum: approved systems, prohibited systems, CUI handling rule (default deny into any model that is not in the CUI enclave), owner of each system, and the exception process.

### 2. A named owner, not a shared mailbox

**AI RMF:** GOVERN 2 — accountability and a workforce that can actually do the job.

**What CMMC gives you:** personnel screening (`PS.L2-3.9.1`), offboarding (`PS.L2-3.9.2`), role training (`AT.L2-3.2.2`).

**What it does not give you:** a human who is accountable for *this model* — promote rights, corpus changes, vendor SKU changes — and training that is about prompts, retrieval, and tool-use rather than annual phishing.

Why it matters: when a completion contains CUI and the ticket says “the AI did it,” you need a name. Shared service accounts already fail `IA.L1-3.5.1`. Shared responsibility fails GOVERN 2 the same way. Offboarding that kills VPN but leaves a vendor API key in a teammate’s laptop is how residual access survives the HR ticket.

### 3. Inventory with purpose — not just a CMDB row

**AI RMF:** MAP 1, MAP 2, MAP 3 — context, categorization, capability versus limits.

**What CMMC gives you:** `CM.L2-3.4.1` inventory and baselines. `CM.L2-3.4.6` least functionality.

**What it does not give you:** intended purpose, prohibited uses, risk tier (CUI-touch vs public FAQ bot), and a plain-language list of what the system cannot do.

Why it matters: “We have Copilot” is not a map. Copilot-on-mail is a different system from a RAG box sitting on ITAR PDFs. If you do not write the purpose, nobody can tell a legitimate summary from a bulk exfil that looks like a summary. Least functionality (`CM.L2-3.4.6`) is the closest CMMC analogue — disable tool-use, code execution, and web browse if the use case does not need them — but it does not record *why* the system exists. That sentence is what MAP 1 is for.

Shadow AI is the practical failure mode. `SI.L2-3.14.7` (unauthorized use) and `CM.L2-3.4.9` (user-installed software) will find some of it. They will not find it if you never defined authorized.

### 4. Impacts CMMC was never written to score

**AI RMF:** MAP 5 — impacts to people, organizations, and society. MEASURE 2 — test, evaluate, verify, validate the *system you mapped*.

**What CMMC gives you:** `RA.L2-3.11.1` periodic risk assessment. `RA.L2-3.11.2` vulnerability scans. `CA.L2-3.12.1` control assessment. `IR.L2-3.6.3` IR tests.

**What it does not give you:** jailbreak rate, retrieval-leak rate, grounding tests against CUI facts, output-filter tests, or any evaluation of bias, safety, or group harm.

Why it matters: a clean Qualys scan on the inference host says nothing about whether the model will quote an export-controlled paragraph when asked to “summarize the folder.” Vulnerability management is necessary. It is the wrong instrument for model behavior.

If you only do CMMC TEVV, you will discover the leak in production, then discover that your IR playbook (`IR.L2-3.6.1`) has no row for “CUI in a vendor prompt log.” That is a DFARS incident with a new packet shape. The reporting clock does not care that the packet was a JSON completion.

Extend `RA.L2-3.11.1` so the existing risk assessment *names* AI uses. Then add tests CMMC will not run: can an unauthorized role retrieve CUI through the model, can a prompt bypass the output filter, does a corpus change alter what leaves the boundary. Put failures on the same POA&M. Do not invent a second tracker.

### 5. The vendor contract is the control

**AI RMF:** GOVERN 6 and MANAGE 3 — third-party data, models, APIs, residual vendor risk.

**What CMMC gives you:** `AC.L1-3.1.20` (connections to external systems), `AC.L2-3.1.14` (managed access points), `IA.L2-3.5.10` (protect authenticators), `SC.L2-3.13.11` (FIPS), `MA.L2-3.7.2` / `3.7.5` (who maintains the box).

**What it does not give you:** “you will not train on our CUI,” “you will purge on demand,” “you will name subprocessors,” “you will tell us when the base model changes,” “we can test before you ship a new SKU.”

Why it matters: the model vendor is now in your CUI flow. A MET score on `AC.L1-3.1.20` means you *authorized the connection*. It does not mean the other side is forbidden from using the prompt as training data. That sentence lives in the contract and in the architecture (private tenant, no-train endpoint, or keep CUI out of the prompt entirely).

If you cannot get FIPS and no-train, the honest control is **avoid**: do not put CUI in that model. That is a MANAGE 2 decision. Write it down. “We will use the public API for marketing copy only” is a control. “Everyone has a key and we will be careful” is not.

---

## Two categories you should not fake

**GOVERN 3** (diversity, equity, inclusion, and accessibility in the AI workforce) and **GOVERN 5** (engagement of affected stakeholders) have no honest CMMC analogue. Do not map personnel screening (`PS.L2-3.9.1`) to DEI. Do not map incident notification (`IR.L2-3.6.2`) to stakeholder engagement. If those AI RMF categories are in scope for a customer or a state law, they are a separate workstream. Lying in the crosswalk helps no one at assessment time.

---

## Why this order exists

The useful sequence is not “get the AI cert, then sprinkle CMMC.” It is the reverse.

1. Score the 110. `cmmc2 assess` exists so that step is not a two-week spreadsheet.
2. Join NOT MET rows to `cmmc-to-ai-rmf.csv`. Filter `Strength = STRONG`. That is the joint POA&M.
3. Write the five additional artifacts CMMC will not emit: AI-use policy, named owners, purpose and tier per system, model tests, vendor clauses.
4. Put AI systems in the SSP boundary so the next assessment does not pretend the model is outside the system.

People skip step 1 because AI governance sounds newer. The leak path does not care. An unauthorized process (`AC.L1-3.1.1`), an unmanaged external connection (`AC.L1-3.1.20`), and an unencrypted prompt (`SC.L2-3.13.8` / `3.13.11`) are the same three failures whether the accessor is a person or a model.

The additional controls matter because they are how you *notice* that the accessor changed. CMMC tells you the door is locked. AI RMF is the part where you admit a new kind of key exists, write down what it is allowed to open, and test whether it opens anything else.

---

## What to put on the POA&M this week

If you handle CUI and anyone in the company can reach a model:

- [ ] SSP lists every model, vendor, and CUI flow (`CA.L2-3.12.4`)
- [ ] No CUI to any endpoint that fails FIPS or trains on customer data (`SC.L2-3.13.11` + contract)
- [ ] Agents and API principals have unique identities; keys are vaulted (`IA.L1-3.5.1`, `IA.L2-3.5.10`)
- [ ] Inference events are logged and attributable (`AU.L2-3.3.1`, `AU.L2-3.3.2`)
- [ ] IR playbook has a row for CUI in a prompt or vendor log (`IR.L2-3.6.1`)
- [ ] One page: approved AI, banned AI, owner names (GOVERN 1 / 2 — extra)
- [ ] One test: can the model retrieve CUI the caller is not allowed to open? (MEASURE 2 — extra)

The first five are CMMC. The last two are the additional controls. Both lists belong on the same POA&M. Split trackers are how things get lost.

Repo: [github.com/tkhemraj/cmmc2](https://github.com/tkhemraj/cmmc2)

*Informational. Not official NIST or DoD guidance. CMMC 2.0 / NIST SP 800-171 Rev 2 still governs CUI. AI RMF 1.0 does not replace it.*
