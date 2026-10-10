# PayPal

**Read when:** sandbox orders, invoices, refunds, Postman collection, or the payment adapter.

**Do not use for:** catalog search ([`channel3.md`](channel3.md)), deploy ([`render.md`](render.md)), or UI grids ([`bryntum.md`](bryntum.md)).

## Role in Agent Ledger

PayPal Sandbox is the payment lifecycle for the prototype: authenticate, create an order, buyer approval, capture, refunds, invoices, and transaction lookup. Live money is out of scope unless the user explicitly authorizes otherwise. Never add a live fallback, payment execution, or deployment as an incidental change.

## Features

### Sandbox accounts

Use a Business sandbox merchant and a separate Personal sandbox buyer. Keep client ID and secret in `.env`. Record aliases, environment, role, and currency only — not passwords — in non-secret notes.

### Orders

Create and look up sandbox orders through the policy adapter. Do not create or capture an order unless the current task explicitly asks for it.

### Invoices

Sandbox invoicing (create, send, reminders) stays behind the same adapter and approval controls.

### Refunds and disputes

Refunds, dispute lookup, and related mutations are financial actions: approval, idempotency, and audit required.

### Postman collection

The [PayPal public collection](https://www.postman.com/paypal/paypal-public-api-workspace/collection/ujhlb45/paypal-apis) is first-line API validation. Start with `Authentication → Generate access_token`, then `Orders` only for an explicitly requested sandbox transaction. Postman MCP/desktop is coding/QA only.

### Local vs remote MCP

Local `@paypal/mcp` needs Node.js 18+ and a short-lived `PAYPAL_ACCESS_TOKEN` minted from `.env`. Remote sandbox transports are `https://mcp.sandbox.paypal.com/sse` and `/http`. Neither replaces backend approval controls.

### APIMatic plugin

The APIMatic PayPal context plugin supplies API-contract context while writing the adapter. It is not a runtime MCP and does not execute payments.

## Coding agent

- Skill/plugin: APIMatic PayPal context plugin
- MCP: `paypal-sandbox`; optionally `postman`
- Connect only for PayPal/API-validation work

## Runtime

MCP first through the policy adapter; [PayPal REST](https://developer.paypal.com/docs/api/overview/) is the tested fallback for webhooks, deterministic flows, and MCP gaps. Provenance label: `paypal_sandbox`. No unrestricted payment tools on deployed agents.

## Secrets / env

`PAYPAL_ENVIRONMENT` (sandbox), `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, plus sandbox merchant/buyer alias fields in [`.env.example`](../.env.example).

Official links: [Developer Dashboard](https://developer.paypal.com/dashboard/applications/sandbox) · [Sandbox testing](https://developer.paypal.com/tools/sandbox/) · [MCP](https://developer.paypal.com/ai-tools/mcp-server)

## Related

[`coding-agents.md`](coding-agents.md) · [`render.md`](render.md)
