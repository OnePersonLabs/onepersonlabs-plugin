---
name: write
description: Write or revise prose, emails, questionnaires, UI text, documentation, specifications, plans, GitHub issues, and agent instructions. Apply shared drafting rules and automatically add the relevant precision, documentation, editing, or concise-reply guidance.
---

# Write

## Universal drafting foundation

Start with what the reader is trying to understand or do. Lead with the answer,
useful action, or result and its practical meaning. Explain concrete behavior and
relationships before introducing unfamiliar internal names. Omit implementation
and test vocabulary unless it changes the reader's understanding or next action.
When needed, explain what happens or what was checked and why it matters to their
goal. Generic substitutes for technical names do not supply that explanation.
If the facts are insufficient, omit nonessential detail or inspect its source;
do not invent a concrete explanation. Use informative
headings that reveal the section's point or task; remove empty teasers. Select
facts, examples, and structure for the reader's goal, not the writer's inventory.
Apply this foundation to all writing, including chat, UI and page text, reports,
correspondence, documentation, specifications, plans, and agent instructions.

Cut content that does not help the reader understand, decide, or act. Remove
ceremony, repetition, generic significance, promotional padding, canned contrasts,
vague attribution, and chatbot residue instead of swapping words for synonyms.
Link supporting detail when the reader does not need it in the main path. Prefer
concrete facts, ordinary verbs, natural grammar, varied rhythm, and the voice
appropriate to the reader. A clean sentence needs no cosmetic rewrite.

Keep the facts, causal relationships, conditions, exceptions, uncertainty,
requirement strength, and exact technical strings that make a claim true. Distinguish
current capability, verified results, recommendations, and unfinished work. Do not
turn a limited result into a finished capability by shortening it. Retain useful
nuance, meaningful qualifications, the author's voice, and the requested language,
format, spelling convention, length, and depth. Clarity must preserve technical precision.

Last source review: `2026-10-31`. On the first use 30 or more days after that date,
read [source maintenance](references/maintenance.md) and complete its due-check
workflow before drafting. Do not make a source request before the interval expires.
The same maintained foundation appears in the plugin `AGENTS.md`. Its additional
clarity sources and the limits of mechanical checking are recorded in
[clarity evidence](references/clarity.md).

## Select additional guidance automatically

Infer the reader, purpose, medium, source constraints, and intended action from
the task and surrounding artifact. Ask only when missing context changes the
result. Apply each relevant layer; selecting one never disables the foundation.

- **Every assistant reply and progress update, including routine replies:** read
  [Caveman concision](references/caveman.md) before the first reply and reuse it
  while its contents remain in context. Apply its rules and before-and-after
  examples without requiring a user request. This layer controls the assistant's surrounding
  commentary, not the voice of an email or document it delivers.
- **Agent-consumed or operational text:** read
  [technical English](references/technical-english.md) before authoring or revising
  specs, implementation plans, `AGENTS.md`, skill entrypoints and references,
  prompts, tool descriptions, assignments, handoffs, GitHub issue requirements,
  decisions, acceptance criteria, procedures, or recovery instructions.
- **Short work reports, including rolling-wave checkpoints:** use
  [concise-report mode](#concise-report-mode). Also select it when the user or
  another skill explicitly requests this mode.
- **Documentation creation or substantive updates:** read
  [the complete documentation workflow](references/documentation.md) before
  drafting. Trace current behavior and finish the reader's journey. Add technical
  English for instructions. Prose editing does not replace this workflow.
- **Prose rewrite or audit:** read [the signs catalogue](references/signs.md).
  For local rewrites, run `scripts/check_ai_signs.py` on the completed changed
  text during final validation. Use an earlier scan only for a requested audit
  or comparison, or when its result will guide the revision. Reuse a valid scan.
  Drafting alone needs neither the catalogue nor a scanner run.
- **Source refresh:** read [source maintenance](references/maintenance.md) when
  due or explicitly requested. Update the shared foundation and its consumers
  together, rather than treating the catalogue as the only maintained surface.

Use the active platform's Python: `python -B -X utf8` on Windows, `python3` on
POSIX. Run scripts from this skill directory or use their absolute paths.

## Compose for the actual reader

Choose vocabulary, depth, tone, and structure for what the reader knows and needs.
Build from familiar information to the new point. Keep related words together,
subjects near verbs, and one developed point per paragraph. Use concrete subjects
and active verbs; keep passive voice when the affected object or unknown actor
is what matters. Use established technical terms when the reader knows them and
they carry precise meaning; explain unfamiliar concepts through what they do.

Use prose for reasoning, lists for parallel items or steps, and tables for
comparisons. Use headings that identify an answer, action, or specific subject;
do not make the reader open a section to discover what it is about. Keep terminology
consistent. Authored text must make sense without this conversation; keep the
account of drafting and review in the conversation.

Remove `real` when deleting it leaves the same claim. If it marks a distinction
the reader needs, name the distinction when that is clearer. Skip phrases such
as `the useful promise` that announce the value of a point. State the outcome
or ask the question directly.

For correspondence, preserve the relationship, author's voice, necessary context,
and the request or response the recipient needs.

For a requested questionnaire or question set for another person, separate
preparation context the user can supply from facts or decisions the recipient
must provide. Recover available context before asking the user about consequential
gaps, such as audience, purpose, scope or confidentiality. Leave recipient-owned
facts as questions in the deliverable. Give the recipient enough context to answer
independently. Prioritize important questions and keep each independently answerable.
Allow partial answers and explicit uncertainty. When using replies, keep unanswered
questions unresolved if a decision depends on them. Use the requested medium and
destination; do not invent deadlines or effort estimates. Drafting does not
authorize sending or inbox operations.

For UI and page text, start with the user's task and inspect the actual state,
surrounding controls, available action, and recovery. Name the action or outcome
before product architecture or internal names. Use concise labels and fragments
where the interface calls for them. Remove sections, sentences, or labels that
do not help the user complete the task; do not hide necessary limits to make a
page sound simpler. Describe available behavior accurately, including partial
or unavailable capability. Distinguish edits retained in the current view from
edits durably saved; use "saved" only when persistence is established. For errors,
state what failed, its effect on the user's work, and the known recovery action.
If recovery is unknown, say so rather than inventing a step or guarantee.
Check rendered fit and interaction through the existing design workflow
when those affect meaning. Creative work retains intentional rhythm, repetition,
ambiguity, and character voice; generic editing rules do not override its purpose.

Comments and docstrings explain relied-on behavior, constraints, non-obvious
effects, and decisions the code cannot explain. Keep local reasons near the code.
Commits and PRs describe the net change and reason; PRs include relevant validation
and limits. Issues distinguish observed from expected behavior and facts from
suspected causes. Plans distinguish decisions from assumptions and open questions.
Reports develop claims from evidence and keep limits beside the claims they qualify.

## Concise-report mode

Answer the reader's current question about the work. State what changed for
their goal, explain what it does, and distinguish what worked from what remains
unfinished. Lead with what the evidence establishes about the user's goal, rather
than the technical checks themselves. Include preparation, workflow, implementation,
or test details only when they change the conclusion or next action. When a check
matters, say what behavior was checked or what results were compared and why that
supports the claim. Do not replace internal names with vague phrases such as
"numerical setup" or "candidate values." Omit nonessential detail that the supplied
facts cannot explain, or inspect its source; do not infer an explanation from its
name. If headings help, make them carry the finding or task; omit them when a short
paragraph is enough.

State the evidence needed to support the result and any limitation that changes
its meaning or the reader's next action. Link supporting detail when available.
Do not turn an untested change or unfinished check into a success claim.

## Preserve and review

When faithfully rewriting supplied text, keep every fact, number, name, date,
link, condition, and meaningful qualification. Remove padding while preserving
the author's person, spelling, formatting system, and genuine quirks.
For researched answers and summaries, select information relevant to the requested
result. Preserve the accuracy, necessary context, conditions, and qualifications
of included claims; selection must not change requirements or their force.
Keep quotations, titles, legal text, code, identifiers, and commands unchanged
unless changing them is the explicit task. Do not invent details to make prose
concrete.

The de-AI scanner accepts files, directories, or `-` for stdin; `--summary` adds
counts. It finds advisory mechanical signals, not authorship or writing quality.
After editing, read the whole piece for generic structure, unnecessary summaries,
synonym cycling, and unwarranted contrasts. Keep scanner hits when quoted, literal,
required by the context, or the clearest wording. Precision wins over compression.

Lead with finished prose or edited files. For an audit, report the relevant
findings, representative changes and deliberate remaining hits. Include
before/after counts only when that comparison was part of the audit.
Distinguish source review, exercised behavior, and human comprehension.
