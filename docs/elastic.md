# Elastic

**Read when:** retrieval, Agent Builder, or Elasticsearch API fallback.

**Do not use for:** the transactional store ([`render.md`](render.md) PostgreSQL).

## Role in Agent Ledger

Elastic Cloud / Elasticsearch provides retrieval and vector search for approved knowledge, evidence, agent memory references, and operational search. PostgreSQL remains the transactional authority.

## Features

### Documentation MCP

`elastic-docs` searches official Elastic documentation. It has no business data.

### Agent Builder MCP

Bounded search and Agent Builder tools for coding-agent and runtime retrieval. Use a least-privilege API key. Do not expose unrestricted index writes to an agent.

### API fallback

[Elasticsearch API](https://www.elastic.co/docs/api/doc/elasticsearch) remains for index lifecycle, deterministic ingestion, and MCP fallback.

## Coding agent

- Skill: none in the shared tree
- MCP: `elastic-docs` (docs); `elastic-agent-builder` (integration)
- Connect only for search/retrieval work

## Runtime

MCP first for agent retrieval/tools through the policy adapter. API for ingestion and fallback.

## Secrets / env

`ELASTIC_API_KEY`, `ELASTICSEARCH_URL`, `ELASTIC_KIBANA_URL`, `ELASTIC_AGENT_BUILDER_MCP_URL` in [`.env.example`](../.env.example).

Official links: [Elastic Cloud](https://cloud.elastic.co/) · [Agent Builder MCP](https://www.elastic.co/docs/solutions/search/agent-builder/mcp-server)

## Related

[`coding-agents.md`](coding-agents.md) · [`render.md`](render.md)
