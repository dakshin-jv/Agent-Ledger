---
type: Interaction Pattern
title: Home attention, pulse and active operations
description: Decision-oriented attention items, role-aware business context and operational
  drill-down.
tags:
- erp
- design
- design
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
design_progress: concept-discussed
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Attention as a decision

Replace vague alerts with a business issue, its supporting context and a proposed next action.

Example: SKU-204 may run out in 9 days; current stock 840; expected demand 1,270; supplier lead time 14 days; procurement recommends 1,500 units. Discussed actions: Approve PO, Review, Dismiss. All figures are examples; the recommendation has no validated reorder computation yet.

Home previews what needs the current user. Work is the full operational inbox. Dismissal should not be assumed to resolve the underlying issue; its semantics are open.

# Priority

The discussion suggested ranking using financial impact, urgency, confidence and operational dependencies, rather than only time received. An illustrative multiplicative formula was mentioned; it is not a production rule.

Critical: tomorrow's delivery puts ₹18.2L at risk. High: shortage affects 14 orders. Medium: invoice approval due in four days. These are examples, not chosen thresholds.

Open question: how should uncertainty affect priority? A severe issue with weak evidence must not disappear merely because a score multiplies by low confidence. Decide ranking, evidence labels, ties and overrides in [Step 4](/next-steps/step-04-work.md).

# Active operations

Give a compact sense of movement across the business, with clickable counts or amounts. Examples discussed:

| Area | Example categories |
|---|---|
| Orders | Received, fulfilling, shipped, at risk |
| Purchasing | Open, awaiting supplier, awaiting approval |
| Money | Collected, scheduled, unmatched |

Whether counts are overlapping, daily events or current states remains open. Do not add them as if they form one complete partition.

# Pulse and proactive explanation

Use the role-aware metric set in [Home](/design/home.md). Explain a meaningful anomaly briefly, link its evidence, and provide Investigate. The source data, calculation windows, refresh times and confidence display need later specification.
