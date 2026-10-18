# Agent-Ledger — Department Matrix & Design Doc

> **Status: draft proposal.** Not a decision. Conflicts with the repo are listed in [OKF decisions P-01..P-08](../plan/ERP_Design_OKF_Bundle/progress/decisions.md#draft-rough-spec-reconciliation-2026-10-18); standing entries there win. Entry points: [`AGENTS.md`](../AGENTS.md), [`plan/BUILD_START_HERE.md`](../plan/BUILD_START_HERE.md).

*PayPal AI Hackathon 2026 · solo dev (Cursor) · deadline **Thu Nov 12 2026***

## 0. TL;DR
- **Agent-Ledger** is an agentic ERP: each department is a **plugin** (`plugin.yaml` + one MCP server + one lead agent + 4–6 specialist agents), and they coordinate over **A2A**.
- **Every money move goes through one Core Money Rail** (`platform.money_rail`). It applies policy limits, waits for human approval above a threshold, writes a double-entry ledger posting, logs to the audit table, and then calls the PayPal sandbox.
- Long processes that span departments run as **Render Workflows**. Agents run as **Render Background Workers**. MCP servers run as **Render Private Services**. State lives in **Postgres** (ledger plus the A2A task store) and the **Key Value** queue.

### Stack
| Layer | Choice | Render service type |
|---|---|---|
| API / UI backend | Python 3.13, FastAPI (`chat.py`, webhooks, approvals UI) | Web Service |
| Agent runtime | LangGraph + `deepagents` (planner + sub-agents + virtual FS), Sarvam LLM (`sarvam-m` via OpenAI-compatible client) | Background Worker (one per department, or pooled) |
| Tools | MCP servers, one per department (streamable HTTP) | Private Service |
| Agent↔agent | A2A protocol: agent cards at `/.well-known/agent-card.json`, tasks `submitted → working → input-required → completed` (+ `failed`/`canceled`) | served by each lead agent's worker sidecar / FastAPI router |
| Long processes | Render Workflows (durable steps, retries, waits on approval) | Workflow |
| Schedules | Render Cron Jobs | Cron Job |
| Data | Postgres (ledger, sub-ledgers, audit, A2A tasks), Key Value (task queue, idempotency keys, locks) | Postgres / Key Value |
| Money rail | PayPal **sandbox** REST | external |

### Legend
- 💰 = calls PayPal, always **through `platform.money_rail`** or the read-only `platform.paypal_read` client. Agents never hold PayPal credentials.
- 👁 = read-only PayPal call. ✋ = human-approval gate.
- PayPal APIs used (all real): **Invoicing v2** (`/v2/invoicing/invoices`, `/send`, `/remind`, `/cancel`, `/payments`, `/generate-next-invoice-number`, `/search-invoices`), **Orders v2** (`/v2/checkout/orders`, `/capture`, `/authorize`), **Payments v2** (`/v2/payments/captures/{id}/refund`, `/authorizations/{id}/capture|void`, `/refunds/{id}`), **Payouts v1** (`/v1/payments/payouts`, `/payouts-item/{id}`, `/payouts-item/{id}/cancel`), **Disputes v1** (`/v1/customer/disputes`, `/provide-evidence`, `/accept-claim`, `/make-offer`, `/acknowledge-return`, `/appeal`, `/send-message`), **Transaction Search v1** (`/v1/reporting/transactions`, `/v1/reporting/balances`), **Catalog Products v1** (`/v1/catalogs/products`), **Subscriptions v1** (`/v1/billing/plans`, `/v1/billing/subscriptions`, `/suspend|activate|cancel|capture`, `/transactions`), **Webhooks v1** (`/v1/notifications/webhooks`, `/verify-webhook-signature`), **OAuth2** (`/v1/oauth2/token`).
- Not built on PayPal: supplier bank wires, payroll tax filings, GST filings. These are modelled as ledger entries plus exported files, and PayPal **Payouts** stands in for disbursing to vendors and employees in the sandbox. This is clearly a demo assumption.

---

## 1. Hierarchy & conventions
```
Department (plugin: plugin.yaml, 1 MCP server, 1 lead agent = A2A router)
 └─ Specialist agents (4–6)   ← LangGraph/deepagents sub-agents
     └─ Skills (3–6 each)     ← skills/<name>/SKILL.md (instructions + which tools)
         └─ Tools             ← MCP tools on that dept's server (snake_case, dept-prefixed in registry)
Workflows ← belong to *processes* (O2C, P2P…), span departments, call lead agents via A2A
```
| Rule | Detail |
|---|---|
| Naming | tools are `verb_noun`; the registry ID is `<dept>.<tool>` (e.g. `collections.send_invoice_reminder`) |
| Money | only `platform.money_rail.execute(intent)` may make a mutating PayPal call. Department tools build a **MoneyIntent** `{type, amount, currency, counterparty, paypal_op, idempotency_key, source_task}` and submit it |
| Ledger | every posting is double-entry in `ledger_entries` (balanced per `journal_id`) and posted by `r2r.post_journal` or by the rail itself. The `Dr/Cr` columns in the tables below are the default postings |
| Policy | `platform.policy` evaluates `{dept, op, amount, counterparty_risk}` and returns `allow` / `needs_approval` / `deny` |
| A2A | the lead agent of each department publishes one agent card with its skills = the specialist capabilities. Cross-department calls are **only** A2A tasks to leads; there are no direct cross-department MCP calls |
| Audit | every tool call, A2A transition, approval and PayPal response is appended to `audit_log` as a hash chain |

### Default policy limits (sandbox, `platform/policy/limits.yaml`)
| Op | Auto-allow ≤ | Needs 1 approver ≤ | Needs 2 approvers / deny |
|---|---|---|---|
| Refund (Payments v2) | ₹5,000 / $60 | ₹50,000 | > ₹50,000 deny |
| Payout single item (Payouts v1) | ₹10,000 | ₹2,00,000 | > ₹2,00,000 two approvers |
| Payout batch (payment run / payroll) | never auto | always 1 | > ₹10,00,000 two approvers |
| Dispute accept-claim / make-offer | ≤ ₹2,000 | ≤ ₹50,000 | above: Finance controller |
| Subscription cancel | auto | — | — |
| New payee / vendor bank change | never auto | always 1 | — |

---

## 2. Mapping of existing repo files
| Existing file | Becomes | Department | Notes |
|---|---|---|---|
| `router.py` | `platform/agents/orchestrator.py` (global A2A router) + base class `BaseLeadAgent` for every department lead | Platform | Intent classification → picks the department lead by agent card skills |
| `chat.py` | `app/api/chat.py` (FastAPI WS/SSE) → orchestrator | Platform (UI) | Also hosts the approval inbox endpoints |
| `treasury.py` | `plugins/finance/agents/treasury.py` (TreasuryAgent) | Finance | Cash position from Transaction Search balances, payment runs |
| `collection.py` | `plugins/finance/agents/collections.py` (CollectionsAgent) | Finance | Invoicing v2 reminders and dunning |
| `cash_app.py` | `plugins/finance/agents/cash_application.py` (CashApplicationAgent) | Finance | Matches PayPal transactions to open AR |
| `procurement.py` | `plugins/procurement/agents/lead.py` + split into `sourcing.py` and `purchase_order.py` | Procurement | Carve out the specialists; keep the old file as a shim until tests pass |

---

## 3. Departments

> Each section gives: **agents** table (role · skills · tools), **ledger postings**, **A2A in/out**, **plugin.yaml permissions**.

### 3.1 Finance (`plugins/finance`) — lead: `finance_lead`
Finance is the largest plugin. Its six sub-domains map to six specialists; the lead routes tasks to them.

| Agent | Role | Skills | Tools |
|---|---|---|---|
| **TreasuryAgent** (`treasury.py`) | Cash position, liquidity forecast, payment runs | `cash_position_report`, `liquidity_forecast`, `payment_run_planning`, `fx_exposure_check`, `sweep_recommendation` | `get_paypal_balances` 👁💰 *(Transaction Search v1 `/v1/reporting/balances`)*, `list_paypal_transactions` 👁💰 *(Transaction Search v1)*, `forecast_cash_13w`, `build_payment_run`, `submit_payout_batch` 💰✋ *(Payouts v1 create batch via rail)*, `get_payout_batch_status` 👁💰 *(Payouts v1 `GET /v1/payments/payouts/{id}`)*, `cancel_unclaimed_payout_item` 💰 *(Payouts v1 `/payouts-item/{id}/cancel`)* |
| **CollectionsAgent** (`collection.py`) | AR invoicing, dunning, promises to pay | `issue_customer_invoice`, `dunning_sequence`, `promise_to_pay_tracking`, `credit_hold_decision`, `ar_aging_review` | `create_paypal_invoice` 💰 *(Invoicing v2 create)*, `send_paypal_invoice` 💰 *(Invoicing v2 `/send`)*, `send_invoice_reminder` 💰 *(Invoicing v2 `/remind`)*, `cancel_paypal_invoice` 💰 *(Invoicing v2 `/cancel`)*, `search_paypal_invoices` 👁💰 *(Invoicing v2 `/search-invoices`)*, `get_ar_aging`, `set_credit_hold` |
| **CashApplicationAgent** (`cash_app.py`) | Match receipts to invoices, unapplied cash | `match_payment_to_invoice`, `handle_short_pay`, `unapplied_cash_triage`, `fee_netting` | `list_paypal_transactions` 👁💰 *(Transaction Search v1)*, `get_paypal_invoice` 👁💰 *(Invoicing v2 GET)*, `record_invoice_payment` 💰 *(Invoicing v2 `/payments`, only for external/offline receipts)*, `fuzzy_match_open_items`, `apply_cash`, `post_paypal_fee` |
| **APAgent** | Vendor bills, 3-way match, vendor payouts | `bill_capture`, `three_way_match`, `vendor_payment_scheduling`, `duplicate_bill_detection`, `vendor_onboarding_check` | `ingest_vendor_bill`, `match_bill_po_grn`, `detect_duplicate_bill`, `schedule_vendor_payment`, `pay_vendor_via_payout` 💰✋ *(Payouts v1 via rail)*, `get_payout_item` 👁💰 *(Payouts v1 `/payouts-item/{id}`)*, `get_ap_aging` |
| **R2RAgent** (GL & Close) | Journals, reconciliations, month-end close | `post_journal_entry`, `bank_paypal_reconciliation`, `accruals_and_prepaids`, `month_end_close_checklist`, `trial_balance_review`, `intercompany_elims` | `post_journal`, `reverse_journal`, `get_trial_balance`, `reconcile_paypal_account` 👁💰 *(Transaction Search v1 transactions + balances)*, `create_accrual`, `run_close_checklist`, `lock_period` ✋ |
| **TaxAgent** | GST/indirect tax calc, TDS on vendor payouts, filings prep | `gst_calculation`, `tds_withholding`, `tax_return_prep`, `tax_code_mapping` | `calc_gst_for_invoice`, `calc_tds_for_payment`, `build_gstr_export`, `map_tax_code`, `post_tax_liability` |

**Ledger postings**
| Event | Dr | Cr |
|---|---|---|
| Invoice issued (Invoicing v2) | Accounts Receivable | Revenue, GST Output Payable |
| PayPal receipt applied | PayPal Clearing | Accounts Receivable |
| PayPal fee | PayPal Fees Expense | PayPal Clearing |
| Vendor bill | Expense/Inventory, GST Input Credit | Accounts Payable, TDS Payable |
| Vendor payout (Payouts v1) | Accounts Payable | PayPal Clearing |
| Payout returned/unclaimed | PayPal Clearing | Accounts Payable |
| Accrual | Expense | Accrued Liabilities (auto-reversed on day 1) |
| PayPal recon variance | Suspense | PayPal Clearing (or reverse) |

**A2A**: *In*: `sales.close_deal→issue_customer_invoice`, `procurement.grn_posted→three_way_match`, `hr.payroll_approved→payment_run`, `support.refund_approved→post refund`, `analytics.request_kpis`, `projects.expense_approved→reimburse`. *Out*: `sales.credit_hold_notice`, `procurement.vendor_paid`, `analytics.close_completed`, `platform.request_approval`.

```yaml
# plugins/finance/plugin.yaml (permissions excerpt)
permissions:
  ledger: [read, write:journals, write:subledger_ar, write:subledger_ap, lock_period]
  paypal_read: [reporting.balances, reporting.transactions, invoicing.read, payouts.read]
  money_rail: [invoicing.create, invoicing.send, invoicing.remind, invoicing.cancel,
               invoicing.record_payment, payouts.create_batch, payouts.cancel_item]
  a2a_call: [sales, procurement, hr, analytics, platform]
  data: [customers:read, vendors:read, vendors:write_bank_details:approval]
```

### 3.2 Sales & CRM (`plugins/sales`) — lead: `sales_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **LeadQualAgent** | Lead capture and scoring | `lead_scoring`, `lead_enrichment`, `lead_routing` | `create_lead`, `score_lead`, `enrich_company`, `assign_owner` |
| **OpportunityAgent** | Pipeline and forecast | `pipeline_hygiene`, `deal_forecast`, `next_best_action`, `stage_progression` | `list_opportunities`, `update_opportunity_stage`, `forecast_pipeline`, `log_activity` |
| **QuoteOrderAgent** | Quote-to-order, checkout links | `quote_builder`, `discount_guardrail`, `order_capture`, `checkout_link_generation` | `create_quote`, `apply_discount` ✋(>20%), `convert_quote_to_order`, `create_paypal_order` 💰 *(Orders v2 create)*, `capture_paypal_order` 💰 *(Orders v2 `/capture`)*, `get_paypal_order` 👁💰 *(Orders v2 GET)* |
| **SubscriptionAgent** | Recurring revenue | `plan_setup`, `subscription_lifecycle`, `churn_save`, `mrr_tracking` | `create_catalog_product` 💰 *(Catalog Products v1)*, `create_billing_plan` 💰 *(Subscriptions v1 plans)*, `create_subscription` 💰 *(Subscriptions v1)*, `suspend_subscription` 💰, `activate_subscription` 💰, `cancel_subscription` 💰, `list_subscription_transactions` 👁💰 *(Subscriptions v1 `/transactions`)* |
| **AccountMgmtAgent** | Customer 360, renewals | `customer_360`, `renewal_playbook`, `upsell_detection` | `get_customer_360`, `list_renewals_due`, `create_task`, `request_credit_check` (A2A→finance) |

**Ledger**: an order captured via Orders v2 posts *Dr PayPal Clearing / Cr Revenue, GST Output* through Finance. A subscription payment (webhook `PAYMENT.SALE.COMPLETED`) posts the same entry, plus *Deferred Revenue* for annual plans.
**A2A** *In*: `support.churn_risk`, `inventory.stock_available`. *Out*: `finance.issue_invoice`, `finance.credit_check`, `inventory.reserve_stock`, `manufacturing.make_to_order`, `analytics.pipeline_snapshot`.
```yaml
permissions:
  ledger: [read]
  paypal_read: [orders.read, subscriptions.read]
  money_rail: [orders.create, orders.capture, catalog.products.create, subscriptions.plans.create,
               subscriptions.create, subscriptions.suspend, subscriptions.activate, subscriptions.cancel]
  a2a_call: [finance, inventory, manufacturing, analytics]
  data: [customers:write, leads:write, opportunities:write]
```

### 3.3 Procurement (`plugins/procurement`, from `procurement.py`) — lead: `procurement_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **RequisitionAgent** | Intake of purchase requests | `requisition_intake`, `budget_check`, `catalog_buy_suggest` | `create_requisition`, `check_budget` (A2A→finance), `search_catalog`, `route_req_for_approval` ✋ |
| **SourcingAgent** | RFQs, vendor selection | `rfq_generation`, `bid_comparison`, `vendor_scoring`, `negotiation_brief` | `create_rfq`, `collect_bids`, `score_vendor`, `compare_bids` |
| **PurchaseOrderAgent** | PO lifecycle | `po_creation`, `po_change_management`, `po_followup` | `create_po`, `amend_po`, `send_po_to_vendor`, `get_po_status` |
| **ReceivingAgent** | Goods/service receipt | `grn_capture`, `quality_inspection_hold`, `return_to_vendor` | `post_grn`, `flag_quality_hold`, `create_rtv` |
| **VendorMgmtAgent** | Vendor master and risk | `vendor_onboarding`, `vendor_risk_review`, `contract_renewal` | `create_vendor`, `verify_vendor_payout_email` ✋, `update_vendor_bank` ✋, `list_expiring_contracts` |

**Ledger**: the PO itself makes no posting (only a commitment in `budget_commitments`). GRN posts *Dr Inventory/Expense / Cr GRNI (Goods Received Not Invoiced)*. The AP bill clears GRNI. Procurement **never** pays: payment is A2A to Finance AP.
**A2A** *In*: `inventory.reorder_request`, `manufacturing.material_shortage`, `hr.laptop_request`. *Out*: `finance.three_way_match`, `finance.budget_check`, `inventory.expected_receipt`.
```yaml
permissions:
  ledger: [read, write:grni]
  paypal_read: []
  money_rail: []            # no money movement
  a2a_call: [finance, inventory, platform]
  data: [vendors:write, purchase_orders:write]
```

### 3.4 Inventory & Warehouse (`plugins/inventory`) — lead: `inventory_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **StockControlAgent** | On-hand, reservations | `stock_level_check`, `reservation_management`, `cycle_count` | `get_stock_level`, `reserve_stock`, `release_reservation`, `post_cycle_count_adjustment` |
| **ReplenishmentAgent** | Reorder points, demand | `reorder_point_calc`, `demand_forecast`, `safety_stock_tuning` | `calc_reorder_point`, `forecast_demand`, `raise_reorder_request` (A2A→procurement) |
| **FulfillmentAgent** | Pick/pack/ship | `pick_list_generation`, `shipment_creation`, `tracking_upload` | `create_pick_list`, `create_shipment`, `add_paypal_tracking` 💰 *(Orders v2 `POST /v2/checkout/orders/{id}/track`)* |
| **ReturnsAgent** | RMA, restock | `rma_processing`, `restock_or_scrap`, `return_inspection` | `create_rma`, `receive_return`, `restock_item`, `scrap_item` |
| **ValuationAgent** | COGS and inventory valuation | `fifo_wac_costing`, `inventory_valuation_report`, `shrinkage_analysis` | `compute_cogs`, `get_valuation`, `post_inventory_adjustment` |

**Ledger**: shipment posts *Dr COGS / Cr Inventory*. Adjustment/scrap posts *Dr Inventory Shrinkage / Cr Inventory*. Restock posts *Dr Inventory / Cr COGS*.
**A2A** *In*: `sales.reserve_stock`, `support.return_received`, `manufacturing.consume_materials`. *Out*: `procurement.reorder_request`, `finance.post_cogs`, `support.return_inspected`.
```yaml
permissions:
  ledger: [read, write:inventory_subledger]
  paypal_read: [orders.read]
  money_rail: [orders.add_tracking]   # non-monetary but mutating PayPal call → still via rail
  a2a_call: [procurement, finance, support, manufacturing]
  data: [items:write, warehouses:write, shipments:write]
```

### 3.5 HR & Payroll (`plugins/hr`) — lead: `hr_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **RecruitingAgent** | Req to offer | `job_req_creation`, `candidate_screening`, `offer_letter_draft` | `create_job_req`, `screen_candidate`, `draft_offer` ✋ |
| **OnboardingAgent** | Hire-to-retire start | `onboarding_checklist`, `equipment_provisioning`, `access_provisioning`, `policy_acknowledgement` | `create_employee`, `start_onboarding_checklist`, `request_laptop` (A2A→procurement), `request_accounts` (A2A→platform) |
| **PayrollAgent** | Gross-to-net, payouts | `payroll_calculation`, `statutory_deductions`, `payslip_generation`, `payroll_disbursement` | `compute_payroll`, `compute_pf_esi_pt_tds`, `generate_payslips`, `submit_payroll_payouts` 💰✋ *(Payouts v1 batch via rail)*, `get_payout_batch_status` 👁💰 *(Payouts v1)* |
| **LeaveTimeAgent** | Time and attendance | `leave_balance`, `timesheet_approval`, `overtime_calc` | `get_leave_balance`, `apply_leave`, `approve_timesheet` ✋ |
| **EmployeeLifecycleAgent** | Changes, exits | `compensation_change`, `offboarding`, `full_and_final_settlement` | `update_compensation` ✋, `start_offboarding`, `compute_fnf`, `revoke_access` (A2A→platform) |

**Ledger**: payroll accrual posts *Dr Salary Expense / Cr Salaries Payable, PF/ESI/PT/TDS Payable*. Payout posts *Dr Salaries Payable / Cr PayPal Clearing*.
**A2A** *In*: `projects.timesheet_hours`. *Out*: `finance.payment_run (payroll)`, `procurement.laptop_request`, `platform.provision_access`, `analytics.headcount`.
```yaml
permissions:
  ledger: [read, write:payroll_journals]
  paypal_read: [payouts.read]
  money_rail: [payouts.create_batch]   # always ✋, 2 approvers above limit
  a2a_call: [finance, procurement, platform, analytics]
  data: [employees:write, pii:salary:restricted]
```

### 3.6 Customer Support (`plugins/support`) — lead: `support_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **TicketTriageAgent** | Intake, classify, SLA | `ticket_classification`, `sla_tracking`, `sentiment_escalation` | `create_ticket`, `classify_ticket`, `escalate_ticket`, `get_order_context` |
| **RefundAgent** | Refunds on PayPal captures | `refund_eligibility`, `partial_refund`, `refund_status_followup`, `authorization_void` | `check_refund_policy`, `refund_paypal_capture` 💰✋ *(Payments v2 `/v2/payments/captures/{id}/refund`)*, `get_paypal_refund` 👁💰 *(Payments v2 `/refunds/{id}`)*, `void_paypal_authorization` 💰 *(Payments v2 `/authorizations/{id}/void`)*, `get_paypal_capture` 👁💰 *(Payments v2 `/captures/{id}`)* |
| **DisputeAgent** | Chargebacks and PayPal disputes | `dispute_intake`, `evidence_assembly`, `dispute_decision`, `dispute_messaging`, `return_acknowledgement` | `list_paypal_disputes` 👁💰 *(Disputes v1)*, `get_paypal_dispute` 👁💰 *(Disputes v1)*, `provide_dispute_evidence` 💰 *(Disputes v1 `/provide-evidence`)*, `accept_dispute_claim` 💰✋ *(Disputes v1 `/accept-claim`)*, `make_dispute_offer` 💰✋ *(Disputes v1 `/make-offer`)*, `send_dispute_message` 💰 *(Disputes v1 `/send-message`)*, `acknowledge_dispute_return` 💰 *(Disputes v1 `/acknowledge-return`)*, `appeal_dispute` 💰✋ *(Disputes v1 `/appeal`)* |
| **KnowledgeAgent** | KB answers, macros | `kb_answer`, `macro_suggestion`, `kb_gap_detection` | `search_kb`, `draft_reply`, `create_kb_article` |
| **RetentionAgent** | Churn save | `churn_risk_detection`, `goodwill_credit` | `score_churn_risk`, `issue_goodwill_credit` ✋, `notify_account_manager` (A2A→sales) |

**Ledger**: refund posts *Dr Sales Returns / GST Output (reversal) / Cr PayPal Clearing*. Dispute hold posts *Dr Disputed Funds Receivable / Cr PayPal Clearing*. A lost dispute posts *Dr Chargeback Loss / Cr Disputed Funds Receivable*, and a won dispute releases the hold.
**A2A** *In*: webhooks `CUSTOMER.DISPUTE.CREATED/UPDATED/RESOLVED`, `PAYMENT.CAPTURE.REFUNDED`. *Out*: `finance.post_refund`, `inventory.expect_return`, `sales.churn_risk`, `platform.request_approval`.
```yaml
permissions:
  ledger: [read]
  paypal_read: [payments.captures.read, payments.refunds.read, disputes.read]
  money_rail: [payments.captures.refund, payments.authorizations.void, disputes.provide_evidence,
               disputes.accept_claim, disputes.make_offer, disputes.send_message,
               disputes.acknowledge_return, disputes.appeal]
  a2a_call: [finance, inventory, sales, platform]
  data: [tickets:write, customers:read]
```

### 3.7 Manufacturing / Operations (`plugins/manufacturing`) — lead: `mfg_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **BOMAgent** | Bills of materials, routings | `bom_management`, `routing_definition`, `engineering_change` | `get_bom`, `update_bom` ✋, `define_routing` |
| **PlanningAgent** | MRP and capacity | `mrp_run`, `capacity_planning`, `make_vs_buy` | `run_mrp`, `check_capacity`, `raise_material_shortage` (A2A→procurement) |
| **ProductionAgent** | Work orders | `work_order_release`, `material_issue`, `production_reporting`, `scrap_reporting` | `create_work_order`, `issue_materials` (A2A→inventory), `report_output`, `report_scrap` |
| **QualityAgent** | QC and NCRs | `inspection_plan`, `nonconformance_handling`, `capa_tracking` | `record_inspection`, `create_ncr`, `track_capa` |
| **MaintenanceAgent** | Assets and PM | `preventive_maintenance`, `breakdown_ticket`, `spare_parts_request` | `schedule_pm`, `log_breakdown`, `request_spares` |

**Ledger**: material issue posts *Dr WIP / Cr Raw Materials*. Output posts *Dr Finished Goods / Cr WIP*. Variance posts *Dr/Cr Production Variance*. No PayPal calls.
**A2A** *In*: `sales.make_to_order`. *Out*: `inventory.consume_materials`, `procurement.material_shortage`, `finance.post_wip`.
```yaml
permissions:
  ledger: [read, write:wip]
  paypal_read: []
  money_rail: []
  a2a_call: [inventory, procurement, finance]
  data: [boms:write, work_orders:write, assets:write]
```

### 3.8 Projects & Expenses (`plugins/projects`) — lead: `projects_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **ProjectPlanAgent** | Projects, budgets, milestones | `project_setup`, `budget_vs_actual`, `milestone_tracking` | `create_project`, `get_budget_vs_actual`, `update_milestone` |
| **TimesheetAgent** | Time capture for billing/payroll | `timesheet_capture`, `utilization_report`, `billable_rules` | `log_time`, `get_utilization`, `send_hours_to_hr` (A2A→hr) |
| **ExpenseAgent** | Employee expense claims | `receipt_extraction`, `expense_policy_check`, `expense_approval`, `reimbursement` | `parse_receipt`, `check_expense_policy`, `submit_expense_for_approval` ✋, `reimburse_employee_payout` 💰✋ *(Payouts v1 via rail)* |
| **ProjectBillingAgent** | T&M / milestone billing | `tm_billing`, `milestone_billing`, `wip_revenue_recognition` | `compute_billable`, `request_project_invoice` (A2A→finance; Invoicing v2 there), `recognize_project_revenue` |

**Ledger**: approved expense posts *Dr Expense (by category), GST Input / Cr Employee Reimbursement Payable*. Reimbursement posts *Dr Reimbursement Payable / Cr PayPal Clearing*. Unbilled revenue posts *Dr Unbilled AR / Cr Revenue*.
**A2A** *In*: `hr.employee_created`. *Out*: `finance.issue_invoice`, `hr.timesheet_hours`, `analytics.project_margin`.
```yaml
permissions:
  ledger: [read, write:project_journals]
  paypal_read: [payouts.read]
  money_rail: [payouts.create_batch]   # reimbursements, single-item batches
  a2a_call: [finance, hr, analytics]
  data: [projects:write, expenses:write, receipts:write]
```

### 3.9 Analytics / Leadership (`plugins/analytics`) — lead: `analytics_lead`
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **KPIAgent** | Metric layer | `kpi_computation`, `metric_definitions`, `dashboard_refresh` | `query_ledger`, `compute_kpi`, `refresh_dashboard` |
| **FPandAAgent** | Budgets and forecasts | `budget_build`, `variance_analysis`, `rolling_forecast`, `scenario_modeling` | `get_budget`, `compute_variance`, `run_forecast`, `run_scenario` |
| **CFOBriefAgent** | Exec narrative | `weekly_cfo_brief`, `board_pack`, `cash_runway_narrative` | `draft_brief`, `fetch_department_summaries` (A2A fan-out), `export_pdf` |
| **AnomalyAgent** | Risk/fraud signals | `anomaly_detection`, `paypal_activity_monitoring`, `alert_routing` | `detect_ledger_anomaly`, `scan_paypal_transactions` 👁💰 *(Transaction Search v1)*, `raise_alert` |
| **NLQueryAgent** | "Ask the ERP" | `nl_to_sql`, `chart_generation`, `answer_with_citations` | `nl_to_sql`, `run_readonly_sql`, `render_chart` |

**Ledger**: none (read-only).
**A2A** *In*: requests from any lead and from `chat.py`. *Out*: fan-out `*.summary` to all leads, `platform.alert`.
```yaml
permissions:
  ledger: [read]
  paypal_read: [reporting.transactions, reporting.balances]
  money_rail: []
  a2a_call: ["*:read_only_skills"]
  data: ["*:read"]
```

### 3.10 Platform / Admin (`plugins/platform`, core, not uninstallable) — lead: `orchestrator` (`router.py`)
| Agent | Role | Skills | Tools |
|---|---|---|---|
| **OrchestratorAgent** (`router.py`, `chat.py`) | Global router, chat front door, A2A task broker | `intent_routing`, `agent_card_discovery`, `task_state_tracking`, `multi_dept_planning` | `list_agent_cards`, `send_a2a_task`, `get_a2a_task`, `cancel_a2a_task`, `start_render_workflow` |
| **MoneyRailAgent** | **The core money rail** (deterministic code with a thin agent wrapper) | `money_intent_validation`, `idempotent_execution`, `paypal_webhook_ingest`, `rail_reconciliation` | `execute_money_intent` 💰 *(dispatches to Invoicing v2 / Orders v2 / Payments v2 / Payouts v1 / Disputes v1 / Subscriptions v1)*, `get_paypal_access_token` *(OAuth2 `/v1/oauth2/token`)*, `verify_webhook_signature` 💰 *(Webhooks v1 `/v1/notifications/verify-webhook-signature`)*, `register_webhooks` 💰 *(Webhooks v1 `/v1/notifications/webhooks`)*, `route_webhook_event` |
| **PolicyAgent** | Limits, approvals | `policy_evaluation`, `approval_routing`, `segregation_of_duties` | `evaluate_policy`, `create_approval_request`, `record_approval_decision`, `check_sod` |
| **AuditAgent** | Immutable audit and evidence | `audit_logging`, `audit_query`, `evidence_export` | `append_audit_event`, `verify_audit_chain`, `query_audit`, `export_evidence_pack` |
| **PluginStoreAgent** | Install/enable plugins | `plugin_install`, `permission_review`, `plugin_health` | `list_plugins`, `install_plugin` ✋, `grant_permissions` ✋, `get_plugin_health` |
| **IdentityAgent** | Users, roles, access | `access_provisioning`, `access_revocation`, `role_management` | `create_user`, `assign_role` ✋, `revoke_user` |

**Ledger**: the MoneyRail writes the PayPal-side posting atomically with the PayPal call outcome (outbox pattern: intent row → PayPal call → result → journal). Every other department's postings are requested through `r2r.post_journal`.
**A2A** *In*: everything. *Out*: `*.approval_decided`, `*.webhook_event`.
```yaml
permissions:
  ledger: [read, write:paypal_clearing, write:audit]
  paypal_credentials: true       # ONLY plugin with secrets (PAYPAL_CLIENT_ID/SECRET env on rail service)
  money_rail: ["*"]
  a2a_call: ["*"]
  admin: [plugins, policy, identity]
```

---

## 4. Workflows catalog
Execution types: **RW** = Render Workflow (durable, multi-step, waits on approvals). **WT** = worker task (Key Value queue → Background Worker). **CRON** = Render Cron Job that kicks off a WT or RW.

### 4.1 Summary
| # | Workflow | Process | Trigger | Type | Depts | Gates |
|---|---|---|---|---|---|---|
| W1 | Order-to-Cash | O2C | deal closed / checkout | RW | Sales, Inventory, Finance | discount >20%, credit hold |
| W2 | Procure-to-Pay | P2P | requisition | RW | Procurement, Inventory, Finance | req approval, payout approval |
| W3 | Month-end close | R2R | CRON day 1, 02:00 IST | RW | Finance (all), Analytics | period lock |
| W4 | Payroll run | H2R | CRON 25th | RW | HR, Projects, Finance | 1–2 approvers |
| W5 | Hire-to-retire onboarding | H2R | offer accepted | RW | HR, Platform, Procurement, Projects | offer, access roles |
| W6 | New-hire laptop | H2R/P2P sub-flow | from W5 | RW (child) | Procurement, Inventory, Finance | PO approval |
| W7 | Refund / dispute | O2C reverse | ticket or PayPal webhook | RW | Support, Inventory, Finance | refund/dispute limits |
| W8 | Inventory reorder | P2P | stock < ROP | WT (→ W2) | Inventory, Procurement | via W2 |
| W9 | Nightly PayPal recon | R2R | CRON 01:00 IST | CRON → WT | Finance, Platform, Analytics | variance > threshold |
| W10 | Treasury payment run | P2P/H2R | CRON Tue/Fri or W4 | RW | Finance, Platform | always ✋ |

### 4.2 Steps
**W1 O2C (RW)**
| Step | Handler | PayPal | Gate |
|---|---|---|---|
| 1 Quote → order | `sales.QuoteOrderAgent.create_quote`, `convert_quote_to_order` | — | ✋ discount >20% |
| 2 Credit check | A2A → `finance.CollectionsAgent.credit_hold_decision` | — | auto-hold over limit |
| 3 Reserve stock | A2A → `inventory.StockControlAgent.reserve_stock` | — | — |
| 4a Card/wallet checkout | `sales.create_paypal_order` → buyer approves → `capture_paypal_order` | Orders v2 | — |
| 4b B2B invoice | A2A → `finance.create_paypal_invoice` + `send_paypal_invoice` | Invoicing v2 | — |
| 5 Ship + tracking | `inventory.FulfillmentAgent.create_shipment`, `add_paypal_tracking` | Orders v2 track | — |
| 6 Wait for payment | workflow waits for webhook `PAYMENT.CAPTURE.COMPLETED` / `INVOICING.INVOICE.PAID` (verified by Webhooks v1) | Webhooks v1 | — |
| 7 Dunning (if unpaid) | `finance.send_invoice_reminder` on D+3/7/14 (child WT) | Invoicing v2 remind | — |
| 8 Cash application + GL | `finance.CashApplicationAgent.apply_cash`, `post_paypal_fee` | Transaction Search v1 | — |

**W2 P2P (RW)**
| Step | Handler | PayPal | Gate |
|---|---|---|---|
| 1 Requisition + budget | `procurement.create_requisition`, A2A `finance.check_budget` | — | ✋ manager |
| 2 Source | `procurement.SourcingAgent.create_rfq`, `compare_bids` (skip for catalog items) | — | — |
| 3 PO | `procurement.create_po`, `send_po_to_vendor` | — | ✋ > ₹1L |
| 4 Receipt | `procurement.ReceivingAgent.post_grn` → A2A `inventory` receipt | — | quality hold |
| 5 Bill + 3-way match | A2A `finance.APAgent.ingest_vendor_bill`, `match_bill_po_grn`, `detect_duplicate_bill`, Tax `calc_tds_for_payment` | — | ✋ on mismatch |
| 6 Schedule | `finance.schedule_vendor_payment` → queued into W10 | — | — |

**W3 R2R month-end close (RW, CRON-triggered)**
| Step | Handler | Gate |
|---|---|---|
| 1 Cut-off: freeze sub-ledgers | `finance.R2RAgent.run_close_checklist` | — |
| 2 Final PayPal recon | run W9 for the full month | variance ✋ |
| 3 Sub-ledger tie-outs (AR/AP/Inventory/Payroll) | A2A fan-out to each lead's `*_subledger_tieout` | — |
| 4 Accruals, prepaids, depreciation | `finance.create_accrual`, `post_journal` | ✋ manual JEs > ₹50k |
| 5 Tax liability | `finance.TaxAgent.post_tax_liability`, `build_gstr_export` | — |
| 6 Trial balance + flux | `finance.get_trial_balance`, `analytics.FPandAAgent.compute_variance` | — |
| 7 Lock period | `finance.lock_period` | ✋ controller |
| 8 CFO brief | `analytics.CFOBriefAgent.draft_brief` | — |

**W4 Payroll run (RW)**
| Step | Handler | Gate |
|---|---|---|
| 1 Pull hours/leave | A2A `projects.TimesheetAgent`, `hr.LeaveTimeAgent` | — |
| 2 Gross-to-net | `hr.compute_payroll`, `compute_pf_esi_pt_tds` | — |
| 3 Review | diff vs last month; anomalies → `analytics.AnomalyAgent` | ✋ HR head |
| 4 Accrue | `finance.post_journal` (salary accrual) | — |
| 5 Disburse | `hr.submit_payroll_payouts` → rail → **Payouts v1** batch | ✋ finance (2 approvers above limit) |
| 6 Confirm | poll `get_payout_batch_status`; unclaimed → `cancel_unclaimed_payout_item` after 30 days | — |
| 7 Payslips | `hr.generate_payslips` | — |

**W5 Hire-to-retire onboarding (RW)**
| Step | Handler | Gate |
|---|---|---|
| 1 Offer accepted → employee | `hr.RecruitingAgent` → `hr.create_employee` | ✋ offer |
| 2 Accounts | A2A `platform.IdentityAgent.create_user`, `assign_role` | ✋ privileged roles |
| 3 Laptop | start child **W6** | — |
| 4 Payroll + payee setup | `hr` adds payee; `platform.evaluate_policy` (new payee) | ✋ |
| 5 Project assignment | A2A `projects` assign | — |
| 6 Day-1 checklist | `hr.start_onboarding_checklist`, waits until complete (≤ 30 days) | — |
| (exit mirror) | `start_offboarding` → `revoke_user` → `compute_fnf` → Payouts via W10 | ✋ |

**W6 New-hire laptop (child RW)**
| Step | Handler | Gate |
|---|---|---|
| 1 Check spare stock | A2A `inventory.get_stock_level` (IT assets) | — |
| 2a In stock → reserve & ship | `inventory.reserve_stock`, `create_shipment` | — |
| 2b Not in stock → P2P | start **W2** with catalog item (skip sourcing) | ✋ PO |
| 3 Asset capitalize | `finance.post_journal` (Dr Fixed Asset / Cr GRNI) | — |
| 4 Notify HR | A2A `hr` checklist item done | — |

**W7 Refund / dispute (RW)**
| Step | Handler | PayPal | Gate |
|---|---|---|---|
| 1 Intake | ticket via `support.create_ticket` **or** webhook `CUSTOMER.DISPUTE.CREATED` | Webhooks v1 | — |
| 2 Context | `support.get_paypal_capture`, `get_paypal_dispute` | Payments v2, Disputes v1 | — |
| 3a Refund path | `check_refund_policy` → `refund_paypal_capture` via rail | Payments v2 refund | ✋ by amount |
| 3b Dispute path | `DisputeAgent.evidence_assembly` (order, tracking, chat log) → `provide_dispute_evidence` **or** `make_dispute_offer` / `accept_dispute_claim` | Disputes v1 | ✋ accept/offer by amount |
| 4 Return | A2A `inventory.ReturnsAgent.create_rma`; `acknowledge_dispute_return` when received | Disputes v1 | — |
| 5 Wait resolution | waits for `CUSTOMER.DISPUTE.RESOLVED` (or ≤ 20 days, re-poll) | Disputes v1 | — |
| 6 Post | A2A `finance.post_journal` (refund / chargeback loss / release) | — | — |

**W8 Inventory reorder (WT)**
| Step | Handler |
|---|---|
| 1 Trigger on stock movement or nightly CRON | `inventory.ReplenishmentAgent.calc_reorder_point` |
| 2 Below ROP → request | `raise_reorder_request` → A2A `procurement_lead` |
| 3 Procurement starts **W2** (catalog fast-path) | procurement |

**W9 Nightly PayPal recon (CRON 01:00 IST → WT)**
| Step | Handler | PayPal | Gate |
|---|---|---|---|
| 1 Pull last 24h (Transaction Search has up to ~3h latency, so use a 27h window) | `finance.R2RAgent.reconcile_paypal_account` | Transaction Search v1 transactions | — |
| 2 Pull balances | `treasury.get_paypal_balances` | Transaction Search v1 balances | — |
| 3 Match to rail intents & ledger | `platform.MoneyRailAgent.rail_reconciliation`, `cash_app.fuzzy_match_open_items` | — | — |
| 4 Post fees, flag breaks to Suspense | `finance.post_paypal_fee`, `post_journal` | — | ✋ variance > ₹1,000 |
| 5 Anomalies + summary | `analytics.AnomalyAgent.scan_paypal_transactions` | — | — |

**W10 Treasury payment run (RW, CRON Tue/Fri, or triggered by W4/W5 exit)**
| Step | Handler | PayPal | Gate |
|---|---|---|---|
| 1 Collect due items (AP, reimbursements, payroll) | `finance.TreasuryAgent.build_payment_run` | — | — |
| 2 Cash check | `get_paypal_balances`, `forecast_cash_13w` | Transaction Search v1 | short cash → ✋ prioritization |
| 3 Policy + SoD | `platform.evaluate_policy`, `check_sod` | — | — |
| 4 Approve | `platform.create_approval_request` (A2A task goes to `input-required`) | — | ✋ always |
| 5 Execute | `submit_payout_batch` → rail `execute_money_intent` (`sender_batch_id` = idempotency key) | Payouts v1 | — |
| 6 Track | webhooks `PAYMENT.PAYOUTSBATCH.SUCCESS`, `PAYMENT.PAYOUTS-ITEM.SUCCEEDED/FAILED/UNCLAIMED/RETURNED` | Payouts v1, Webhooks v1 | — |
| 7 Post + notify | `finance.post_journal`; A2A `procurement.vendor_paid`, `hr.payroll_paid` | — | — |

### 4.3 A2A task state ↔ approval mapping
| A2A state | Meaning in Agent-Ledger |
|---|---|
| `submitted` | task queued in Key Value; audit event written |
| `working` | specialist executing tools |
| `input-required` | waiting on a human approval (`approval_id` in the task metadata) or missing data. The Render Workflow step waits on it |
| `completed` | artifacts carry `journal_id`, `paypal_ref`, `audit_hash` |
| `failed` / `canceled` | compensation step (e.g. void authorization, cancel payout item, reverse journal) |

---

## 5. Department plugin template (stamp out with Cursor)
```
plugins/<dept>/
├── plugin.yaml                 # manifest + permissions (see below)
├── mcp_server.py               # FastMCP server exposing ALL dept tools; one Render Private Service
├── tools/
│   ├── __init__.py
│   └── <area>.py               # pure functions; money tools only build MoneyIntent
├── agents/
│   ├── lead.py                 # BaseLeadAgent subclass: A2A server, routes to specialists
│   └── <specialist>.py         # deepagents sub-agent: system prompt + skills + MCP tool subset
├── skills/
│   └── <skill_name>/
│       └── SKILL.md            # frontmatter: name, description, tools[], approval_gates[]; then steps
├── a2a/
│   ├── agent-card.json         # served at /.well-known/agent-card.json
│   └── tasks/<task_type>.json  # JSON schema for task input/output artifacts
├── ledger/
│   └── postings.yaml           # event → Dr/Cr account mapping (validated in tests)
├── workflows/                  # only if dept owns a process (e.g. finance/close.py)
└── tests/
    ├── test_tools.py           # unit tests; PayPal mocked with respx
    ├── test_agents.py          # scripted LLM (fake Sarvam) → expected tool calls
    ├── test_a2a_contract.py    # agent-card + task schemas validate
    └── test_ledger_balanced.py # every posting balances
```

**`plugin.yaml` template**
```yaml
id: finance
name: Finance
version: 0.1.0
core: false
lead_agent: agents/lead.py:FinanceLead
mcp:
  entry: mcp_server.py
  render_service: private        # agent-ledger-mcp-finance
  port: 8000
agents:
  - {id: treasury, entry: agents/treasury.py:TreasuryAgent, skills: [cash_position_report, liquidity_forecast]}
  # ...
permissions:
  ledger: [read, write:journals]
  paypal_read: [reporting.balances]
  money_rail: [payouts.create_batch]
  a2a_call: [platform, analytics]
  data: [vendors:read]
approvals:
  - {op: payouts.create_batch, policy: payment_run}
events:
  subscribes: [PAYMENT.PAYOUTSBATCH.SUCCESS, INVOICING.INVOICE.PAID]
  emits: [finance.close_completed]
```

**`SKILL.md` template**
```markdown
---
name: dunning_sequence
description: Remind overdue customers on D+3/7/14 and escalate to credit hold.
tools: [search_paypal_invoices, send_invoice_reminder, set_credit_hold]
approval_gates: []
---
1. search_paypal_invoices(status=SENT|PARTIALLY_PAID, due_before=today-3)
2. For each: pick tone by days overdue → send_invoice_reminder (rail).
3. >30 days → set_credit_hold + A2A sales.credit_hold_notice.
```

**Cursor prompt to stamp a department**: "Using `plugins/_template`, create `plugins/<dept>` from section 3.x of Agent-Ledger-Department-Matrix.md: one tool stub per tool, one SKILL.md per skill, an agent-card listing the specialist skills, and postings.yaml from the Ledger table. Make all tests pass."

**Render services (`render.yaml`)**
| Service | Type | Count |
|---|---|---|
| `agent-ledger-api` (FastAPI, chat, webhooks, approvals UI) | Web | 1 |
| `mcp-<dept>` | Private Service | 10 (free-tier tip: one image with `DEPT=` env, or merge into one multi-mount MCP service while developing) |
| `agents-worker` | Background Worker | 1–3 (pooled by queue; split Finance out first) |
| `agent-ledger-workflows` | Workflow | 1 (holds W1–W7, W10) |
| `cron-recon`, `cron-close`, `cron-payrun`, `cron-reorder` | Cron Job | 4 |
| `ledger-db` | Postgres | 1 |
| `queue` | Key Value | 1 |

---

## 6. Totals
| Department | Agents | Skills | Tools |
|---|---|---|---|
| Finance | 6 | 29 | 39 |
| Sales & CRM | 5 | 18 | 25 |
| Procurement | 5 | 16 | 19 |
| Inventory & Warehouse | 5 | 15 | 17 |
| HR & Payroll | 5 | 17 | 19 |
| Customer Support | 5 | 17 | 23 |
| Manufacturing/Ops | 5 | 16 | 16 |
| Projects & Expenses | 4 | 13 | 13 |
| Analytics/Leadership | 5 | 16 | 16 |
| Platform/Admin | 6 | 20 | 25 |
| **Total (specialists)** | **51** | **177** | **212** (tool slots; ~200 unique) |
| + 10 lead agents | **61 agents** | | |

Unique PayPal-touching tools: about 45, across 9 PayPal APIs plus OAuth2. Workflows: 10.

---

## 7. Build order (Oct 18 → Nov 12, one person, about 26 days)
The plan is honest about depth: **"Fully deep"** applies to the design. The build gets 3 departments working for real, 3 shallow but working, and the rest stubbed.

| Phase | Dates | Deliverable | Exit test |
|---|---|---|---|
| P0 Skeleton | Oct 18–20 | repo restructure (map 6 files), `_template` plugin, Postgres schema (ledger, audit, a2a_tasks, money_intents), Render blueprint, Sarvam client | `render deploy` green; `test_ledger_balanced` passes |
| P1 Money rail | Oct 21–24 | `platform`: OAuth2, rail with idempotency + outbox, policy limits, approval inbox (FastAPI), audit hash chain, webhook verify + router | sandbox Payouts and Refund run end-to-end with approval |
| P2 A2A core | Oct 25–26 | `BaseLeadAgent`, agent cards, task states, orchestrator from `router.py`, chat from `chat.py` | chat → finance lead → specialist → `completed` |
| P3 Finance deep | Oct 27–Nov 1 | Treasury, Collections, CashApp, AP, R2R (Tax shallow); W9 recon cron; W10 payment run RW | demo: invoice → paid → applied → recon → payment run |
| P4 Sales + Support | Nov 2–5 | Orders v2 checkout + Invoicing; Refund + Disputes; W1 O2C, W7 refund/dispute | demo: order → capture → dispute → evidence → ledger |
| P5 Procurement + Inventory | Nov 6–8 | `procurement.py` split, GRN, 3-way match; W2 P2P, W8 reorder | reorder → PO → GRN → bill → payout |
| P6 HR thin + Analytics | Nov 9–10 | payroll calc (simple) + W4 Payouts batch; W5/W6 onboarding/laptop happy path; CFO brief + NL query | "Run payroll" in chat → approvals → Payouts |
| P7 Polish | Nov 11–12 | stub Mfg/Projects (cards + 2 tools each), plugin store UI, demo video, README, submission | submit by **Nov 12, 18:00 IST** (buffer before the stated deadline) |

**Target real implementation by Nov 12**: about 28 specialist agents, about 70 skills, about 110 tools working. The rest exist as manifests, agent cards and stubs that return `NotImplemented`, shown in the plugin store as "coming soon".

## 8. Scope risks (honest)
| Risk | Impact | Mitigation |
|---|---|---|
| 61 agents / 212 tools is far more than one person can build in 26 days | high | Implement Finance, Sales, Support and Platform deep; generate the rest from templates; demo only 3 workflows live (W1, W7, W10) and keep W9 as cron |
| 10 Private Services + workers + workflows cost a lot and are slow to deploy | med | One MCP image switched by `DEPT` env; merge MCP servers locally; split only for the demo |
| Render Workflows API is newer; SDK changes possible | med | Keep workflow steps as plain idempotent functions with a WT fallback runner over Key Value |
| Sarvam tool-calling reliability with large tool sets | high | ≤ 8 tools per specialist; deterministic code for money and recon; LLM only plans and fills args; schema validation + retry |
| PayPal sandbox quirks: disputes are hard to create on demand, Transaction Search lag (hours) | med | Seed disputes via sandbox buyer accounts early (P1); recon uses a 27h window; record fixtures for tests |
| Payroll/GST correctness | med | Label as simplified demo rules; not compliance-grade |
| A2A spec version drift | low | Pin the SDK version; contract tests on agent cards |
| Security of money paths | high | Credentials only on the rail service; per-plugin permissions enforced at the rail; approval UI with SoD; audit chain verify in the demo |
