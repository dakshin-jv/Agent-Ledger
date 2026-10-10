---
type: Competitive Inference
title: SAP S/4HANA, Ariba, and Joule
description: ARTW #2. Joule copilot, Assistants, Agents, and Joule Work on module ERP.
tags:
- erp
- competitive
- sap
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: joule-work
  resource: https://www.sap.com/products/artificial-intelligence/joule-work.html
  title: Joule Work
- id: joule-agents
  resource: https://www.sap.com/products/artificial-intelligence/ai-agents.html
  title: Joule Agents and Assistants
- id: fps2
  resource: https://community.sap.com/t5/technology-blog-posts-by-sap/exploring-ai-and-key-innovations-in-sap-cloud-erp-private-2025-fps2/ba-p/14497888
  title: Cloud ERP Private 2025 FPS2 AI
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-taxonomy-medium-on-GA
---

# Treat as

**Peer.** S/4HANA remains MM / SD / FI Fiori apps. Documents remain PO, GR, IR, invoice, payment. **Business One has no Joule** (Ask AI is read/analyze). **ByDesign** delisted for new sales 20 Apr 2026.

# AI surface

Do not conflate:

| Name | Role |
| --- | --- |
| Business AI | Governance platform (graph, gateway, RBAC, audit) |
| Joule copilot | Chat in Fiori; skills = atomic API actions |
| Joule Assistants | Role coordinators (Closing, AP, Receiving, Sourcing) |
| Joule Agents | Multi-step doers; conversational, embedded, or system-triggered |
| Joule Studio | Build skills/agents; agent builder GA Q1 2026 (trade coverage) |
| Joule Work | Engagement layer (Conversations, Spaces). **Does not replace Fiori.** EAC as of Sapphire 2026 |
| WalkMe action bar | Screen overlay DAP, not ERP redesign |

**Write vs propose:** Mixed. High-risk steps need human approval; some agents post (journal entry, purchase contract POST, returns). Assistants largely **EAC**; GA cited Q4 2026–Q1 2027 in FPS2 community post. Ariba/Fieldglass agents claimed GA Jun 2026 (trade press). Fieldglass is **services**.

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Partial | Joule Work: state intent, compose Spaces. Fiori modules remain SoR; Private Cloud still needs launchpad. |
| C2 One case | Different | LOB assistants stitch S/4 + Ariba + Fieldglass. Objects stay separate documents. |
| C3 Agent drafts | Partial | SuccessFactors/sales: proposals until confirm; some finance paths write. |
| C4 Named owner | Partial | HITL + existing SAP workflow, not version accept/return of a case. |
| C5 Funding gate | Different | Treasury/AP policy, not a case-level second gate. |
| C6 Chat ≠ books | Match | Joule Work is engagement; actions inherit user identity. |
| C7 Views | Different | Work Zone, Fiori, Ariba, Business Network are products. |
| C8 Isolated agents | Partial | Multi-system tasks, not one-case sandbox. |
| C9 Recovery | Different | Reverse documents / workflow. |
| C10 Goods P2P | Partial | Strongest GA story is Ariba + Fieldglass. Goods GR/MM still classic + EAC Receiving. |

# Steal / hold

Steal: skill vs agent vs assistant; chat as engagement; keep transactional UI to verify output. Hold: one case as SoR; version + funding sequence; six views; goods P2P without an Ariba+S/4 split; SMB-native agents (B1/ByDesign will not get this stack).
