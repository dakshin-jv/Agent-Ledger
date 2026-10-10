---
type: Screen Outline
title: Workspace outlines beyond Home
description: The limited sketches for Work, Orders, Money, Network and Intelligence
  without prematurely finalising them.
tags:
- erp
- design
- design
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: outline-only
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Scope

These outlines preserve concepts already discussed. They are not finished page designs. Only Home has been explored at Step 3 detail.

| Workspace | Existing discussion | Pending detail |
|---|---|---|
| Work | Unified tasks, approvals, exceptions, handoffs, investigations; Needs me / Agents working / Waiting / Completed | Step 4 initial queue/detail structure discussed; detailed journey pending |
| Orders | All / Sell / Buy / Fulfil / Return; sales orders, POs, shipments, returns; order as workspace | List layout, creation, lifecycle, per-order tabs and agents |
| Money | Cash available; to collect; to pay; overdue and unmatched attention; detailed finance records below | Accounting depth, payments, reconciliation and authority |
| Network | Customers, suppliers, products, locations; entity health and linked activity | Grouping usability, operational inventory, entity onboarding |
| Intelligence | Business question → answer + evidence + chart + action; saved views and reports | Analytics interaction, metric definitions, repeatability and uncertainty |

# Examples from the discussion

Order #4821 for Reliance Retail, ₹12.4L, shows fulfilment stages and a shortage explanation: Warehouse B has 312 of 500 required units. “Resolve with Agent” opens contextual work. The earlier sample placed Paid after Shipped in one line; payment and fulfilment can progress independently, so that illustration is not an adopted state model.

Money illustrates ₹42.8L cash, ₹11.3L to collect and ₹8.7L to pay, alongside overdue invoices and unmatched payments. Values are mock data.

Supplier ACME Packaging illustrates 47 orders, ₹38.2L spend, 94% on-time performance and two quality issues. A proposed insight notes lead time rising from 12 to 16 days over 60 days. No real supplier history is implied.

Intelligence examples: why margin fell, which customers may reorder, which products may run out in 14 days, and supplier performance comparison.

# Next

Develop [Work](/next-steps/step-04-work.md) first. The other workspaces are proposed later steps in [the tracker](/progress/tracker.md).
