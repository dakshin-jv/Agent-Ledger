---
type: Reference
title: 2025 ERP application revenue ranking
description: Apps Run The World top 10 and which vendors are real AgentLedger peers.
tags:
- erp
- competitive
- foundation
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: artw
  resource: https://www.appsruntheworld.com/top-10-erp-software-vendors-and-market-forecast/
  title: Top 10 ERP Software Vendors, Market Size and Forecast 2025-2030
design_progress: documented
implementation_status: not-evidenced
bundle_revision: 0.1.0
---

# Ranking used

| Rank | Vendor | 2025 share | Flagship counted by ARTW | Treat as |
| --- | --- | --- | --- | --- |
| 1 | Oracle | 6.7% | Fusion Cloud ERP, NetSuite | Peer |
| 2 | SAP | 6.6% | S/4HANA, Business One, ByDesign | Peer |
| 3 | Intuit | 4.5% | QuickBooks Online, Enterprise Suite | Finance ERP-lite |
| 4 | CSI | 4.0% | Harris, Jonas, Volaris, Topicus | VMS holding co. |
| 5 | Microsoft | 2.2% | Dynamics 365 Finance/SCM, Business Central | Peer |
| 6 | FIS | 2.0% | Core banking, GETPAID, Integrated Payables | Bank / treasury rail |
| 7 | Roper | 2.0% | Deltek Costpoint, Aderant Expert, Vertafore AMS360 | Vertical SoR roll-up |
| 8 | Sage | 1.7% | Intacct, X3 | Finance + mid ERP |
| 9 | Infor | 1.3% | CloudSuite LN / M3 / SyteLine | Goods ERP peer |
| 10 | Workday | 1.0% | Workday Financial Management | HCM + FM + spend |

Gartner’s 2025 worldwide ERP share note says leaders were unchanged; the vendor table is not public in snippets. “Leading ERP” product lists often swap CSI/FIS/Roper for IFS, Epicor, Acumatica, Odoo.

# Peer rule

Score **Oracle, SAP, Microsoft, Infor** as goods/finance ERP UX competitors. Score **Workday, Sage, Intuit** as adjacent finance/spend. Score **CSI, FIS, Roper** as ranking artifacts unless a named holding (K2B, Deltek, GETPAID) is in scope.
