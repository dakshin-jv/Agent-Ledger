# Agent-Ledger — Agentic ERP (Rough Draft Spec v0.1)

> **Status: draft proposal.** Not a decision. Conflicts with the repo are listed in [OKF decisions P-01..P-08](../plan/ERP_Design_OKF_Bundle/progress/decisions.md#draft-rough-spec-reconciliation-2026-10-18); standing entries there win. Entry points: [`AGENTS.md`](../AGENTS.md), [`plan/BUILD_START_HERE.md`](../plan/BUILD_START_HERE.md).

PayPal AI Hackathon 2026 · Deadline Nov 12, 2026 12:00 PM PST (Nov 13, 1:30 AM IST)

## 1. Vision
An action-oriented ERP with no menus. Users clear their work from an **Action Feed** and a **Command Bar**; department agents do the work across processes, and every money movement runs on the **PayPal rail** with policy limits, human approval, and an audit trail. Everything beyond the small core is a **plugin** that anyone can build.

## 2. Tech stack
- Backend: Python 3.13, FastAPI, uvicorn, Pydantic v2, uv
- Agents: LangGraph + deepagents; LLM via Sarvam (`langchain-sarvam`), swappable per agent
- Tools: MCP servers (one per department plugin); A2A for agent-to-agent handoffs
- Payments: PayPal sandbox (REST APIs + PayPal Agent Toolkit)
- DB: Postgres (SQLite for local dev), Alembic migrations
- Frontend: Next.js/React, AG Grid for data views (sponsor prize)
- Observability: OpenTelemetry + Langfuse

## 3. Architecture
```
UI (Action Feed · Command Bar · Approval Cards · Live Canvas · Plugin Store)
        │
   Router / Coordinator agent
        │  A2A bus
 ┌──────┼─────────┬──────────┬────────┬─────────┐
 O2C   P2P       H2R        P2I      I2R     Treasury
 └──────┴────┬────┴──────────┴────────┴─────────┘
         R2R Ledger  ──►  Analytics
 Core services: Data layer · Money rail (PayPal) · Policy engine · Audit log · Plugin runtime
```

## 4. Processes and agents
| Process | Agents | Key actions | PayPal APIs | Posts to R2R |
|---|---|---|---|---|
| Order-to-Cash | Sales, Collections (`collection.py`), Cash App (`cash_app.py`) | Quote → order → invoice → remind → match payment | Invoicing, Orders, Webhooks | AR, Revenue, Cash |
| Procure-to-Pay | Procurement (`procurement.py`), AP | Reorder → PO → receipt → bill → 3-way match → pay | Payouts | AP, Expense/Inventory, Cash |
| Record-to-Report | Ledger, Close | Journals, PayPal/bank recon, month-end close, statements | Transaction Search, Reporting | — (owner) |
| Treasury | Treasury (`treasury.py`) | Cash position, forecast, payment runs, approve large payments | Balances, Transaction Search | Cash transfers |
| Hire-to-Retire | HR, Payroll | Onboard, leave, payroll, contractor payouts | Payouts | Salary, Liabilities |
| Plan-to-Inventory | Inventory | Stock levels, forecast, reorder → P2P | — | Inventory adj. |
| Issue-to-Resolution | Support | Refunds, disputes | Refunds, Disputes | Revenue reversal |
| Analytics | Insights | Daily briefing, ask-anything canvas | — | Reads only |

## 5. Shared data model (core entities)
Company, User/Role, Customer, Vendor, Employee, Item, Warehouse, StockMove, Quote, SalesOrder, Invoice, Payment, PurchaseOrder, GoodsReceipt, Bill, Payout, Refund, Dispute, JournalEntry/Line, Account (CoA), Approval, Action (feed item), AuditEvent, Plugin, PluginGrant.

## 6. Plugin system (open, manifest + permissions)
Plugin types: department, data connector, payment rail, policy, model, UI.

```yaml
# plugin.yaml
id: payroll
version: 0.1.0
type: department
agents: [payroll_agent]
mcp_tools: [run_payroll, pay_contractor, get_payslip]
a2a_card: a2a/payroll.json
entities: {read: [Employee], write: [Payout, JournalEntry]}
ui_cards: [payroll_run_card]
permissions:
  - ledger.post
  - paypal.payouts: {per_txn_limit: 50000, daily_limit: 500000, currency: INR}
  - network: [api.example-hrms.com]
```
- Plugins never hold PayPal or DB credentials; they call the core money rail and data layer.
- Admin approves permissions at install (app-store style prompt).
- Lifecycle: install → enable → upgrade (migrations) → disable → uninstall.
- Policy engine enforces limits and routes over-limit actions to an approval card.

## 7. UX
- **Action Feed**: ranked cards (Approve / Edit / Delegate)
- **Command Bar**: intent → multi-step plan across agents → approve
- **Approval Card**: "About to pay ₹X to Y via PayPal" with policy reason
- **Live Canvas**: generated, pinnable charts/tables (AG Grid)
- **Plugin Store**: browse, review permissions, install

## 8. Repo layout (proposed)
```
backend/src/core/{data,money_rail,policy,audit,plugin_runtime,a2a}
backend/src/agents/{router,treasury,procurement,collection,cash_app,...}
backend/plugins/<plugin_id>/{plugin.yaml,agent.py,mcp_server.py,a2a/}
frontend/
.cursor/rules/{project.mdc,core.mdc,plugin-system.mdc,o2c.mdc,p2p.mdc,r2r.mdc,treasury.mdc,h2r.mdc,inventory.mdc,support.mdc,analytics.mdc}
```

## 9. Build plan (to Nov 12)
1. Week 1: core (data model, money rail on PayPal sandbox, policy, audit, router, A2A), plugin runtime + manifest
2. Week 2: O2C and P2P end to end, R2R ledger + recon, Treasury
3. Week 3: H2R, Inventory, Support as plugins; frontend feed, command bar, canvas, plugin store
4. Final days: seed demo company, demo script, video, README, public repo

## 10. Demo script (draft)
1. Morning briefing on the Action Feed; manager clears approvals in one go.
2. "New hire needs a laptop" → HR + Procurement + PayPal payout + ledger posting.
3. Install Payroll plugin live → permission prompt → run payroll via PayPal Payouts.
4. Over-limit payment blocked by policy → approval card → approved → audit trail.

## 11. Open decisions
- Mock company type (product vs services) and currency (INR vs USD in sandbox)
- A2A library choice; frontend framework
- Which plugins to ship fully vs as thin demos
- Fix `.claude` rules mismatch; add FastAPI and PayPal deps

## 12. Agent layers: tools, MCP, skills, agents, A2A
- **Tool**: one Python function (`create_invoice`, `pay_vendor`) that only touches data/money via core services.
- **MCP server**: one per department plugin; exposes its tools; runs as a Render Private Service; checks plugin permissions on every call.
- **Skill**: reusable recipe (instructions + tool steps), loaded on demand by deepagents (e.g. `three_way_match`, `chase_overdue`).
- **Agent**: LangGraph/deepagents agent with a role, skills, and its department MCP server.
- **A2A**: each agent publishes an agent card (name, capabilities, endpoint). Agents delegate by sending tasks; states: submitted → working → input-required (approval) → completed/failed.

## 13. Runtime on Render
| Render service | Runs |
|---|---|
| Web Service `ledger-api` | FastAPI, router agent, PayPal webhooks, A2A gateway |
| Static Site `ledger-web` | Frontend (feed, command bar, canvas, plugin store) |
| Private Services `mcp-<dept>` | Department MCP servers (internal network only) |
| Background Workers `agent-<dept>` | Department agents consuming A2A tasks from Key Value |
| Render Workflows | Long processes: month-end close, payroll run, payment batch, bulk recon |
| Cron Jobs | Nightly PayPal recon, morning briefing, treasury forecast (trigger workflows) |
| Render Postgres | Ledger + shared data model |
| Render Key Value | A2A queues, cache, sessions |
| Env group `ledger-secrets` | PayPal sandbox + LLM keys, shared by all services |

**Flow rules**
1. Workers think and talk (fast, conversational A2A tasks).
2. Workflows execute heavy, multi-step processes with retries and fan-out; each step calls the same MCP tools.
3. Over-limit steps pause, raise an approval card, and resume on approval.
4. PayPal webhooks → Web Service → A2A task to the owning agent.
5. MCP is the only path to data or money.

## 14. Model Gateway & Settings (provider-agnostic, type-safe decisions)

### 14.1 Principles
- Agents never import a provider SDK. They request a **role** from the core `ModelGateway`.
- Every decision returns a **Pydantic contract** (validated, retried on failure, logged to audit).
- Model providers are a **plugin type** (`type: model_provider`), configured in Settings.

### 14.2 Roles
| Role | Use | Default tier |
|---|---|---|
| `decision` | Approve/hold/escalate, match, route (System 1) | Typesafe AI if key set, else fast model |
| `reasoning` | Low-confidence or high-value escalations, close, forecasts (System 2) | Strong model (e.g. Claude) |
| `fast` | Classification, extraction, summaries | Small/cheap model |
| `conversation` | Command bar, chat | Mid model |
| `embedding` | RAG over docs/ledger | Embedding model |

### 14.3 Decision resolution order
1. If `TYPESAFE_AI_API_KEY` is set and the role is `decision` → **Typesafe AI** provider.
2. Else → the model mapped to the role in Settings (agent override → department override → global).
3. On provider error/timeout → next in fallback chain (e.g. Claude API → Bedrock Claude → Azure → open model).
4. If `confidence < threshold` or amount > policy limit → escalate to `reasoning`, then to human approval card.

### 14.4 Supported providers (adapters)
Anthropic Claude API · AWS Bedrock · Azure OpenAI / Azure AI Foundry · OpenAI · Google · Sarvam · Groq · open models via Ollama / vLLM / any OpenAI-compatible endpoint · Typesafe AI. Implemented via LangChain `init_chat_model` (or LiteLLM) behind one `ModelProvider` interface:
```python
class ModelProvider(Protocol):
    id: str
    def chat(self, model: str, **kw) -> BaseChatModel: ...
    async def decide(self, schema: type[T], messages: list, **kw) -> T: ...  # structured output
```

### 14.5 Decision contracts (examples)
```python
class PaymentDecision(BaseModel):
    action: Literal["approve", "hold", "escalate"]
    amount: Decimal
    currency: str
    payee_id: str
    reason: str
    confidence: float = Field(ge=0, le=1)

class CashMatchDecision(BaseModel):
    payment_id: str
    invoice_ids: list[str]
    match_type: Literal["exact", "partial", "short_pay", "no_match"]
    variance: Decimal
    confidence: float

class RouteDecision(BaseModel):
    department: str
    agent: str
    intent: str
    requires_approval: bool
    confidence: float

class RefundDecision(BaseModel):
    action: Literal["full_refund", "partial_refund", "deny", "escalate"]
    amount: Decimal | None
    reason: str
    confidence: float
```

### 14.6 Settings page
- **Providers**: add/remove, keys stored in vault (Render env group), health check.
- **Role mapping**: role → provider + model, with department and per-agent overrides.
- **Fallback chain** and timeouts.
- **Thresholds**: confidence threshold per role; escalation rules.
- **Spend caps**: per provider, per day.
- **Test decision**: run one input against two models side by side.
- **Evals**: saved decision cases auto-run before a provider/model change goes live; show accuracy and cost.

### 14.7 Config (example)
```yaml
models:
  roles:
    decision:     { provider: typesafe_ai, fallback: [anthropic:claude-sonnet, bedrock:claude-sonnet, ollama:llama] }
    reasoning:    { provider: anthropic, model: claude-opus }
    fast:         { provider: sarvam, model: sarvam-m }
    conversation: { provider: azure_openai, model: gpt-4o }
  overrides:
    finance.treasury: { decision: { provider: anthropic, model: claude-sonnet } }
  thresholds: { decision_confidence: 0.8 }
```
