# Native workflow choices

Read this reference when selecting tracker, review, or automation settings.
Inspect the repository's existing choices first. Adopt the smallest change that
serves its acceptance criteria; a Project board is optional.

## Tracker and native automation

Reuse existing fields, labels, priority and dependency conventions. If GitHub is
the tracker, `$opl:github-workflow` reconciles ongoing work through standard
GitHub tools, with the assigned root owning writes. Workers return proposals.

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

Human merge is the default. Native auto-merge is an explicit per-project option
under its branch protections. Record how the builder waits for review/merge and
resumes after feedback, and how the base is synchronized before next work. An
operator advances the workflow until Stage 2 qualifies unattended admission.

Sources: [self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners),
[runner security](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions),
[auto-merge](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/automatically-merging-a-pull-request).
