---
type: Progress Tracker
title: ERP design progress
description: What is documented, what remains unvalidated and the next screen to design.
tags:
- erp
- design
- progress
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T16:14:35+00:00'
sources:
- id: discussion
  resource: /references/discussion-record.md
  title: ERP design discussion supplied by the user
- id: session-02
  resource: /references/session-02-agent-development.md
design_progress: checkpoint-recorded
implementation_status: not-evidenced
bundle_revision: 0.5.0
---

# Current checkpoint

## IN PROGRESS

### PostgreSQL runtime

- Render PostgreSQL is the store for concurrent workflow execution.
- Runtime configuration and the idempotent foundation migration apply through `DATABASE_URL`.
- Do not send a database URL in chat; add it only to local `.env` and Render’s secret environment settings.

## COMPLETED

### PayPal Sandbox merchant OAuth validation

- The Sandbox app credentials stored only in the ignored local `.env` completed a client-credentials OAuth request successfully.
- Result: HTTP 200; Bearer token returned; `expires_in` was 32,400 seconds. The token was discarded immediately and was not stored in the repository, database or this tracker.
- This validates only Sandbox app authentication. No PayPal order, payment, refund, balance/reporting request, notification or deployment was performed.
- The Business Sandbox account is the primary integration identity. Buyer credentials are retained locally only for a later Checkout demonstration and are not used by the current merchant flow.
- Next PayPal task: run a separately authorised, read-only merchant reporting/capability check before implementing any payment lifecycle.

### Channel3 external goods discovery

- Installed and used the `channel3-api` skill; the Python SDK is configured server-side through the ignored `CHANNEL3_API_KEY` environment variable.
- Added a procurement discovery adapter that returns only `external_channel3`-labelled product/offer snapshots. It does not create supplier approval, inventory, contract or payment authority.
- Live read-only search validation succeeded with one candidate and one USD offer. No result was persisted.
- Locale is currently the API-supported default `en` / `US` / `USD`; do not treat it as an India-market coverage confirmation. Next: select and verify a supported demo locale/category before presenting discovery results in a workflow.

Steps 1–3 are documented at discussion level. Step 4 Work has begun at structural level. **Next: first-agent happy-path specification, connected to Work and Orders.** No screen implementation, production integration or usability testing is evidenced in this bundle.

| Step | Topic | Discussion status | Artifact | Design validation | Implementation |
|---|---|---|---|---|---|
| 1 | Traditional ERP baseline and transformation lens | Discussed | [Baseline](/foundation/traditional-erp.md), [map](/foundation/transformation-map.md) | Not validated with target users | Not evidenced |
| 2 | Navigation architecture | Working direction: six tabs | [Navigation](/design/navigation.md) | Labels and grouping open | Not evidenced |
| 3 | Home interaction model | Concept discussed | [Home](/design/home.md), linked interaction patterns | Wireframe and usability validation pending | Not evidenced |
| 4 | Work / Attention Queue | Initial queue/detail structure discussed; scenario pending | [Step 4 brief](/next-steps/step-04-work.md) | Pending | Not started in this bundle |
| Proposed 5 | Orders + guided creation + order workspace | Outline only | [Workspace outlines](/design/workspace-outlines.md) | Sequence and scope to confirm | Not started in this bundle |
| Proposed 6 | Money | Outline only | [Workspace outlines](/design/workspace-outlines.md) | Pending | Not started in this bundle |
| Proposed 7 | Network + inventory placement | Outline only | [Open questions](/progress/open-questions.md) | Pending | Not started in this bundle |
| Proposed 8 | Intelligence | Outline only | [Workspace outlines](/design/workspace-outlines.md) | Pending | Not started in this bundle |
| Proposed 9 | Settings / agent authority | Principles only | [Agent visibility](/design/agent-visibility.md) | Pending | Not started in this bundle |
| Proposed 10 | Cross-screen prototype and user testing | Not discussed in detail | [Step template](/next-steps/design-step-template.md) | Pending | Not started in this bundle |

Steps beyond 4 are a suggested continuation sequence, not a user-approved roadmap. They contain room for future design, not completed specifications.

# Next-session checklist

- [ ] Confirm the first role and scenario for Work design.
- [ ] Define the Work list and decision detail.
- [ ] Clarify statuses and ownership.
- [ ] Define approval, agent continuation and failed-action feedback.
- [ ] Resolve priority handling and dismissal semantics.
- [ ] Record the new decisions and remaining questions.
- [ ] Update progress and log; do not mark implementation complete from a design conversation.

# Future update fields

| Field | Current value |
|---|---|
| Owner | Not assigned |
| Latest checkpoint | Step 4 structure and agent/service direction documented |
| Next deliverable | First-agent happy path + corresponding Work interaction |
| Next review date | Not set |
| Blocking decision | Confirm first agent, persona and procurement scenario |
| Prototype link | Not created |
| Usability findings | None recorded |

# Agent development and architecture progress

| Topic | Current standing | Next action |
|---|---|---|
| Agent-by-agent method | User direction recorded | Apply to one workflow |
| Happy path before fallbacks | User direction recorded | Specify first happy path |
| Shared agents across pages | Working architecture direction | Define agent contract |
| Astropods + Render | Proposed split; not integrated | Test authenticated invocation and structured result |
| Sarvam + TypeSafe | User reports keys; untested | Test model/evaluation calls |
| Five priority services | Explicit user priority | Map meaningful calls and UI contributions |
| Channel3 / Elastic / SQL boundaries | Proposed | Confirm SQL provider and schemas |
| Procurement first | Recommendation; not explicitly chosen | Confirm scenario and persona |

See [service priorities](/architecture/service-priorities.md) and [Procurement brief](/next-steps/procurement-agent.md). No build completion is claimed.

# PayPal checkpoint

Sandbox and AI Toolkit explicitly required; official hackathon overview/resources rechecked. Configuration and integration tests remain pending. See [PayPal plan](/architecture/paypal-sandbox-toolkit.md).

# Current next step

Render PostgreSQL is the store. Enterprise requirements clarified. Next: enterprise Procurement requisition intake happy path. Goods/services scope and first persona remain unresolved.

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
