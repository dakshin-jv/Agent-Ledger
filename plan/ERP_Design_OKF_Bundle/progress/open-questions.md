---
type: Open Questions
title: Unresolved design questions
description: Material choices that future work must resolve instead of silently assuming.
tags:
- erp
- design
- progress
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
design_progress: open
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Before detailed Work design

| ID | Question | Why it matters | Current answer |
|---|---|---|---|
| Q-01 | Who is the first user: founder, operations manager, procurement or finance? | Changes queue content and primary actions | Unresolved |
| Q-02 | Which real scenario should anchor Step 4? | Prevents designing an abstract inbox | Unresolved; delayed order, shortage and payment approval are examples |
| Q-03 | How do Work statuses, ownership and agent run statuses relate? | A waiting task is not the same as a running agent | Proposed labels only |
| Q-04 | What constitutes approval versus execution? | Prevents ambiguous commitment and success feedback | Principles discussed; detail open |
| Q-05 | How do urgency, impact and uncertain evidence affect priority? | Keeps important uncertainty visible | Formula not adopted |
| Q-06 | What do Dismiss, Delegate, Pause and Request changes do? | Needed to avoid misleading controls | Only some controls mentioned; exact semantics open |

# Before broader design or coding

| ID | Question | Current answer |
|---|---|---|
| Q-07 | Keep Network label for products and locations? Where do stock operations live? | Unresolved |
| Q-08 | Does Orders combine sale and purchase effectively for target users? | Proposed; untested |
| Q-09 | Which accounting, compliance, geography and currency requirements are in scope? | Unresolved |
| Q-10 | Do users need a separate Agents / Automation area? | Floated; not finalised |
| Q-11 | Full ERP replacement or initial workflow on existing stack for first release? | Long-term replacement goal; first-release boundary open |
| Q-12 | What is the new product name? | AgentLedger is historical; final name unresolved |
| Q-13 | Which visual style, components and accessibility/responsive rules? | Unresolved |
| Q-14 | What is the hackathon demo scope and chosen implementation stack? | Historical architecture exists; latest scope reconciliation pending |
| Q-15 | Which metric definitions and source refresh rules back Home? | Mock examples only |
| Q-16 | How do payment, fulfilment, approval and agent states progress independently? | No adopted cross-domain state model |

# Parking lot

Use this table for additional loose ends instead of implementing guesses.

| New question | Affected step | Evidence needed | User answer | Resolution date |
|---|---|---|---|---|
| To be added | — | — | — | — |

# Agent and service questions added

- Q-17: Confirm Procurement first and the persona/scenario.
- Q-18: Define Render-to-Astropods endpoint, authentication and sync/async contract.
- Q-19: Confirm supported Sarvam model/client and TypeSafe evaluation schema.
- Q-20: Choose SQL provider and transactional schema.
- Q-21: Select Bryntum component and planning inputs; AG Grid edition/licence.
- Q-22: Verify APIMatic plugin setup and document its development contribution.
- Q-23: Confirm demo merchant/payment model and approval continuation.
- Q-24: Define Elastic indexing, access and freshness rules.

Q-14 is partially narrowed: five service priorities are explicit; remaining technical choices and demo scope remain open.

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
