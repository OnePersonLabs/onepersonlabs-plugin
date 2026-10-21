---
name: unslop
description: Trace a specific agent failure to its cause and compare corrective instructions through explicit session replay.
---

# Unslop

Investigate one identified agent failure. A correction, apology, or acknowledgment
is not by itself evidence of a failure or a trigger for replay. Resolve ambiguity
about the incident before anchoring the analysis to it.

## Recover the causal chain

Record what happened, what should have happened, and the affected scope. Inspect
the source session and relevant implementation. Separate the observable symptom,
the general failure pattern, and any enabling instruction or configuration.
Quote a causal instruction with its source; do not assume every failure has an
instruction vulnerability.

Reconstruct what was available at the decision point, what action followed,
which relevant evidence was missed, and why the decision process missed it.
Treat reconstructed reasoning as inference unless the transcript establishes it.
Consider competing causes and benign counterexamples. Do not treat confidence,
agreement, or a convenient narrative as proof.

Prefer correcting the responsible instruction or implementation over adding a
counterweight. Preserve concurrent and unrelated work. Code ownership does not
forbid an authorized causal fix to untouched code; inspect its contracts and
callers before changing it. Follow the host's change and permission boundaries.

## Choose analysis or replay

A causal analysis can stand without replay. Label a proposed rule **reasoned,
not replay-tested** when interactive replay is unavailable, unreproducible, or
not authorized. Do not infer broad validation from one successful trial.

When explicit replay is authorized and can decide a material uncertainty, read
[interactive replay](references/replay.md). It preserves Codex and Claude session
routing, forging, native Windows and POSIX commands, comparison evidence, and
synthetic-session cleanup. Follow the host's AI permission and batching rules.
A request for analysis alone does not authorize token-consuming replay.

Keep a self-contained trace at `.unslop/replay/<timestamp>-<incident-slug>.md`
when a trace is requested or needed for the investigation. Preserve existing
traces. Record source anchors, observations, inferred causes, counterevidence,
proposed correction, and verification limits. Keep replay trials distinct from
the original session and preserve them while comparison is in progress.

Report the causal finding, proposed intervention, evidence, and remaining
uncertainty. State whether the change is implemented or proposed and whether
it was reasoned or replay-tested. Obtain approval for an instruction change
when it is outside the authorized task; do not turn a replay result into new
standing authority.
