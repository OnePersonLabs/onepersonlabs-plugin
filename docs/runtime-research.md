# Per-project runtime research

Evidence date: 2026-10-20. This is a source-based comparison, not a runtime
qualification report. No candidate is selected for unattended deployment.

Itervox v0.2.1 is the strongest inspected local candidate. It supplies much of
the scheduling and Codex continuity path, but it does not supply the complete
feedback-delivery and landing contract. The next useful step is the
[local upstream proposal](itervox-upstream-proposal.md), not an OPL adapter or a
pilot of a source-proven gap. That proposal has not been submitted upstream.

## Intended outcome

Each project has its own explicit hard limit on independent issue workers.
The default is one primary issue from admission through actual landing and base
synchronization. Optional helper subagents have a separate limit. A project can
choose useful parallel issue work when dependencies, contracts and shared
resources permit it; available slots are not a quota to fill.

GitHub remains the actionable backlog. Workers preserve project instructions,
capture distinct defects with evidence, deduplicate before creating issues,
maintain ownership and review/rework/blocked state, and keep the original builder
responsible for PR and CI repairs. Local checks remain the default. Human merge
remains the default. Waiting for work, capacity, CI or review must not require
model inference. Restart, cancellation and repeated feedback must not silently
lose ownership or resume the wrong conversation.

Use the existing Codex subscription where supported. No measured subscription
savings, cache benefit, cost or elapsed-time improvement is established here.

## What the public Codex repository automates

At inspected commit `e1b9c945`, OpenAI's public workflows use the API-key-backed
Codex Action for [issue labels](https://github.com/openai/codex/blob/e1b9c945/.github/workflows/issue-labeler.yml),
[duplicate suggestions](https://github.com/openai/codex/blob/e1b9c945/.github/workflows/issue-deduplicator.yml)
and [translation](https://github.com/openai/codex/blob/e1b9c945/.github/workflows/issue-translator.yml).
The workflows pin Action version 1.7 and separate model output from jobs that
apply GitHub changes. This is concrete issue automation, not evidence that the
whole repository develops itself or a ready local subscription worker pool.

An older Codex-running Action was [removed in commit aa5fc58](https://github.com/openai/codex/commit/aa5fc5855d16e5e708628d79a4256cc9ef6c9004)
because its authors identified design issues. A historical automation example
does not establish the current development loop or private internal tooling.

Their [CI strategy](https://github.com/openai/codex/blob/e1b9c945/.github/workflows/README.md)
also separates fast pre-merge checks from heavier cross-platform verification
after merge. That supports choosing hosted execution for useful environment
coverage; it does not require copying OpenAI's scale or build infrastructure.

## Released candidates and decisive limits

Release dates below are GitHub publication dates. A tagged feature, an open fix,
current main and a locally qualified deployment are different evidence states.

| Candidate and pinned evidence | Useful behavior | Decisive limit for this outcome |
| --- | --- | --- |
| [Itervox v0.2.1](https://github.com/vnovick/itervox/releases/tag/v0.2.1), Sep 28; [tagged source](https://github.com/vnovick/itervox/tree/cb09d4bf1711f86479b47e4d9c665df07045ac88) | GitHub intake, bounded dispatch, dependency gates, priority/critical-path scheduling, local Codex login and saved-session continuation. | Feedback enqueue does not identify or acknowledge consumption by the intended pending question. Automatic external landing reconciliation is incomplete. Release assets target Linux/macOS; WSL and actual project toolchains remain unqualified. |
| [Agent Orchestrator v0.14.3](https://github.com/OrchestratorInc/agent-orchestrator/releases/tag/v0.14.3), Oct 19; [SCM observer](https://github.com/OrchestratorInc/agent-orchestrator/blob/v0.14.3/backend/internal/observe/scm/observer.go) | Native PR/CI observation and retained-worker feedback are useful references. | The relevant hard-intake-cap fix [#5649](https://github.com/OrchestratorInc/agent-orchestrator/pull/5649) was still open and unmerged at inspection. Do not attribute it to v0.14.3. Dependency/priority admission and duplicate-PR recovery still need qualification. |
| [GitHub Agentic Workflows v0.92.0](https://github.com/github/gh-aw/releases/tag/v0.92.0), Oct 15; [released queue](https://github.com/github/gh-aw/blob/v0.92.0/docs/src/content/docs/reference/work-queue.md), [Codex engine](https://github.com/github/gh-aw/blob/v0.92.0/docs/src/content/docs/engines/codex.md) | Its bounded fair/DAG queue is implemented. A DAG is a dependency graph without cycles. | Actions execution and the queue's authoritative Git ledger differ from the desired local Codex workflow. Authentication and persistent creator-session repair do not establish the required subscription-based local loop. |
| [Kata Symphony stable v2.3.3](https://github.com/gannonh/kata-symphony/releases/tag/symphony-v2.3.3), Aug 2; [repository](https://github.com/gannonh/kata-symphony) | GitHub-oriented scheduling and lifecycle guidance. | Current main has features beyond the stable release. Inspected adapter attempts start fresh Codex threads; retained builder repair across attempts is not established. Do not combine stable packaging with main-only claims. |
| [OpenAI Symphony v0.0.3](https://github.com/openai/symphony/releases/tag/v0.0.3), Sep 15; [tagged README](https://github.com/openai/symphony/blob/v0.0.3/elixir/README.md) | Includes GitHub Issues as well as other tracker adapters. Its landing helper is a concrete code reference. | The README identifies the implementation as prototype software for evaluation. It is not a qualified deployment recommendation. |
| [Fabro v0.254.0](https://github.com/fabro-sh/fabro/releases/tag/v0.254.0), June 4; [automation documentation](https://docs.fabro.sh/execution/automations) | An existing workflow engine is preferable to inventing one. | Current documentation/nightly capabilities must not be assigned to the stable release. No ready local GitHub issue-to-landing loop was established; controller work would remain. |
| [Codex Orchestrator v2.0.35](https://github.com/SergiiMytakii/codex-orchestrator/releases/tag/v2.0.35), Oct 20; [tagged README](https://github.com/SergiiMytakii/codex-orchestrator/blob/v2.0.35/README.md) | Same-session repair for eligible review feedback. | Its documented run completes at review-ready. Strategic priority/dependency admission and retained issue ownership through actual landing remain unqualified. |
| [Devin Automations](https://docs.devin.ai/product-guides/automations), live documentation; [PR integration](https://docs.devin.ai/integrations/gh), [billing](https://docs.devin.ai/admin/billing/self-serve) | Managed GitHub events, queueing and replies to existing PR sessions. | Separate billing/execution. Active-session concurrency does not prove one issue through landing or strategic backlog admission. Consider only if local options cannot meet the requirements; no purchase or selection is implied. |

The decision follows capability and integration evidence, not popularity or an
age cutoff. The shortlist includes small specialist projects. Additional search
leads did not resolve the decisive continuity and ownership gaps.

## Why the proposed OPL watcher was rejected

In Itervox v0.2.1, the
[worker](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/worker.go)
runs `after_run` synchronously before the event loop parks an input-required
builder. That worker also excludes input-required exits from `pr_opened`
automation. An early callback can therefore arrive before the pending question
exists.

The [HTTP handler](https://github.com/vnovick/itervox/blob/v0.2.1/internal/server/handlers.go#L766-L787)
returns 202 after
[`ProvideInput`](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/issue_control.go#L273-L295)
enqueues an identifier and message without looking up a parked owner. The
[event loop](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/event_loop.go)
drops the message if no question exists; otherwise it consumes the then-current
pending entry for that identifier. The operation has no expected run/question
identity or consumption receipt. A successful enqueue is not proof of delivery.

The real [`input_required` automation](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/automation.go)
can launch a model helper that runs an observer and supplies input. That is a
native mechanism, but it adds a model invocation and does not establish the
required durable conditional-delivery contract. It is not a zero-inference
ordinary-code observation job.

For landing, the native
[`pr_merged` dispatcher](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/automation_pr_merged_dispatch.go)
exists, but its comments describe polling external merges as a future caller.
The presence of a trigger name does not establish human-merge reconciliation.

## Concern-to-change coverage

The independently shippable OPL research/setup guidance preserves these
requirements. It does not implement the missing runtime behavior.

| Concern | Existing owner or proposed change | Acceptance boundary |
| --- | --- | --- |
| Current evidence and honest selection | OPL research guidance; dated comparison here | Pin versions, distinguish main/open fixes, disclose unsupported paths. Itervox remains a candidate. |
| Independent project root cap versus helpers | Native Itervox dispatch/config and native Codex helper settings | Set `agent.max_concurrent_agents` explicitly: proposed setup default 1, optional 2. Its release default is 10. Helper limits exclude the root; disclose aggregate model threads. No OPL aliases/schema. |
| One issue through landing; useful parallelism | Native admission plus proposed lifecycle reconciliation | Retain issue ownership while parked; reserve delivery capacity. Recheck dependencies, settled contracts and contention. Prove independent projects do not share an accidental pool. |
| GitHub defects, deduplication and accurate state | Project issue policy and runtime tracker adapter | Helpers propose; authorized owning workers capture distinct defects. Capture does not authorize execution. Closed-unmerged PRs do not complete unresolved issues. |
| Local checks and original-builder repair | Project checks/review policy; native saved Codex session plus proposed conditional delivery | Repair in the creator conversation. Do not substitute an existing workspace or PR link for session identity. |
| No inference while idle, full or waiting | Native scheduler and proposed ordinary-code observation lifecycle | No model starts merely to inspect capacity, poll CI or decide whether feedback changed. Changed-backlog dependency analysis can still use inference; disclose it. |
| Restart, cancellation, duplicate/stale feedback | Proposed native job ownership and accepted/consumed receipts | Retry uncertain transport safely; do not redirect old events to a new question or claim exactly-once execution. |
| Human merge and base synchronization | Proposed native PR lifecycle and existing workspace owner | Reconcile merge, closed-unmerged and head changes. Verify base refresh before admitting the next serial issue. |
| Toolchain, permissions and delivery lanes | Native runtime/configuration qualification | Qualify WSL, credentials, PATH, project checks and Codex permission mode. Trusted direct commits and local branch integration remain native Codex choices; unattended no-PR delivery is unmet. |

Itervox's [dispatch](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/dispatch.go),
[configuration](https://github.com/vnovick/itervox/blob/v0.2.1/internal/config/config.go)
and [Codex runner](https://github.com/vnovick/itervox/blob/v0.2.1/internal/agent/codex.go)
support the narrower source claims above. `pause_dispatch_when_any_in_state`
can hold new admission during review; it does not alone prove the complete
landing lifecycle. A process limit and an issue-through-landing limit are
different contracts.

The released [event-loop selector](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/event_loop.go#L330-L350)
uses [critical-path ordering](https://github.com/vnovick/itervox/blob/v0.2.1/internal/orchestrator/sort_critical_path.go#L76-L145)
by default: priority first, then downstream reach and chain length. The selectable
strict mode puts downstream reach and chain length first. These are actual native dispatch modes,
not inferred capabilities of the optional model analyzer. Graph scope and
project-specific dependency quality still need qualification.

## Decision and next gate

Prepare native changes only after separate executable-work authorization and
upstream design agreement. Prefer a maintained release; a pinned fork requires
an explicit maintenance decision. Do not install a personal patch and call the
runtime qualified.

Keep the full unattended scope in [issue #4](https://github.com/OnePersonLabs/opl/issues/4)
open: independent projects, supported admission, useful bounded parallelism,
same-builder repair, feedback recovery, accurate state, waiting without inference,
landing, base synchronization and next-issue dispatch must work together.
Manual advancement does not satisfy unattended dispatch. A later attended
four-issue disposable-repository campaign needs its own procedure and budget;
this research authorizes neither runtime execution nor model evaluations.
