# Edge cases — open questions

Single **procurement agent** and its edge cases only (intake/spec, sourcing, PO, GR, IR, pay). Leave existing headings in place. Other agents and combinations are later. Do not discuss them here.

Add a heading per capability/agent. Against each pointer, one question only. No handling notes here.

User types are parked. This file is **procurement-agent logic and functions** only. User / analyst / business owner below are **gates on the case**, not personas to design for.

## RBAC

Parked with user types.

How does the same person — or two people of the same user type — exercise requester, business-owner, and funding-owner gates on one case?

- [ ] Requester = business owner
- [ ] Business owner = funding owner
- [ ] Same person on all three
- [ ] Two users, same type; only one is assigned
- [ ] Policy forbids a pair (e.g. requester cannot fund)

## Procurement agent

### User

- [ ] G01 clean intake — After spec and funding, what does the agent hand to sourcing?
- [ ] G02 missing fields — Stay draft, or block submit?
- [ ] G03 unit ambiguity — Does the agent wait on the user to resolve pack vs each?
- [ ] G04 duplicate — Flag only, or wait for merge/withdraw?
- [ ] G09 funding unresolved — Does the agent hold the case (not skip the gate)?
- [ ] G11 model invalid/outage — Manual correction only — no inferred spec?
- [ ] Vague / missing spec measure — Ask the user and keep the draft?
- [ ] G13 withdraw vs approve race — Which transition wins?

### Analyst

- [ ] G05 stock sufficient — Reuse, still buy, or split — what does the agent propose vs wait on?
- [ ] G06 contract covered — Recommend the contract, or stop external sourcing?
- [ ] G07 contract expired — Treat as no coverage?
- [ ] G08 policy unavailable — Block, or allow an exception path?
- [ ] G10 discovery outage — Continue with Channel3 skipped?
- [ ] G14 restart / duplicate dispatch — One handoff, surviving review?

### Business owner

- [ ] Conflicting requirements — Block those rows until the owner resolves?
- [ ] G12 authority / stale approval — Reject and require a current review?
- [ ] Non-owner acting — Work item to the assigned owner, no proxy?
- [ ] G15 recall with dependents — Pause downstream until the owner reviews?
- [ ] Recall after sourcing started — Pause and compensate, not delete?
- [ ] G16 evidence isolation — Deny, with no cross-tenant leak?

## Sourcing

Same case. Approved spec and still-valid funding in. Channel3 is a tool. One question per pointer.

### User

- [ ] Need / qty / date changes while sourcing — Pause sourcing and return to intake/spec?
- [ ] User favours a listing — Candidate only, or does it rewrite the spec?

### Analyst

- [ ] No feasible candidate — Explain and wait; no invented supplier?
- [ ] Stale price / availability — Recheck; no commit on stale data?
- [ ] Unknown delivery — Block commit, or pass unknown to the owner?
- [ ] Live contract vs Channel3 — Contract first; listing is never a supplier?
- [ ] Search failure — Continue without external options (same as G10)?

### Business owner

- [ ] Candidate conflicts with approved spec — Return to spec; no silent overwrite?
- [ ] Sourcing timeout — Hold the case; do not retry as a purchase?
- [ ] Spec-matching recommendation — Owner accepts; analyst proposes; listing click does not commit?

## PO

Same case. Spec accepted, funding still valid, source accepted. PO is a record on the case, not payment. One question per pointer.

### User

- [ ] Favoured listing — Can the user post a PO from it?
- [ ] Need changes on a draft PO (not sent) — Return to spec/sourcing?

### Analyst

- [ ] Draft/post PO — Only from owner-accepted source plus still-valid funding?
- [ ] Withdraw vs send — Unused send cancelled; already sent becomes recall/amend?
- [ ] Duplicate send / retry — One PO, not two?

### Business owner

- [ ] Owner-accept of source — Does that already mean the PO is sent?
- [ ] Material PO change after accept — New owner review on current version?

## GR

Same case. PO sent. Goods receipt is a record on the case, not payment and not a second agent run. One question per pointer.

### User

- [ ] User says goods arrived — Is that a receipt record, or only a note until recorded against the PO?
- [ ] Partial arrival — Keep the case open for the rest, or close the PO?

### Analyst

- [ ] Qty mismatch vs PO — Record discrepancy; do not silently rewrite the PO?
- [ ] Quality fail — Block accept-into-stock; hold the case?
- [ ] Duplicate / retry receipt — One GR effect, not two?

### Business owner

- [ ] Over-receipt or quality fail — Owner disposition (accept / return / split) before AP?
- [ ] Receipt without a sent PO — Refuse; do not create a backdated PO?

## IR

Same case. AP attaches here; it does not own the case. Invoice vs PO vs GR. Invoice accept is not payment. One question per pointer.

### User

- [ ] Supplier bill in hand — Is that the invoice record, or only evidence until matched?
- [ ] User “OK to pay” — Does that post the invoice or release cash?

### Analyst

- [ ] 3-way match (invoice vs PO vs GR) — Block if unmatched; no silent rewrite of PO/GR?
- [ ] Invoice before GR — Hold (goods need receipt), or allow 2-way?
- [ ] Duplicate invoice — One invoice effect, not two?
- [ ] Price/qty variance — Within policy tolerance vs owner/funding review?

### Business owner

- [ ] Match fail / over-tolerance — Owner disposition; do not auto-post?
- [ ] Invoice accepted — Does that already pay the supplier?

## Pay

Same case. Cash out is a separate gate from spec, sourcing, PO, GR, and IR. Authorised rail only. One question per pointer.

### User

- [ ] Channel3 listing / “pay this shop” — Can the user release cash?
- [ ] User “OK to pay” after IR — Does that execute payment?

### Analyst

- [ ] Pay without accepted IR + still-valid funding — Hold?
- [ ] Channel3 retailer as payee — Refuse (listing is not a payee)?
- [ ] Duplicate pay / retry — One payment effect?
- [ ] Provider timeout / unknown outcome — Reconcile first; do not pay again?

### Business owner

- [ ] IR accept or owner “looks good” — Does that release cash?
- [ ] Payment failure — Compensate/retry only after known status; case not deleted?

## Recovery

Same agent, same case. After a step has started or committed. One question per pointer.

### User

- [ ] User cancels before PO sent — Stop forward work; keep history?
- [ ] User cancels after PO sent — Recall/amend, not delete?

### Analyst

- [ ] Concurrent edit vs agent run — Recheck current version; no write on stale?
- [ ] Rejection at any gate — Stop that path; case remains, not a new silent run?
- [ ] Partial completion (some lines received/paid) — Continue the rest; no all-or-nothing wipe?

### Business owner

- [ ] Funding revoked after a later step — Block further commit; compensate what already posted?
- [ ] Owner rejects after agent drafted — Draft discarded/superseded; no auto-retry as commit?

## UI design

Out of scope for now. Do not design screens here.

- [ ] How does the UI customise for role types?
- [ ] Same case: which actions are visible to user vs analyst vs business owner?
- [ ] Work: one queue filtered by assignment, or a different layout per role type?
- [ ] When one person holds two gates, does the UI show two decisions or one screen?
