---
name: optimize-workflow
description: Improve agent workflow when speed, elapsed time, cost, or rework is a concern. Account for preparation, execution, verification, coordination, and repair; change the next work batch while preserving scope and correctness.
---

# Optimize the execution workflow

Use this workflow at the first concern about agent speed, elapsed time, cost, or
repeated work, or when repeated preparation, repair, or coordination materially
delays completion. Reassess before the next costly step. Keep the intervention
proportionate; a neutral ETA question does not require an extensive audit.

Preserve the requested outcome, accepted constraints, current work, and required
checks. This skill changes execution order and work allocation; it does not grant
permission for new services, optional broader model evaluations, publication, or
reduced scope. Task-specific AI verification follows the shared policy in the
plugin `AGENTS.md`.

## Account for the work

Use the existing conversation, timestamps, tool results, and work record. Separate
preparation, implementation, verification, coordination, rework, and waiting when
the distinction changes the next action. Distinguish command runtime from the
time spent preparing its inputs and recovering failed launches. Mark unknown
intervals; do not infer precise durations or token costs from narrative. Parallel
activity overlaps, so its durations do not sum to elapsed time.

Keep the account in the conversation or existing work owner. Use a short table
when useful. Do not create an accounting ledger, telemetry, or a transcript archive.
Finish this step with a supported account of the main cost and its uncertainty.

## Find the avoidable cost

When worker selection, context transfer, cache assumptions, duplicate investigation
or repeated worker corrections contribute to the cost, read
[subagent guidance](../configure-harness/references/subagents.md). Compare complete
successful work, including parent input, briefs, child input and output, review,
repairs and integration. Select model and effort for the next task; choose context
separately. Neither the parent's model nor a cache percentage selects the winner.

Inspect the remaining dependencies and reuse established decisions and valid
evidence. Identify whether repeated setup, partial migrations, changing contracts,
serial coordination, or redundant verification is delaying completion. Distinguish
necessary investigation from work that will be invalidated by a known next step.
Treat harness startup failures separately from product failures.

Finding counts are not counts of independent design jobs. Base estimates on
comparable completed work, the remaining responsibilities, and unresolved
dependencies. If those facts are insufficient, state what remains unknown.
Identify the bottleneck and the next process change before adding more machinery.

## Choose a complete, bounded batch

Choose a coherent responsibility and settle the interfaces that dependent work
needs. Do not turn batching into an unbounded repository rewrite. Resolve a
decisive uncertainty with a focused check before committing dependent effort.

For structural migrations, establish one complete old-to-new path and symbol map.
Include imports, exports, runtime loading, embedded tool code, build entries,
documentation inventories, and selector patterns. Account for moved consumers as
well as moved targets. Prefer installed semantic tooling where it supports the
transformation; inspect unsupported and computed forms explicitly. Reject
ambiguous or overlapping edits rather than guessing. Inspect the scoped diff and
check for missed consumers. When the transformation supports a dry run, repeat it
to check that no edits remain; otherwise inspect the affected consumers directly.

Move mechanical test references with their source. Stabilize changed interfaces
before adapting semantic fixtures. Run an early reproduction or diagnostic check
only when its result can change the next decision. Keep test-first development
for an explicit user choice. Otherwise batch necessary validation after the
affected implementation is complete, before delivery.

Apply scoped automatic fixes and formatting before final type and lint checks.
A tool's safe-fix classification does not prove compiler compatibility or correct
behavior. Check the complete changed consumer set, including tools outside the
main compiler project through their applicable checks.

## Coordinate and verify

Keep tightly coupled work with one owner. Delegate only when independent work or
judgment exceeds setup and integration cost. Settle shared contracts, assign
disjoint write ownership, reuse workers, and confirm that assignments started.
Use the host's current tool contracts for starting, resuming, and waiting on work.

After writers stop changing the reviewed scope, overlap independent review and
final verification when useful. Select the minimum checks covering changed
behavior, connected consumers and required gates. Reuse valid results across
workers and stages; rerun only invalidated checks or a newly identified gap.
After verification, make targeted repairs rather than running broad mutating
fixers. Check command success before a dependent mutation or completion claim.
Follow the existing two-failed-repair reassessment rule when progress stops.

## Resume and assess

Report the supported bottleneck, the revised next batch and ownership, preserved
guarantees, and required checks. State what the next meaningful boundary will
reveal about the change, then resume authorized work. Do not require another
approval for an execution adjustment already within scope.

At that boundary, compare the observed preparation, execution, coordination, and
rework with the earlier account. Do not claim a measured speedup from incomparable
tasks or command timings alone. Use [$onepersonlabs:optimize](../optimize/SKILL.md)
when choosing a winner requires a controlled performance comparison. Use
[$onepersonlabs:research-solutions](../research-solutions/SKILL.md) only when the
remedy introduces a consequential tool or integration decision.

Use existing evidence to select a useful execution change and resume authorized
work. Stop investigating when the expected value of another finding no longer
justifies its cost. Do not replay expensive agent work merely to manufacture a
baseline; report unavailable measurements as unknown.

Package checks establish structure and installation behavior. Reliable implicit
invocation and improved future execution remain unverified until observed.
Optional broader AI evaluations require separate explicit authorization.

Stop reassessing when the next execution path is clear. This skill adds no
recurring review loop, mandatory model escalation, scheduler, or generic codemod
framework. Remove disposable probes when their purpose ends under the existing
cleanup policy.
