---
name: adversarial-review
description: Audit a requested plan, proposal, architecture, instruction system, or agent workflow for concrete failure modes.
---

# Adversarial review

Review the requested decision or artifact against its intended outcome. Use native
code review for routine diffs. This skill supplies focused critical judgment;
it does not add a standing commit or publication gate.

Establish the review boundary from the request and existing checkpoint. Inspect
recoverable source before asking for missing context. State unavailable evidence
and limit conclusions to what can be inspected.

Reconstruct success, necessary assumptions, and the concrete case most likely to
break them. Examine ownership, duplicated authority, hidden coupling, failure and
recovery, evidence quality, operating cost, and the user's ability to understand
consequential behavior. Choose relevant surfaces rather than a fixed checklist.
Trace changed contracts through producers, consumers, and non-code references.
For changes to responsibility, state, or acceptance boundaries, use the relevant
[architectural questions](references/architecture.md).

Verify a suspected defect when a cheap source read or safe check can decide it.
Separate observed facts from inference. A passing test establishes only what it
exercises; a plausible concern is not a finding without a supported failure path.
Prefer correcting the owning premise over adding compensating process.

For a consequential change that requires independence, use one scoped independent
reviewer under the host's delegation rules. If unavailable, report that limit.
Reuse that reviewer for repair deltas, affected consumers, unresolved findings,
and invalidated evidence. Expand only for a concrete dependency or expertise gap.
Do not create a reviewer panel or fixed number of passes.

Report findings in consequence order with evidence anchors, failure scenario,
required correction, and remaining uncertainty. State the reviewed revision or
scoped diff, verification performed, and material exclusions. If no meaningful
defect is found, say so without treating missing evidence as acceptance.
