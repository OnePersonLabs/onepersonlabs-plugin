---
name: rolling-wave-workflow
description: Use when multi-phase work needs a broad roadmap, detailed next-phase planning, and human review or replanning checkpoints. Coordinate phase cadence and concise checkpoint reports alongside available implementation and GitHub workflow skills.
---

# Rolling Wave Workflow

Keep the destination visible, plan the next leg, and return to the human at each
agreed checkpoint. Use rolling-wave planning: distant phases retain only the
detail needed to show the route and consequential dependencies. Make the next
phase executable. A phase boundary does not reduce the intended capability.

This is a process skill: plot, implement, review and repair, report, then replot.
Use the applicable step skills for the work inside that process. A routine edit
or issue update alone does not need this workflow.

## Compose the steps

Use only companion skills exposed as available in this session. Installation or
a source checkout does not establish that a disabled plugin is available. If
Conductor is available for the target repository, load its applicable step skill
and pass its repository setup gate before doing Conductor work:

| Activity | Conductor step |
| --- | --- |
| Investigate and plan the next phase | `$conductor:plan` |
| Implement the authorized phase | `$conductor:implement` |
| Independently review the assigned scope | `$conductor:review` |
| Change GitHub issue scope, status, or relationships | `$conductor:manage-issues` |

Conductor owns its repository gate, issue and delivery rules, review ownership,
and runtime controls. This skill owns phase cadence, actual Plan Mode for course
plotting, the checkpoint report, and the return to the human. Produce one plan
and reuse the existing acceptance and work records. Load each applicable skill
once and reuse it; reciprocal pointers are not recursive dispatch instructions.

When Conductor is unavailable or its implicit setup gate fails, continue under
the host and repository instructions without Conductor. Do not require its
installation, enable it, or repair setup merely to use this workflow. An explicit
Conductor invocation still reports its own setup failure. Conductor also works
without this skill; the optional companion does not change standalone behavior.

The coordinating root owns the phase boundary. Delegated builders and reviewers
complete their assigned step and return to that root; they do not initiate a
second roadmap, mode switch, or human checkpoint. Ordinary planning is not a
director request. With existing automation, use its current owner and controls
to honor an agreed boundary; do not start, stop, adopt, or reconfigure it through
this skill. Full automation alone does not select a human-checkpoint process.

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

## Report the phase result

After verification and review repairs, use
[$onepersonlabs:optimize-workflow](../optimize-workflow/SKILL.md) to account for
the work and change the next batch where evidence supports it. Use
[$onepersonlabs:write](../write/SKILL.md#concise-report-mode)'s concise-report
mode for phase reports, including retrospectives of existing work.

Read [checkpoint delivery](references/checkpoint.md) when preparing the report
and chart. Deliver a static, JavaScript-free HTML chart with responsive CSS,
linked cards with SVG branch edges, and native links to the full story. Show
each card's numbered name, description, owner, and status directly in the graph.
Stack graph and supporting report on phones; at 768 pixels and wider, use roughly
equal columns with a 24-pixel gap. Use ordinary
document scrolling without scrollable panels. Preserve the graph on phones
and in print. Explain what the change does, whether it worked, and what remains
unfinished. Include only context and evidence that affect the takeaway or next
decision. Keep unknown time and usage unknown. Compare phases only when their
measurements are comparable.

Distinguish the phase result from issue delivery. Outstanding required review,
publication, or delivery work remains unfinished under its existing owner; a
checkpoint does not close an issue or override a hold.

Stop at the agreed human checkpoint. Do not treat a proposed next phase as
authorization to execute it. If Plan Mode is inactive, request it before plotting
the next course. Reuse the same work owners and chart when continuing.

Project meaning, decisions, and task status remain with their existing owners.
The chart presents those records; it is not a second task registry. This skill
starts no service, scheduler, background runner, or model configuration change.
