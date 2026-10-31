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

- **[$onepersonlabs:write](../skills/write/SKILL.md)** -- Discoverable. Write or revise text with universal drafting rules and automatically selected guidance for concise replies, technical precision, documentation, and editing. Documentation uses the full source-grounded reader workflow. The old `de-ai-writing`, `simplified-technical-english`, and `write-docs` names remain explicit compatibility entrypoints.
- **[$onepersonlabs:debug](../skills/debug/SKILL.md)** -- Explicit. Diagnose a concrete failure and, when requested, verify a causal fix. Result: a supported cause, counterevidence, and original-scenario verification. A symptom or passing test alone does not establish the cause.
- **[$onepersonlabs:test-driven-development](../skills/test-driven-development/SKILL.md)** -- Explicit. Use a red-green-refactor loop for an observable behavior. Result: a meaningful test-first change with honest reporting of whether tests came before the implementation. It is optional and follows the repository's test policy.
- **[$onepersonlabs:adversarial-review](../skills/adversarial-review/SKILL.md)** -- Explicit. Audit a plan, architecture, instruction system, or agent workflow for concrete failure paths. Result: prioritized findings tied to evidence and a plausible failure scenario. Routine code diffs use the native review path.
- **[$onepersonlabs:agent-instructions](../skills/agent-instructions/SKILL.md)** -- Discoverable. Author, consolidate, audit, or score agent instructions and skill packages. Result: the requested instruction artifact or a scoped review; a score is not a runtime behavior test.
- **[$onepersonlabs:handoff](../skills/handoff/SKILL.md)** -- Explicit. Prepare a compact continuation document for a fresh agent. Result: a temporary handoff with current ownership, permission boundaries, decisions, evidence, and recovery state. It does not start a new session.
- **[$onepersonlabs:refresh-local-plugins](../skills/refresh-local-plugins/SKILL.md)** -- Discoverable. Refresh selected changed plugin sources in existing Windows and WSL user homes. Result: per-home install and hook-trust status, plus any remaining failure. Requires a source checkout, Node.js, Codex plugin commands, and the human-collaboration pause/resume procedure when that service is in use. Publishing is separate.
- **[$onepersonlabs:long-command-wakeup](../skills/long-command-wakeup/SKILL.md)** -- Discoverable. Queue one continuation after a safe local command that is demonstrably expected to run for more than about two minutes. Result: a retained command log and one completion request. Requires Python 3.11+ and `codex queue`; do not use for interactive, approval-dependent, destructive, or natively waitable work.
- **[$onepersonlabs:route-agent-question](../skills/route-agent-question/SKILL.md)** -- Discoverable. Route a child agent's blocked question to its parent and return the scoped answer. Result: a decision or clarification delivered through the assignment owner. Requires an active parent assignment; only the root asks the user.

## Choose and understand an approach

- **[$onepersonlabs:research-solutions](../skills/research-solutions/SKILL.md)** -- Discoverable. Find and assemble current reference implementations for consequential tool, architecture, infrastructure, or integration choices. Result: source-linked options and compatibility or recovery findings. Requires current external evidence; it is unnecessary for routine repairs.
- **[$onepersonlabs:develop-alternatives](../skills/develop-alternatives/SKILL.md)** -- Discoverable. Develop concrete competing approaches when a consequential choice needs design work. Result: distinct mechanisms, assumptions, and trade-offs for the current owner to decide. It can pass a settled choice to `$onepersonlabs:pov`.
- **[$onepersonlabs:pov](../skills/pov/SKILL.md)** -- Discoverable. Form a source-grounded position on a supplied decision. Result: a recommendation with reasons, alternatives, and conditions that would change it. It does not invent missing product goals.
- **[$onepersonlabs:optimize](../skills/optimize/SKILL.md)** -- Discoverable. Compare changes to a working system when the best measurable option is unknown. Result: a measurement-based decision against a current baseline, correctness gates, and required trade-offs. Requires a meaningful workload, metric, and oracle; it does not turn noisy results into a win.
- **[$onepersonlabs:solve-novel-software](../skills/solve-novel-software/SKILL.md)** -- Discoverable. Resolve a consequential technical uncertainty with a small falsifying check and independent correctness oracle. Result: evidence that changes or narrows an implementation decision. Any experiment remains subject to the task's authorization and resource limits.
- **[$onepersonlabs:build-understanding](../skills/build-understanding/SKILL.md)** -- Discoverable. Explain a complex system, teach a concept, or shape a human decision flow when relationships or choices are hard to grasp. Result: a representation or worked example matched to the reader's task. Simple exchanges remain simple.
- **[$onepersonlabs:design-perceptual-interfaces](../skills/design-perceptual-interfaces/SKILL.md)** -- Discoverable. Design or critique consequential visual meaning, interaction, or semantic motion. Result: a design grounded in rendered product evidence and checked against its intended meaning. Requires an observable product or specimen for claims about implementation; an image concept alone is not implementation evidence.

## Collaborate and resume

- **[$onepersonlabs:human-collaboration](../skills/human-collaboration/SKILL.md)** -- Discoverable. Prepare and integrate requested human contributions, questions, reviews, or feedback on a running page. Result: a retained submission integrated by its owner with an explicit outcome. Substantive participation uses the shared authenticated inbox service; saving a draft does not submit it.
- **[$onepersonlabs:adhd](../skills/adhd/SKILL.md)** -- Discoverable. Reduce task overload, recover after interruption, or choose one active path when the user asks for that support. Result: one concrete next action with a visible stopping point. This is optional project assistance, not diagnosis or treatment.
- **[$onepersonlabs:session-reader](../skills/session-reader/SKILL.md)** -- Discoverable. Find prior Codex messages or extract a focused transcript range. Result: bounded history evidence with its source and location. Requires accessible canonical Codex session history; it does not rebuild a repository's complete history.
- **[$onepersonlabs:session-history-rebuild](../skills/session-history-rebuild/SKILL.md)** -- Explicit. Reconstruct a complete, auditable repository conversation and evolving design history. Result: a source-anchored chronology with evidence limits. Requires the canonical session sources and an explicit reconstruction request; focused lookups use `session-reader`.

## Configure Codex and diagnose integrations

- **[$onepersonlabs:configure-harness](../skills/configure-harness/SKILL.md)** -- Discoverable. Inventory one Codex home, prepare a reversible capability/configuration change, or diagnose host input. Result: a sourced inventory and reviewed change plan, with an application receipt if applied. Requires the selected Codex home and repository; availability does not prove a tool is installed, enabled, authenticated, or callable.
- **[$onepersonlabs:codex-hook-debug](../skills/codex-hook-debug/SKILL.md)** -- Discoverable. Diagnose hook discovery, trust, execution, output, or continuation failures across user, repository, and plugin layers. Result: a verified cause and repair in the owning layer. Requires the triggering event and active Codex environment; Git and React hooks are out of scope.
- **[$onepersonlabs:update-instructions](../skills/update-instructions/SKILL.md)** -- Explicit. Check and replace outdated global OnePersonLabs instructions. Result: a verified installed baseline and a dated byte-exact backup when replacement occurs. Replacement discards custom rules rather than merging them; established authorization applies, or the skill asks once.
- **[$onepersonlabs:camofox-browser](../skills/camofox-browser/SKILL.md)** -- Discoverable. Control an existing Jo CamoFox browser through its REST API. Result: navigation or page interaction using current snapshots and element references. Requires the installed, authenticated Jo service and its owned launcher; Windows/WSL visible mode needs the matching browser binary and display.
- **[$onepersonlabs:camofox-cli](../skills/camofox-cli/SKILL.md)** -- Discoverable. Use the `camofox` terminal command from the redfox CamoFox package. Result: command-driven navigation, snapshots, interaction, or saved-session work. Requires that package's CLI and its configured server; the Jo REST integration uses `camofox-browser` instead.

## Research, writing, and review of agent behavior

- **[$onepersonlabs:last30days](../skills/last30days/SKILL.md)** -- Discoverable. Research recent reactions, recommendations, comparisons, or source health across supported services. Result: a cited synthesis with actual source coverage and saved-artifact location. Requires Python 3.12+ and usable configured sources; it is not for timeless general research.
- **[$onepersonlabs:slop-buster](../skills/slop-buster/SKILL.md)** -- Explicit. Capture an identified agent incident or audit selected session history and maintain evidence-backed detectors. Result: source-anchored findings and resumable coverage, or one captured incident. Corpus runs require the configured private evidence repository; review modes use model assistance. Hooks are advisory.
- **[$onepersonlabs:unslop](../skills/unslop/SKILL.md)** -- Explicit. Trace one identified agent failure and, when authorized and useful, compare instruction corrections through replay. Result: causal analysis labeled as replay-tested or reasoned without replay. Requires a specific incident; replay additionally needs explicit permission and supported session tooling.

## Invocation notes

The explicit skills are `adversarial-review`, `debug`, `handoff`,
`session-history-rebuild`, `slop-buster`,
`test-driven-development`, `unslop`, `update-instructions`, `de-ai-writing`,
`simplified-technical-english`, and `write-docs`. Name them in
the request.

All other listed skills are marked discoverable in their package metadata.
Codex may select one when its description fits, or you may name it directly.
Invocation does not itself authorize external writes, human outreach, paid
services, or experiments; the skill and current task determine their limits.
