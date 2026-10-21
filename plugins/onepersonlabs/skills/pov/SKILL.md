---
name: pov
description: Form a source-grounded position on a supplied decision, document direction, or set of approaches. Use when the user asks what we should choose, adopt, change, or believe, or when a consequential unresolved decision determines active work. Use develop-alternatives when a defined choice needs real competing designs first; use research-solutions for current implementation evidence.
---

# Form a grounded position

Answer a decision with a position the project can use. First establish the exact
question and consequence. Then verify the evidence that could change the answer,
weigh the strongest alternatives, and return the position with its reasons and
reversal conditions. Use the existing project's decisions and evidence; do not
create another decision ledger.

This skill is selected by the agent when the user's request asks for a judgment,
or when dependent work hinges on an unsettled consequential choice. A routine
choice with clear project precedent does not need a POV. A request to understand
behavior goes to `build-understanding` or `debug`; an explicit audit goes to
`adversarial-review`; external implementation research goes to
`research-solutions`. A decision with a concrete brief but undeveloped competing
mechanisms goes to `develop-alternatives`, which returns here to judge the result.

## Frame the decision

Resolve the subject and the decision from the request and active work. Classify it
as adoption or replacement, a position on supplied approaches, or a holistic take
on a document. Keep a factual explanation separate from a judgment. Infer the
consequence of being wrong from the affected data, interfaces, commitments, and
reversibility. Use that consequence to scale the evidence work.

If two plausible readings would change the recommendation, state the missing
distinction and ask the root to resolve it. Do useful evidence gathering first.
Do not spend research on an invented question. When the choice requires unknown
requirements, return that dependency to the existing product owner rather than
pretend to decide it.

## Ground the position

For the project side, verify a concrete incumbent and relevant code, configuration,
issue, decision, or documented constraint. For a new capability, verify where it
would enter and which local contracts it must satisfy. For an external adoption,
also verify the outside claims that make the recommendation viable. These are
separate evidence requirements: strong outside evidence cannot establish local
fit, and local fit cannot establish an external capability.

Read relevant accepted Conceptor meaning and current project decisions when the
project uses them. Check that they still apply. Inspect authoritative source for
any claim borrowed from conversation, prior work, or an agent. Conversation gives
useful hypotheses; it does not establish a project fact. Search for disconfirming
evidence before relying on a premise that raises the recommended commitment.

For current adoption or replacement, route through `$onepersonlabs:research-solutions`
for current implementations, integration, maintenance, and recovery evidence. A
clear, locally answerable question needs no broad survey. If the needed source
cannot be verified, hold the position and say exactly what evidence would change
that. Read [project knowledge](../agent-instructions/references/project-knowledge.md)
when a rule or local convention could govern the decision; cite any rule that shaped the result.

## Choose and explain

Consider keeping the incumbent and doing nothing. Compare actual alternatives on
the requirement that determines this decision, not a generic scorecard. Preserve
important downside, unknowns, and who bears the cost. Use these positions for a
bounded adoption decision:

- **Adopt** when project fit and required evidence support using the candidate.
- **Trial** when a reversible, scoped use can settle a consequential unknown.
- **Hold** when a named prerequisite or evidence gap must be resolved first.
- **Reject** when the verified mismatch outweighs the benefit for this project.
- **Not our problem** when a specific exposure does not reach this project.

For an approach set, choose a supported option or say that the remaining options
are both viable. For a document, state its direction, strengths, and risks instead
of turning the answer into line-by-line findings. If the evidence cannot support
a position, return a clear hold or blocker, not a confident guess.

Lead with the position. Include the question, project facts, decisive outside facts
when relevant, material alternatives, uncertainty, and what would reverse the
position. Cite source paths and sections so the next worker can check them. Make
the reasoning compact for a simple reversible choice and fuller for an expensive
or hard-to-reverse commitment.

## Independence and completion

First form a position from verified evidence. When the user asks for other views,
use only a currently available, authorized independent reviewer. Give that reviewer the same question, project sources, and constraints without
your initial verdict. Treat concurrence as a useful cross-check, never a vote or proof. If positions
differ on a decision-changing fact, verify that fact at its source and share the
same evidence with each surviving reviewer before reconciling. Report unresolved
disagreement or unavailable review plainly. Do not install another model route or
send project material to a new recipient to satisfy this procedure.

The position is a decision artifact, not permission to implement, publish, or
change project meaning. Return it to the current workflow owner. If implementation
continues, carry its sources, open conditions, and position into that owner's
existing plan or checkpoint. Stop when that consumer has enough information to
act or state the specific missing dependency.
