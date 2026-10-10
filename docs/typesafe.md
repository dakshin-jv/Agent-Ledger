# TypeSafe

**Read when:** typed extraction, ranking, routing, or verification.

**Do not use for:** treating the community MCP as runtime authority. There is no official hosted data MCP; SDK/API is runtime primary.

## Role in Agent Ledger

TypeSafe supplies typed AI judgments for extraction, ranking, routing, verification, and other bounded decisions in workflows.

## Features

### Extraction

Structured extraction from unstructured evidence. Treat outputs as proposals with confidence, not facts.

### Ranking

Bounded ranking of candidates (for example catalog or routing options).

### Routing

Decision routing inside a workflow. Does not grant approval or payment permission.

### Verification

Typed checks against schema and policy. Persist through the backend adapter.

## Coding agent

- Skill: `typesafe-ai`
- MCP: `typesafe` (community; evaluation)
- Connect community MCP only for experiments

## Runtime

Official [API/SDK](https://docs.typesafe.ai/api.md) through a typed backend adapter. Keep the MCP adapter as an evaluated option only.

## Secrets / env

`TYPESAFE_API_KEY` in [`.env.example`](../.env.example).

Official links: [TypeSafe](https://typesafe.ai/) · [API docs](https://docs.typesafe.ai/api.md)

## Related

[`coding-agents.md`](coding-agents.md) · [`channel3.md`](channel3.md)
