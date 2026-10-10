---
type: Comparison Frame
title: AgentLedger comparison criteria
description: The design points used to score every vendor in this bundle.
tags:
- erp
- competitive
- foundation
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: agents-md
  resource: /AGENTS.md
  title: AgentLedger contributor guide
- id: okf
  resource: /plan/ERP_Design_OKF_Bundle/index.md
  title: ERP Design OKF bundle
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.1.0
---

# Scorecard

Score each vendor on these points. Do not score “has AI” as a win.

| ID | Point | AgentLedger meaning |
| --- | --- | --- |
| C1 | Intent first | Operator states create / check / investigate / approve / recover. Intent is the work object, not a search bar on a module. |
| C2 | One case | Order, stock, PO, bill, and payment are one commercial case (lines, money, owner, evidence), not five documents glued by agents. |
| C3 | Agent drafts | Agent prepares a versioned draft on that case. |
| C4 | Named owner | Assigned owner accepts or returns the **current version**. A job title is not a yes. |
| C5 | Funding gate | Paying is a second, separate permissioned yes after commercial accept. |
| C6 | Chat ≠ books | Ledger, permissions, and history stay the system of record. Chat drafts and routes. |
| C7 | Views | Home, Work, Orders, Money, Network, Intelligence are views of the same case, not five products. |
| C8 | Isolated agents | One case at a time, only inside granted authority. |
| C9 | Recovery | Withdraw, undo, or reverse as a first-class path, not only GL void after the fact. |
| C10 | Goods P2P first | First detailed journey is goods procurement; services wait on data. |

# What is already table stakes

Conversational front door, invoice OCR, copilot sidecar, “agents inherit user permissions,” and human-in-the-loop on AP documents. Do not claim novelty there.

# Reading

Product method: [`/plan/ERP_Design_OKF_Bundle/`](/plan/ERP_Design_OKF_Bundle/). Cross-vendor result: [synthesis](/synthesis.md).
