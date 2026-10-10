---
type: Screen Design
title: Step 3 — Home interaction model
description: The five Home zones and the intended first-screen feel from the discussion.
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

# Status

Concept discussed; wireframe, visual design and implementation not completed. The user asked to move through Step 3; this is a discussion checkpoint, while individual details remain proposals.

# Purpose and feel

Home answers: What needs me? What is happening? What should happen next? What can I ask the system to do?

Feel: an operational command center, simple at first glance, with business context and structured drill-down. Complexity appears progressively. Typography, colour palette, spacing, responsive rules and component library are not selected.

# Five functional zones

| Zone | What appears | Interaction |
|---|---|---|
| Command bar | Greeting; “What do you want to get done?”; input | Ask, create, find, analyse or act |
| Attention queue | Decisions requiring human action | Review → Work item or contextual record |
| Business pulse | A small set of role-aware metrics | Drill into evidence or relevant workspace |
| Active operations | Work moving through orders, purchasing and money | Open filtered operational workspace |
| Agent activity | Proposed, ongoing and completed agent actions | Inspect explanation, data and result |

# Above the fold

The discussed order is greeting and global controls; prominent command input; quick actions; attention queue; compact business pulse; active operations. Agent activity follows lower on the page. Exact fold depends on viewport; do not promise all content fits every device.

Quick actions discussed: Create order, Buy stock, Pay supplier, Investigate. They support direct interaction as well as language input.

# Illustrative Home content

| Zone | Example only |
|---|---|
| Attention | 3 orders at risk; ₹12.4L PO needs approval; 2 exceptions |
| Pulse | Revenue ₹18.2L; 128 orders; cash ₹42.8L; receivables ₹11.3L; 4 SKUs at risk |
| Operations | 72 fulfilling; 14 purchasing; 8 awaiting payment |
| Agent activity | Procurement proposed a PO; finance matched 47/49 payments; fulfilment changed an allocation |

These are independent mock examples, not a reconciled dataset or verified actions. No metric definition or production counting rule has been selected.

# Role-aware pulse

Target no more than five metrics in the initial view.

| Role example | Suggested pulse |
|---|---|
| CEO | Revenue, cash, margin, major risks, forecast |
| Procurement | Stock risk, open POs, supplier delays, spend, exceptions |
| Finance | Cash, receivables, payables, overdue, reconciliation |

For anomalies, show a short explanation and Investigate. Example: margin fell mainly due to increased packaging costs and express shipping. This must be grounded in actual data when implemented, not generated as plausible copy.

# Home exclusions discussed

No large module grid, dozens of charts, report gallery, customer/product database tables, accounting journal, warehouse table, long notification feed or half-screen persistent chatbot. Deeper records and reports remain accessible elsewhere.

# Detailed behaviour references

See [command interactions](/design/command-interactions.md), [attention and operations](/design/attention-and-operations.md) and [agent visibility](/design/agent-visibility.md).

# Still to resolve

Home empty/loading/error/offline states; first-use onboarding; mobile layout; keyboard behaviour; role switching; accessible focus; data freshness display; attention selection limits; command result placement. These remain pending design questions, not silently implemented requirements.
