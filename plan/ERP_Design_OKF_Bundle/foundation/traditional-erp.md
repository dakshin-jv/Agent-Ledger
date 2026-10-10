---
type: Reference
title: Traditional ERP experience baseline
description: The modules, screen types and daily workflow used as the redesign baseline.
tags:
- erp
- design
- foundation
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T03:22:52+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Scope of this baseline

This is the illustrative baseline from our discussion, not a measured claim about every ERP vendor. The earlier estimate was roughly 8–12 main modules; actual products and role permissions vary.

# Primary tabs and contents

| Traditional tab | Typical contents in the discussion |
|---|---|
| Dashboard / Home | KPIs, alerts, approvals, sales, inventory, cash and tasks |
| Sales / Orders | Quotes, sales orders, customers, pricing, returns and invoices |
| Procurement / Purchase | Vendors, RFQs, POs, approvals and supplier quotes |
| Inventory / Warehouse | Products, SKUs, stock, transfers, batches, warehouses and replenishment |
| Finance / Accounting | Receivables, payables, invoices, payments, journals, expenses and reconciliation |
| Customers / CRM | Profiles, conversations, opportunities, complaints and account history |
| Suppliers / Vendors | Profiles, contracts, prices, performance, invoices and compliance |
| Operations / Fulfilment | Picking, packing, shipping, delivery and returns |
| Products / Catalog | Product master, SKUs, price lists, variants, tax, units and suppliers |
| Reports / Analytics | Sales, stock, profitability, cash and supplier metrics |
| Approvals / Tasks | Purchase/payment approvals, exceptions and assigned tasks |
| Settings / Admin | Users, roles, taxes, rules, integrations and company setup |

# Recurring interaction

Module → list → record → form → approval → report. Users navigate to an object, open it, enter fields, submit it and track the workflow.

Example: Sales → Orders → Sales Orders → New. Fields include customer, billing/shipping addresses, products, quantities, price, tax, discount, warehouse, delivery date, payment terms, salesperson and notes. Common buttons: Save Draft, Submit, Approve, Confirm, Cancel. Record tabs may include Items, Billing, Shipping, Payments, Activity, Documents and History.

Other examples: Purchase → Purchase Orders → New; Finance → Invoices → New; Vendors → Supplier → New; Inventory → Transfers → New.

# Seven screen types

| Screen | Traditional role | Redesign question |
|---|---|---|
| Dashboard | KPIs, alerts and links | Can it surface actions and explanations? |
| List | Search, filters, sorting, export and Create | Which structured browsing tools remain valuable? |
| Record detail | Status, lines, money, shipment, notes, attachments and history | How can the record become a workspace? |
| Form | Data entry and validation | What can the agent fill, and what must the user confirm? |
| Workflow / approval | Approve, reject or request changes | Can the user receive a decision brief? |
| Report | Choose template, filters, generate and interpret | Can a business question return evidence and an action? |
| Admin | Configure users, rules, taxes and integrations | Which complexity can be moved away from daily work? |

# Daily journey discussed

An operations manager checks the dashboard, opens troubled orders, checks inventory, creates a PO, checks a supplier invoice, approves a payment, then generates a report. The friction is repeated movement between departmental modules to resolve one connected business problem.

The discussion described 3–5 navigation levels as an illustrative pattern. Do not use that estimate as a universal benchmark. [Transformation mapping](/foundation/transformation-map.md) is the next design lens.
