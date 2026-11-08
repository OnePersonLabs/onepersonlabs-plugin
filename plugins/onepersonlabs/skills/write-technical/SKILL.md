---
name: write-technical
description: Write developer-facing answers, findings, progress updates, and delivery reports. Also write specifications, requirements, plans, procedures, acceptance criteria, code comments, docstrings, issues, and PR descriptions. Apply clear technical English while preserving exact meaning.
---

# Explain technical work clearly

Apply the shared drafting foundation in the applicable OnePersonLabs AGENTS.md.
This skill owns expression and semantic precision. The work's existing owner
retains product decisions, planning, authority, review and delivery.

Read [technical English](references/technical-english.md) before writing any of
the covered text. For developer-facing responses, also read
[concise response examples](references/concise-responses.md) once and reuse them
while available in context. The examples guide surrounding answers and progress
updates; an embedded artifact retains its own audience and voice.

## Answer the actual question

Start with what the result means for the developer's goal. Explain what changed
through what it does, whether it worked and what remains unfinished when those
facts answer the question. Include implementation and check details only when
they change understanding, the conclusion or the next action. Explain a necessary
check through what behavior it tested. Do not substitute generic labels such as
"the setup" for missing facts. Inspect an essential unexplained detail or omit it
when it is unnecessary; do not infer meaning from its name.

Keep the cause that makes an explanation useful. Report current capability,
verified results, recommendations and unfinished work distinctly. Do not append
disclaimers about claims the answer never made. Link supporting detail when it
does not belong in the main answer. End on the last useful point.

When asked why the agent acted a certain way, identify the governing instruction
or code, quote its relevant wording and link the source. Explain its effect on
the action and distinguish recorded cause from inference. For a restriction or
requirement, state its owner, trigger, required action and effect on the request;
use a concrete example when the consequence is unclear. Follow AGENTS.md's
correction-and-steering rule when repairing an explanation.

## Match the artifact

Requirements, specifications, plans, procedures and instructions state conditions,
actors and outcomes precisely. Derive acceptance criteria from authorized behavior;
identify missing decisions instead of inventing guarantees or extra requirements.
Plans distinguish decisions, assumptions and open questions. Keep actual planning
and review with their existing workflow owners.

Comments and docstrings explain relied-on behavior, constraints and decisions the
code cannot explain. Keep local reasons near the code. Commits and PRs describe
the net change and reason; PRs include relevant validation and limits. Issues
distinguish observed and expected behavior, facts and suspected causes. Reviews
name the exact behavior, evidence and requested action.

For an instruction system, use $onepersonlabs:write-agent-instructions as the
authoring owner; this skill supplies its precision guidance. Documentation uses
$onepersonlabs:write-documentation. UI controls use $onepersonlabs:write-ui;
their labels can be fragments. Required structured results keep their exact
schemas and enum values. Apply writing guidance inside text fields, without
decorative prefixes or Markdown fences around machine-readable output.

Check the result with the reference's applicable lint mode for saved artifacts.
For chat, self-check meaning and wording without creating a file merely to lint it.
