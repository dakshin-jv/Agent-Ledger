---
type: Architecture Decision
title: Render scheduled owner notifications and RBAC design
description: Scheduled reminders through Render Cron Jobs and Workflows; backend authority
  and owner approval
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T17:40:00+00:00'
sources:
- id: session
  resource: '7 October 2026: user requests schedule service and RBAC implementation
    plan'
- id: cron
  resource: https://render.com/docs/cronjobs
- id: workflows
  resource: https://render.com/docs/workflows
bundle_revision: 0.5.0
implementation_status: not-started
---

# Service fit and recommendation

Render Cron Jobs plus Render Workflows fit scheduling within the already-prioritised stack. Render documents cron-triggered workflow tasks. Cron runs in UTC and cannot access a persistent disk. Therefore the scheduled dispatcher calls authenticated backend APIs; it does not open the database directly. This is the proposed service choice, not a deployment or native owner-email feature. Delivery channel remains in-app by default; external email/push provider remains unselected.

# Scheduled notification design

Create the pending approval and initial notification outbox atomically when a non-owner submits. Initial dispatch is event-driven for prompt delivery; recurring cron handles due reminders, retries and escalation rather than delaying all first notices until a cron tick. One recurring dispatcher scans due schedules across decisions, not one cron service per request. Interval is configurable with documented maximum expected reminder delay; no exact-time delivery promise.

Backend owns `notification_schedule`: ID, tenant, decision ID, target specification version, current owner ID, notification kind, due_at UTC, display timezone, cadence/expiry, next_attempt_at, attempt count, event key, pending/claimed/sent/cancelled/failed status, task correlation and evidence. Store recipient as an identity reference, not arbitrary caller-supplied address. Resolve current authorised delivery destination at use time.

Cron requests an atomic bounded claim of due entries; Render Workflow executes dispatch through backend-approved notification API. Recheck pending approval, version, current owner and RBAC immediately before sending. Delivery attempts use stable idempotency keys. External provider duplicate suppression is required if later email/push delivery is added; backend deduplication alone does not guarantee exactly-once external delivery after an ambiguous timeout. Record sent/failed/unknown outcomes and reconcile where possible.

Approval/rejection, withdrawal, superseding edits and authorised owner reassignment cancel obsolete schedules; material edits create fresh review/schedule entries. Jobs already in flight recheck validity and skip stale work. Already delivered notices cannot be unsent; their links display current authoritative state. Deadline escalation requires a configured accountable destination, never guessed approver or automatic approval. No ChatGPT reminder or real message is created by this design.

# RBAC implementation planned — not deferred as a feature

User now explicitly plans RBAC. Backend authorization must combine role permissions with tenant/entity scope, record ownership and workflow state. Proposed roles: requester (create/edit own permitted drafts, submit/withdraw), business owner (review assigned specifications), funding owner (separate intake funding confirmation), procurement analyst (prepare/check/coordinate), administrator (controlled assignments and role management), automation service (narrow dispatch/validation permissions). Roles are proposals; permission matrix and separation-of-duties rules require review before implementation.

A business-owner role alone is insufficient: the actor must also be the current assigned owner within scope. Requesters cannot change owner to themselves as an approval bypass. Agents/schedulers cannot grant roles or approve decisions. Administrators do not gain business approval automatically. Role/delegation changes apply immediately to pending decisions and execution-time checks. Approval already used may require authorised compensation rather than retroactive history alteration. Notification links confer no rights.

Capture user ID, action, resource/version, policy version and allow/deny outcome in restricted audit records. Check permissions for reads and evidence as well as writes. Avoid leaking specification content in notifications outside permitted scope. Map human-role changes and notification destinations to current identity data.

# Setup and verification slots

Future setup: backend API authentication and schedule table; event outbox; bounded cron dispatcher; workflow retry policy; in-app notifications; UTC/timezone handling; RBAC middleware/policy; cancellation and reconciliation. All remain unconfigured. Test non-owner routing, assigned-owner approval, role revocation, ownership change, missed cron runs/catch-up, duplicate jobs, notification failure, stale links, cancellation race and restart. Persist expected/actual outcomes later.

# Recovery

Every schedule can be cancelled or rescheduled with history. Disabling cron pauses delivery, not approval records; re-enable catches up only still-valid due entries. Cancelling a run is not proof no notification was sent. On unknown delivery, reconcile or use channel idempotency; never retry a business approval/payment as a notification retry. Recoverable scheduling failure leaves the owner's Work item visible. Full RBAC design detail and delivery timing/channel are the next refinements.
