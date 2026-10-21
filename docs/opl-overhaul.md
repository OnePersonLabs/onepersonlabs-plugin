# OPL overhaul audit

Stage 1 implements a lean personal contract and per-repository setup. Stage 2
unattended issue dispatch remains open in [issue #4](https://github.com/OnePersonLabs/opl/issues/4).
No dispatcher, standing agent fleet, global project queue, or hosted runner was
installed. [Issue #3](https://github.com/OnePersonLabs/opl/issues/3) owns Stage 1.

The frozen source baseline is `81c65e4a1234911ab168978084f6b44425d124bb`.
Checkpoint commits remain intact; review must compare the complete series with
that baseline. The implementation's local evidence and remaining limits are
recorded below. A plan's acceptance is separate from implementation verification.

## Decisions and source basis

The attached October 19 research supplies hypotheses, not measured savings for
this installation. Current primary guidance supports shorter always-loaded
instructions, specific skill triggers, conditional references, bounded delegation,
and proportionate verification. It does not establish that debugging, TDD, or
independent judgment is obsolete. Those methods remain explicit tools.

| Reference | Applied decision | Limit |
| --- | --- | --- |
| [Astra instruction guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Remove generic scaffolding and broad triggers; use progressive disclosure. | Guidance is not a benchmark of OPL. |
| [GPT-6 family maintenance experiment](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family) | Sol 6.1/medium is the selected personal default; narrow Astra escalation. | One maintenance workload does not establish all-task optimality. |
| [Skills configuration](https://learn.chatgpt.com/docs/build-skills) | Explicit-only setup/debug/TDD/adversarial metadata. | Discovery does not prove invocation or outcomes. |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) | Optional bounded helpers, explicit ownership, isolated independent writers. | Additional agents consume tokens; no universal savings claim. |
| [Codex pricing](https://learn.chatgpt.com/docs/pricing) | Choose local or GitHub review per project; keep accounting categories distinct. | Subscription consumption is not inferred from API token prices. |
| [Native review 0.160.1](https://github.com/openai/codex/blob/rust-v0.160.1/codex-rs/core/src/tasks/review.rs#L118-L138), [delegate](https://github.com/openai/codex/blob/rust-v0.160.1/codex-rs/core/src/codex_delegate.rs) | Inline native review starts a separate conversation; retain builder for repairs. | Version-specific; no promised shared builder history or cached prefix. |
| [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Preserve useful conversation continuity; report observed cache usage. | Matching prefixes are required; rereading a file does not itself establish cost. |
| [GitHub auto-add](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically), [status workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations), [PR linking](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | Native automation where useful; initial reconciliation; close only complete acceptance. | Auto-add does not backfill existing matching items. Projects are optional. |
| [Self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) | Local checks first, optional standard runners; hosted execution for useful differences. | No automatic runner deployment or claim that public fork code is safe locally. |
| [Red/green TDD practice](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/) | Retain explicit red/green method and honest tests-after reporting. | TDD is a choice, not a universal activation rule. |

## Every skill disposition

All retained packages keep explicit invocation metadata and their working tools.
Verification combines package structure/reference checks with relevant existing
executable suites. No permanent invocation tests or evaluation service is added.

| Skill | Disposition and reason | Dependencies / verification |
| --- | --- | --- |
| `$consensus` | Remove prescribed panels and voting overhead. | Material alternatives remain in core reasoning; remove package/callers. |
| `$explore-deeply` | Remove generic multi-angle recipe. | Proportionate source investigation remains core. |
| `$quiz` | Remove blanket planning interview activation. | Ask material unresolved questions through host tools. |
| `$distill-self-improvements` | Remove broad personal-history mining. | Explicit bounded session analysis remains with session-reader/Slop tools. |
| `$review-changes` | Remove generic diff-review duplication. | Native review; full-series baseline; acceptance questions retained conditionally. |
| `$review-repo` | Remove broad review campaign scaffolding. | Native scoped code review; architectural questions under adversarial-review. |
| `$optimize-agent-instructions` | Merge optional scrutiny/comparison into agent-instructions; remove recursive pipeline. | Moved reference; explicit AI budget; no mandatory model evaluation. |
| `$probe-agent-profile-usage` | Merge diagnostic helper into configure-harness. | Script/test paths migrated; interrupted instrumentation restoration retained. |
| `$recover-request-user-input` | Merge host diagnosis into configure-harness. | No forced retries; parent routing remains available. |
| `$debug` | Retain explicit causal diagnosis. | Symptom, divergence, falsifiable cause/counterevidence, original-scenario verification; no compulsory TDD. |
| `$test-driven-development` | Retain explicit concise red/green workflow. | Honest tests-after distinction; no universal coverage mandate. |
| `$adversarial-review` | Retain explicit plan/architecture/instruction/workflow audit. | Native review for ordinary diffs; conditional architectural/acceptance questions. |
| `$agent-instructions` | Retain ownership and surface selection; merge optional comparisons. | References resolve; no recursive mandatory optimization. |
| `$configure-harness` | Retain supported inventory, transactions, diagnosis and recovery. | Existing transaction tests; root model settings outside features/agents ownership; optional budgeted measurement. |
| `$github-workflow` | Retain root-owned issue reconciliation throughout authorized work. | Dedup, scope authority, status mapping, uncertain-write recovery; no competing backlog. |
| `$solve-novel-software` | Retain distinctive falsification/oracle method. | Remove arbitrary breadth/artifacts; preserve production transfer and limits. |
| `$design-perceptual-interfaces` | Retain domain evidence and visual workbench. | No fixed variant count; existing evidence/tool contracts retained. |
| `$assimilate` | Retain donor inspection, integration and provenance. | Remove campaign artifacts and orphaned broken donor README. |
| `$adhd` | Retain interruption recovery and actionable next step. | Shorter entrypoint; preserve meaningful task support. |
| `$camofox-browser` | Retain separate REST integration. | Use shared command catalog; REST/CLI distinction preserved. |
| `$camofox-cli` | Retain separate CLI integration. | One command catalog; detail routed to reference. |
| `$codex-hook-debug` | Retain lifecycle/trust/version diagnosis. | Remove assumptions tied to deleted gates; existing hook tests. |
| `$refresh-local-plugins` | Retain native installation/trust and recovery. | Pause/resume even after failure; existing Windows/WSL helpers and installed tests. |
| `$update-instructions` | Retain versioned replacement/backups/no-downgrade. | Reuse established authorization; startup notice cannot mutate or block. |
| `$long-command-wakeup` | Retain conditional detached completion delivery. | Prefer native waits; no invented execution deadline; existing watcher tests. |
| `$route-agent-question` | Retain immediate-parent routing. | No forced retry choreography; root alone asks human. |
| `$human-collaboration` | Retain actual service, explicit submission and recovery. | Detailed briefs/delivery moved behind references; preserve user drafts and pause/resume. |
| `$handoff` | Retain resumable ownership and checkpoint. | Remove boilerplate repetition; existing state remains authoritative. |
| `$session-reader` | Retain bounded extraction engine. | Narrow description; no broad history loading. |
| `$session-history-rebuild` | Retain damaged-history recovery. | Conditional procedural detail and existing helpers retained. |
| `$slop-buster` | Retain evidence, resumable coverage and watermarks; advisory hooks. | Nullable unrated feedback and persisted/exported Stop-only findings; reader default updated. |
| `$unslop` | Retain replay and comparison tools. | Remove fixed counts, forced self-ratings and touched-code restrictions; no automatic scope extension. |
| `$last30days` | Retain research engine. | Narrow trigger; setup/run detail conditional; no provider self-preference policy. |
| `$de-ai-writing` | Retain deliberate prose-editing tool. | Narrow trigger; no every-response loading. |
| `$simplified-technical-english` | Retain precision-writing engine/tools. | Narrow trigger; no global every-response loading. |
| `$setup-repo-workflow` | Add explicit-only repository setup. | Reconcile existing native configuration, preserve unrelated settings, document operator advancement and Stage 2 limit. |

## Concerns mapped to behavior

| Concern | Implemented response |
| --- | --- |
| Quota burn and excessive orchestration | Compact core, fewer entrypoints/roles/gates; optional focused delegation and review; no invented savings. |
| Small reviewable commits | Global and repository rules require coherent checked task-owned checkpoints; no blanket staging or per-checkpoint refresh. |
| TDD/debug/review redundancy | Explicit methods for distinct value; native routine diff review; independent judgment when risk warrants it. |
| Cache loss during repairs | Same builder owns PR repairs; reviewers get scoped facts/diff; no cache-hit promise. |
| Two projects at once | Independent per-project policy and worktrees; no portfolio controller or global admission limit. |
| Useful parallel workers | Default up to two optional helpers; project may opt into more primary issues/workers; one writer per mutable surface. |
| Automatic bug capture and issue states | Root reconciles while working; dedup, suspected/confirmed distinction, priorities/dependencies, review/rework/blocked, full-scope closure. |
| Synchronous development momentum | Ready issue through landing; operator advances where supported wake/admission is unqualified. Stage 2 remains separately open. |
| GitHub Actions minutes | Local verification first; no Actions/runner deployed; hosted jobs reserved for valuable environment differences. |
| Existing human collaboration and recovery | Service protocol and refresh pause/resume retained; source fallback on installer failure; listener/process checks retained. |
| Global config ownership | Root preferences backed up separately on Windows/WSL; checker owns only features/agent defaults and verified package registrations. |

## Shared implementation and verification

The first checkpoint fixes staged revision validation: insufficient staged bumps
are rejected without rewriting the working tree or index. The profile catalog
synchronization dependency is removed. Seven general profiles are removed; two
Slop profiles and native/user-authored delegation remain.

Response/artifact phrase, skill-review, sigil, model-selection, newline repair,
and duplicate refresh hooks are removed with orphaned helpers/tests. The narrow
destructive-shell matcher remains. HTTP clients are permitted. Task-watch and
human-collaboration lifecycle hooks remain. Slop findings are advisory: this loses
forced immediate correction, but preserves evidence and NULL unrated feedback.

Configuration and global-instruction startup inspection is read-only/nonblocking.
Stale marker normalization happens only in explicit backed-up mutation commands.
Compatibility accepts an empty policy, retains real repository constraints, and
reports unavailable ignored IDs as nonblocking warnings without a retired-ID list.

Root model preferences were applied on Windows and WSL as Sol 6.1/medium/Standard
(`service_tier = "default"`), with dated byte-exact backups and semantic comparison
proving unrelated settings unchanged. Explicit planning-mode overrides remain.
Shipped optional child defaults are Luna/high; Slop reading is Luna/medium.

Focused checks passed: revision validation 9; lifecycle/shell/boundaries 12;
compatibility 46; configuration preservation/recovery 16; Slop Buster 48.
The OPL package contract checkpoint passed. Windows full installed-copy validation
passed with 27 unit test files and trust verified for all 23 hooks. WSL Codex
0.155.1 passed its isolated package/discovery/trust checkpoint for the same 23
hooks; Windows CLI is 0.160.1. Changed Python/JSON/TOML parsed and all changed
local Markdown links resolved (88 files checked). Bash replay syntax passed.

One fresh independent reviewer inspected the entire frozen-baseline series
through `5c59609` and the final test-only deletion, reporting no material finding.
It also checked the four recorded comparison outcomes and snapshot identity.
No further model calls were made. Full repository pre-push gates run at delivery.

Two inherited last30days tests were removed: one mirrored canonical metadata
already validated generically; another asserted exact setup prose that moved to
a conditional reference. Its eight runtime contract tests remain and pass.
Configuration fixes fill optional child defaults only when absent, preserve
explicit child choices, and refuse ambiguous user-profile name collisions.

Global instructions fell from 5,148 to 1,332 whitespace-separated words (552 to
163 lines). This measures instruction size, not model quota or accepted-change
cost. The Stage 1 skill inventory is 27 packages versus 35 initially.

### Four isolated software comparisons

Exactly four Codex 0.160.1 runs used Sol 6.1/medium/Standard: baseline revision 54
and revised revision 55 on the same timeline-resolution task and lease-cache
causal-diagnosis task. Each used a disposable Git repository and Codex home with
unrelated hooks/plugins/skills disabled, identical task fixtures, and no subagents,
live service operations, or extra model calls. Authentication copies were removed
afterward. Scratch logs remain outside the repository; no permanent AI tests exist.

| Task / instructions | Independent checks | Input / cached input tokens | Output tokens | Elapsed seconds |
| --- | --- | --- | --- | --- |
| Timeline / baseline | 211 passed | 94,109 / 54,528 | 3,300 | 81.21 |
| Timeline / revised | 211 passed | 85,502 / 55,680 | 3,460 | 82.15 |
| Causal diagnosis / baseline | 9 passed | 153,078 / 109,824 | 2,051 | 60.44 |
| Causal diagnosis / revised | 9 passed | 95,390 / 78,720 | 2,474 | 67.46 |

No root repair was needed. Both diagnosis runs identified the first incorrect
stored deadline (350 seconds instead of 100.25), supplied counterevidence, and
verified original expiry and renewal scenarios. One baseline command failed as
an expected red-test observation, not a failed delivered implementation. The
revised arms made coherent local commits; baseline arms left verified edits.
The timeline oracle used seeded discrete-time ownership and invalid-input cases;
the lease oracle checked deadline, boundaries, renewal and missing/zero leases.

Across these two tasks, revised reported input was 26.8% lower, output 10.9%
higher, and summed run time 5.6% longer. Cache observations are reported directly;
cache state was uncontrolled. This tiny sample supports no subscription-quota or
general performance claim. Results establish the exercised software behavior,
not field qualification or automatic skill invocation. CLI emitted harmless
PowerShell snapshot/temp-alias warnings; all four model sessions exited zero.

## Open Stage 2 acceptance

Qualify an existing implementation against independent project operation,
supported wake/admission ownership, same-builder repair continuity, feedback
deduplication, accurate issue state, waiting through review/merge, base
synchronization, and starting the next eligible issue without inference polling.
Manual advancement cannot satisfy unattended dispatch.

[Agent Orchestrator reactions](https://docs.orchestrator.inc/guides/reactions/)
are a feedback reference, not a complete selected solution; its
[GitHub intake is read-only](https://docs.orchestrator.inc/plugins/trackers/github/).
[Symphony](https://github.com/openai/symphony/blob/main/elixir/README.md) remains a
reference prototype. Any runtime pilot needs a concrete candidate, procedure,
and separately authorized budget. No automatic intake is enabled by Stage 1.

Delivery is PR first, human merge, then source synchronization and Windows/WSL
installation refresh. The current session retains its previously loaded tools
and instructions until a fresh session. An isolated installed-copy check is not
a refresh of the user's active homes.

## Current-reference research and workflow delivery

[Issue #6](https://github.com/OnePersonLabs/opl/issues/6) owns the companion delivery
against frozen baseline `3ce8948d19a834c66834c0bb015b48b1c153cfe5`. It preserves the
eight Stage 1 commits and PR #5. The new source instruction revision is 56, and
the new skill brings the inventory to 28 packages.

| Change | Reason and dependencies | Evidence boundary |
| --- | --- | --- |
| Add `$opl:research-solutions`, implicitly discoverable, with a short global route | Make current expert/maintainer research and assembled-contract inspection automatic for consequential choices. Keep the procedure conditional and routine repairs proportionate. | [Supported skill metadata](https://learn.chatgpt.com/docs/build-skills). Structure and discovery metadata do not prove automatic invocation or accepted-change savings. |
| Extend explicit `$opl:setup-repo-workflow` and its native reference | Distinguish serial commits, parallel worktrees/local integration and PR delivery; preserve existing tracker, checks, protections, builder repairs and resumption. | [Native worktrees](https://git-scm.com/docs/git-worktree), [Codex helper settings](https://learn.chatgpt.com/docs/agent-configuration/subagents). Two helpers is per primary session, excluding the primary; independent roots and extra reviews add to the total. |
| Align `$opl:github-workflow` helper scope and conditional reference | Keep one owner for issue reconciliation and one native-setting reference; no duplicate backlog or controller. | Project settings use supported native files. The harness application helper owns global files and cannot apply project files. |
| Publish the [runtime comparison](runtime-research.md) and [local upstream proposal](itervox-upstream-proposal.md) | Preserve source/version limits, concern coverage and the missing native observation, feedback-delivery and landing contracts. | Itervox is a candidate, not a selected or qualified runtime. No OPL adapter, runtime, service, fork, upstream submission or live pilot is included. |

The four Stage 1 model comparisons above remain the complete authorized evaluation
set. This delivery adds no invocation tests, AI evaluations or live qualification.
The integration checkpoint passed OPL contract checks, all 27 unit test files,
source/installed inventory comparison and trust verification for 23 hooks in the
isolated Windows Codex home. Relative links and changed skill metadata passed
structural checks. This evidence covers package structure and existing executable
contracts; automatic discovery outcomes and runtime behavior were not model-tested.
Active Windows/WSL refresh follows human merge; isolated installed checks do not
change active homes or the instructions already loaded by a session.

## Perceptual scaffolding

[Issue #8](https://github.com/OnePersonLabs/opl/issues/8) owns this companion delivery
against frozen baseline `e14d18d81b1a293a971f59f93afc2ff8bb88cca8`, stacked on PR #7.
Source revision 57 adds a soft communication preference and routes substantial
explanation, teaching, exploration and human interaction design to
`$opl:build-understanding`. The inventory is now 29 skills.

The skill selects representations for accurate understanding and control with
less unnecessary mental reconstruction. It includes nonvisual input and output,
keeps simple exchanges simple, and loads its evidence/patterns reference only
when useful. Existing perceptual-design and human-collaboration packages retain
visual implementation, submissions and service ownership.

The [OPL at-a-glance guide](opl-at-a-glance.md) is the first application: portable
Mermaid maps, a worked repair case and expandable details explain roles, delivery
choices, worker/helper limits, source/install/session boundaries and the absence
of an installed unattended runtime. Its exact procedures stay with their
existing owners.

Research sources and their limits are in the skill's conditional reference.
Rendering and structural checks establish different facts from human comprehension
or measured learning improvement. No invocation tests, AI evaluations, permanent
presentation scoring, new service or runtime are part of this delivery.

The official Mermaid CLI 12.0.0 rendered all three maps in light and dark
themes. Browser inspection at 390-pixel and 1280-pixel widths found no page
overflow; all four native expandable sections opened and closed from the
keyboard with focus retained. SVG titles/descriptions, equivalent text routes
and grayscale presentation were checked. This was a local preview, not a
qualification of GitHub's hosted renderer or a human learning study.

Skill structure, metadata, relative references and instruction revision checks
passed. The isolated installed-copy checkpoint passed OPL contract checks,
all 27 unit test files, source/installed inventory comparison and trust checks
for 23 hooks. Active Windows/WSL homes and session-loaded instructions remain
unchanged until the human-merge and refresh boundary.

## Automatic landing and opt-in PR delivery

The user authorized landing the accumulated stack and revised the default on
2026-10-21. PRs #5, #7, #9 and #11 are merged into `main`; all 15 original commits
remain in history. The four completed local and remote branches were removed
after ancestry and remote-head checks. The checkout returned to `main`.

Instruction revision 58 makes serial work in the selected checkout and branch
the default. New delivery branches and PRs require an explicit user or project
choice; parallel independent writers still need isolation. Commits remain
coherent units that can be understood and reviewed on their own.

For selected PR delivery, the builder completes required checks and reviews and
merges automatically, preserving commit units and existing protections. Explicit
manual-merge requirements still apply. OPL's native GitHub auto-merge setting is
enabled; individual PRs still need to be armed. Native auto-merge waits only on
GitHub-enforced requirements, so local checks and reviews must finish before an
immediately available merge. Verify actual landing and accepted-base sync.

This supersedes the earlier human-merge default recorded above. It adds neither
review-feedback delivery nor unattended next-issue dispatch; those remain owned
by issue #4. Sources: [GitHub auto-merge](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request)
and [native CLI merge options](https://cli.github.com/manual/gh_pr_merge).
