---
type: Interaction Pattern
title: Commands and guided creation
description: Four command intents, risk-aware outcomes and the structured alternative
  to language input.
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

# Four intent classes

| Intent | Examples discussed | Expected result direction |
|---|---|---|
| Create | Order, PO, customer, invoice | Prepare a validated draft |
| Find | Invoice 482; orders from Reliance | Return matching records |
| Analyse | Why did margin fall? Why is inventory growing? | Answer with evidence and drill-down |
| Act | Approve PO; send reminder; reorder | Prepare or execute within the user's authority |

The command bar handles business work and keeps context; it is not a generic chat box.

# Examples

- “Create an order for ABC for 500 units of Product X.”
- “Which orders are likely to be delayed this week?”
- “Pay all approved supplier invoices below ₹1 lakh.”
- “Compare our last three quotes for packaging.”
- “Why did gross margin fall this month?”

Examples describe intents, not guaranteed supported commands or granted permissions.

# Risk-aware response

| Situation | Discussed behaviour |
|---|---|
| Read-only question | Return answer / records immediately if permitted |
| Reversible preparation | Create a draft, such as a PO for 1,000 units |
| High-impact commitment | Prepare a reviewable proposal and request the required approval |

Policy, roles and thresholds still need definition. A natural-language request does not bypass them.

# Payment proposal example

Supplier ACME Packaging; ₹12,00,000; invoice INV-8821; due 9 Oct; masked account HDFC ••••2741. Present the invoice approval, PO match, goods receipt and duplicate-payment checks with their actual outcomes. Then expose the action “Approve ₹12,00,000” to an authorised user.

All values and passing checks in this example are illustrative. Do not claim the checks succeeded without evidence. Payment execution and approval are distinct events; exact failure and confirmation UX is pending.

# Guided Create Order alternative

Clicking Create Order opens a small structured entry point: customer search; product and quantity; delivery timing. The agent then proposes pricing, tax, customer terms, inventory source and shipping options from available data. Show what it filled and let the user review. An advanced user can open the full form.

Avoid silently selecting a customer/product or inventing commercial terms. Missing information and ambiguity handling are still to be designed in the Orders step.

# Global context

Command access remains reachable on every workspace, for example via “Ask ERP.” Inside Order #4821, “Why hasn't this shipped?” uses the current order context. Exact shortcut, trigger and response panel are open. Context must remain visible enough for users to know which record an action targets.

# Progress

Intent classes and interaction direction are discussed. No parser schema, tool catalogue, agent framework, command API or full creation wizard is finalised.
