# Find the right OnePersonLabs skill

OnePersonLabs skills are reusable procedures for Codex. Ask in ordinary
language when the request matches a **discoverable** skill. You can also name
any skill directly, for example, `$onepersonlabs:debug`. Codex may select a
discoverable skill when its description fits. It may not invoke one for every
matching request. **Explicit** skills run only when you name them.

Each entry links to the skill's full instructions. Read those instructions for
the exact workflow, limits, and any conditional references before using a
specialized tool.

## Diagnose, implement, and review

- **[$onepersonlabs:python-scripting](../skills/python-scripting/SKILL.md)** -- Discoverable. Find, reuse and organize Python tools for agent-side work. Descriptive names and header keywords support lookup before creating another script. A shared store in the active Codex home handles hot, cold and temporary scripts; maintained repository utilities remain with their consumers.
- **[$onepersonlabs:optimize-workflow](../skills/optimize-workflow/SKILL.md)** -- Discoverable. Respond to the first concern about workflow speed, cost, or rework by accounting for effort and improving the next work batch. Result: an evidence-based bottleneck finding and revised execution sequence that preserves scope and required checks. A neutral ETA question does not require an extensive audit; controlled performance comparisons use `$onepersonlabs:optimize`.
- **[$onepersonlabs:write](../skills/write/SKILL.md)** -- Discoverable. Draft correspondence, questionnaires and general prose; faithfully edit or summarize for the intended reader. Drafting does not send messages or start an inbox.
- **[$onepersonlabs:write-technical](../skills/write-technical/SKILL.md)** -- Discoverable. Clear developer replies and precise specifications, plans, procedures, issues and PRs.
- **[$onepersonlabs:write-documentation](../skills/write-documentation/SKILL.md)** -- Discoverable. Guides and reference material grounded in current product behavior.
- **[$onepersonlabs:write-ui](../skills/write-ui/SKILL.md)** -- Discoverable. Interface actions, states and errors that match the actual product.
- **[$onepersonlabs:debug](../skills/debug/SKILL.md)** -- Explicit. Diagnose a concrete failure and, when requested, verify a causal fix. Result: a supported cause, counterevidence, and original-scenario verification. A symptom or passing test alone does not establish the cause.
- **[$onepersonlabs:adversarial-review](../skills/adversarial-review/SKILL.md)** -- Explicit. Audit a plan, architecture, instruction system, or agent workflow for concrete failure paths. Result: prioritized findings tied to evidence and a plausible failure scenario. Routine code diffs use the native review path.
- **[$onepersonlabs:write-agent-instructions](../skills/write-agent-instructions/SKILL.md)** -- Discoverable. Author, consolidate, audit, or score agent instructions and skill packages. Result: the requested instruction artifact or a scoped review; a score is not a runtime behavior test.
- **[$onepersonlabs:handoff](../skills/handoff/SKILL.md)** -- Explicit. Prepare a compact continuation document for a fresh agent. Result: a temporary handoff with current ownership, permission boundaries, decisions, evidence, and recovery state. It does not start a new session.
- **[$onepersonlabs:refresh-local-plugins](../skills/refresh-local-plugins/SKILL.md)** -- Discoverable. Refresh selected plugins from a source checkout in the current user’s default Codex home. The helper reports installation and hook trust. Requires a source checkout, Node.js, Codex plugin commands, and the human-collaboration pause/resume procedure when that service is in use. Publishing is separate.
- **[$onepersonlabs:long-command-wakeup](../skills/long-command-wakeup/SKILL.md)** -- Discoverable. Queue one continuation after a safe local command that is demonstrably expected to run for more than about two minutes. Result: a retained command log and one completion request. Requires Python 3.11+ and `codex queue`; do not use for interactive, approval-dependent, destructive, or natively waitable work.
- **[$onepersonlabs:route-agent-question](../skills/route-agent-question/SKILL.md)** -- Discoverable. Route a child agent's blocked question to its parent and return the scoped answer. Result: a decision or clarification delivered through the assignment owner. Requires an active parent assignment; only the root asks the user.

## Choose and understand an approach

- **[$onepersonlabs:research-solutions](../skills/research-solutions/SKILL.md)** -- Discoverable. Find and assemble current reference implementations for consequential tool, architecture, infrastructure, or integration choices. Result: source-linked options and compatibility or recovery findings. Requires current external evidence; it is unnecessary for routine repairs.
- **[$onepersonlabs:develop-alternatives](../skills/develop-alternatives/SKILL.md)** -- Discoverable. Develop concrete competing approaches when a consequential choice needs design work. Result: distinct mechanisms, assumptions, and trade-offs for the current owner to decide. It can pass a settled choice to `$onepersonlabs:pov`.
- **[$onepersonlabs:pov](../skills/pov/SKILL.md)** -- Discoverable. Form a source-grounded position on a supplied decision. Result: a recommendation with reasons, alternatives, and conditions that would change it. It does not invent missing product goals.
- **[$onepersonlabs:optimize](../skills/optimize/SKILL.md)** -- Discoverable. Compare changes to a working system when the best measurable option is unknown. Result: a measurement-based decision against a current baseline, correctness gates, and required trade-offs. Requires a meaningful workload, metric, and oracle; it does not turn noisy results into a win. Requests about agent delivery speed, coordination, or rework route directly to `$onepersonlabs:optimize-workflow` before any benchmark procedure.
- **[$onepersonlabs:solve-novel-software](../skills/solve-novel-software/SKILL.md)** -- Discoverable. Resolve a consequential technical uncertainty with a small falsifying check and independent correctness oracle. Result: evidence that changes or narrows an implementation decision. Any experiment remains subject to the task's authorization and resource limits.
- **[$onepersonlabs:build-understanding](../skills/build-understanding/SKILL.md)** -- Discoverable. Explain a complex system, teach a concept, or shape a human decision flow when relationships or choices are hard to grasp. Result: a representation or worked example matched to the reader's task. Simple exchanges remain simple.
- **[$onepersonlabs:design-perceptual-interfaces](../skills/design-perceptual-interfaces/SKILL.md)** -- Discoverable. Design or critique consequential visual meaning, interaction, or semantic motion. Result: a design grounded in rendered product evidence and checked against its intended meaning. Requires an observable product or specimen for claims about implementation; an image concept alone is not implementation evidence.

## Collaborate and resume

- **[$onepersonlabs:human-collaboration](../skills/human-collaboration/SKILL.md)** -- Discoverable. Prepare and integrate requested human contributions, questions, reviews, or feedback on a running page. Result: a retained submission integrated by its owner with an explicit outcome. Substantive participation uses the shared authenticated inbox service; saving a draft does not submit it. Draft-only requests use `$onepersonlabs:write`; explicit invocation of this skill retains its inbox workflow.
- **[$onepersonlabs:adhd](../skills/adhd/SKILL.md)** -- Discoverable. Applies automatically when the user describes overwhelm, mental exhaustion, difficulty following explanations, or trouble starting or resuming work. No ADHD label or explicit skill request is needed. Recover available context, answer the central question, and keep one useful active path without reducing the requested scope. The user can opt out with `normal mode` or `stop ADHD mode`.
- **[$onepersonlabs:session-reader](../skills/session-reader/SKILL.md)** -- Discoverable. Find prior Codex messages or extract a focused transcript range. Result: bounded history evidence with its source and location. Requires accessible canonical Codex session history; it does not rebuild a repository's complete history.
- **[$onepersonlabs:session-history-rebuild](../skills/session-history-rebuild/SKILL.md)** -- Explicit. Reconstruct a complete, auditable repository conversation and evolving design history. Result: a source-anchored chronology with evidence limits. Requires the canonical session sources and an explicit reconstruction request; focused lookups use `$onepersonlabs:session-reader`.

## Configure Codex and diagnose integrations

- **[$onepersonlabs:configure-harness](../skills/configure-harness/SKILL.md)** -- Discoverable. Inventory one Codex home, prepare a reversible capability/configuration change, or diagnose host input. Result: a sourced inventory and reviewed change plan, with an application receipt if applied. Requires the selected Codex home and repository; availability does not prove a tool is installed, enabled, authenticated, or callable.
- **[$onepersonlabs:restart-codex-desktop](../skills/restart-codex-desktop/SKILL.md)** -- Discoverable. Reload Desktop after plugin or configuration changes, optionally reopening an existing chat and submitting one authorized continuation. The agent arms an independent Windows helper, then invokes the app's observed Quit control through supported computer-use. The helper verifies exit and relaunches the app. Choose a fresh chat when new initial context is needed. Queue acceptance does not prove resumed work; other platforms need a verified native route.
- **[$onepersonlabs:codex-hook-debug](../skills/codex-hook-debug/SKILL.md)** -- Discoverable. Diagnose hook discovery, trust, execution, output, or continuation failures across user, repository, and plugin layers. Result: a verified cause and repair in the owning layer. Requires the triggering event and active Codex environment; Git and React hooks are out of scope.
- **[$onepersonlabs:update-instructions](../skills/update-instructions/SKILL.md)** -- Explicit. Check and replace outdated global OnePersonLabs instructions. Result: a verified installed baseline and a dated byte-exact backup when replacement occurs. Replacement discards custom rules rather than merging them; established authorization applies, or the skill asks once.
- **[$onepersonlabs:camofox-browser](../skills/camofox-browser/SKILL.md)** -- Discoverable. Control an existing Jo CamoFox browser through its REST API. Result: navigation or page interaction using current snapshots and element references. Requires the installed, authenticated Jo service and its owned launcher; Windows/WSL visible mode needs the matching browser binary and display.
- **[$onepersonlabs:camofox-cli](../skills/camofox-cli/SKILL.md)** -- Discoverable. Use the `camofox` terminal command from the redfox CamoFox package. Result: command-driven navigation, snapshots, interaction, or saved-session work. Requires that package's CLI and its configured server; the Jo REST integration uses `camofox-browser` instead.

## Research, writing, and review of agent behavior

- **[$onepersonlabs:last30days](../skills/last30days/SKILL.md)** -- Discoverable. Research recent reactions, recommendations, comparisons, or source health across supported services. Result: a cited synthesis with actual source coverage and saved-artifact location. Requires Python 3.12+ and usable configured sources; it is not for timeless general research.
- **[$onepersonlabs:slop-buster](../skills/slop-buster/SKILL.md)** -- Explicit. Capture an identified agent incident or audit selected session history and maintain evidence-backed detectors. Result: source-anchored findings and resumable coverage, or one captured incident. Corpus runs require the configured private evidence repository; review modes use model assistance. Hooks are advisory.
- **[$onepersonlabs:unslop](../skills/unslop/SKILL.md)** -- Explicit. Trace one identified agent failure and, when useful, compare instruction corrections through replay. Result: causal analysis labeled as replay-tested or reasoned without replay. Requires a specific incident; replay needs supported session tooling. Task-specific verification follows the shared policy, while broader replay requires separate authorization.

## Invocation notes

The explicit skills are `$onepersonlabs:adversarial-review`, `$onepersonlabs:debug`, `$onepersonlabs:handoff`,
`$onepersonlabs:session-history-rebuild`, `$onepersonlabs:slop-buster`,
`$onepersonlabs:unslop` and `$onepersonlabs:update-instructions`. Name them in
the request.

All other listed skills are marked discoverable in their package metadata.
Codex may select one when its description fits, or you may name it directly.
Invocation does not itself authorize external writes, human outreach, paid
services, or experiments; the skill and current task determine their limits.
