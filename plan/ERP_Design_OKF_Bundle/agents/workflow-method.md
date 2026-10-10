---
type: Design Method
title: Happy path first, then agent fallbacks
description: The agreed development sequence and reusable handling of external uncertainty.
tags:
- erp
- agents
- agents
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T15:35:00+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: user-directed-method
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Development sequence

User direction: happy path first, fallbacks next, agent by agent. Complete a coherent first journey and its essential recovery before expanding coverage.

1. Define user goal, inputs and completion conditions.
2. Specify agent steps, tools and evidence.
3. Include mandatory approval in the normal path.
4. Show confirmed outcome and updated records.
5. Define what the user sees throughout.
6. Add business exceptions, tool failures and uncertain outcomes.

# Scenario inventory

There is no fixed count. The discussion proposed ten families: sales order creation; allocation/fulfilment; shortages/replenishment; sourcing/PO creation; goods receipt/discrepancies; invoicing/collection; supplier payments; reconciliation; cancellations/returns/refunds; customer/supplier issues. These are a scope inventory, not ten required agents or ten approved build commitments.

# Shared fallback patterns

| Situation | Proposed response |
|---|---|
| Missing or ambiguous input | Ask for the specific decision-critical input |
| No feasible option | Explain constraints and present alternatives |
| External dependency | Persist Waiting, responsible party and review time |
| Temporary failure | Bounded safe retries, then escalate |
| Concurrent update | Recheck current records before committing |
| Approval refused | Revise or stop according to the user's decision |
| Outcome uncertain | Query authoritative external status before retrying |
| No safe continuation | Preserve progress and create Needs review |
| Action already committed | Supported reversal or corrective workflow |

# Boundaries

Define permissions, spending/step/time limits, duplicate-action protection and audit records. Agents cannot control supplier or carrier events; the system must control its next action and make unresolved work visible. Payment status, agent status and business status remain separate.

# Not yet specified

Exact state machine, retry settings, error taxonomy, recovery APIs and approval rules. These must be filled per workflow. See [Procurement brief](/next-steps/procurement-agent.md).
