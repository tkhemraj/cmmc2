# Scope and exemption

The AI RMF material in this repo is **in scope by default only when AI is in the environment**. It is not a CMMC Level 2 practice. A C3PAO will not fail you for skipping GOVERN/MAP/MEASURE/MANAGE if no model exists. They will fail you if a model exists and CUI still hits `AC.L1-3.1.1`, `AC.L1-3.1.20`, or `SC.L2-3.13.11`.

## Mark the AI layer N/A when all of these are true

- No hosted or vendor LLM, Copilot-class assistant, RAG, agent, or embedding pipeline
- Acceptable-use / DLP already blocks staff from pasting work data into public chatbots, and that control is tested
- No plans in the current SSP period to add the above

Write one line in the SSP: *"No AI systems in the authorization boundary. Public LLM use prohibited for FCI/CUI. Revisit at next SSP update."* That is the exemption. Revisit it. Shadow AI is how exemptions rot.

## Keep the AI layer in scope when any of these are true

- Private model, fine-tune, or vector index on organizational data
- Public or multi-tenant LLM (API, ChatGPT Enterprise, Copilot, Claude, Gemini) reachable from a CUI or FCI workstation
- Agents or RPA that call tools against files, tickets, or mail
- Aerospace / dual-use: same engineering system serves a DoD program and a commercial product line
- Civilian company with no CMMC contract that still wants a control language for LLM guardrails

## Dual-use and civilian use

Aerospace primes and suppliers often have one network story and two customers. The 110 practices still protect CUI on the DoD side. The same identities, logs, crypto, and change control are the guardrails on the civilian side. You do not owe a C3PAO an AI RMF score. You do owe both sides an answer to “what is allowed to see this file.”

Civilian companies can use the crosswalk without pretending they are in the DIB. Read STRONG rows as “these are the controls that actually constrain a model.” Ignore SPRS if you do not report it. Keep the POA&M idea: one list of gaps, not a second GRC tool.

## Do not exempt piecemeal

Exempt the *layer*, or keep it. Do not mark `AC.L1-3.1.20` N/A because “it is just ChatGPT” while CUI workstations have outbound HTTPS. That is not an exemption. That is an external system you refused to name.
