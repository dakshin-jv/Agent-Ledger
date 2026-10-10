---
type: Competitive Inference
title: FIS Global
description: ARTW #6 ranking artifact. Core banking and AR/AP overlays, not a commerce case ERP.
tags:
- erp
- competitive
- fis
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: artw
  resource: https://www.appsruntheworld.com/top-10-erp-software-vendors-and-market-forecast/
  title: ARTW Top 10 ERP
- id: getpaid
  resource: https://www.fisglobal.com/products/fis-getpaid
  title: FIS GETPAID
- id: treasury
  resource: https://www.fisglobal.com/products/neural-treasury
  title: Neural Treasury
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-category-split
---

# Treat as

**Not a commerce-ERP peer.** ARTW counts **core banking + GETPAID + Integrated Payables** as ERP. Corporates keep SAP/Oracle/NetSuite as SoR; FIS posts and pays. Relevant as a **money rail / treasury** analog.

# AI surface

Neural Treasury / Treasury GPT: assistive forecast, recon, fraud viz. GETPAID: AR email classify and draft replies. Banking agents with Anthropic (May 2026): AML evidence pack → investigator first; broader H2 2026. Issuer “agentic commerce”: authorize agent-initiated card txs — rails for other people’s agents.

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Different | Product suites, not intent as work object. |
| C2 One case | Different | Not a goods-order case. |
| C3 Agent drafts | Partial | AR email, AML packs. |
| C4 Named owner | Partial | AP workflows; investigator-in-the-loop. |
| C5 Funding gate | Match | Payment Hub / treasury vs ERP AP subledger. |
| C6 Chat ≠ books | Different | For corporates, ERP remains SoR. |
| C7 Views | Different | — |
| C8 Isolated agents | Partial | Bank-agent governance, not commerce case isolation. |
| C9 Recovery | Partial | Disputes, returns, payment controls. |
| C10 Goods P2P | Different | Not in product. |

# Steal / hold

Steal: keep funding off the operational subledger. Ignore HORIZON/IBS cores and issuer agentic commerce for P2P/O2C design.
