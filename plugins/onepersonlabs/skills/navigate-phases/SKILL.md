---
name: navigate-phases
description: Navigate multi-phase work with rolling-wave planning, a branching course chart, and checkpoint stories. Use when the user requests phase-by-phase execution, replanning checkpoints, or a retrospective that leads into the next phase.
---

# Navigate phases

Keep the destination visible, plan the next leg, and return to the human at each
agreed checkpoint. Use rolling-wave planning: distant phases retain only the
detail needed to show the route and consequential dependencies. Make the next
phase executable. A phase boundary does not reduce the intended capability.

## Plot in actual Plan Mode

Read the host's current collaboration mode. Initial plotting, replanning, and
detailed planning of the next phase require actual Plan Mode. If it is not active,
request that the user switch modes. Until the host confirms Plan Mode, inspect
existing work and report its retrospective; leave the new course unplotted.
User approval, a heading, and a tool invocation do not establish a mode change.

In Plan Mode, recover the intended outcome, accepted constraints, current work,
and existing roadmap from their owners. Keep later phases broad. Detail the next
phase's behavior, connected consumers, interfaces, acceptance, verification,
resource constraints, and stopping point. Resolve decisions that affect its
execution. Preserve requirements and account for substantive changes in course.
Present the plan through the host's normal planning interface.

## Execute one agreed phase

Begin only when the phase is authorized and the host permits implementation.
Finish the connected behavior and required checks. Keep routine repairs inside
the phase. If new evidence invalidates its approach, stop dependent work and
return to the Plan Mode gate before replanning.

Keep tightly coupled work with one owner. Use existing delegation and review
guidance when independent work helps. Preserve the selected root model; escalate
only for a concrete unresolved decision under the current authorization.

## Return with the story

After verification and review repairs, use
[$onepersonlabs:optimize-workflow](../optimize-workflow/SKILL.md) to account for
the work and change the next batch where evidence supports it. Use
[$onepersonlabs:write](../write/SKILL.md) for the explanation.

Read [checkpoint delivery](references/checkpoint.md) when preparing the story and
chart. Present what happened, what now works, the evidence limits, and what the
experience changes. Keep unknown time and usage unknown. Compare phases only
when their measurements are comparable.

Stop at the agreed human checkpoint. Do not treat a proposed next phase as
authorization to execute it. If Plan Mode is inactive, request it before plotting
the next course. Reuse the same work owners and chart when continuing.

Project meaning, decisions, and task status remain with their existing owners.
The chart presents those records; it is not a second task registry. This skill
starts no service, scheduler, background runner, or model configuration change.
