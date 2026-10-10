---
type: Information Architecture
title: Six primary workspaces
description: The current six-tab navigation proposal and how traditional modules map
  into it.
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
design_progress: working-direction
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Current working direction

Six primary desktop tabs, with Admin / Settings accessible separately through a profile or utility menu. This is the navigation explored before Home design; labels and grouping remain subject to user validation.

| Tab | Purpose | Contents discussed | Detail maturity |
|---|---|---|---|
| Home | Business command center | Command bar, attention, pulse, operations, agent activity | Step 3 concept documented |
| Work | Unified operational inbox | Tasks, approvals, exceptions, handoffs, investigations | Step 4 pending |
| Orders | Commercial activity | Sales/purchase orders, fulfilment, returns, order agents | Broad outline only |
| Money | Financial operations | Invoices, payments, receivables, payables, expenses, ledger, reconciliation and cash | Broad outline only |
| Network | Business entities and relationships | Customers, suppliers, products, locations, contracts | Broad outline only |
| Intelligence | Ask, analyse and forecast | Answers, evidence, charts, actions, saved views, dashboards, reports and forecasts | Broad outline only |

# Traditional module mapping

| Traditional area | Proposed primary destination | Contextual access |
|---|---|---|
| Sales | Orders | Customer in Network; invoices in Money |
| Procurement | Orders | Supplier in Network; approvals in Work |
| Fulfilment / logistics | Orders | Locations in Network; exceptions in Work |
| Finance / accounting | Money | Financial approvals in Work |
| CRM / customers | Network | Customer records linked to Orders and Work |
| Suppliers / vendor master | Network | POs in Orders; bills in Money |
| Products / warehouse master | Network | Operational inventory placement remains open |
| Reports / analytics | Intelligence | Small role-aware pulse on Home |
| Tasks / approvals | Work | Home previews items needing attention |
| Administration | Separate Settings access | Specialist configuration and permissions |

# Important unresolved grouping

Putting products and warehouses in Network covers master records. It does not yet define where stock counts, transfers, batches, reservations or replenishment work live. Validate this explicitly; do not hide warehouse operations in a supplier directory by assumption.

# Agent navigation

Agents are embedded capabilities: order agent in an order; supplier context in a supplier; finance assistance in a payment; global command access everywhere. An Agents tab was floated, not finalised. Automation was also mentioned as a utility destination; it is not approved as a seventh primary tab.

# Navigation depth

Intent → relevant workspace → granular record. Users can still browse directly without typing commands. Shared record links should connect the workspaces, so a single issue does not require remembering departmental navigation.
