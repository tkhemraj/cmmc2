# LinkedIn draft — LLM guardrails in the CMMC tooling

Paste-ready. Edit the first person if needed.

---

Clients stopped asking me for another policy deck.

They asked: how do we put guardrails on the models we already have — the private box in the enclave and the public LLM someone opened in a browser — without standing up a second GRC program next to CMMC.

So I wired NIST AI RMF 1.0 into the CMMC tooling I already ship.

Not as a second score. As a map. The 110 NIST SP 800-171 practices CMMC Level 2 already requires are the same controls that constrain a model when it can see CUI, FCI, or anything else you actually care about. Identity. External systems. Flow. Logs. FIPS crypto. Change control. SSP and POA&M. An agent is a process acting on behalf of a user. `AC.L1-3.1.1` already said that. There is no “it is just AI” exemption for the practice.

If AI is truly not in the mix, exempt the layer. One sentence in the SSP. Test that people cannot paste work data into a chatbot anyway. Do not invent a governance program for a shop that does not have a model.

If AI is in the mix, do not invent new language either. Public LLM plus CUI is almost always avoid — or a tenant you can actually assess for FIPS and no-train. Private model plus CUI is an enclave, a named identity, a corpus the caller is allowed to see, and the model written into the SSP so it stops being invisible.

That map is useful past the DIB.

Aerospace and other dual-use shops live on the bridge: DoD program on one side, commercial product line on the other, often the same engineering system. The 110 still protect CUI. The STRONG rows are the guardrails on the civilian side. You do not owe a C3PAO an AI RMF score. You owe both customers an answer to “what is allowed to see this file.”

Civilian companies that will never file SPRS can still use the list. Ignore the score. Keep the gap list. That is the guidance: which controls actually help when a prompt becomes a data flow.

What CMMC will not write for you is short: a one-page allowed/banned policy, a named owner per system, a purpose and tier, one retrieval-leak test, and the vendor clause that says they will not train on your data. Those extras belong on the same POA&M. Split trackers are how this gets lost.

Tool and docs: https://github.com/tkhemraj/cmmc2

Guardrails (public vs private): https://github.com/tkhemraj/cmmc2/blob/master/docs/guardrails.md

When to exempt: https://github.com/tkhemraj/cmmc2/blob/master/docs/scope-and-exemption.md

Crosswalk: https://github.com/tkhemraj/cmmc2/tree/master/mappings
