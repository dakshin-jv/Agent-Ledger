---
type: Competitive Inference
title: Roper Technologies
description: ARTW #7 ranking artifact. Vertical SoRs (Deltek, Aderant, Vertafore) with task agents.
tags:
- erp
- competitive
- roper
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: artw
  resource: https://www.appsruntheworld.com/top-10-erp-software-vendors-and-market-forecast/
  title: ARTW Top 10 ERP
- id: dela
  resource: https://www.deltek.com/products/platform/dela/
  title: Deltek Dela
- id: aderant
  resource: https://www.aderant.com/aderant-agent-center/
  title: Aderant Agent Center
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-roll-up
---

# Treat as

**Not a goods-commerce ERP.** Holding company. ARTW counted apps: **Deltek Costpoint, Aderant Expert, Vertafore AMS360** (GovCon, legal, insurance). Deltek is project + procurement + manufacturing for FAR/DCAA, not retail/wholesale goods. There is no “Deltek Copilot”; the brand is **Dela**.

# AI surface

| Brand | Product | Pattern |
| --- | --- | --- |
| Deltek | Dela / Ask Dela | NLQ; Costpoint agents; HITL |
| Aderant | MADDI, Agent Center | Job agents draft; users remain decision makers |
| Vertafore | Velocity AI | Intake/recon with review/exceptions |
| PowerPlan | Intelligent Unitization | Accountant reviews AI lines |
| iTradeNetwork | Order Agent | Inbound PO → OMS/ERP — **not in ARTW ERP trio** |

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Different | Module/product ERPs. |
| C2 One case | Different | Project, matter, policy — not one commercial goods case. |
| C3 Agent drafts | Match | Strong across brands. |
| C4 Named owner | Match | Explicit HITL. |
| C5 Funding gate | Different | Compliance gates, not commerce funding. |
| C6 Chat ≠ books | Match | Agents write into licensed SoRs. |
| C7 Views | Different | — |
| C8 Isolated agents | Partial | Job/plugin isolation, not commercial case. |
| C9 Recovery | Partial | Audit-heavy; recover not first-class. |
| C10 Goods P2P | Different | iTN Order Agent is OMS sidecar. |

# Steal / hold

Market converges on **task agents on the SoR + human approve**. Copy HITL/audit language from regulated verticals, not the module split.
