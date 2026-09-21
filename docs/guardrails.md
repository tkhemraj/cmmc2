# Guardrails on private and public LLMs

Clients asked how to constrain models — not how to buy another framework. The answer in this repo is: reuse the 110 CMMC practices as guardrails, then add a short list CMMC will not write for you.

Private and public models fail in different places. The control IDs do not change.

## Public / multi-tenant LLM (API or consumer SaaS)

Default posture for CUI and FCI: **do not put it in the prompt.**

| Guardrail | CMMC ID | Why |
|---|---|---|
| Treat the vendor as an external system | `AC.L1-3.1.20` | If the workstation can reach it, it is in scope |
| Force traffic through a managed point (gateway, CASB, allowlist) | `AC.L2-3.1.14`, `SC.L2-3.13.6` | Default-deny outbound to random model hosts |
| FIPS-validated crypto or do not send CUI | `SC.L2-3.13.8`, `SC.L2-3.13.11` | Most public endpoints fail FIPS — that is the stop |
| Contract: no-train, purge, subprocessors | extra (GOVERN 6) | `3.1.20` authorizes the pipe; the clause governs the data |
| Unique API identities, vaulted keys | `IA.L1-3.5.1`, `IA.L2-3.5.10` | Shared “chatgpt” keys are not attributable |
| Log metadata of calls (principal, model, dest) | `AU.L2-3.3.1`, `AU.L2-3.3.2` | You cannot investigate a paste you never recorded |
| Banner / policy: no CUI in public models | `AC.L2-3.1.9`, `AT.L1-3.2.1` | Weak alone; required so “nobody told us” dies |
| Output must not publish CUI | `AC.L2-3.1.22` | Public bots and “share this chat” |
| IR row: CUI in a vendor log | `IR.L2-3.6.1` | DFARS clock does not care it was JSON |

If you cannot get FIPS + no-train, the guardrail is **avoid**. Write that as a MANAGE decision, not as hope.

## Private / enclave model (on-prem, VPC, dedicated tenant)

Default posture: **allowed only inside a CUI enclave**, with the model treated as a process on behalf of a user.

| Guardrail | CMMC ID | Why |
|---|---|---|
| Agent / service is an identified process | `AC.L1-3.1.1`, `IA.L1-3.5.1` | No anonymous retriever |
| Least privilege on the corpus | `AC.L2-3.1.5` | The model gets the folder the user may see, not the share |
| CUI flow control on retrieve + complete | `AC.L2-3.1.3` | Retrieval is a flow |
| Isolation from general productivity AI | `SC.L2-3.13.2` | Do not share GPU, index, or prompt store with the public bot |
| Encrypt index, prompt store, checkpoints | `SC.L2-3.13.16`, `MP.L2-3.8.9` | Backups of the vector DB are CUI media |
| Change control on prompt, tools, weights, corpus | `CM.L2-3.4.3`, `CM.L2-3.4.4` | A new plugin is an impact analysis |
| Disable tools the use case does not need | `CM.L2-3.4.6` | No code-exec / web browse “on just in case” |
| MFA on model admin and vector admin | `IA.L2-3.5.3` | Admin plane is the real prize |
| Wipe weights and indexes on retirement | `MP.L2-3.8.3` | Decommission is a control |
| Name it in the SSP | `CA.L2-3.12.4` | Invisible models are unassessed models |

## Extra on both (CMMC will not emit these)

- One-page AI-use policy (approved / banned / exception path)
- Named owner per system
- Purpose and risk tier per system (CUI-touch vs public copy)
- One retrieval-leak test: can the model return CUI the caller cannot open?
- Vendor notice when the base model changes

Those five are the article in [`../mappings/additional-controls.md`](../mappings/additional-controls.md).

## Practical rule

Public LLM + CUI = almost always **avoid** or a dedicated Fed-aligned tenant you can actually assess.
Private LLM + CUI = **enclave**, identity, flow, crypto, change control, SSP.
No LLM at all = **exempt the layer**, write the SSP sentence, test that staff cannot paste CUI into a browser chatbot anyway.
