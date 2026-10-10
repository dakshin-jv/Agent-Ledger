---
type: Competitive Inference
title: Oracle Fusion Cloud and NetSuite
description: ARTW #1. Module ERPs with Agent Studio, Ask Oracle, and agentic applications.
tags:
- erp
- competitive
- oracle
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: studio
  resource: https://docs.oracle.com/en/cloud/saas/fusion-ai/26d/aiaas/overview-of-ai-agent-studio.html
  title: Overview of AI Agent Studio
- id: agentic-apps
  resource: https://www.oracle.com/news/announcement/oracle-introduces-fusion-agentic-applications-2026-03-24/
  title: Oracle Introduces Fusion Agentic Applications
- id: ask-oracle
  resource: https://www.netsuite.com/portal/resource/articles/erp/netsuite-2026-2-brings-ask-oracle-capabilities-to-netsuite.shtml
  title: NetSuite 2026.2 Ask Oracle
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-names-medium-on-live-UX
---

# Treat as

**Peer.** Fusion (Financials, Procurement, SCM) and NetSuite are separate products. Both remain **module → work area → record**.

# AI surface

| Product | Stack | GA note |
| --- | --- | --- |
| Fusion | AI Agent Studio; Fusion Agentic Applications; Fusion Claw; Ask Oracle; Marketplace | Finance agents Ledger/Expenses/Payables/Payments **GA in 26B** (cohort still Oracle-managed). Many agentic apps announced, rollout uneven. |
| NetSuite | Ask Oracle; named page agents; Bill Capture; AI Connector (MCP); SuiteCloud Agent Skills | Ask Oracle **GA where enabled** (2026.2). Agents do not replace records or SuiteApprovals (Oracle docs). |

**Writes:** Fusion business-object tools can create/update under RBAC. Prebuilts write invoices, draft/submit sales orders, sourcing events, payment-run schedule. Many others advise and deep-link. NetSuite Bill Capture → vendor bill; MCP can create PO/bill/payment from external clients.

**Approval:** Existing BPM / invoice / procurement access. Studio Human Approval Node (pause, approve/reject). **Funding is not a distinct gate** from commercial accept.

**UX:** Outcome workspaces (Collectors, Spend Command Center) stitch a **process**, not one case ID. Chat often not resumable (Ledger Agent 26B).

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Partial | Ask Oracle / Claw “define outcome in NL.” Pillars remain canonical. |
| C2 One case | Different | Requisition, PO, invoice, payment, SO, receipt stay separate. |
| C3 Agent drafts | Partial | Draft SO, Bill Capture review, HITL node. |
| C4 Named owner | Partial | Role/approver on a module record, not case assignee on a version. |
| C5 Funding gate | Different | Pay/approve still AP/Payments policy. |
| C6 Chat ≠ books | Match | Explicit: agents do not replace records/approvals. |
| C7 Views | Different | Home = Ask Oracle / Redwood / ERP Agents menu. |
| C8 Isolated agents | Partial | Multi-agent workflows, not one commercial case. |
| C9 Recovery | Different | Reverse/void/credit. |
| C10 Goods P2P | Partial | Fusion Procurement + Autonomous Sourcing among many pillars. NS SuiteProcurement is mostly indirect goods. |

# Steal / hold

Steal: Agent Studio (tools, HITL, permissions); draft then native validation; “agents don’t replace records.” Hold: case as object; views; funding gate; per-case isolation and recover.

# Adjacent

Aera Decision Cloud writes back to Oracle ERP (overlay, not Oracle-owned). Coupa is P2P engagement; ERP remains SoR. EBS/JDE/PeopleSoft are out of the Fusion agent roadmap.
