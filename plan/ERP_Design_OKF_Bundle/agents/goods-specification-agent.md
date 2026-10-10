---
type: Agent Design Specification
title: Goods Specification Agent and business-owner decision routing
description: Versioned goods specifications, owner notifications, fallback paths and
  recovery contracts
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T17:36:14+00:00'
sources:
- id: session
  resource: '7 October 2026 user confirmation: business owner approves for now; RBAC
    later; route non-owner decisions as notifications; user authorises fix'
bundle_revision: 0.5.0
design_progress: specified-awaiting-validation
implementation_status: not-started
---

# Confirmed direction

Goods only, design only. Business owner approves specifications for now. RBAC will be implemented; this update defines its design only. If the acting user is not the assigned business owner, route the decision to that owner through an approval work item and notification. This is a specification-stage approval rule, not an override of the distinct funding-owner gate defined for intake. No software, service setup or API test is performed by this update.

# Human decision routing — current rule

Backend resolves the assigned business owner from the request, never from an AI suggestion or notification recipient supplied by a caller. Authenticate the acting user. If that user matches the assigned owner, present the same version-bound approval pack and allow an explicit decision. Being the owner never automatically approves work. If the user differs, allow submission and clarification, create one pending owner decision in Work, and notify the owner. That user cannot approve on the owner's behalf. Ownership does not confer funding, contract-signature or payment authority.

Pack includes request/specification IDs and versions, requirements, evidence, unresolved issues, change summary, decision needed, effect of approval and configured deadline. Owner chooses approve, reject or request changes. Approval binds the exact reviewed content; current version and owner identity are rechecked when the decision is saved and before handoff. No open blocking concern may be silently accepted. Qualified review remains necessary for unresolved specialist/safety issues; business-owner identity alone does not resolve them.

Notification is a pointer to the authoritative work item, not an approval or bearer authorization. Its channel is unselected; in-app Work/notification UI is the design baseline. Email or other channels may be configured later. No real notification is sent here. Deduplicate using decision ID, recipient and notification event/version. Delivery failure does not lose the work item; record delivery status and retry within configured limits. Reminder and escalation durations remain configurable, not invented SLAs. A read receipt, timeout, natural-language model response or notification delivery cannot become consent.

Missing owner: pending assignment with named administrative resolution queue where configured; never select an arbitrary approver. Unavailable owner: retain pending state and flag reassignment. Reassignment needs a controlled accountable operator procedure, to be configured before implementation, and cannot be self-service bypass. On authorised reassignment, invalidate outstanding owner decision, close obsolete review work and route a new review to the new owner, preserving history. Full role-based rules will extend these controls later; authenticated identity, owner matching and tenant isolation are needed from the first prototype.

# Happy path and per-step recovery

| Step | Forward action / output | Recovery |
|---|---|---|
| Receive intake | Accept approved request version, evidence, need/funding confirmations and named owner | Return deficient handoff with reasons; preserve intake history |
| Structure | Sarvam interprets goods requirements; editable draft fields with original source anchors | Discard extraction or restore previous draft; preserve original input |
| Check | TypeSafe flags ambiguity/contradictions; backend validates units, types and evidence references | Invalidate findings and rerun affected checks |
| Define evaluation/acceptance | Draft requirement-to-bid-evidence-to-evaluation-to-acceptance matrix | Restore previous row version; invalidate affected approvals |
| Submit review | Freeze specification version; resolve owner and create work item | Withdraw; cancel pending work and future reminders |
| Owner decision | Explicit approve/reject/request changes on that version | Revoke before use; if used, initiate recall/compensation |
| Handoff to sourcing | Persist approved specification and recipient acceptance | Request recall, pause dependent work, assess downstream effects; no automatic deletion |

Request status, specification status, agent run status and approval state remain separate. Proposed specification states: draft, needs clarification, awaiting owner, changes requested, approved, handed off, withdrawn; approval revocation/reopening must preserve history. Failed/cancelled agent runs never imply withdrawn or approved business state. Reconciliation required if cancellation arrives after a side effect has occurred.

# Requirement dataset

Each requirement has stable ID, tenant/request/line IDs, specification version, text, structured value/unit where relevant, mandatory/desirable class, rationale, original source/version/anchor, proposed bid evidence, evaluation method, acceptance method, tolerance where relevant, acceptance owner, finding references and review status. Missing applicable fields are explicit unknowns. Do not invent engineering tolerances, standards or safety certifications. Delivery, compatibility, packaging, installation, warranty and quality fields appear where relevant to the goods category rather than becoming universal requirements.

Every mandatory requirement needs a measurable evaluation and acceptance method, or an explicitly reviewed explanation for an inapplicable method. Contradictory or unsupported mandatory criteria remain blocking. Technical interpretations and changes to intake scope go back for requester/owner confirmation; scope/value changes also trigger affected intake funding/need checks. Candidate attributes never overwrite required specifications without confirmation.

# Structured agent output contract — proposed

`schema_version`, `request_id`, `request_version`, `specification_id`, `specification_version`, `requirements[]`, `findings[]`, `clarification_questions[]`, `source_refs[]`, `suggested_next_action`.

Requirements follow the dataset above. Finding includes ID, code, severity, affected requirement/field IDs, reason, evidence refs, proposed resolution and `requires_human_review`. Question includes affected field, question and intended respondent role. Suggested action enum: clarify, revise_draft, request_owner_review. No output field can grant authority, mark human approval or commit a handoff. Backend determines blocking status from configured validation rules; model severity does not override policy. Reject schema mismatch, unknown field paths, cross-tenant refs and invented evidence. Deterministic checks reperform quantities/unit conversions; qualitative correctness needs owner review.

# Fallback and recovery scenarios

| Trigger | Containment / next owner | Resume condition / recovery |
|---|---|---|
| Missing detail or vague measure | Keep draft; ask requester | Confirmed measurable requirement; rerun findings |
| Conflicting requirements/units | Block affected rows; show source conflict | Owner resolves; preserve alternative versions |
| Unsupported supplier/product claim | Mark unverified; retain candidate provenance | Valid supporting evidence or approved requirement revision |
| Brand-restrictive wording | Flag and ask for functional/compatibility rationale | Owner documents rationale; sourcing policy review when required |
| Required standard unavailable | Mark check unavailable, never compliant | Authorised source/qualified review obtained |
| Model/Elastic/Channel3 outage | Persist progress; manual editing; optional discovery can be skipped | Valid manual evidence or safe bounded retry |
| Current user not owner | Pending Work item; notify assigned owner | Owner explicit decision |
| Missing/unavailable owner | Hold owner decision; flag assignment/reassignment | Controlled assignment recorded and fresh review routed |
| Notification fails | Keep Work item; record error and bounded retry | Owner acts through authenticated queue; delivery is not approval |
| Material edit after submission | Supersede review; invalidate affected approvals | New version reviewed; old notifications cannot approve new content |
| Stale/duplicate owner response | Reject stale use; duplicate same decision is idempotent | Current review remains authoritative |
| Withdrawal overlaps approval | Atomic state/version transition prevents both progression and withdrawal | Reconcile winner; no orphan continuation |
| Owner changes | Invalidate outstanding review; preserve audit | New owner reviews current version |
| Specialist/safety concern unresolved | Block affected specification; request qualified input | Evidence-supported disposition; no owner-only competence assumption |
| Recall after sourcing started | Pending recall; notify downstream owner and pause affected work | Confirm dependency assessment and compensation; retain unresolved state if failure |

# Service contributions and boundaries

Sarvam handles interpretation/clarification; TypeSafe generates structured findings; Channel3 supplies external candidate attributes; Elastic retrieves permitted documents; AG Grid displays/edit requirements and review matrix; Astropods hosts shared agent; Render executes bounded checks/continuations; backend owns records and approvals. PayPal/APIMatic/Toolkit and Bryntum have no forced role in this specification stage. They remain reserved for payment development and meaningful timeline/delivery work respectively.

# Acceptance definitions — tests pending

Verify owner and non-owner paths; missing owner; notification outage; stale link/version; wrong tenant; duplicate response; ownership change; material edit; rejection/change request; withdrawal race; restart pending review; unresolved technical concern; approved handoff and recall. Assert that only current assigned-owner explicit approval of the current non-blocked version enables sourcing readiness, alongside still-valid applicable intake gates. Capture expected/actual results later; no test has run here.

# Next design step

Review this contract, then design goods sourcing/market analysis happy path, retaining approved specification as input. Fixture country/currency/category, notification delivery channels, timing, controlled owner reassignment and detailed RBAC policy remain open configuration items. No implementation approval is inferred from design agreement.
