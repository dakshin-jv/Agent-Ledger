# Observability

**Read when:** defining what a product-agent tick is allowed to show or log (case/Work, Render ops). Not for designing a run store.

**Do not use for:** guardrail policies ([`guardrails.md`](guardrails.md)); Elastic as retrieval ([`elastic.md`](elastic.md)); Render hosting/Blueprint ([`render_agent_sdk.md`](render_agent_sdk.md), [`render.md`](render.md)); Intelligence dashboards.

**Do not persist agent-runtime** this pass. A durable run store (Postgres, Elastic, or both) and memory are later discussions. Runtime envelope (reference, not a build track): [`render_agent_sdk.md`](render_agent_sdk.md).

## Role

Operators stay on the **case**. Engineers use **Render logs/metrics**. There is no source of truth for invoke/node/tool traces until a save milestone.

## Live signals

| Audience | Where | What |
| --- | --- | --- |
| Operator | Case / Work (Postgres ledger) | Requisition status, approval, `discovery_candidates`, next action, HITL item. Not System 2 transcripts or hidden reasoning. |
| Engineer | Render logs and service metrics | Ephemeral task output for `invoke` / `resume`. Not SoR. Ops: [`render.md`](render.md). |

No OpenTelemetry, Datadog, or Elastic APM in this contract. Elastic remains retrieval, not an agent index.

## Do not save (agents)

Do **not** write any of the following this pass:

- `harness.*` rows on `audit_events`
- `agent_runs` / `node_runs` / tool-counter / visit-counter tables
- Elastic documents for traces or raw texts
- System 2 transcripts, chain-of-thought, or secrets anywhere durable

`audit_events` stays for **ledger** mutates only (requisition, approval, withdraw, `discovery_candidates`). Call limits and `max_visits` are in-process for the tick.

Postgres today (not agent runtime): `users`, `role_assignments`, `requisitions`, `approvals`, `audit_events`, `notification_outbox`, `recovery_journal`, `discovery_candidates`. Schema: `backend/migrations/`.

## Sourcing map

Contract walkthrough (reference): [`render_agent_sdk.md` — Walkthrough](render_agent_sdk.md#walkthrough-procurement-sourcing).

| Node | Operator (ledger / Work) | Engineer (Render logs) | Durable agent save |
| --- | --- | --- | --- |
| `start` | Case load | Task start | None |
| `choice` / `gate` | Next action or HITL if routed | Outcome ids/scores in logs | None |
| `search` | — | Tool name, errors | None |
| `persist` | `discovery_candidates` + ledger `audit_events` | Persist result | Ledger only (candidates), not a run doc |
| `draft` / `judge` | Proposal on the case when persisted as ledger data | Token/error logs; **no** transcript store | None |
| `hitl` | Work item | Exit reason | None |
| `end` / `fail` | Case status | Stop reason | None. Read-only sourcing: no `recovery_journal` |

## Non-goals (this pass)

Intake SSE transcripts as an agent store. Retrieval-as-memory. Index lifecycle. Copying a run summary onto the requisition for traces. Mutating-graph compensation via `recovery_journal`.

## Related

[`render_agent_sdk.md`](render_agent_sdk.md) · [`guardrails.md`](guardrails.md) · [`render.md`](render.md) · [`elastic.md`](elastic.md) · [`procurement.md`](procurement.md) · [`AGENTS.md`](../AGENTS.md)
