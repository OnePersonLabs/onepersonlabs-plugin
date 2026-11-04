# Subagent usage and configuration

Use this guidance when choosing or diagnosing subagent models, effort, context,
cost or coordination. OnePersonLabs owns the complete workflow without another
plugin. Checked on 2026-11-01 against installed Codex
0.166.0, Desktop 0.166.0-alpha.5.1, their relevant source, the current tool
contract, and the sources below.
Recheck affected claims after a host, model, tool-contract or configuration change.
No source establishes one universally fastest or cheapest agent arrangement.

Use the existing conversation and project work owner. When Conductor is installed
and in use, it can own project job coordination; this guidance does not start its
runner. When Conceptor is installed and in use, it owns accepted meaning and
reassessment. Neither plugin is required for assignments, integration or review.

## Choose the work and context together

| Situation | Starting choice | Tradeoff to inspect |
| --- | --- | --- |
| A collaborator continues an established design or investigation | Inherit relevant parent history | Preserves decisions and their reasons, but also inherits irrelevant material and the parent's assumptions |
| Independent planning | Start fresh with requirements, accepted decisions and evidence pointers | The brief must preserve reasons and authority that the parent transcript would otherwise supply |
| Independent review | Start fresh with requirements, baseline, stable diff and source pointers | Reduces anchoring on the builder's conclusions; omitted requirements can produce wrong findings |
| A self-contained lookup or mechanical task | Start fresh with a complete assignment | Saves unnecessary context; the assignment must contain everything that changes the answer |
| A change depends on an unsettled shared interface | Keep one decision owner until that interface is settled | Adding writers before then increases incompatible decisions and repair work |
| A worker repeatedly lacks facts or returns incorrect work | Diagnose the missing context, interface, evidence or capability | A larger model cannot repair a contradictory assignment; a smaller model is not cheaper when repeated corrections dominate |

Cognition reports both full-context specialist consultation and fresh independent
review as useful production patterns. It also reports failures when a weaker
coordinator cannot ask the right question. These are engineering observations,
not a controlled Codex cost comparison.
[Cognition, April 2026](https://cognition.com/blog/multi-agents-working)

Give each assignment the outcome, relevant reasons and constraints, settled
interfaces, affected consumers, write ownership, evidence required and stop
condition. A fork avoids rewriting the entire discussion; it does not excuse a
vague task. Workers should ask for a missing decisive fact instead of inventing
it. Anthropic observed misinterpretation and duplicated searches from weak briefs.
[Anthropic's research system](https://www.anthropic.com/research/multi-agent-research-system)

Select `fork_turns: "none"` explicitly for a fresh native child; the current
host defaults to inherited history. An App Server `thread/start` without a
parent transcript supplies a fresh initial worker. Related follow-ups and
repairs can resume that worker's own session. Calling an assignment independent
does not itself change the host's context selection.

## Coordinate the complete change

Separate decomposition from delegation: a plan's subtask boundary does not
require another agent. Keep dependent steps inline unless delegation supplies
useful independence, specialization or context isolation.

Map connected consumers and failure paths before splitting implementation.
Delegate independent evidence gathering while the root settles shared decisions.
Parallel writers need disjoint ownership and a known integration order. Treat the
thread limit as available capacity, not a number of workers to fill. Nested
delegation must preserve these ownership boundaries and the root's ability to
account for descendants.

Inherited history is a starting snapshot. Notify affected workers when a new
finding changes their interface, requirement, or causal hypothesis. Shared files
do not communicate the reasons behind an edit. Reuse a worker while its retained
context remains relevant; choose fresh context when independence or irrelevant
history warrants it. Return conclusions, source anchors, changed files, checks
and unresolved facts instead of dumping raw logs into the parent.

Before returning a tool result to model context, select the fields or diagnostic
range needed for the decision. When a coherent subtask finishes, preserve its
result, reasons, source anchors and unresolved dependencies for the remaining
work. Use supported host context mechanisms; do not rewrite transcripts or add
an archive/controller to imitate a research harness. A downstream consumer must
check a consequential fact at its source when a summary could have omitted a
condition that changes the answer.

Recent experiments support these distinctions. Spine improved results and cost
against a recursive baseline in one tested coding setup, but it is a substantial
runtime modification, and another setting cost more than native Codex. The
Skills comparison changed direction depending on the quality of task interfaces.
MS-Eval found both orchestration overhead and errors propagated through summaries.
These results do not establish a universal agent count or justify installing a
replacement harness here.
[Spine](https://arxiv.org/html/2610.37224v1),
[Subagents vs Agent Skills](https://arxiv.org/html/2609.09233v1),
[MS-Eval](https://arxiv.org/html/2610.22869v1)

Start independent review after the reviewed scope stops changing. The root
reconciles each finding against the full task, resolves disagreements with
evidence, integrates the result and checks the connected behavior. A worker's
success report is evidence to verify. Component passes cannot establish the
integrated outcome. After two failed repair cycles on the same observable problem,
apply the existing reassessment rule before more dependent edits.

Anthropic's compiler experiment shows the boundary: parallel work helped where
tasks were separable, while agents duplicated effort on a shared blocking bug.
Its experience also supports concise diagnostic output and meaningful end-to-end
verification. It does not establish a universal worker count.
[Anthropic compiler experiment](https://www.anthropic.com/research/building-c-compiler)

Use native completion notifications. A wait timeout means the observation ended;
it is not proof that a worker stopped. Check the existing handle before retrying
or replacing it. Stop obsolete writers and reconcile their outstanding operations
before transferring ownership. Interrupting an agent does not undo its edits or
establish that every tool-launched process has stopped.

## Model and configuration side effects

The current spawn contract defaults to `fork_turns: "all"`; `"none"` starts without
parent history. It restricts explicit model/effort overrides to fresh children.
Released 0.166.0 code resolves each requested model and effort independently,
falling back to its corresponding `agents.default_subagent_model` or
`agents.default_subagent_reasoning_effort` before the fork branch. The selected
role can then override model settings and supply instructions. OnePersonLabs
fills missing child preferences with Luna/high and preserves explicit user
preferences. Keep this inexpensive fallback; select a different model and effort
when the particular task warrants them. Parent history does not itself select
the parent's model.
[Released child configuration](https://github.com/openai/codex/blob/rust-v0.166.0/codex-rs/core/src/agent/child_config.rs#L51-L85)

The Desktop alpha has the same child-configuration implementation. Before reload,
live Desktop evidence included child selections unexplained by on-disk defaults
and the apparent request. After a verified Desktop restart on 2026-11-02, one
authorized fresh default-role child with no model or effort override recorded
Luna/high in its own turn metadata, matching the configured fallback. That check
does not establish full-history fork or role-override behavior. Inspect the active
home, loaded configuration, selected role and a new child's own turn metadata
when actual selection matters. Do not mistake inherited parent turn records for
the child's selected model. Report unresolved runtime selection explicitly.
[Exact Desktop-version source](https://github.com/openai/codex/blob/rust-v0.166.0-alpha.5.1/codex-rs/core/src/agent/child_config.rs#L103-L121)

If the observed model is suitable, accept that choice explicitly for the task.
If a different model is required, use a fresh child with a suitable explicit
model and effort selection and a complete brief, or keep the coupled work with the root. The
current tool contract does not support full history plus an explicit model
override. Do not keep respawning the same assignment to chase an assumed model.

Choose model and reasoning effort deliberately for the worker's responsibility.
Luna/high is the inexpensive fallback, not a requirement to spend high effort on
every bounded task. Fresh Luna work can suit a complete lookup, mechanical change
or bounded review. Sol can suit demanding work with multiple dependent decisions.
Use stronger effort or Astra only for a concrete unresolved reasoning need that
can change the result; a parent running Astra is not that evidence. Include
handoff, reading, correction and integration costs in the choice. Decide context
separately: keep coupled work with the root when a fresh brief would lose decisive
history and the tool cannot combine that history with the required model choice.
Higher reasoning effort can cost time and tokens.
[OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Inspect the active host's configured and effective concurrency limit; treat it as
a ceiling rather than a target. In the checked V2 implementation, concurrency
accounting adds the root internally. V2 ignores
the V1 `agents.max_depth` setting; do not add it as an effective recursion guard.
`preserve_fork_prefix` already defaults to true. Wait settings control observation
intervals, not worker deadlines. Preserve specialized OnePersonLabs roles for
their declared jobs; they are not general-purpose worker defaults.
[Released configuration schema](https://github.com/openai/codex/blob/rust-v0.166.0/codex-rs/core/config.schema.json)

Workers inherit the parent's effective permissions. A role described as read-only
is an instruction, not a separate sandbox. Honor the active host's approval and
tool rules. Inspect effective configuration when it differs from the file or tool
description; an existing Desktop chat can retain an earlier configuration.
[OpenAI permissions and custom roles](https://learn.chatgpt.com/docs/agent-configuration/subagents#approvals-and-sandbox-controls)

## Cache behavior that changes decisions

Root and descendants normally share a session identity and cache-routing group,
while retaining different thread IDs. The upstream regression test checks both
the session header and prompt-cache key. A fresh worker can still reuse common
instructions; a full fork can preserve much more of the conversation prefix.
[Released routing regression test](https://github.com/openai/codex/blob/rust-v0.166.0/codex-rs/core/tests/suite/prompt_cache_key.rs#L100-L225)

| Mechanism | Consequence |
| --- | --- |
| Cache matching uses the unchanged rendered prefix, including instructions and tools | Similar meaning or a shared session does not guarantee a hit |
| A different model uses different model state | Do not assume a cheaper model can reuse the parent's model cache |
| Tool, instruction, relevant setting or early-history changes can alter the prefix | Keep correct shared context stable; append task-specific updates when the host supports it |
| Compaction changes the prefix | It can reduce reuse and still lower total cost by reducing irrelevant input |
| Cache entries and routing are finite resources | Eligibility does not establish an actual hit or latency gain |
| Cached input remains context; new output is generated | Caching does not eliminate context limits, reasoning cost or incorrect conclusions |

Avoid padding prompts, retaining irrelevant history, delaying necessary compaction
or keeping the wrong model merely to raise a cache percentage.
[OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

Codex 0.166.0 exposes no user TOML setting for cache keys, retention or API cache
options. Do not copy API TTL settings into this configuration or add a cache
wrapper. The host owns routing. API write prices and retention controls are not
Codex subscription controls.
[Released request fields](https://github.com/openai/codex/blob/rust-v0.166.0/codex-rs/codex-api/src/common.rs#L280-L307)

Codex publishes discounted cached-input credit rates and has no separate cache
write charge. It also states that credit prices alone do not determine included
subscription usage. Do not promise a subscription saving from a cache-eligible
fork. Judge total task cost and successful completion, including parent and child
input/output, generated handoffs, retries, review, repairs and integration.
[Codex pricing](https://learn.chatgpt.com/docs/pricing)

Existing usage counters can show reported cached input. They cannot identify
which parent's prefix caused a hit or establish a counterfactual saving. Keep
per-call and cumulative counters distinct; do not sum repeated cumulative
snapshots. A fair performance comparison also needs equivalent tasks and final
correctness. No such comparison is established by this policy.
[Released usage conversion](https://github.com/openai/codex/blob/rust-v0.166.0/codex-rs/codex-api/src/sse/responses.rs#L130-L147)

## Red flags during long work

- Workers are assigned spot edits before their shared contract and consumers are known.
- A fresh assignment omits a rejected approach or the reason for a constraint.
- Several workers make the same cross-cutting decision independently.
- The parent repeats delegated exploration or accepts summaries without their evidence.
- Review starts against changing files, or a reviewer inherits the builder's verdict.
- New workers, tests or broad fixers repeat the same unsuccessful repair hypothesis.
- Dependent steps become a serial chain of agents without useful specialization or context isolation.
- A downstream worker treats a lossy summary as complete authority for a consequential decision.
- A timeout causes a duplicate launch without checking the original operation.
- Lower per-token prices, more workers or a high cache-hit percentage are treated as proof of lower total cost.

At these signals, correct the assignment, owner or hypothesis before adding work.
Use the existing conversation or project issue for decisions, sources and unfinished work. Do not create
a transcript archive, recurring benchmark or new task ledger for this policy.

Configuration changes and rollback files remain with their existing owner.
Use configure-harness transactions only within their supported scope; root model
preferences remain outside the startup-baseline transaction. Retire temporary
probes after their verification consumer finishes. Preserve unresolved recovery
state until reconciled, then use its owning cleanup operation.
