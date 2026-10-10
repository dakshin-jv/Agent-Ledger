---
type: Competitive Inference
title: Microsoft Dynamics 365 and Business Central
description: ARTW #5. Copilot assist vs autonomous agents vs Copilot Studio on Finance, SCM, and BC.
tags:
- erp
- competitive
- microsoft
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: fo-copilot
  resource: https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/fin-ops/copilot/copilot-for-finance-operations
  title: Copilot in finance and operations
- id: bc-payables
  resource: https://learn.microsoft.com/en-us/dynamics365/business-central/payables-agent
  title: Payables Agent
- id: scm-proc
  resource: https://learn.microsoft.com/en-us/dynamics365/supply-chain/procurement/procurement-agent-supplier-com-overview
  title: Procurement Supplier Communications Agent
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-docs-preview-lag
---

# Treat as

**Peer.** Finance and Supply Chain share an F&O Copilot platform. **Business Central is a separate SMB product** with more complete first-party AP/O2C agents.

# AI surface

| Layer | Meaning |
| --- | --- |
| Copilot | User-initiated assist: chat, summaries, propose matches |
| Agents | Background workers (mailbox/events); configured autonomy; humans in the loop |
| Copilot Studio | How agents are shipped/customized (Dataverse, Power Automate, credits) |
| ERP MCP / Cowork | NL tools into ERP logic; write summary before changes |

**Procurement:** SCM Supplier Communications Agent (preview) emails **existing POs** and proposes field updates. Not intent → source → PO → pay.

**AP:** BC Payables Agent: PDF → extract → 3-way match → **unposted draft** → supervisor. **Does not post.** Agent review ≠ BC approval workflow. F&O has no first-party AP invoice agent in the Copilot catalog.

**O2C:** BC Sales Order Agent: email → quote → order with limited permissions.

**UX:** Module / Role Center. Immersive Home ranks **classic workspaces** plus agent tasks. Chat is a sidecar.

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Partial | Cowork can start from a prompt; shipped agents are mailbox/module. |
| C2 One case | Different | Finance ≠ SCM ≠ BC. Role-slice agents. |
| C3 Agent drafts | Match | Strong draft/recommend/apply. |
| C4 Named owner | Partial | Supervisor/role, not case owner of a version. |
| C5 Funding gate | Partial | Post ≠ pay stays existing AP, not an explicit second gate on one case. |
| C6 Chat ≠ books | Match | Sidecar; Cowork uses user privileges; agent identity + roles. |
| C7 Views | Different | Immersive Home is an inbox of agent tasks. |
| C8 Isolated agents | Partial | Per company/instance/task, not per commercial case. |
| C9 Recovery | Partial | Cancel job / don’t post — not withdraw/undo/reverse as method. |
| C10 Goods P2P | Partial | SCM agent is PO comms, not full P2P. |

# Steal / hold

Steal: name Copilot vs agent vs studio; **draft ≠ approve ≠ post ≠ pay**; agent identity; MCP as tool layer. Hold: intent → one case across P2P; named owner; funding gate; per-case isolation; recover; goods P2P as spine.
