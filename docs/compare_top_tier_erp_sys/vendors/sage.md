---
type: Competitive Inference
title: Sage Intacct, X3, and 200
description: ARTW #8. Copilot overlay; Intacct close and AP first; X3 sales Copilot; 200 without Copilot.
tags:
- erp
- competitive
- sage
status: draft
generated:
  by: cursor/grok
  at: '2026-10-10T16:00:00+00:00'
sources:
- id: copilot-pr
  resource: https://www.sage.com/en-us/news/press-releases/2026/04/sage-expands-ai-agents-across-finance-hr-and-operations-to-automate-workflows/
  title: Sage expands AI agents April 2026
- id: close
  resource: https://www.intacct.com/ia/docs/en_US/help_action/Copilot/Close_workspace/about-close-workspace.htm
  title: Close Workspace
- id: x3
  resource: https://www.sage.com/en-us/news/press-releases/2025/06/sage-copilot-comes-to-sage-x3-powering-high-performance/
  title: Sage Copilot on X3
design_progress: researched
implementation_status: not-evidenced
bundle_revision: 0.1.0
confidence: high-on-GA-lists
---

# Treat as

**Finance + mid ERP.** Usual ERP + governed Copilot overlay — the pattern AgentLedger is designed against.

# AI surface

| Product | Copilot | Note |
| --- | --- | --- |
| Intacct | Panel + named agents | Close Automation **GA**. Finance Intelligence Agent **early adopter**. AP automation / PO match **GA**. Copilot **production only, not sandbox**. |
| X3 | Copilot GA global (2025); Sales Intelligence Agent GA; AP capture GA; Supply Chain Intelligence **EA US** | Chat sales-limited; procurement/inventory Copilot **future** (Jun 2025 launch copy). |
| Sage 200 | **Absent** from Apr 2026 official Copilot SKU list | Traditional modules only. Do not confuse with Sage 50 Copilot. |

Glass box: log recommend vs approve vs who. Partner marketplace agents need FIA + AWS Marketplace.

# Score

| Criterion | Score | Why |
| --- | --- | --- |
| C1 Intent first | Different | Copilot on Purchasing/AP/GL/Close. |
| C2 One case | Different | Close Workspace is the close process, not order→pay. |
| C3 Agent drafts | Partial | Strong on bills/close/time; not commercial case draft. |
| C4 Named owner | Partial | Role + Close assignees; not case version owner. |
| C5 Funding gate | Different | AP/treasury workflow. |
| C6 Chat ≠ books | Match | Overlay; humans post. |
| C7 Views | Partial | Close Workspace only. |
| C8 Isolated agents | Partial | Functional isolation (Close vs FIA vs AP), not case isolation. |
| C9 Recovery | Partial | Draft-then-post; GL outliers return to submitter. |
| C10 Goods P2P | Different | Opposite order: close/AP/sales first. |

# Steal / hold

Steal: glass-box logs; agents as subscriptions; Close as a process hub; AP capture→match→draft→human post. Hold: intent → one case; owner version; funding gate; six views; goods P2P first. Watch X3 procurement Copilot.
