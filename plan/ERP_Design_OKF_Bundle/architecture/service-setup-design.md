---
type: Design Specification
title: Service setup design and human recovery gates
description: Service setup design and human recovery gates
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T17:20:00+00:00'
sources:
- id: session
  resource: 'User design decisions, 7 October 2026: goods only, demo data, TypeSafe,
    human review, undo and design-only delivery'
- id: astropods
  resource: https://docs.astropods.com/ask-for-input
- id: render
  resource: https://render.com/docs/workflows-defining
- id: trigger
  resource: https://render.com/docs/workflows-running
bundle_revision: 0.5.0
design_progress: specified-awaiting-review
implementation_status: not-started
---

# Design-only setup brief for future Codex

Do not install packages, create accounts, deploy, generate seed databases or run API/payment calls from this bundle task. Later implementation must recheck current provider docs and this bundle, retain one current bundle, and mark each operation planned/configured/tested with evidence. User reports Sarvam and TypeSafe keys, but no credentials were supplied or validated here. Never place secrets in the bundle, fixtures, prompts or audit output.

# Setup matrix

| Service | Intended contract / configuration | Readiness evidence later required | Failure and recovery |
|---|---|---|---|
| Backend + PostgreSQL | One backend instance owns persistent DB, business APIs, auth, version checks, approval/outbox journal; configure backup and restore | Persistence across restart; migrations/restore tested; tenant isolation; atomic dispatch and undo races | Restore with event reconciliation; never reset ledger to hide an external effect |
| Render | Bounded check/continuation tasks; authenticated dispatch, task IDs, timeout/retry policy, outbox consumer | Duplicate task does not duplicate effect; interruption recovery; task logs correlate with request | End tasks while awaiting long approvals; checkpoint first; retry only safe work |
| Astropods | Shared intake agent, authenticated backend access, structured task/result versioning; choose supported adapter | Adapter schema validation; per-case isolation; interrupted elicitation recovery | Use ERP review queue if surface lacks input; recover from backend state |
| Sarvam | Interpretation/voice adapter; language/model/audio settings and transcript provenance | Supported input/language, correction and outage tests; cost/latency measured | Manual form; preserve original input; rerun requires current request version |
| TypeSafe AI | Schema-bound missing-field/ambiguity assessment; exact provider model/API capability to verify | Valid response, invalid schema, unknown evidence and timeout cases | Reject result; retry bounded; human review; cannot grant approval |
| Channel3 | Discovery adapter, locale/currency, external IDs, retrieval dates and cache policy | Access, category/locale coverage, attribute/unit normalization and source links | Optional failure; refresh stale data; unselect candidate without altering need |
| Elastic | Permitted policy/document retrieval; tenant/entity filters, evidence version and index lag | Access control; retrieval cites original authorised document; deleted/changed source invalidated | Source store remains authority; unavailable retrieval visible; reindex later |
| AG Grid | Goods-line editing, candidate comparison, validation/status columns; accessible review | Field validation, source badge visibility, dirty/version state, undo display | Restore server version; stale save conflict shown rather than overwrite |
| Bryntum | Later verified delivery milestones, dependencies and resources | Real domain dates shown; permissions; schedule changes require authority | Timeline drag proposes change; cancellation doesn't silently change contracts |
| APIMatic | Coding context and API integration support for PayPal | Generated/client calls validated against current official APIs | Revert client change; retain payment journal; no assumed operation coverage |
| PayPal AI Toolkit | Coding assistance and sandbox tool access where supported | Tool inventory, sandbox-only auth, exact operation permissions | No agent bypass of backend approvals; missing tool uses approved API integration later |
| PayPal Sandbox | See dedicated setup design; identity/currency mapping, payment IDs, verified events | Account/API capability matrix and scenario evidence | Unknown effect reconciled before retry; void/refund are distinct compensation |

No service is included merely to claim use. Bryntum and payment operations belong in later lifecycle steps; Elastic needs controlled documents; AG Studio remains an optional analytics candidate, not selected. External-service limits, paid plans, rate budgets, API versions and retention require confirmation before implementation.

# Human-in-the-loop implementation design

Astropods documents `elicit`/`render` structured user input; Mastra supports suspend/resume, custom Node adapters can call them; standard LangChain, AI SDK, Claude Agent SDK adapters and Python lack this support in the reviewed docs. Native chat elicitation is not the ERP approval ledger. Restarts can abandon in-memory waits. Render docs reviewed establish task orchestration/triggering, not a native business approval inbox. Use backend-persisted approval records and the ERP Work queue for durable multi-role decisions.

Approval pack: request ID/version, exact action and digest, goods/amount/currency/location where relevant, evidence/unknowns, consequence, next action, permitted approver and deadline. Reviewer selects approve/reject/request changes; backend authenticates reviewer and checks current delegation, content version, state and expiry. Persist decision and outbox event atomically; execute-time check ensures approval still applies. An approval never substitutes for source data or payment-provider consent. Unknown identity, missing evidence, expired authority and timeout cannot become approval.

Request corrections do not invalidate unrelated approvals arbitrarily: dependency map identifies affected checks; conservative invalidation applies if materiality cannot be determined. Review/approval route and separation of duties are configurable; demonstration defaults must be explicit. Cancellation, rejection and requested changes have distinct statuses. Reminder escalation has an owner and due date, never automatic approval.

# Forward/recovery transitions

| Step | Forward state/event | Recovery contract |
|---|---|---|
| Capture | Draft version saved | Restore prior version, preserve history |
| Extract | Assessment proposed | Discard/supersede; preserve source |
| Confirm | Requester-confirmed version | Reopen; invalidate dependent checks |
| Discover | Candidate link saved | Unlink; keep baseline requirement |
| Check | Findings saved with inputs | Invalidate/rerun; unavailable not clear |
| Submit | Submitted baseline, review tasks | Withdraw; cancel pending review/dispatch |
| Need approval | Version-bound decision | Revoke before execution; else request compensation |
| Funding approval | Basis/limit-bound decision | Revoke; release any uncommitted fixture reservation atomically |
| Handoff | Recipient acceptance recorded | Recall requested; recipient pauses/reviews downstream impact |

Every action declares undo eligibility, actor, deadline, dependency effects, expected recovery state and verification evidence. Recovery journal states: requested, awaiting approval, running, completed, failed, manual intervention. Forward task cancellation is a request, not proof side effects stopped. Serialize action claims/version transitions; if external result is unknown, reconcile first. Human controls apply to consequential compensations. A sent message cannot be unsent; an issued commitment needs amendment/cancellation; physical returns and payments require appropriate compensation rather than record deletion.

# Future setup order and checkpoints

1. Read current bundle and confirm fixture configuration (country/currency/category/rules/personas). Create dataset definitions first; generate data only in separately authorised implementation.
2. Establish backend identity, persistence, record versioning, evidence store, action journal and approvals.
3. Implement manual intake path and deterministic fixture checks before models.
4. Add Sarvam/TypeSafe adapters, then optional discovery/retrieval; verify outages and malformed responses.
5. Connect Render and Astropods around the same persisted business state; exercise restart/retry/approval/undo races.
6. Add later procurement stages one at a time; configure PayPal Sandbox only when payment journey and merchant roles are explicit.
7. Capture results in bundle progress without claiming successful configuration from plans alone.

# Specification owner routing checkpoint — revision 0.5.0

Business owner approves goods specifications for now; RBAC implementation planned. Non-owner action creates a pending owner review and notification; no proxy approval. Missing/unavailable owners remain pending for controlled assignment. Material edits, withdrawal and owner reassignment invalidate affected reviews; stale notifications cannot authorize execution. Intake funding authority remains distinct. See [Specification Agent](/agents/goods-specification-agent.md). Design-only; implementation and tests pending. Next: goods sourcing design.

# Latest scheduling and RBAC direction

RBAC will be implemented; current delivery is design only. Render Cron Jobs plus Workflows recommended for owner reminders/retries, with immediate initial notification via outbox. See [scheduled owner notifications](/architecture/scheduled-owner-notifications.md). This supersedes earlier RBAC-deferral wording. Delivery timing/channel and detailed permission policy await review.
