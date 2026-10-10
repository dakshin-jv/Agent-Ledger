---
type: Design Specification
title: 'Goods procurement datasets: design-only contracts'
description: 'Goods procurement datasets: design-only contracts'
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T17:20:00+00:00'
sources:
- id: session
  resource: 'User design decisions, 7 October 2026: goods only, demo data, TypeSafe,
    human review, undo and design-only delivery'
bundle_revision: 0.5.0
design_progress: specified-awaiting-review
implementation_status: not-started
---

# Authority and scope

User-confirmed: goods only; services deferred; use labelled demo enterprise records; use PayPal Sandbox for supported payment/account operations; include TypeSafe AI, human review and recovery at every step. This document specifies datasets, not actual seed data, SQL, migrations or running services. Proposed field contracts and scenario counts below are reviewable design choices. No organisation-specific rules, currency, country, product category or monetary thresholds are finalised.

# Shared record conventions

Every business record carries `id`, `tenant_id`, `entity_id` where applicable, `version`, `created_at`, `updated_at`, `created_by`, `data_origin`, `source_ref`, `demo_scenario_id` when synthetic and lifecycle status. Origins: `demo_fixture`, `user_input`, `external_channel3`, `paypal_sandbox`, `derived`. Derived records retain all source origins. Do not label a mixed record simply real or demo: show provenance per relevant field. Times stored UTC, displayed with configured timezone. No real employee, bank or supplier identities in fixtures.

Identifiers are stable opaque values. Foreign keys include tenant scope. Money uses decimal strings with currency and configured minor-unit precision; quantities use decimal strings and controlled units. No binary floating-point money calculations. Unknown values are null with reason, never zero. Physical units require explicit conversion factors; pack size must be distinct from item count. Dates cannot silently become midnight in an inferred timezone. Evidence links must resolve to authorised documents; malformed or inaccessible evidence is unverified.

Backend owns writes. Agents submit proposals through business APIs. Optimistic version checks reject stale edits. Revisions, withdrawals and compensation events preserve previous records. Archive rather than erase auditable records. Retention and authorised deletion policy remain to be configured.

# Dataset catalogue and field contracts

Required fields below refer to a valid active record; drafts may lack fields subject to explicit readiness rules.

| Dataset / owner | Main fields and relationships | Validation / control | Recovery |
|---|---|---|---|
| Organisation / admin | Tenant, entities, departments, cost centres, receiving locations, timezone, default currency; parent IDs | Active entity/location; cost centre belongs to entity; currency is configuration | Version configuration; prevent changes that orphan transactions |
| Users and delegation / admin | User, role assignments, entity/cost-centre scope, delegate, validity dates, permitted actions, approval rule reference | Authenticated identity; explicit delegation; self-approval/separation rules configured; agent cannot create own authority | Revoke future access; historical actor remains; reroute pending tasks |
| Goods master / procurement | Internal item ID, description, category, unit, pack quantity, functional specs, mandatory criteria, inspection owner, active flag | Goods only; distinguish equivalent item vs exact match; specification owner approves | Supersede item/spec version; invalidate affected matches |
| Inventory / receiving | Item/location, on-hand, reserved, quarantined, snapshot time; reservation ID, quantity, request line | Available quantity derived from authoritative components; no negative/duplicate allocation; fixture truth labelled | Release reservation atomically; physical movement uses adjustment/return event |
| Approved suppliers / procurement | Supplier identity, categories, qualification status, evidence, review/expiry date, approved entity scope, optional sandbox merchant mapping | Channel3 retailer is not automatically approved; expiry visible; payment mapping independently verified | Suspend prospective use; reassess dependent selections; no silent remap |
| Contracts and coverage / contract owner | Supplier, entity, validity, item/spec coverage, price/currency/unit, ceiling and used commitment, delivery/payment terms, document version | Executed status, validity and remaining coverage checked; textual similarity alone insufficient | Amend with authority; invalidate stale coverage checks; preserve baseline |
| Budget / finance | Period, entity/cost centre, currency, approved allocation, reservations, committed and actual amounts, funding owner | Demo ledger; reservation-to-commitment-to-actual conversions do not double count; available formula governed by ledger state | Release uncommitted reservation; reverse/reclassify entries with authority |
| Procurement policy / governance | Rule ID/version, applicability, required checks, blocking reasons, approval routes, competition rules, tolerances, exception authority | No universal thresholds; incomplete policy means unavailable governance check; fixture rules explicitly illustrative | Version rules; determine impact on pending requests; never rewrite past approvals |
| Requisition header / requester | Purpose, entity, department, cost centre, owner, location, required date, status, submitted version, funding route | Required for routing; purpose confirmed by requester; request is not PO or payment | Draft restore, withdraw or downstream recall |
| Requisition lines / requester | Item description, quantity/unit, mandatory specs, optional item ID/candidate, estimated cost/currency, estimate source/time | Positive quantity; at least one goods line; null estimate permitted with reason; candidate cannot alter required specs silently | Restore line revision; invalidate dependent checks/approvals |
| Discovery candidates / external adapter | Channel3 product/offer IDs, retailer, URL, title, structured attributes, price/currency, availability claim, locale, retrieved time, raw-response reference | External snapshot, not bid, approved supplier, stock truth or delivery guarantee; locale coverage checked | Unlink candidate; refresh snapshot; preserve original requirements |
| Evidence documents / record owner | Document ID, hash, version, classification, origin, permitted audience, storage reference, extraction anchors | Tenant/role access; immutable approved source versions; bidder isolation reserved for future RFx | Supersede extraction/document; retain prior evidence subject to retention policy |
| Validation findings / backend | Check ID, request version, rule version, source versions, `clear/flagged/unavailable`, severity, blocking flag, reason, owner, checked time | Failure never becomes clear; deterministic arithmetic; duplicate matching only flags unless confirmed | Invalidate and rerun; human disposition records reason and authority |
| AI assessments / agent owner | Task/model/provider version where exposed, source refs, schema version, response, missing fields, ambiguities, suggested action, reviewer edits | Sarvam interpretation and TypeSafe structured assessment are proposals; schema/field-path validation; no approval state in AI response | Discard/supersede assessment; manual structured input remains available |
| Human decisions / named owner | Request version, exact action/payload digest, decision, role, actor, time, reason, authority-rule version, expiry | Pending/approved/rejected/changes-requested/revoked/expired; approval binds reviewed content; timeout is not consent | Revoke before use; after execution start compensation request |
| Workflow runs / backend | Request/run IDs, step, attempt, task IDs, agent refs, input versions, outcome, correlation key, timestamps | Agent status separate from request and approval; bounded retries; no ephemeral authoritative state | Cancel requested, reconcile completed effects, resume from persisted state |
| Action and recovery journal / backend | Unique action key, target/version, before/after refs, side-effect ID, recovery action, approver, state, error, original-action link | Recovery contract for every step; atomic claim prevents execution/undo race; failed recovery stays visible | Retry safe compensation or escalate; never erase the original event |
| Handoffs and work items / next owner | Version, sender/recipient role, decision pack, acceptance time, next action, due date, status | Named recipient accepts responsibility; handoff task deduplicated | Recall requested; recipient acknowledges pause and dependency impact |
| Notifications / backend | Work item, recipient, event key, channel, delivery result, reminder deadline | Notification is not authority; retry delivery without duplicate business action | Supersede/cancel future reminder; sent message remains logged |
| Supplier/contract obligations / future contract owner | Deliverables, KPI definitions, milestone, due date, evidence, warranty, claim, owner | Future lifecycle reference only; separate operational completion from financial/residual closure | Authorised variation or reopening; no expiry-only full closure |

# Budget semantics

Design separate reservation, commitment and actual ledgers. A request estimate does not reserve automatically. If reservation is later enabled, policy specifies when. On conversion, release/reduce the prior reservation and add commitment in one transaction. On actual posting, consume the relevant commitment. Available budget derives from allocation less active reservation, outstanding commitment and actual consumption according to configured accounting rules. No sum of currencies without explicit FX source, rate date and conversion approval. PayPal balance never changes enterprise budget directly.

# Screen and AI contract

Create Goods Requisition contains need text/voice, attachments, header fields, editable AG Grid goods lines, optional discovery, evidence-backed findings and review summary. Preserve original transcript alongside requester correction. TypeSafe response schema: `schema_version`, `request_version`, `missing_fields[{field_path,question}]`, `ambiguities[{field_paths,reason,evidence_refs}]`, `evidence_refs`, `suggested_next_action` from `clarify/run_checks/request_owner_review`, and `review_reasons`. Backend rejects unknown fields/actions and unsupported evidence claims. Confidence may be retained only if the provider supplies it; it never grants permission.

# Readiness and progressive population

Intake may save incomplete draft. Submission requires requester-confirmed purpose, owner/routing fields, delivery details, at least one positive-quantity goods line and interpretable mandatory specs. Price estimate can remain unknown, but funding confirmation must document its basis and any limit before handoff. Required unavailable checks block readiness unless an explicitly authorised policy exception records alternative evidence. Optional discovery failure does not block. Duplicate flags are reviewed; no automatic merge. Stock sufficiency prompts reuse review, not silent cancellation of demand.

# Proposed scenario fixture plan — definitions, not generated data

Use isolated scenario namespaces and explicit fixed clock per scenario; proposed relative deadlines derive from that clock, avoiding eventual expiry of static dates. One fictional tenant with configurable entities, departments and approver roles is enough initially. Values, category, country, currency and counts are not user-selected. Use synthetic product requirements; external product snapshots remain separately labelled.

| Scenario | Fixture conditions | Expected observable outcome |
|---|---|---|
| G01 clean intake | Complete goods request, no duplicate, verified fixture checks, valid reviewers | Specification handoff only after both required confirmations |
| G02 missing fields | Missing quantity/location/spec | Clarification; draft preserved |
| G03 unit ambiguity | Pack vs each inconsistent | Requester resolves; deterministic total recalculated |
| G04 duplicate | Similar open request and supporting lines | Review flag; merge/withdraw only through authorised decision |
| G05 stock sufficient | Available stock satisfies compatible specs | Reuse option shown; procurement continuation requires disposition |
| G06 contract covered | Active compatible contract with capacity | Existing-contract route recommended with evidence |
| G07 contract expired | Similar contract expired | No valid coverage claim |
| G08 policy unavailable | No applicable configured rule | Blocking unavailable check; governance review |
| G09 funding unresolved | Missing basis or insufficient fixture allocation | No handoff; funding owner decision |
| G10 discovery outage | Channel3 failure/unsupported locale | Manual goods intake continues; discovery unavailable |
| G11 model invalid/outage | Sarvam/TypeSafe malformed result or timeout | Manual correction; no fabricated assessment |
| G12 authority/stale approval | Wrong role, revoked delegation or changed request | Reject decision/use; request current review |
| G13 withdraw/race | Withdrawal overlaps approval or dispatch | Exactly one permitted transition; no orphan continuation |
| G14 restart/duplicate | Task retried or backend restarted | Pending review survives; single handoff |
| G15 recall failure | Specification has dependent work | Recall pending; owner reviews effects and recovery |
| G16 evidence isolation | Wrong tenant/document audience | Access denied; no source leakage |

Later PO/receipt/invoice/payment fixtures use linked item, contract, quantity, tax basis, acceptance and invoice-uniqueness evidence. Intake does not pretend these later stages are already approved. Inspection, match, performance and closeout schemas are reserved extensions, to specify agent by agent rather than build now.

# Specification owner routing checkpoint — revision 0.5.0

Business owner approves goods specifications for now; RBAC implementation planned. Non-owner action creates a pending owner review and notification; no proxy approval. Missing/unavailable owners remain pending for controlled assignment. Material edits, withdrawal and owner reassignment invalidate affected reviews; stale notifications cannot authorize execution. Intake funding authority remains distinct. See [Specification Agent](/agents/goods-specification-agent.md). Design-only; implementation and tests pending. Next: goods sourcing design.

# Latest scheduling and RBAC direction

RBAC will be implemented; current delivery is design only. Render Cron Jobs plus Workflows recommended for owner reminders/retries, with immediate initial notification via outbox. See [scheduled owner notifications](/architecture/scheduled-owner-notifications.md). This supersedes earlier RBAC-deferral wording. Delivery timing/channel and detailed permission policy await review.
