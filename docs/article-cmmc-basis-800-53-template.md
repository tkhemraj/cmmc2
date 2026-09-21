# CMMC as the basis, 800-53 as the depth, and a template when no one is watching

Clients did not ask for a new religion.

They already liked the CMMC 2.0 shape: 110 practices, 14 families, a score a CFO can read, a POA&M you can work in order. That is why the tooling exists. Run the assessment, get SPRS, get the holes, stop guessing.

Then they asked the question that actually costs money.

What if the people who have to live with those controls are deployed without oversight — a small contractor site, a dual-use aerospace cell, a civilian shop that will never see a C3PAO, a pilot that is really a laptop and a model? What do they implement when there is no assessor in the room, and how do they do it without buying a GRC platform that costs more than the work?

That is a control problem and a cost problem. Treat only one and you fail the other.

## Why CMMC was the right basis

NIST SP 800-53 is the parent catalog. It is large on purpose: families, baselines, overlays, organization-defined parameters. Correct for a federal system with a named authorizing official.

Most of the people who called did not have that. They had CUI or something that behaves like it, a deadline, and staff with day jobs. CMMC Level 2 — 800-171 Rev 2, 110 requirements — is 800-53 cut down to what a nonfederal company must do to protect someone else’s information. Clients got fluent in that cut first. That is the right order. You cannot “do 800-53” if you cannot name the 14 families and say which of the 110 you actually implemented.

Once they could walk AC, IA, AU, SC, CM, RA, and CA in English, 800-53 stopped looking like a wall of identifiers. Access Control is still Access Control. Identification and Authentication is still how you know the user — or the process acting for the user. System and Communications Protection is still the boundary and the crypto. 800-171 `3.13.11` and the 800-53 SC-8 / SC-13 conversation are the same fight: sensitive data rides validated cryptography, or it does not ride.

That is what they meant by liking CMMC as the basis. Not that CMMC replaces 800-53. That CMMC is the on-ramp that makes 800-53 usable.

## What they asked for next

Three things, every time.

A map from the 110 to AI RMF so private models and public LLMs were not a second program. An agent is a process on behalf of a user. A vendor API is an external system. A prompt is a CUI flow. That map is in the repo. Exempt it when there is no AI. Do not exempt `AC.L1-3.1.1` because someone named the process ChatGPT.

Enough 800-53 literacy to talk to a prime, a civilian CISO, or an aerospace quality group that does not live in SPRS. They do not need every enhancement. They need to know `3.1.1` sits on AC-2 / AC-3, logging is AU, crypto is SC, assessment and the POA&M are CA. That is enough to survive “we are a moderate baseline shop” when your team only speaks CMMC IDs.

A template they can run when nobody is coming to grade them. That is the cost conversation.

## Unsupervised is the normal case

The brochure assumes an assessor and a budget line. The field is a site lead, an MSP who bills by the hour, and a model someone enabled after a demo.

Two failures show up.

Control: people implement what is convenient. MFA on email, nothing on the vector database. TLS to the website, plaintext to the model API. An SSP that lists servers and does not list Copilot. You cannot oversee what you refused to name.

Cost: people buy tools to feel overseen. A GRC seat, an AI-governance platform, a SIEM they cannot staff, three vendor “AI policies.” None of that implements `3.5.1`. All of it invoices monthly.

The template is the default for that site: implement the 110 in priority order, reuse those rows as LLM guardrails if models exist, speak 800-53 families when the customer does, and do not spend money on a control you cannot evidence.

## What the template actually says

The working copy is [`docs/templates/unsupervised-deployment.md`](templates/unsupervised-deployment.md). CMMC ID, 800-53 family, what good looks like with no one watching, the cheap way there.

Cheap is not free. Cheap is do not pay twice for the same outcome.

Identity first. Unique IDs for people and processes. MFA on anything that sees sensitive data or administers a model. Vault the API keys. AC and IA in both catalogs. Cost: the IdP you already have.

Flow and boundary second. If the data should not leave, it does not leave through a prompt. Default-deny outbound to random model hosts. Public LLM plus CUI is avoid unless you have a tenant you can assess for crypto and no-train. AC flow, SC boundary. Cost: firewall and allowlist — not a prompt-security startup on day one.

Logs third. If you cannot say who asked which model to touch which corpus, you have folklore. AU in both catalogs. Cost: existing pipeline plus metadata — principal, model, destination. Prompt bodies are sensitive. Do not hoard them to feel compliant.

Crypto fourth. `3.13.11` is the sentence vendors hate. CUI still wants FIPS-validated cryptography. Most public LLMs fail it. That is “do not send the data,” not a white paper. Paying for narrative does not validate a module.

Inventory and change fifth. Model, corpus, system prompt, plugins are configuration items. Missing from the CMDB and the SSP means unassessed. CM and CA. A spreadsheet is legal. A $40k GRC seat is optional.

Risk and incidents depend on the rest. Name AI uses in the risk assessment you already owe. Put “CUI in a vendor prompt log” in the IR plan. RA, CA, IR. An extra page, not a new register product.

Extras CMMC will not emit stay short: one page of allowed and banned AI, a named owner, a purpose line, one retrieval-leak test, a no-train clause. Same POA&M. A second tracker is how unsupervised sites lose the plot.

## Cost without the theater

Unsupervised does not mean unfunded. It means the person on site defends every dollar to someone who does not speak control IDs.

Buy evidence, not narratives. If a tool does not produce an artifact you can hang on a CMMC practice — config, log, screenshot, clause — it is a newsletter. If two tools evidence the same practice, keep the one staff already live in. If the control is “do not put CUI in the public model,” the implementation is an allowlist and a policy, not a broker in front of an endpoint you should not use.

Time is the other bill. Assessor-less sites fail because they spent the quarter choosing a framework. CMMC first, 800-53 families as translation, AI RMF as an optional map, template as the default when nobody is coming. That sequence is the cost control. Everything else is a meeting.

MSPs feel it across ten clients. One catalog, one POA&M shape, one exemption sentence when there is no AI, one guardrail page when there is a private model and a public toy. Repeatable work is cheaper than custom philosophy.

## Who it is for

DoD contractors already on Level 2 — same language, model written into the boundary.

Aerospace and dual-use teams — one engineering system, CUI on the program, commercial data on the product. 800-171 to the program office, 800-53 families to civilian quality. Same locks.

Civilian companies with no SPRS obligation — ignore the score if you want. Keep the 14 families and the STRONG rows. Enough to stop treating a prompt as if it were not a data flow.

The unsupervised site — the point of the template. Default posture, cheap evidence, no second religion.

## What I will not pretend

800-53 literacy and a template do not mean the tool now scores 800-53 baselines or issues an ATO. CMMC is still what it scores. The map and the template are so someone who liked the 110 as a basis can go deeper when a customer talks 800-53, and cheaper when there is no customer in the building.

AI RMF GOVERN 3 and GOVERN 5 still have no honest CMMC analogue. Do not fake them. Model red-team is not a vuln scan. No-train is not `AC.L1-3.1.20` by itself. Those stay extras because unsupervised teams skip them, not because CMMC started requiring them.

The assessment tool, the AI RMF crosswalk, the public-versus-private guardrail page, the exemption rules, and the unsupervised template are in the same repo. Use the layer you need. Exempt the rest. That is the point of a basis instead of a stack you never finish.
