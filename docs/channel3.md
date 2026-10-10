# Channel3

**Read when:** product search, comparable offers, product detail, or catalog provenance.

**Do not use for:** payments ([`paypal.md`](paypal.md)) or Render ops ([`render.md`](render.md)).

## Role in Agent Ledger

Channel3 supplies product catalog search, comparable offers, enrichment, and merchant data for procurement and specification work. Persist results only through the backend adapter.

## Features

### Search

Call catalog search per distinct product type. Explore with coding-agent MCP; save through the procurement adapter.

### Product detail

Full details by product ID or retailer URL.

### Similar / offers

Comparable offers and similar products. Every Channel3 result includes a `thread_id`; pass it back unchanged on subsequent Channel3 calls in the same conversation.

### Provenance

Saved catalog data is labelled `external_channel3`. Do not present unknown values as zero or as verified facts.

## Coding agent

- Skill: `channel3-api`
- MCP: `channel3` (`https://mcp.trychannel3.com`)
- Connect only for procurement/catalog work

## Runtime

MCP first through the procurement adapter; [Channel3 API/SDK](https://docs.trychannel3.com) is the tested fallback so outputs can be validated and saved with provenance.

## Secrets / env

`CHANNEL3_API_KEY`, optional `CHANNEL3_LANGUAGE` / `CHANNEL3_COUNTRY` / `CHANNEL3_CURRENCY` in [`.env.example`](../.env.example).

Official links: [Channel3](https://www.trychannel3.com/) · [API docs](https://docs.trychannel3.com) · [MCP](https://www.trychannel3.com/blog/channel3-mcp)

## Related

[`coding-agents.md`](coding-agents.md) · [`render.md`](render.md) · [`typesafe.md`](typesafe.md)
