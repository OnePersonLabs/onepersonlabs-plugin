---
name: write
description: Write or revise prose, emails, questionnaires, UI text, documentation, specifications, plans, GitHub issues, and agent instructions. Apply shared drafting rules and automatically add the relevant precision, documentation, editing, or concise-reply guidance.
---

# Write

## Universal drafting foundation

Write like a knowledgeable person with something specific to say. Prefer concrete
facts, ordinary verbs, varied rhythm, and the voice appropriate to the reader.
Remove generic significance, promotional padding, canned contrasts, vague
attribution, and chatbot residue instead of replacing flagged words with synonyms.
Apply this foundation to all writing, including chat, UI text, correspondence,
documentation, specifications, plans, and agent instructions. Preserve facts,
conditions, exceptions, uncertainty, requirement strength, and exact technical
strings. Keep useful nuance, the author's voice, and the requested language,
format, spelling convention, and length. A clean sentence needs no cosmetic rewrite.
Avoid needless corrective framing and uniform clipped rhythm; retain corrections
and qualifications that change the meaning or the reader's decision.

Last source review: `2026-10-31`. On the first use 30 or more days after that date,
read [source maintenance](references/maintenance.md) and complete its due-check
workflow before drafting. Do not make a source request before the interval expires.
The same maintained foundation appears in the plugin `AGENTS.md`.

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
is what matters. Introduce unfamiliar concepts before relying on their names.

Use prose for reasoning, lists for parallel items or steps, and tables for
comparisons. Headings and emphasis should help navigation. Keep terminology
consistent. Authored text must make sense without this conversation; keep the
account of drafting and review in the conversation.

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

For UI text, inspect the actual state, surrounding controls, available action,
and recovery. Use concise labels
and fragments where the interface calls for them. Do not promise unsupported
behavior. Check rendered fit and interaction through the existing design workflow
when those affect meaning. Creative work retains intentional rhythm, repetition,
ambiguity, and character voice; generic editing rules do not override its purpose.

Comments and docstrings explain relied-on behavior, constraints, non-obvious
effects, and decisions the code cannot explain. Keep local reasons near the code.
Commits and PRs describe the net change and reason; PRs include relevant validation
and limits. Issues distinguish observed from expected behavior and facts from
suspected causes. Plans distinguish decisions from assumptions and open questions.
Reports develop claims from evidence and keep limits beside the claims they qualify.

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
