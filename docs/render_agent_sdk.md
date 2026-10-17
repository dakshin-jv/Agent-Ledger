# Product-agent harness (Render)

**Superseded as a build track.** This file is the **frozen contract** for loops, HITL `hitl`, `invoke` / `resume`, and one Blueprint. Do **not** implement `backend/src/harness/`, add a Workflow entrypoint, or apply the illustrative stack from this file. Do not treat LangChain, LangGraph, or Deep Agents as a runtime.

**Read when:** you need the product-agent envelope (outer/inner loops, stops, host kinds, sourcing walkthrough).

**Do not use for:** Cursor MCP / Render ops ([`coding-agents.md`](coding-agents.md), [`render.md`](render.md)); PayPal or Channel3 API contracts. Guardrail catalog: [`guardrails.md`](guardrails.md). What a tick may show or log: [`observability.md`](observability.md).

Ops for Workflows, env groups, and PostgreSQL stay in [`render.md`](render.md). Session cadence (Cursor `/loop`, Automations): [`coding-agents.md`](coding-agents.md). Product cadence, if ever hosted: API-triggered `invoke` and Blueprint Cron (later).

## Role

In-house **harness** (contract only): allowlisted tools, middleware around loops, a typed graph, explicit stops, two model ports. If hosted, it would run as Render **Workflow** tasks (`render` Python SDK). The web API owns the ledger. Domain agents stay in `backend/src/agents/`.

Two halves: **Harness** (kit contract) and **Host on Render** (which services would run it). Neither half is a current implementation milestone.

## Harness

Surface, not a package to add:

```text
tools + middleware + graph + model ports + limits
invoke(case_id)
resume(case_id)    # after Work; same case_id
```

### Loops

Bounded loops are first-class.

| Term | Meaning |
| --- | --- |
| **Outer loop** | One Workflow execution: `invoke(case_id)` or `resume(case_id)` after Work. Scheduling (Cron, API event) starts an outer tick; there is no in-graph timer. |
| **Inner loop** | A declared graph cycle (e.g. `draft` → `judge`) until `max_visits[node]`, a `gate`, `fail`, or route to `hitl`. |
| **Agentic step** | Within a node: System 2 action and/or tool call → environment result → next step. |
| **Stop condition** | Caps, `gate`, `fail`, `end`, or HITL `hitl`. Not model-only “good enough.” |

### Stops and verification

- **Ground truth each step:** tool nodes and API reads feed the next node; do not rely on the model recalling prior turns alone.
- **Deterministic stops** beat vague completion: scores, thresholds, ledger checks, `gate` → `hitl` / `fail`.
- **Generate ↔ verify:** keep inner cycles short; verification is System 1 + tools + middleware, not extra System 2 self-approval of edges.
- **Mutating loops** require checks before persist; high-risk paths use **HITL** (Work).
- **Resume idempotency:** `resume` does not replay committed side effects; `correlation_key` on mutates.

### Case state

`case_id` is the thread. **Ledger** persist goes through the API (requisition, approvals, `discovery_candidates`, domain `audit_events`). Working context for a tick is in-process, not Workflow disk. Do **not** persist agent-runtime (runs, node visits, transcripts) this pass — [`observability.md`](observability.md).

### Surface

| Piece | Rule |
| --- | --- |
| **Tools** | Named JSON-schema functions, policy adapter, `correlation_key` on mutates. Retryable tools: task `Retry` and `ctx.run`. |
| **Middleware** | Named policies: planning, model retry, tool retry, call limits, verification, HITL, audit, summarize. Not a LangChain plugin bus. |
| **System 1 port** | TypeSafe. **Edges and judgments only** (route, rank, verify, confidence). Never draft, never approve, never pay. |
| **System 2 port** | Sarvam (or OpenAI-compatible chat). **Generation and other actions**, not edges. Outputs are proposals or evidence. Never pick the next node, never approve, never pay. SSE tokens stay on the web API, not `invoke`. |
| **ModelRouter** | Roles → ports. Node code never imports a vendor. |
| **Graph** | In-process inside `invoke` / `resume`. Nodes: `start`, `system1`, `system2`, `tool`, `persist`, `hitl`, `end`, `fail`. Edges: `always`, `choice` (closed node ids), `gate` (threshold → `hitl` / `fail`). |
| **Loop** | See [Loops](#loops) and [Stops and verification](#stops-and-verification). |
| **State** | See [Case state](#case-state). |
| **Guardrails** | Policy envelope around middleware + API. Catalog: [`guardrails.md`](guardrails.md). |
| **Observability** | Case/Work + Render logs. No agent-run save this pass. [`observability.md`](observability.md). |

**`choice`:** System 1 picks **exactly one** next node from a closed id list (e.g. `search` \| `hitl`). **`gate`:** pass/fail threshold; fail path is `hitl` or `fail`. **`fail`:** terminal failure on the case. **`end`:** this outer tick completed. **`hitl`:** persist, exit Workflow, item in Work; later `resume(case_id)`.

### Middleware

| Middleware | Job |
| --- | --- |
| Planning | Case todos via API; optional System 1 for next todo |
| Model retry | `Retry` on the System 2 task only |
| Tool retry | `Retry` on that tool’s task only |
| Call limits | `max_steps`, `max_visits[node]`, per-tool counters — in-process this pass |
| Verification | System 1 judge/`gate`; tool and ledger ground truth; no model-only “done” |
| HITL | Node `hitl`; process exits; Work is the interrupt |
| Audit / PII | API adapter before persist |
| Summarize | Trim working context before the next `system1` / `system2` call |

### Guardrails

Named policies **Authority**, **Isolation**, **Tool class**, **Untrusted input**, **Persist gate**. Hard violations → `fail`. Judgment → `gate` / `hitl`. Middleware and API; `resume` re-checks current grants. Full catalog: [`guardrails.md`](guardrails.md).

### Observability

Operators see the ledger case and Work. Engineers see Render logs/metrics. No `harness.*` audit rows, no `agent_runs` table, no Elastic agent index this pass. Contract: [`observability.md`](observability.md).

### Hard rules

- `ctx.run` — slow/flaky **tools** only, not every graph node. Never `Retry` persist, approve, or PayPal.
- Workflows — Blueprint `type: workflow` (no service `plan`) or CLI; MCP cannot create Workflows. Skill: `render-workflows`.
- Intake **SSE** (Sarvam tokens, question cards) is the web API, not `invoke`.
- Graph routing is typed edges only — not LLM-chosen next node.
- Fail-closed guardrails; never continue past a hard policy failure.
- Do not persist agent-runtime this pass.

### Non-goals

Host/Workflow filesystem as source of truth, Sandboxes/`execute`, Worker as the agent, KV as SoR, Render MCP as runtime tools, LLM-chosen next node, LangChain/LangGraph/`deepagents` at runtime.

Loop-related: in-graph timers; model-chosen stop without `gate`/ledger; replaying committed mutates on `resume`; proactive multi-case runs without policy and owner bounds.

This pass: durable agent-run store (Postgres or Elastic), raw-text/transcript index, OpenTelemetry/Datadog/Elastic APM, retrieval-as-memory.

## Host on Render

Which Render kinds the contract uses. How to operate them: [`render.md`](render.md). Do not add `render.yaml` or `backend/workflows/` from this file.

### Service map

| Kind | Job in this contract |
| --- | --- |
| **Workflow** | Agent runtime. Tasks `invoke` / `resume`. Scales to zero. |
| **Web (API)** | Ledger owner. Workflow HTTP to this API. Intake SSE here. |
| **Static UI** | Blueprint only; not harness runtime. |
| **Postgres** | SoR via API / `FoundationStore`. No task-level SQL. |
| **Cron** | Later: time-based **outer** ticks (reminders or scheduled `invoke`). |

No Worker / KV / Disk / Sandbox how-tos ([Non-goals](#non-goals)).

### Tasks

Outer ticks are `invoke(case_id)` and `resume(case_id)` after Work. `resume` does not replay mutates. Retryable: System 2 jobs and flaky tools only. `API_URL` from the web service; secrets from the env group. Task authoring and local Workflows: [`render.md`](render.md).

### Cron (later)

Schedule starts an **outer** tick (`invoke` or reminder outbox drain). Not an inner-graph timer. One case (or one drain) per run.

### Blueprint

One YAML source of truth for API, UI, Postgres, and (if ever added) the agent Workflow. Spec and ops: [`render.md`](render.md). Skill: `render-blueprints`.

- **One Blueprint per stack** — conflicting YAML is unsafe; replication suffixes names for env copies, not per department.
- **Agents are capabilities**, not separate Render services ([`AGENTS.md`](../AGENTS.md)); shared case, Postgres, API, Work, UI.
- Deploy would register tasks; it would not run `invoke`. Removing YAML does not delete resources.

| Split | Use? |
| --- | --- |
| One Blueprint: API + UI + Postgres + one Workflow | **Yes** (this stack) |
| Extra `type: workflow` in same YAML | Optional; still one API and DB |
| Extra **tasks** on same workflow (`invoke-procurement`, later `invoke-o2c`) | Preferred isolation |
| Separate Blueprint per department with own Postgres | **No** — splits ledger, dual Work queues, duplicate secrets |
| Replicate Blueprint for full env copy | Yes; expect name suffixes |

## Walkthrough: procurement sourcing

Contract for how harness and host would wire together. Lifecycle: [`procurement.md`](procurement.md). Not a first implementation slice.

```text
# outer: API start invoke(case_id)
  start        load case
  choice       System 1: search | hitl           # closed node ids
  search       tool Channel3 (ctx.run, tool-retry)
  persist      workspace /scratch/candidates.json; node_run complete
  rank         System 1 score per candidate
  gate         low confidence → hitl             # threshold, not a menu
  draft        System 2 complete (brief only)    # generation; other System 2 actions as the node requires
  judge        System 1 ready_for_owner
               # inner: draft→judge until max_visits or hitl
  persist      proposal on the case
  hitl         HITL: exit Workflow                 # Work inbox
# outer: API resume(case_id) after owner accept → end
```

Funding is not this graph. Channel3 search is not payment. Owner accept is Work, not the model.

## Map external ideas

External docs are for **mapping**, not runtime or a kit to port in.

| Topic | Link |
| --- | --- |
| Loop engineering (Anthropic) | https://claude.com/blog/getting-started-with-loops |
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents |
| Long-running harnesses | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| Render Workflows (Python SDK) | https://render.com/docs/workflows-sdk-python |
| Defining tasks, `ctx.run`, retries | https://render.com/docs/workflows-defining |
| Running / triggering tasks | https://render.com/docs/workflows-running |
| Local Workflows | https://render.com/docs/workflows-local |
| Limits / task plans | https://render.com/docs/workflows-limits |
| Blueprint `type: workflow` | https://render.com/docs/blueprint-spec |
| MCP cannot create Workflows | https://render.com/docs/mcp-server |
| TypeSafe System 1 | https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md |
| Sarvam chat / MCP | https://docs.sarvam.ai/api/developer-tools/mcp |

Middleware and loop names in vendor docs map onto the tables above (planning, HITL `hitl` + `resume`, verification, call limits). They are not packages to install.

**Coding sessions:** portable loop checklists → [`coding-agents.md`](coding-agents.md); not product runtime.

## Related

[`guardrails.md`](guardrails.md) · [`observability.md`](observability.md) · [`procurement.md`](procurement.md) · [`render.md`](render.md) · [`typesafe.md`](typesafe.md) · [`sarvam.md`](sarvam.md) · [`channel3.md`](channel3.md) · [`elastic.md`](elastic.md) · [`coding-agents.md`](coding-agents.md) · [`AGENTS.md`](../AGENTS.md)
