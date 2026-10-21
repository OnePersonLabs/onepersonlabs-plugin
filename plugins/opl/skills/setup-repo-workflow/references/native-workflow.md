# Native workflow choices

Read this reference when selecting tracker, review, or automation settings.
Inspect the repository's existing choices first. Adopt the smallest change that
serves its acceptance criteria; a Project board is optional.

## Delivery lane and environment

Default to serial work in the selected checkout and branch. Choose another lane
only under an explicit user or project choice and the existing protections:

| Lane | Working agreement |
| --- | --- |
| Trusted serial commits | One builder handles an authorized issue or finite batch in one conversation. Use direct checked commits only when project policy permits them. Record acceptance, delivery and the next issue explicitly. No per-issue branch or PR is required by OPL. |
| Parallel local integration | Independent issue writers use separate worktrees/local branches. One integration owner checks the combined result and serializes landing. A local branch does not require a GitHub PR. |
| PR delivery | The original builder owns review/check repairs through actual landing. Select the review lane and merge policy. Retain its conversation identity and checkpoint for operator resumption. |

Keep existing protections. If the chosen lane conflicts with them, report the
specific incompatibility rather than weakening a protection. A commit alone
does not satisfy acceptance that includes release or other qualification.

Discover how dependencies, secrets, ignored environment files, local services,
ports and check commands work in each worktree. Verify the actual project
toolchain, filesystem paths and credentials before claiming Windows/WSL support.
Preserve existing worktrees and unrelated configuration. Use the repository's
existing setup helpers and native Git; add no universal environment framework.

Sources: [Git worktrees](https://git-scm.com/docs/git-worktree),
[Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees),
[WSL interoperability](https://learn.microsoft.com/en-us/windows/wsl/interop).

## Independent workers and helper budget

Default to one primary issue through landing. Two optional helper subagents per
primary session is a ceiling, not a target. More independent primary workers
require an explicit project choice; there is no cross-project admission limit.

Independent issue workers and helpers have different owners and settings. In
current Codex, `agents.max_concurrent_threads_per_session` caps open spawned-agent
threads in a session and excludes its primary. A value of `2` therefore permits
three threads including that primary. Two independent primaries can permit six
threads, plus any separately launched review or helper session. Count those
extra sessions; do not describe the helper cap as a project-wide worker limit.

Use `$opl:configure-harness` to inspect supported settings and effective overrides.
For project settings, edit the native repository configuration at its supported
scope; its global-only application helper cannot apply project files. Check the
installed version, configuration trust and existing aliases before writing.
Preserve unrelated TOML, approved model preferences and intentional helper
settings. Add no `MaxAgents` or
`MaxSubagents` aliases. A future qualified runtime must supply its own hard
independent-worker cap and define whether review/merge waiting occupies capacity.
An operator's one-issue working agreement is not an installed scheduler limit.

Prepare parallel issues against current claimed work: satisfied dependencies,
settled shared contracts, low expected write/resource contention, and enough
independent work to justify setup and integration. Different filenames alone
do not establish independence. Keep useful affected-component and dependency
information in existing issues/plans. Recheck it before starting another writer;
do not fill free slots as a quota. Prefer bounded investigation/testing helpers
for small related work.

Source: [Codex subagents and native settings](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Tracker and native automation

Reuse existing fields, labels, priority and dependency conventions. If GitHub is
the tracker, `$opl:github-workflow` reconciles ongoing work through standard
GitHub tools, with the assigned root owning writes. Workers return proposals.

Put a concise route to `$opl:github-workflow` in the repository's existing agent
instructions for ordinary authorized work. The root deduplicates and captures
distinct confirmed defects with evidence, impact, reproduction and acceptance;
uncertain findings need investigation. Ordinary repairs stay on the owning
issue. Capturing an issue does not authorize its execution.

Record ownership at work start and maintain PR links and review/rework/blocked
state. Close only when complete acceptance is satisfied. A closed-unmerged PR
leaves unresolved scope open. Synchronize the accepted base before starting
the next issue; retain unfinished work and original-builder resumption details
in the existing checkpoint.

Use native Project auto-add and Done automation when they fit the repository.
Auto-add applies to matching new or updated items; it does not backfill all
existing matching issues. Reconcile the initial existing set explicitly before
claiming coverage. Match Done automation to actual acceptance: closing a PR or
issue is not sufficient when delivery or qualification remains open. Inspect
filters, scope, and current items before changing automation. Use ordinary
GitHub tools for remaining authorized writes, not a second scheduler.

Official references: [auto-add workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically),
[built-in workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations).

## Review lane

Choose local native Codex review or GitHub review according to the repository's
review needs and access. They use different usage categories: GitHub Code Review
uses the Code Review category; local and other review use general usage. Do not
promise cache hits or cost savings from a shared chat.

Version-specific observation, 2026-10-20: Codex 0.160.1 native local review starts
a fresh delegate even when review appears inline in the chat. It supplies the
review prompt and a new initial history. Recheck installed behavior after a
version change before relying on this detail. For `codex review`, installed
help disallows a custom prompt together with `--base`, `--commit`, or
`--uncommitted`; choose a supported route. Freeze the baseline before creating
new commits so review covers the full series rather than only the latest repair.

Keep the builder responsible for PR repair rounds. Give reviewers requirements,
the baseline, the actual diff, and evidence without an implementer's verdict.
Recheck changed deltas and invalidated evidence after repairs.

Sources: [usage categories](https://learn.chatgpt.com/docs/pricing),
[Code Review](https://learn.chatgpt.com/docs/code-review),
[0.160.1 review task](https://github.com/openai/codex/blob/rust-v0.160.1/codex-rs/core/src/tasks/review.rs#L118-L138),
[delegate history](https://github.com/openai/codex/blob/rust-v0.160.1/codex-rs/core/src/codex_delegate.rs).

## Repository and harness boundaries

Put repository workflow instructions in the repository's existing instruction
files. Use existing tracker state and the existing concise checkpoint; do not
create another queue. Keep Codex installation and agent configuration in
`$opl:configure-harness`. Skills need a clear trigger and optional detail behind
conditional references, not a manual loaded for every task.

Sources for supported Codex surfaces:
[skills](https://learn.chatgpt.com/docs/build-skills),
[best practices](https://learn.chatgpt.com/docs/learn/best-practices),
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Checks, runners, and merge policy

Discover and run existing checks locally. A standard self-hosted Actions runner
is an optional repository choice when it adds useful automation; do not deploy
one automatically. Hosted jobs are useful for platform coverage, clean environment
differences, releases, and isolating public-fork code. Do not spend hosted minutes
merely to repeat local checks without a repository reason. Review runner security
and access before enabling external code execution.

For selected PR delivery, automatic merge is the default after required checks
and reviews pass. Preserve reviewable commits; honor explicit manual-merge policy
and existing protections. Enable the repository's native auto-merge setting when
authorized, then enable it for each selected PR. Repository support alone does not
arm every PR. Use the project's merge method; do not squash distinct units merely
to land the branch.

Native auto-merge waits for GitHub-enforced requirements, not an agent's local
checklist. Where merge is immediately available, finish required local checks and
reviews before merging. Record actual landing and synchronize the accepted base.
Record how the builder resumes after feedback and how review/merge waits are
delivered; automatic merge does not resume the builder or dispatch another issue.
Without a qualified dispatcher, the operator advances to the next eligible
issue. This setup installs no intake or worker service.

Sources: [self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners),
[runner security](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions),
[auto-merge](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/automatically-merging-a-pull-request).
