---
name: solve-novel-software
description: Resolve consequential technical uncertainty with a small falsifying experiment and an independent correctness oracle.
---

# Solve novel software problems

Turn a technical uncertainty into evidence that supports an implementation
decision. This procedure complements the project's implementation workflow.
It does not require a new planning process for routine changes.

Before research or a probe, name the decision it could change. Prefer the
smallest reversible check of the assumption most likely to invalidate useful
work. Preserve the host's resource, authorization, and review boundaries.

## Find the decision that matters

Identify the requested behavior and the constraint most likely to invalidate
the design. Distinguish a missing product decision from a technical question
that local inspection or an experiment can answer. Do useful independent work
while a product decision is pending.

Trace one representative input through the affected boundaries to its observable
result. Include state ownership, external dependencies, and the recovery path
where they affect the decision. Read the installed implementation and exact
dependency versions before relying on a remembered API.

Keep a short record of the active uncertainties in the project's existing task
notes. Use a local task artifact when the project has no suitable location.
For each uncertainty that changes the design, record:

- The claim and the decision that depends on it.
- The evidence already available and its limits.
- An observation that would contradict the claim.
- The smallest authorized check that can distinguish the plausible alternatives.

Rank uncertainties by the cost of being wrong, the amount of dependent work,
and the cost of obtaining useful evidence. Investigate the highest-impact
uncertainty that is practical to resolve. Do not use invented numerical scores
to make a qualitative judgment appear measured.

## Make an experiment change a decision

Compare the current approach with the strongest plausible simpler alternative.
For each, identify the assumption on which it depends. Before running a probe,
state what result would support, reject, or leave the assumption unresolved.
Choose the result threshold from the user's requirement or an existing contract.
If no threshold exists, characterize the behavior without claiming acceptance.

Use the actual runtime or boundary relevant to the question. A mock can check
the caller's behavior; it cannot establish an external system's semantics.
Bound the probe to the inputs, side effects, resources, and cleanup needed for
this decision. Use existing scratch conventions, and keep experimental code
out of production paths. Follow the applicable test and authorization rules.

Choose a correctness oracle before trusting the candidate. An oracle is an
independent basis for deciding whether a result is correct. When no trusted
expected output exists, read [references/oracles.md](references/oracles.md).

Capture the command or observation method, environment, relevant source state,
input, result, and limit of the inference. Include uncommitted changes when
identifying the source state; a commit identifier alone can be insufficient.
Keep credentials and private payloads out of task notes.

After a probe, update the decision. If the result is inconclusive, name the
remaining ambiguity and change the experiment accordingly. Stop a research
branch when further evidence would not change the implementation choice.
If the decisive experiment is unavailable, isolate the uncertain dependency
behind a reversible boundary and report the unverified assumption. Do not
substitute a fabricated success for missing evidence.

## Transfer findings into production

Record which contract the experiment supports, the conditions under which it
holds, and what would invalidate the finding. Carry those conditions into the
implementation plan. A successful experiment supports only the behavior and
environment it exercised.

Build the smallest usable path through the real components before expanding
the implementation. Check the boundary with the greatest uncertainty as soon
as that path can reach it. For parallel work, settle the shared contract first:
inputs, outputs, state ownership, error behavior, and who may change it. Follow
the existing delegation and independent-review rules.

Keep the experimental shortcut separate from the production decision. Use the
project's normal error handling, resource ownership, cancellation, and recovery
conventions where they apply. Inspect consumers when changing a contract; local
success does not establish compatibility for other callers.

Select verification from the actual failure modes. Use existing checks first.
Add durable tests only when the governing test and change-discipline rules permit
them. A one-time probe can answer a question without adding a permanent guard.
After the final relevant edit, verify the integrated behavior against the
original acceptance conditions and obtain required independent review.

Keep the decision, evidence, unverified assumptions, checked state, and next
action in the existing task record. Report feasibility separately from an
integrated implementation that passed its acceptance conditions.

The research basis and limits are in
[references/evidence.md](references/evidence.md). Read it when revising this
procedure or evaluating its claims, not on every implementation task.
