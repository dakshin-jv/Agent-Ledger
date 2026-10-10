# Enterprise Commerce ERP — Build Start Here

Prepared: 8 October 2026. Standing platform decisions updated 10 October 2026: Astropods out of scope; Render PostgreSQL is the store; agents run in-repo on Render. Status: execution handoff design; this document does not itself connect providers, execute payments or deploy.

Use alongside the single current ERP_Design_OKF_Bundle.zip (latest saved content revision 0.5.0). This handoff is a separate requested document, not a second OKF bundle. Dated explicit user decisions supersede older proposals. Future coding agents must inspect the actual current bundle before editing it.

## 1. Scope and authority

The product is an agent-native enterprise commerce ERP. Goods procurement is the first detailed journey; services are deferred because data is unavailable. Broader capability map: orders/O2C, procurement/bids, inventory/receiving, AP, AR, Treasury, R2R, suppliers, customer service, analytics and administration. These areas are not all fully specified or approved for immediate implementation.

Confirmed foundations: clearly labelled demo enterprise data; Channel3 discovery; Sarvam and TypeSafe; shared agents with isolated per-case runs developed in this repository; Render as the sole deployment and orchestration platform (web/API, private services, Workflows, Cron); Render PostgreSQL as the authoritative store; human approvals; RBAC implementation planned; every step has undo or compensating recovery. Astropods is out of scope. Business owner approves specifications; non-owner submission routes a pending decision and notification to that owner. Funding authority remains separate. Runtime provider calls are MCP-first through a backend policy adapter, with SDK/API fallback, as recorded in [`docs/coding-agents.md`](../docs/coding-agents.md) and the per-service files linked from [`AGENTS.md`](../AGENTS.md).

This document plans later execution. It does not supersede the current design-only instruction. Receiving it authorises a readiness assessment, not automatically building every module, deploying, or making payments.

## 2. What Jaya should do first

### Step 1 — Complete the PayPal sandbox prerequisites

You already have PayPal Developer access. In Developer Dashboard:

1. Select Sandbox rather than Live.
2. Locate or create a Business sandbox merchant and a separate Personal sandbox buyer for a proposed Checkout demonstration. Existing default accounts may be reusable.
3. Create/select a sandbox REST application associated with the merchant.
4. Keep the sandbox client ID and secret in local/provider secret settings; do not send the secret in chat or commit it.
5. Record non-secret account/app aliases, roles, country and chosen supported currency. Demo country/currency remains to be confirmed.
6. Keep buyer sandbox login details available privately for payment approval testing.
7. Verify reporting, payment and refund capabilities individually later. Developer access alone does not prove balance-reporting access.

The proposed merchant represents our controlled fictional supplier. A discovered Channel3 seller is not automatically that merchant or a payable recipient. Confirm the payment journey before implementing supplier payment. Personal-buyer Checkout is a demo pattern, not a claim of enterprise AP settlement functionality.

### Step 2 — Choose one coding client and a repository

Use Codex, Claude Code or Cursor; no need to subscribe to all three. Supply this file and the latest OKF ZIP in the same project workspace. Select an existing repository or explicitly request a new one. Use Git with a public licensed repository for eventual submission. A repository MCP is optional: local Git is sufficient initially.

Baseline local capabilities: supported coding client, Git, shell, current supported Node.js/npm for chosen frontend/tooling, and Python only if the implementation selects it. The agent should select/pin dependency versions against current docs; no framework is finalised here. React/TypeScript is a practical proposal because of component integrations, not an approved requirement.

### Step 3 — Obtain Channel3 access

Sign up at https://trychannel3.com/developers and get a developer API key. Sponsor page currently lists promo code PAYPAL-HACKATHON-2026 and 20,000 free API credits. Confirm the benefit is applied in your dashboard. MCP login and API key access are separate credentials/authorization paths; test whichever runtime integration is selected.

### Step 4 — Obtain a Render workspace and PostgreSQL

Render: create/select workspace and use the hackathon credit link on its sponsor page. It currently advertises $50 credits. Connect the intended repository when ready. Provision Render PostgreSQL as the transactional store. Render services use the instance's internal database URL; local development uses the external URL in the ignored `.env`. Workflow/cron filesystems are not authoritative storage. Record plan/credit limits before deploying; credits do not mean unlimited or permanently free hosting.

Do not create an Astropods project. Agents are implemented in `backend/src/agents/` and run on Render (API, private services, workers, Workflows). Durable ERP approvals remain backend records in PostgreSQL.

### Step 5 — Confirm existing model access

Sarvam and TypeSafe: user reports keys already obtained. Verify they are active, usable for intended models, and have quota. At runtime, Sarvam is MCP-first through the policy adapter with SDK/API fallback. TypeSafe uses the official SDK/API as runtime primary until an official data MCP exists; the community MCP is evaluation-only. No new key purchase is assumed. Confirm voice/language use and structured response support through later capability probes.

### Step 6 — Obtain component licences

Use the sponsor-linked AG Grid/AG Studio and Bryntum trials when ready to integrate. Both sponsor pages currently advertise 45-day trials. Record start/expiry date and selected product entitlement. Do not assume that one key enables every product or hosted production use indefinitely. Plan access through the judging period or document a reproducible permitted alternative.

AG Grid supports operational tables; the sponsor opportunity emphasises AG Studio and its agent framework. AG Studio is an analytics candidate pending product selection. Bryntum Scheduler is proposed for owner review planning, with Calendar/Gantt/Pro selected only for a justified timeline/resource/dependency requirement. A deadline alone has no invented duration.

### Step 7 — Obtain Elastic and Postman access when needed

Elastic: choose local Elasticsearch or a cloud project. Sponsor page offers a 14-day trial and a form for a further 30 days. Record endpoint, access scope and enabled features. Agent Builder MCP entitlement is not implied by basic search access.

Postman: create/select workspace; use PayPal's public collection and your own sandbox environment. API key/OAuth is needed if connecting Postman MCP. Collection access does not automatically enable every test execution tool.

### Step 8 — Defer optional providers

Kernel: obtain an account/key only if a concrete authorised browser workflow needs it; sponsor page currently offers $50 credits. Zapier: optional selected external actions or notification delivery; sponsor page advertises a new-account 14-day Professional trial. In-app notifications can operate without either provider. Email/push provider remains unselected.

No standalone RBAC vendor or separate cron vendor is needed for the current design. Render Cron Jobs and Workflows are the scheduled-dispatch path; they call authenticated backend APIs and must not open the database directly. Backend identity implementation still needs review; a third-party identity service is optional, not selected.

## 3. Access checklist and credential boundaries

| Provider | Need | Non-secret proof to record | When |
|---|---|---|---|
| PayPal | Sandbox merchant/buyer, REST app, credentials | Account/app aliases, environment, role, currency, capability result | Now |
| Coding client + Git repository | Project workspace and account | Client/version, repository URL/path | Now |
| Channel3 | API key and/or MCP authorization | Enabled access, locale/category coverage, credit status | Now |
| Sarvam / TypeSafe | Existing API keys | Model IDs, quotas and capability outcomes | Verify now |
| Render | Workspace/repository access; OAuth or API auth for MCP; PostgreSQL instance | Workspace ID, selected plan, credits, database readiness | Now; deploy later |
| AG Grid / AG Studio | Applicable licence/trial | Entitled products, expiry date | Before UI integration |
| Bryntum | Selected product licence/trial | Product/version, expiry | Before scheduling UI |
| Elastic | Local instance or cloud project | Endpoint, scoped access, enabled capabilities | Before retrieval |
| Postman | Workspace; OAuth/key for MCP | Workspace/collection IDs, tool inventory | Before API verification |
| APIMatic | PayPal Context Plugin installation | Loaded plugin/context and installer version | Before payment coding |
| Kernel / Zapier | Optional account and scoped access | Specific approved use case and enabled tools | Only if selected |

APIMatic's sponsor page says its enabled PayPal context requires no extra APIMatic credentials. That does not supply PayPal transaction credentials. External benefit/trial terms must be rechecked at activation.

## 4. MCP inventory — coding assistance versus runtime

No specific MCP is a hackathon-wide entry requirement. Our project requires meaningful service use where selected. Installing a docs MCP does not integrate its UI/service into the product.

| MCP/plugin | Purpose | Recommendation | Verified reference |
|---|---|---|---|
| PayPal AI Toolkit + Sandbox MCP | Coding practices and supported sandbox operations | Project requirement; check plugin-supplied connection before adding duplicate | https://github.com/paypal/AI-Toolkit |
| APIMatic PayPal Context Plugin | API contract and implementation guidance | Project priority; plugin is not payment execution authority | https://github.com/apimatic/context-plugins-installer |
| AG Grid MCP | Framework/version-specific grid docs | Recommended coding assistance | npx ag-mcp; https://github.com/ag-grid/ag-mcp |
| Bryntum MCP + skills/rules | Component implementation guidance | Recommended coding assistance | https://mcp.bryntum.com; https://bryntum.com/agents/ |
| Channel3 MCP | Product discovery and enrichment | Runtime: MCP first through the procurement adapter; keep SDK/API fallback | https://mcp.trychannel3.com |
| Sarvam MCP | Language, voice and related capabilities | Runtime: MCP first through the policy adapter; keep SDK/API fallback | https://docs.sarvam.ai/api/developer-tools/mcp |
| Elastic Agent Builder MCP | Authorised retrieval/tools for runtime agents | Runtime: MCP first for agent retrieval/tools; Elasticsearch API for ingestion and fallback | Project-specific endpoint from Elastic docs |
| TypeSafe community MCP | Typed-judgment experiments | Evaluation only; official SDK/API is the runtime primary | https://docs.typesafe.ai/api.md |
| Render MCP | Service inspection and supported platform changes | Coding/operations only; separate from Render Workflow runtime | https://mcp.render.com/mcp |
| Postman MCP | API workspace/collection/tooling | Coding/development only | https://mcp.postman.com/minimal or regional endpoint |
| Kernel MCP | Browser sessions and web actions | Optional concrete browser use case | https://www.kernel.sh/docs/reference/mcp-server |
| Zapier MCP | Selected external application actions | Optional delivery/integration adapter | https://docs.zapier.com/mcp/home |
| Agent Ledger internal MCP | Domain-safe reads, proposals and authorised actions | Planned private Render service; backend API is sufficient first | Must be designed by us; never a database or payment gateway |

Do not give runtime agents a raw SQL-write MCP, Render-admin MCP, or unrestricted PayPal mutation tools. Runtime calls go through the backend policy adapter with tenant, approval, audit and idempotency. Native code/filesystem/browser verification can suffice; no GitHub or database MCP. Additional Playwright/browser tooling is optional and must have a verified official source before configuration.

RBAC and Render scheduling use backend APIs, Workflows and Cron — not an Astropods deployment.

## 5. Initial installation and connection procedure

1. Ask the coding agent to inspect existing client/plugin/MCP configuration; preserve it rather than overwrite it.
2. Follow the current PayPal Toolkit README for your exact client version. It documents Claude Code, Codex and Cursor routes. Configure only sandbox credentials; refresh expiring tokens through approved secret handling.
3. Install APIMatic's PayPal context using its current installer instructions. Official installer documents `npx context-plugins install paypal`; inspect supported client/configuration options before invoking it. This document has not run it.
4. Add AG Grid MCP using its official `npx ag-mcp` launch guidance.
5. Add Bryntum guidance at the verified endpoint and load its official coding rules/skills.
6. Add Channel3 discovery access. Verify supported locale/category and price/unit normalization with read-only queries.
7. Connect Render using official client/plugin authentication when operations start.
8. Add Elastic/Postman only with correct project/region and required scoped access.
9. List discovered tools and run read-only health/documentation queries before enabling writes.

Client configuration differs. Cursor uses project `.cursor/mcp.json`; Claude Code has its own MCP/plugin mechanisms; Codex supports its client configuration. Use current official instructions and installed-client help. Do not paste one client's JSON wholesale into another. Desktop/cloud/local clients may not share environment variables or authentication.

No copy-paste command in this handoff automatically authorises deployment or financial mutations. Review the exact proposed action and environment first.

Record for each connection: provider/source URL, version, transport, authentication method, scope, available tools, read-only probe outcome, missing operations and ownership. A connected server is not evidence every operation is permitted. AG Grid/Bryntum docs access does not imply a component licence. PayPal MCP may not expose balance reporting; verify inventory and use an approved direct API adapter when necessary.

## 6. Runtime and application layer map

| Layer / capability | Services | System of record / boundary |
|---|---|---|
| Frontend / Home / Work | Operational AG Grid, Bryntum planning, contextual agent UI | Backend work items; user action is a proposal until validated |
| Procurement / specification / sourcing / bids | Sarvam, TypeSafe, Channel3, Elastic, AG Grid | Requirements and internal supplier/contract authority; external listings are not formal bids |
| Orders / O2C | Backend, Render, PayPal Sandbox | Order state, buyer consent, provider resource IDs |
| Inventory / receiving | Backend demo stock, AG Grid, relevant Bryntum schedules | Reservations, receipt, inspection and acceptance; no Channel3 stock truth |
| AP / AR | Backend match rules, permitted PayPal operations, Render | Invoice/payment authority and reconciled outcomes |
| Treasury | Permitted PayPal reporting and analytics | Dated test account snapshots; enterprise budgets kept separate |
| R2R | Accounting records, reconciliation and analytics | Backend ledger/close controls; PayPal is not a general ledger |
| Customer service / disputes | Sarvam, TypeSafe, Elastic, supported PayPal tools | Case evidence and authorised remedies |
| Network / suppliers | Channel3 enrichment, Elastic, grids | Internal qualification, contractual coverage |
| Intelligence | AG Studio candidate, Elastic, structured models | Permitted datasets and defined metrics; Studio selection pending |
| Agent execution | `backend/src/agents/`, Render workers/Workflows, policy adapters | Per-case isolation and typed outputs; no automatic authority |
| Orchestration / reminders | Render Workflows and Cron | Backend persisted state, outbox, schedules and deduplication |
| Settings / governance | Backend identity/RBAC and provider adapters | Permissions, ownership, policies, audit and secret references |

No single agent per page. Shared business capabilities are invoked across pages with isolated record context. Do not use every provider at every stage. APIMatic/Toolkit assist development; actual product behaviour must be demonstrated separately.

## 7. Bryntum and scheduled notification ownership

Bryntum visualizes approved review blocks, deadlines and delivery milestones; drag/reschedule sends a versioned proposal to the backend. Backend checks RBAC, ownership, permissible deadline changes and evidence, then persists the accepted change and updates reminders. Undo restores a permissible prior schedule with history; sent notices remain recorded.

Initial owner notice is event-driven from an approval outbox. A recurring Render Cron Job scans due reminder/retry entries through an authenticated backend API; Render Workflows executes bounded delivery tasks. Cron runs UTC and must not open PostgreSQL directly. Keep due dates in UTC with display timezone. No cron per request is required.

Recheck pending status/current owner/version before dispatch. Cancel obsolete schedules on withdrawal, superseding edits, approval/rejection or owner reassignment. Delivery retry does not retry approval/payment. Unknown external send outcomes require channel-level idempotency/reconciliation where supported. Notification is never consent. Email/push adapter and reminder frequency remain choices.

## 8. Dataset, human approval and recovery requirements

Read bundle dataset contracts before creating fixtures. Required groups: organisation/users/roles, goods master, inventory/reservations, suppliers/contracts, policies/budgets, requisitions/lines, external candidates, evidence/findings, model assessments, human decisions, runs/actions/recovery journals, work handoffs, notifications/schedules, provider account/payment/reporting records.

Label origin per relevant field: demo_fixture, user_input, external_channel3, paypal_sandbox, derived. Unknown is not zero. Use decimal money, currency, controlled units, timestamps and source versions. Source isolation applies per tenant/entity/record.

Specification approval requires authenticated assigned business owner and current reviewed version; role alone is insufficient. Non-owner submission routes a pending Work item and notification. Funding owner remains a separate gate. Models and schedule services cannot grant roles or approve. Full permission matrix and controlled reassignment procedure need review before implementation.

Every step defines eligibility, actor, before/after state, dependencies, recovery action and outcome evidence. Draft restore, check invalidation, request withdrawal, approval revocation, handoff recall and payment compensation are different actions. Sent messages, physical delivery and captured payment cannot be erased by restoring a database snapshot. Refund/void eligibility must be checked against actual provider state.

PayPal reporting can lag up to three hours according to its balance API docs. Display account/currency/as-of/refresh/retrieval timestamps. Sandbox merchant balance is neither enterprise budget nor proof of buyer payment capability. No live fallback or arbitrary Channel3 retailer payout is assumed.

## 9. Execution milestones — after separate implementation authorization

| Milestone | Build scope | Exit evidence |
|---|---|---|
| 0 readiness | Read bundle, inspect repo/client, verify prerequisites, resolve fixture and runtime choices | Readiness report, capability matrix, exact milestone proposal |
| 1 foundation | Auth/RBAC, Render PostgreSQL, demo fixtures, versioning, approvals, audit/recovery/outbox | Restart persistence, tenant isolation, unauthorized/stale action rejection |
| 2 goods intake | Manual path, checks, Sarvam/TypeSafe proposals, confirmations, withdrawal | Happy path, unavailable check, duplicates, edits/retries |
| 3 specification | Requirement/evidence/evaluation/acceptance matrix, owner routing | Correct/non-owner review, stale approval, specialist concern, recall |
| 4 scheduling | Bryntum planning and Render notification dispatch | Deadline edits, undo, duplicate delivery, cancellation, role changes |
| 5 discovery/retrieval | Channel3/Elastic integration | Real read evidence, coverage, provenance, outages |
| 6 next lifecycle stage | Design sourcing, then implement the approved stage | Stage-specific contract, handoff and fallbacks; no invented award authority |
| 7 sandbox payment | Confirmed payment pattern, explicit consent/authority, status/webhook/recovery | Provider IDs, verified outcome, unknown-result reconciliation, permitted refund/void |
| 8 analytics/demo | Selected analytics plus coherent end-to-end journey | Reproducible run, sponsor contributions, data labels, submission assets |

Happy path first, then essential fallbacks. Gates verify actual behaviour, not implementation-mirroring tests. Broader departments stay planned until specified. Change status accurately: designed, configured, tested-pass, tested-fail, unsupported, blocked. Update the single bundle with evidence after each milestone; never claim mocks are live calls.

## 10. Starter prompt for Codex, Claude Code or Cursor

> Read BUILD_START_HERE.md and the latest ERP Design OKF bundle. Identify explicit decisions, superseded statements and unresolved choices. First inspect repository/client state and produce a readiness report: accounts, available MCPs, scopes, licences, missing configuration and provider capability verification. Never expose secrets.
>
> This is currently design-only. Do not build, deploy, send notifications or execute payments until an implementation milestone is explicitly authorised. Propose the foundation milestone and resolve dependencies without inventing organisation policies.
>
> Once authorised, implement only that milestone. Enforce backend RBAC and record ownership, version-bound human approval, labelled demo data, idempotency, audit and recovery. Use provider MCP through the policy adapter at runtime and keep SDK/API fallbacks; use docs/MCP/context tools only at their intended layer. Keep unsupported operations explicit. Preserve one current OKF bundle and update it with actual validation evidence and next steps.

## 11. Hackathon review and submission

Overview, rules, resources, FAQs, updates and all ten sponsor pages were reviewed on 7 October; selected access pages rechecked 8 October. Do not interpret that as reviewing every linked video or signing into private resources. No specific MCP is mandated by the hackathon. PayPal + AI must be meaningful; sponsors are optional overall but our project has explicit priorities.

Future submission: functioning build or reproducible complete run instructions, public licensed repository, tools/use explanation and a public YouTube demo under three minutes. Document significant hackathon-period progress if advancing an existing project. Provide permitted demo access; do not publish privileged provider secrets. Confirm current rules before submission.

## 12. Sources and pending items

Hackathon: https://paypalaihackathon.devpost.com/ ; /resources ; /rules ; /details/faqs ; /updates.
Sponsor pages: https://paypalaihackathon.devpost.com/details/aggrid ; /apimatic ; /astropods ; /bryntum ; /channel3 ; /elastic ; /kernel ; /postman ; /render ; /zapier (each suffix appended to /details).

Primary integration references:

- PayPal accounts: https://developer.paypal.com/sandbox-testing/accounts
- PayPal Toolkit: https://github.com/paypal/AI-Toolkit
- PayPal MCP: https://developer.paypal.com/ai-tools/mcp-server
- PayPal balance: https://developer.paypal.com/api/transaction-search/v1/balances-get/
- APIMatic installer: https://github.com/apimatic/context-plugins-installer
- AG Grid MCP: https://github.com/ag-grid/ag-mcp
- Bryntum: https://bryntum.com/agents/setup/other-agents/
- Channel3 MCP: https://trychannel3.com/mcp
- Render MCP: https://render.com/docs/mcp-server
- Render PostgreSQL: https://render.com/docs/postgresql
- Render scheduling: https://render.com/docs/cronjobs ; https://render.com/docs/workflows
- Elastic MCP: https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server
- Postman MCP: https://learning.postman.com/docs/reference/postman-api/postman-mcp-server/overview/
- Kernel: https://www.kernel.sh/
- Zapier: https://paypalaihackathon.devpost.com/details/zapier

Pending before dependent implementation: coding client/framework, fixture country/currency/category, personas/permission matrix, controlled owner reassignment, notification timings/channel, exact payment topology, account capabilities/licences and authorised implementation scope. APIMatic's sponsor-linked resource previously failed to resolve; the official installer above is a verified alternative, to inspect for current client support. No account authentication or API health probe has run here.
