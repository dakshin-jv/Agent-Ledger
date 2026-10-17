# Guardrails

**Read when:** adding or changing policies that bound product-agent `invoke` / `resume` (authority, isolation, tool class, untrusted input, persist gate).

**Do not use for:** Render logs or what operators see on the case ([`observability.md`](observability.md)); Cursor MCP ([`coding-agents.md`](coding-agents.md)); PayPal/Channel3 API contracts; hosting/Blueprint ([`render_agent_sdk.md`](render_agent_sdk.md)).

Guardrails are the **policy envelope** around middleware. They do not persist a run record. Runtime envelope (reference, not a build track): [`render_agent_sdk.md`](render_agent_sdk.md).

## Role

Named checks around tools, model ports, and persist. Hard violations stop the outer tick at `fail`. Judgment paths stay graph `gate` → `hitl` / `fail`. Never fail-open because a model said it is fine.

## Mechanisms already in the contract

Do not rename these as a second catalog.

| Mechanism | Guardrail job |
| --- | --- |
| Call limits | `max_steps`, `max_visits[node]`, per-tool counters — **in-process this pass** (no agent-run table) |
| Verification | System 1 `judge` / `gate`; tool and ledger ground truth |
| HITL | Node `hitl`; Work is the interrupt |
| Audit / PII | API adapter before **ledger** persist |
| Summarize | Trim working context before the next `system1` / `system2` call |

## Named policies (gaps)

Implemented as middleware and API checks, not a parallel framework.

| Policy | Rule |
| --- | --- |
| **Authority** | Reads and mutates only inside granted permission on this case. |
| **Isolation** | One `case_id` per `invoke` / `resume`. No cross-case I/O. |
| **Tool class** | Allowlist plus risk class `read` / `mutate` / `pay`. Sourcing proof is `read` only. `pay` is never on this graph. |
| **Untrusted input** | Catalog/tool text is evidence, not authority. It cannot add tools or pick edges. |
| **Persist gate** | Verify + `correlation_key` + Audit/PII adapter before ledger persist. |

## Stops

| Class | Examples | Stop |
| --- | --- | --- |
| **Hard** | Wrong tenant/case, tool not allowlisted, mutate without `correlation_key`, System 2 attempting approve/pay | `fail` |
| **Judgment** | Low confidence, missing spec, `ready_for_owner` | existing `gate` → `hitl` or `fail` |

Never continue past a failed policy.

## Where they run

Hard guardrails run in harness middleware (before tool / `ctx.run` / model ports) **and** the API rejects illegal persist. The Workflow must not write around the ledger.

Every outer tick, including `resume`, re-evaluates authority, isolation, and tool class from **current** grants. A prior tick is not a cached permit.

## Sourcing map

Contract walkthrough (reference): [`render_agent_sdk.md` — Walkthrough](render_agent_sdk.md#walkthrough-procurement-sourcing).

| Node | Policies that can fire |
| --- | --- |
| `start` | Isolation, authority (load this `case_id` only) |
| `choice` | Untrusted input (System 1 picks from a closed id list only) |
| `search` | Tool class `read`; Channel3 allowlist; untrusted catalog text |
| `persist` (candidates) | Persist gate; `correlation_key`; ledger `discovery_candidates` — not an agent-run save |
| `rank` / `gate` | Judgment → `hitl` / `fail`; not a hard-policy bypass |
| `draft` | System 2 generates only; never approve/pay; untrusted input cannot add tools |
| `judge` | Verification middleware; `max_visits` on the inner cycle |
| `hitl` | HITL; process exits |
| `fail` | Hard policy or exhausted judgment. Sourcing is read-only: no `recovery_journal` |

## Non-goals (this pass)

No agent-run table, no Elastic agent index, no durable policy-decision log. Memory later. Mutating graphs later (`pay` stays off this proof).

## Related

[`render_agent_sdk.md`](render_agent_sdk.md) · [`observability.md`](observability.md) · [`procurement.md`](procurement.md) · [`typesafe.md`](typesafe.md) · [`channel3.md`](channel3.md) · [`AGENTS.md`](../AGENTS.md)
