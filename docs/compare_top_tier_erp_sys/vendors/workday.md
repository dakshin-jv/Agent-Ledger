---
type: Competitive Inference
title: Workday Financial Management and Spend
description: ARTW #10. Sana conversational front door and Agent System of Record on HCM/finance/spend.
tags:
- erp
- competitive
- workday
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: sana
  resource: https://newsroom.workday.com/2026-03-17-Introducing-Sana-from-Workday-Superintelligence-for-Work-That-Finds-Answers,-Takes-Action,-and-Automates-Workflows
  title: Introducing Sana from Workday
- id: agents
  resource: https://www.workday.com/en-us/artificial-intelligence/ai-agents.html
  title: Workday AI agents
- id: asor
  resource: https://doc.workday.com/admin-guide/en-us/workday-ai/agents/setup-considerations--agent-system-of-record.html
  title: Agent System of Record
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: medium-on-GA-vs-marketing
---

# Treat as

**Adjacent.** Gartner Cloud ERP **finance / service-centric**, not goods O2C/warehouse. Overlap: finance, spend, contracts, audit. Weak: goods commercial case.

# AI surface

Illuminate (2024) → Illuminate Agents + **ASOR** (2025) → **Sana from Workday** (Mar 2026 GA via Flex Credits). Sana orchestrates specialist agents through ASOR, security, and audit.

Treat marketing “Accounting Agent / Procurement Agent” as umbrellas. Admin catalog (2026-09) lists registrable agents; Procurement Agent is **not** a first-class catalog name. Several finance/spend agents remain early access or 2026 wave.

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Partial | Sana is intent-first UX. Objects stay req/PO/invoice/contract. |
| C2 One case | Different | Process chains, not one commercial case. |
| C3 Agent drafts | Match | Contracts, RFX, invoice checks, audit packs; review recommended. |
| C4 Named owner | Partial | Business process security, not named owner of a versioned case. |
| C5 Funding gate | Different | Budget at purchase / Adaptive Planning, not a second gate after accept. |
| C6 Chat ≠ books | Match | Agents on Workday data, BPs, audit. Closest match. |
| C7 Views | Different | Apps + inbox + one conversational Sana. |
| C8 Isolated agents | Partial | Identity/skill isolation (ASU), not one case at a time. |
| C9 Recovery | Different | No ASOR undo; cancel/adjust via normal BPs. |
| C10 Goods P2P | Different | Internal inventory; quote-to-cash often Salesforce → Workday. |

# Steal / hold

Steal: ASOR / agent identity; draft-then-human on contracts and invoices; orchestrator + specialists. Do not claim novelty on conversational front door or “agents don’t replace the GL.” Hold case object, version, funding gate, views, recover, goods P2P.
