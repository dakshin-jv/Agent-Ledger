---
type: Design Brief
title: First agent candidate — Procurement
description: The proposed first happy path, service mapping and fallback slots awaiting
  detailed design.
tags:
- erp
- agents
- next-steps
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T16:14:35+00:00'
sources:
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: next-candidate
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Status

Procurement is the recommended first agent, not explicitly selected by the user. Agent-by-agent and happy-path-first development are explicit directions. Confirm first workflow and persona before choosing material requirements.

# Proposed happy path

| Step | Business outcome | Proposed services / screen |
|---|---|---|
| 1 | Capture purchasing goal and required constraints | Home command or guided Orders entry; Sarvam as appropriate |
| 2 | Validate input, permission and request record | ERP backend + transactional database |
| 3 | Start bounded sourcing | Render invokes Astropods Procurement agent |
| 4 | Discover external options and retrieve relevant knowledge | Channel3; Elastic where relevant |
| 5 | Produce feasible candidates and an evidence-based comparison | Agent + deterministic constraints; Jev for bounded evaluation if useful |
| 6 | Inspect alternatives and operational consequences | AG Grid comparison + Bryntum plan in order workspace |
| 7 | Review and approve the specific commitment | Work; backend stores approval |
| 8 | Execute supported payment flow and confirm result | Render continuation + authorised PayPal service |
| 9 | Update records and retain outcome for future retrieval | Backend/SQL; index permitted knowledge in Elastic |

This is a discussion-level sequence. APIMatic supports PayPal integration development across the applicable build steps. It is not a runtime step in the purchase lifecycle.

# Payment boundary

Discovering a Channel3 retailer does not establish a supported PayPal payment relationship with that retailer. Earlier architecture recommended a controlled sandbox merchant for the demo. Confirm and label the executable payment model; do not claim arbitrary discovered suppliers were paid.

# Room for detailed design

Persona; realistic scenario; input schema; agent tools; evidence fields; output contract; candidate scoring; timeline inputs; approval rules; payment model; result status; Work detail; user review — all pending.

# Fallbacks after happy path

Missing input; no feasible candidate; stale price/availability; unknown delivery; search failure; agent timeout; concurrent record change; rejection; payment failure; payment outcome unknown; partial completion; cancellation. Define user message, next owner, allowed retry and recovery for each.

# Next delivery

Agree scenario → write detailed happy path → design its Work/Orders surfaces → map actual service calls → test minimum platform handoff → add essential fallbacks. Do not build all ten workflow families at once.

# Enterprise intake checkpoint

User clarified enterprise requirements; avoid narrowing the ERP to electronics/office supplies. Start with requisition intake and inspect internal stock/contracts/approved suppliers before external discovery. Confirm goods, services or both. Render PostgreSQL is the store.

# Current goods-intake design checkpoint — revision 0.4.0

User selected goods only (supersedes the earlier both-goods-and-services discussion). Services deferred for lack of data. Demo-labelled internal datasets and PayPal Sandbox selected. Sarvam and TypeSafe both required. Human approval and recovery required at every step. Design only: do not build, seed, configure or call services in this delivery.

- [Dataset design](/architecture/demo-dataset-design.md)
- [Service setup, human approval and recovery](/architecture/service-setup-design.md)
- [PayPal datasets and setup](/architecture/paypal-sandbox-dataset-setup.md)

Goods-intake schema, forward/recovery transitions and scenario definitions are documented as proposals, not implemented or tested. No stock/contracts/policy datasets or API credentials have been supplied or verified. Next: review fixture configuration (country, currency, goods category, users and illustrative rules), then detailed specification-stage design. Future Codex implementation must update progress with evidence and preserve this single bundle.

# Specification owner routing checkpoint — revision 0.5.0

Business owner approves goods specifications for now; RBAC implementation planned. Non-owner action creates a pending owner review and notification; no proxy approval. Missing/unavailable owners remain pending for controlled assignment. Material edits, withdrawal and owner reassignment invalidate affected reviews; stale notifications cannot authorize execution. Intake funding authority remains distinct. See [Specification Agent](/agents/goods-specification-agent.md). Design-only; implementation and tests pending. Next: goods sourcing design.

# Latest scheduling and RBAC direction

RBAC will be implemented; current delivery is design only. Render Cron Jobs plus Workflows recommended for owner reminders/retries, with immediate initial notification via outbox. See [scheduled owner notifications](/architecture/scheduled-owner-notifications.md). This supersedes earlier RBAC-deferral wording. Delivery timing/channel and detailed permission policy await review.
