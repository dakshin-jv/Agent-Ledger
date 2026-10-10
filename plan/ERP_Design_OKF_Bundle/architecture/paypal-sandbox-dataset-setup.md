---
type: Design Specification
title: PayPal Sandbox account, balance and transaction design
description: PayPal Sandbox account, balance and transaction design
status: draft
generated:
  by: codex/gpt-6
  at: '2026-10-07T17:20:00+00:00'
sources:
- id: session
  resource: 'User design decisions, 7 October 2026: goods only, demo data, TypeSafe,
    human review, undo and design-only delivery'
- id: accounts
  resource: https://developer.paypal.com/sandbox-testing/accounts
- id: balances
  resource: https://developer.paypal.com/api/transaction-search/v1/balances-get/
- id: payments
  resource: https://developer.paypal.com/api/payments/v2
- id: reporting
  resource: https://developer.paypal.com/api/transaction-search/v1
bundle_revision: 0.5.0
design_progress: specified-awaiting-review
implementation_status: not-started
---

# Scope and evidence

PayPal Sandbox is required by the user. This document defines intended accounts, records and setup checks; no accounts, apps, tools or payments are configured. Sandbox means test funds and test transactions, not production Treasury. Balance visibility for our particular account/app remains unverified.

Official sources reviewed 7 October 2026 list a reporting balances API, transaction search, payment authorization/capture/void/refund operations and sandbox account setup. Operation documentation is not proof that an app has access. Verify app scopes and account eligibility per operation. Toolkit/MCP operation availability also requires separate inventory checks.

# Proposed account topology — confirmation before implementation

Use a controlled sandbox merchant representing the fictional goods supplier, and a separate sandbox buyer representing the demonstration requester. A personal sandbox buyer can demonstrate Checkout; it is not an assertion that enterprise AP pays suppliers from the merchant app. The credentials used for reporting observe the authorised account associated with that app, not arbitrary buyers or every supplier.

Decide before implementation whether the demonstration is buyer-approved merchant Checkout or another explicitly supported supplier-payment flow. Orders/Payments integration is a proposed first demo route; Payouts, arbitrary vendor transfers and balance-only funding are not assumed. Channel3 sellers are discovery sources, not sandbox recipients. Map only our controlled demo merchant to a fixture supplier, with conspicuous disclosure. Country, supported currency and funding sources are configuration choices still pending. Do not assume UAE/India locale/account compatibility.

# Setup specification

| Setup object | Configuration to record without secrets | Later verification / recovery |
|---|---|---|
| Sandbox accounts | Internal account reference, role (buyer/merchant), country, currency, fake-fund setup, owner, account ID after creation | Distinct test accounts; correct login environment; disable mapping rather than delete historical IDs |
| REST app | App alias, owning merchant reference, sandbox environment, credential secret references, granted capabilities | OAuth and capability probes; rotate credentials without losing transaction history |
| API boundary | Sandbox base `https://api-m.sandbox.paypal.com`; approved operation allowlist | Reject live endpoint/credential mix; no live fallback |
| Balance reporting | `GET /v1/reporting/balances`; optional currency/as-of filters; `reporting/balances/read` scope | Authorised merchant response or explicit unavailable/forbidden result |
| Payment journey | Explicit buyer consent, order/authorization/capture model, amount/currency/payee, internal invoice reference | Sandbox approval is separate from ERP approval; authenticate and bind exact transaction |
| Events/status | Configured webhook IDs and verification method, resource queries, event deduplication | Forged/duplicate/out-of-order events do not create false completion |
| Recovery operations | Supported authorization void and capture refund; amount limits and approver | Inspect provider state first; verify result; retain both original and recovery IDs |
| Reporting/reconciliation | Account/currency/time window, refresh policy, payment/fee/refund mappings | Reporting delay visible; missing provider entries are unresolved, not fabricated |

Secrets reside in provider/backend secret storage, never dataset fixtures or AI context. Record secret names/owners/rotation procedure, not values. Missing permissions remain blocked/unavailable until resolved.

# Dataset field specifications

| Dataset | Fields | Meaning and constraints |
|---|---|---|
| Account mapping | Tenant/entity, internal account ref, provider account ID, sandbox flag, merchant/buyer role, app ref, currency capabilities, fixture supplier link | Explicit mapping; merchant ID/account ID types stay distinct; no universal buyer visibility |
| Capability results | Operation, account/app, scope, checked time, supported/denied/unverified, provider error and evidence ref | Never infer balance or refund access from successful Checkout |
| Balance snapshot | Account, currency, total/available/withheld balance, provider `as_of_time`, `last_refresh_time`, retrieved time, source ref, availability state | Decimal money; dated observation; preserve provider components; never overwrite with fixture balance |
| Payment instruction | Internal invoice/order reference, amount/currency, payee mapping, ERP approval/version/digest, action key, intended operation | No execution without matching authority; separate from PayPal order |
| Provider payment resources | Provider order ID, authorization ID, capture ID, resource status, amounts, timestamps, source response ref | Distinct typed IDs; retain provider status alongside internal normalized state |
| Webhook inbox | Event ID/type, resource ID, verified status, received time, payload ref, processing outcome | Process verified events idempotently; restricted raw payload retention |
| Refund/void request | Original resource ID, amount/currency where relevant, reason, approval, action key, provider recovery ID/status | Original cannot be erased; partial/full amounts constrained to eligible remainder |
| Reconciliation finding | Invoice/payment/resource link, gross/fee/net/refund data where supplied, period, discrepancy, evidence, owner/disposition | Payment completion does not prove invoice match or receipt; no assumed real-time balance delta |

# Balance boundaries

PayPal documents up to three hours before balances appear in its list-balances call. Display account, currency, as-of/refresh/retrieval times and availability. Refresh does not imply a newly settled balance. Do not invent a universal stale cutoff; configure the demo display threshold separately from provider latency.

Budget is fixture spending authority; PayPal balance is an observed test account balance. A merchant reporting balance is not the buyer's procurement funding. Available funds do not guarantee transaction success; funding sources, provider restrictions and payment state matter. Multi-currency balances stay separate. If reporting access fails, show unavailable with reason and last snapshot clearly marked; manual sandbox observation, if used, has its own source/time and is not misrepresented as an API read.

# Proposed scenario definitions — no test execution

| Scenario | Planned stimulus | Expected outcome / recovery |
|---|---|---|
| P01 permitted balance | Read enabled merchant balance | Sandbox snapshot, account/currency/time visible |
| P02 denied balance | App lacks scope/access | Unavailable; no invented balance or approval |
| P03 reporting lag | Capture followed by early report | Payment state verified independently; dated balance remains separate |
| P04 buyer approved payment | Matching ERP authorization and sandbox buyer consent | Resource IDs recorded; provider completion reconciled |
| P05 buyer declines | Sandbox approval cancelled | No capture claim; request can return to review |
| P06 unknown outcome | Timeout after mutating call | Unknown state; query/reconcile before safe retry using operation's documented idempotency |
| P07 duplicate dispatch/event | Repeated command/webhook | One business effect; duplicates journalled |
| P08 void | Eligible uncaptured authorization | Approval plus verified provider void; failed eligibility escalates |
| P09 refund | Eligible completed capture | Separate approved refund, verified provider result; no claim original transaction vanished |
| P10 partial refund | Configured eligible remaining amount | Remaining refundable amount checked; over-refund rejected |
| P11 stale approval | Changed amount/payee/currency | Block execution; require new review |
| P12 mismatch | Provider amount/account/currency differs | Reconciliation hold; owner investigates |
| P13 invalid webhook | Unverified event | No business state advancement |
| P14 insufficient-funds narrative | Provider-supported negative test if available | Verify actual documented failure mechanism; otherwise label simulated backend failure, never a real PayPal result |

# Future acceptance evidence

For every implemented case retain account/app alias, sandbox flag, operation, request correlation, redacted resource result, expected/actual outcome, actor, timestamps and recovery verification. Distinguish designed, configured, tested-pass, tested-fail and unsupported. Do not manufacture resource IDs or claim toolkit coverage. Recheck current API idempotency support and retention before relying on retry headers. Production payment, supplier settlement, full Treasury, tax and accounting policy remain out of this setup scope.
