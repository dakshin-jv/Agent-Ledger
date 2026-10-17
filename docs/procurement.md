# Procurement (goods)

**Read when:** designing or implementing the goods procurement agent and its case lifecycle (intake → spec → funding gate → source → purchase order → goods receipt → invoice receipt → pay).

**Do not use for:** PayPal API contracts ([`paypal.md`](paypal.md)); Channel3 search syntax ([`channel3.md`](channel3.md)); harness primitives, Blueprint, or Workflow IaC ([`render_agent_sdk.md`](render_agent_sdk.md)); Cursor MCP install ([`coding-agents.md`](coding-agents.md)); Render ops ([`render.md`](render.md)).

Stage is `docs` → `agents` → `refine`. This area is **docs / inprogress**. Do not implement a slice the user has not authorized. The Render harness contract is **superseded as a build track** ([`render_agent_sdk.md`](render_agent_sdk.md)); do not add `backend/src/harness/` from that file. `ProcurementDiscoveryAgent` is a read-only Channel3 wrapper; it is not the lifecycle.

Goods only. Services wait on data. One **case** end to end. Chat drafts and routes; it does not replace the ledger, permissions, or history.

## Role

A commerce operator states a purchasing intent. The procurement **capability** drafts on that case: lines, evidence, owner, and next action. Home, Work, Orders, Money, Network, and Intelligence are views of the same case. Finance functions (AP, treasury, pay) stay distinct from this cross-functional flow (OKF D-17). Agents are capabilities, not pages.

Method: [`plan/ERP_Design_OKF_Bundle/`](../plan/ERP_Design_OKF_Bundle/) · shared agents: [`agents/shared-agent-model.md`](../plan/ERP_Design_OKF_Bundle/agents/shared-agent-model.md) · first brief: [`next-steps/procurement-agent.md`](../plan/ERP_Design_OKF_Bundle/next-steps/procurement-agent.md) · spec gate: [`agents/goods-specification-agent.md`](../plan/ERP_Design_OKF_Bundle/agents/goods-specification-agent.md) · command UX: [`design/command-interactions.md`](../plan/ERP_Design_OKF_Bundle/design/command-interactions.md) · open questions: [`next-steps/todo_edgecases.md`](../plan/ERP_Design_OKF_Bundle/next-steps/todo_edgecases.md).

Loops, HITL, `invoke` / `resume`, Blueprint split (reference only): [`render_agent_sdk.md`](render_agent_sdk.md). Astropods is out of scope.

## Rules

These bind every step. Edge-case *questions* live in [`todo_edgecases.md`](../plan/ERP_Design_OKF_Bundle/next-steps/todo_edgecases.md); do not invent answers there.

| Rule | Meaning |
| --- | --- |
| One case | Requisition id is the thread (`case_id`). No per-order deployed agent. |
| One isolated run | The harness `invoke`s / `resume`s one case inside granted authority. |
| Intent → draft → owner → funding | The model never approves. Funding is a **separate gate**, not a node in the sourcing graph. |
| Chat ≠ ledger | Intake cards and Sarvam tokens draft. Owner decide is Work. A streamed reply is not consent. |
| Three statuses | Business (`requisitions.status` / approvals), agent run (`node_run`), platform (Render task-run). A finished Workflow is not an approved spec. A failed task does not withdraw the case. |
| Owner identity | Backend resolves the assigned business owner from the record. Non-owner action creates Work for that owner. No proxy approval. |
| Version bind | Approval binds the reviewed version. Material edit, withdraw, or owner reassignment invalidates outstanding reviews. |
| Provenance | Channel3 saves as `external_channel3`. Uploads are `user_upload`. Listings are not suppliers, contracts, or payees. |
| Idempotency | Mutates carry `correlation_key`. Never `Retry` persist, approve, or PayPal. |
| Recovery | Every step has withdraw, undo, or reverse. Do not delete history. |

## Design steps

Happy path first, then fallbacks, this agent only ([`workflow-method.md`](../plan/ERP_Design_OKF_Bundle/agents/workflow-method.md)).

1. Confirm goods-only intake, named owner, and still-valid funding as a **later** gate.
2. Specify inputs, permitted tools, evidence fields, and structured outputs per stage.
3. Put owner review on the **normal** path (node `hitl`), not as an afterthought.
4. Show the confirmed outcome on the case (Work + Orders), with audit.
5. Define what Home / Work / Orders show while the run is in progress (guided intake is a case panel, not a Home chatbot).
6. Add fallbacks: missing input, no candidate, discovery outage, timeout, concurrent version, reject, uncertain pay outcome.

Build slices when authorized. Harness contract (reference, not a kit to build): [`render_agent_sdk.md`](render_agent_sdk.md).

| Slice | Outcome | Not yet |
| --- | --- | --- |
| 0a Intake cards | Case panel: single / multi / Other; persist answers; no models | Deploy |
| 0b SSE copy | Web API streams Sarvam tokens (`sarvam-105b-conversations`) | Stream via Workflow |
| 0c TypeSafe turn | After submit: completeness, contradictions, next `question` schema | LLM-picked next field |
| 0d Upload + extract | Evidence file + Sarvam Doc-AI; original kept | Sandbox VM |
| 0e Spec review | Ready → existing `submit_for_owner_review` | Funding graph |
| 1–5 Harness + sourcing | Graph, workspace API, `invoke` / Channel3 / `hitl` / `resume` | Internal stock/contracts; PayPal |
| 6 Ship | Local Workflows then the one Blueprint | Per-dept Blueprints |

## Lifecycle

Same case throughout. AP attaches at invoice receipt; it does not own the case. Cash out is the last gate.

```text
intent (Home / command / Orders case panel)
  → intake draft          ledger: requisition; cards + uploads + SSE
  → specify               Sarvam draft + TypeSafe findings
  → hitl (spec)           Work; version freeze
  → funding gate          separate authority; not this graph
  → source                Channel3 + harness graph (proof)
  → hitl (source)         Work; accept / reject / changes
  → purchase order        record on the case; not payment
  → goods receipt         receipt vs PO; not payment
  → invoice receipt       3-way match; invoice accept ≠ pay
  → pay                   PayPal Sandbox after funding + IR
  → recover               withdraw / recall / compensate
```

### 1. Intake (guided panel)

Operator states purpose. API creates a `draft` requisition (`FoundationStore.create_requisition`): tenant, requester, assigned business owner, purpose, version 1, `data_origin=user_input`. Empty purpose is refused.

Surface: a **case panel** on Home command or Orders — transcript plus **question cards**, not a generic chatbot and not a persistent Home bot ([`command-interactions.md`](../plan/ERP_Design_OKF_Bundle/design/command-interactions.md), [`home.md`](../plan/ERP_Design_OKF_Bundle/design/home.md)). Bryntum stays Grid / TaskBoard / Scheduler / Gantt ([`bryntum.md`](bryntum.md)). Intake is custom React.

Each turn:

1. User uploads a document, clicks options, and/or types Other.
2. Browser `POST`s **structured** answers (not “the model parsed the click”).
3. API persists evidence + answers on the case (`correlation_key`).
4. TypeSafe `judge` (fast, structured): completeness, unit ambiguity, contradictions, next question **schema**.
5. Sarvam streams copy for the next prompt (`stream=true`; prefer `sarvam-105b-conversations`). Original user/Sarvam text stays as evidence.
6. UI applies SSE events; refresh reloads from Postgres.

Card kinds: `single` (radio), `multi` (checkboxes), always an **Other / suggestions** slot. TypeSafe Choice fills closed options; code owns the form. No field grants approval.

Uploads: `POST /cases/{id}/evidence` (multipart). Store hash + `data_origin=user_upload`. Extract via Sarvam Doc-AI (`/doc-ai/v1/job/extract`) as a **proposal**; keep the original. A sandbox VM is not required for this step.

SSE events from the **web service** (illustrative):

```text
event: token      # Sarvam fragment
event: question   # { id, kind: single|multi, options, allow_other: true }
event: finding    # TypeSafe flag + confidence
event: draft      # requirements[] after the turn
event: done       # suggested_next: clarify | revise_draft | request_owner_review
```

Keys stay on the API. Browser never holds `SARVAM_API_KEY` / `TYPESAFE_API_KEY` / `CHANNEL3_API_KEY`.

### 2. Specification

On the same case, structure goods requirements. Sarvam interprets; TypeSafe flags ambiguity and contradictions; backend validates units and evidence refs. Output is a **proposal** (`schema_version`, requirements, findings, clarification questions). No field grants authority or marks approval ([`goods-specification-agent.md`](../plan/ERP_Design_OKF_Bundle/agents/goods-specification-agent.md)).

Submit freezes the version (`submit_for_owner_review`) and opens Work for the assigned owner.

### 3. Owner on spec

Owner chooses approve, reject, or request changes on **that** version (`decide_approval`). Being the owner never auto-approves. Notification is a pointer to Work, not consent. Missing owner stays pending assignment. After approve, the case is sourcing-ready **only if** intake funding is still valid — funding is checked, not inferred.

### 4. Funding gate

Distinct from business-owner spec review. Funding owner / still-valid need. The sourcing graph must not skip this. PayPal is not started here.

### 5. Sourcing (v1 harness proof)

Sourcing graph (contract walkthrough, not a harness build): [`render_agent_sdk.md` — Walkthrough](render_agent_sdk.md#walkthrough-procurement-sourcing). Internal stock/contracts are the intended first look; Channel3 is **external observation** when those are absent or insufficient. A Channel3 retailer is not an approved supplier.

```text
API start invoke(case_id)
  start        load case via API
  choice       System 1: search | hitl
  search       tool Channel3 (ctx.run, tool-retry middleware)
  persist      workspace key candidates.json; node_run complete
  rank         System 1 score per candidate
  gate         low confidence → hitl
  draft        System 2 complete (brief only, not the file)
  judge        System 1 ready_for_owner
               cycle draft→judge until max_visits or hitl
  persist      proposal on the case
  hitl         HITL: process exits
API resume(case_id) after owner accept → end
```

`discovery_candidates` stores snapshots (`external_channel3`, `correlation_key`). Persist through the API, not the Workflow disk. Workspace paths in the kit (`/scratch/candidates.json`) are **logical names**.

Existing code: [`backend/src/agents/procurement.py`](../backend/src/agents/procurement.py) (`ProcurementDiscoveryAgent.discover_external_options`), [`backend/src/integrations/channel3.py`](../backend/src/integrations/channel3.py), migration [`002_discovery_candidates.sql`](../backend/migrations/002_discovery_candidates.sql).

Intake turns stream on the web API. Sourcing `invoke` is JSON in/out — no token pipe to the browser. Node `hitl` exits; Work is the interrupt. Refresh reloads the case from Postgres.

### 6. Purchase order (PO)

After owner-accepted source **and** still-valid funding: a PO **record** on the case. Owner-accept of a source does not send a PO by itself. Duplicate send is one effect. Unsent withdraw ≠ recall of a sent PO.

### 7. Goods receipt (GR)

Goods receipt vs the sent PO. Partial, qty mismatch, and quality fail stay on the case. Receipt without a sent PO is refused. GR is not payment.

### 8. Invoice receipt (IR)

AP matches invoice vs PO vs GR on this case. Invoice accept is not cash out. Over-tolerance waits on owner/funding. Duplicate invoice is one effect.

### 9. Pay

Authorised PayPal **Sandbox** only, after accepted IR and still-valid funding ([`paypal.md`](paypal.md)). Never `Retry` capture because a Workflow timed out. Reconcile unknown outcomes before a second attempt. Channel3 “pay this shop” is refused.

### 10. Recover

Requester may withdraw before approved execution (`withdraw_requisition` + `recovery_journal`). After commit: recall/amend/compensate, not delete. Concurrent agent run rechecks current version. Rejection stops that path; the case remains.

## Case memory

Working context lives on the case via the API, not a Workflow disk. System 2 messages are a **brief**, not raw files or node-run status.

| Layer | Holds for this flow |
| --- | --- |
| Ledger | requisition, version, owner, approvals, candidates, audit |
| Working memory | `intake_answers.json`, `extract.json`, `requirements_draft.json`; sourcing `candidates.json`, `proposal.json`; `node_runs`, todos |
| Model context | Summarize middleware → short brief |

Observe as three statuses (business / agent run / platform). Structured logs carry `case_id`, `node`, `correlation_key`.

## What this flow uses

| Need | Service | Role here |
| --- | --- | --- |
| Catalog search | Channel3 | External snapshots only (`external_channel3`) |
| Judgments / next card | TypeSafe System 1 | Edges, scores, findings, Choice — not prose, not approve |
| Draft / SSE / extract / other System 2 actions | Sarvam | Intake `sarvam-105b-conversations` streamed; sourcing `complete` from a brief; STT/TTS/translate/Doc-AI as the node requires; outputs are proposals |
| Pay | PayPal Sandbox | Last gate, after IR + still-valid funding |
| Lists / board | Bryntum | Work / Orders; intake is custom React |
| Retrieval | Elastic | Later; not the ledger |

Harness graph, middleware, `invoke` / `resume`, and Blueprint (reference): [`render_agent_sdk.md`](render_agent_sdk.md). Skills / MCP for a coding session: [`coding-agents.md`](coding-agents.md).

## Ledger already on the case

| Record | Role in this lifecycle |
| --- | --- |
| `requisitions` | Case; status draft / awaiting_owner / approved / withdrawn |
| `approvals` | Version-bound owner decision |
| `audit_events` | Every mutate; unique `correlation_key` |
| `notification_outbox` | Pointer to Work; delivery ≠ consent |
| `recovery_journal` | Withdraw / later compensate |
| `discovery_candidates` | External snapshots only |

Do **not** add `agent_runs`, `node_runs`, `case_workspace`, `case_todos`, or tool-counter tables this pass. Agent-runtime save is deferred ([`observability.md`](observability.md)).

## Related

[`AGENTS.md`](../AGENTS.md) · [`coding-agents.md`](coding-agents.md) · [`render_agent_sdk.md`](render_agent_sdk.md) · [`guardrails.md`](guardrails.md) · [`observability.md`](observability.md) · [`render.md`](render.md) · [`channel3.md`](channel3.md) · [`typesafe.md`](typesafe.md) · [`sarvam.md`](sarvam.md) · [`paypal.md`](paypal.md) · [`elastic.md`](elastic.md) · [`bryntum.md`](bryntum.md) · [`plan/BUILD_START_HERE.md`](../plan/BUILD_START_HERE.md)
