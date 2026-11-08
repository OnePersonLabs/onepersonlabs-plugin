---
name: write
description: Draft or revise emails, messages, articles, proposals, questionnaires, and general prose. Use for faithful edits, summaries, and prose-quality audits. Scope excludes product documentation, interface copy, technical specifications, and agent instructions.
---

# Write for the intended reader

Apply the shared drafting foundation in the applicable OnePersonLabs AGENTS.md.
Infer the reader, purpose, medium, source constraints, and intended action from
the request and surrounding artifact. Recover available context before asking
about a gap that would change the result.

Choose the owner by the artifact's purpose, including during rewriting and audits:
guides and reference material use $onepersonlabs:write-documentation; application
controls and states use $onepersonlabs:write-ui; technical requirements, procedures
and developer responses use $onepersonlabs:write-technical; agent instruction
systems use $onepersonlabs:write-agent-instructions. Work on mixed artifacts through
the appropriate sections without starting duplicate authoring workflows.

## Draft and edit

Organize the piece around what the reader needs to understand or do. Build from
familiar information to the new point. Keep related words together, subjects near
verbs, and one developed point per paragraph. Keep passive voice when the affected
object or unknown actor matters. A clean sentence needs no cosmetic rewrite.

For correspondence, preserve the relationship, author's voice, necessary context,
and the request or response the recipient needs. For creative work, preserve
intentional rhythm, repetition, ambiguity and character voice.

For faithful edits, preserve supplied facts, numbers, names, dates, links,
conditions and meaningful qualifications. For summaries or requested restructuring,
remove information the reader does not need while keeping the resulting account
accurate. Preserve the conditions and distinctions that make its claims true.
Keep quotations, titles, legal text, code, identifiers and commands exact unless
changing them is the task. Do not invent details to make prose concrete.

For questionnaires, separate preparation context the user can supply from facts
or decisions the recipient must provide. Recover context before asking the user
about audience, purpose, scope or confidentiality. Leave recipient-owned facts as
questions. Supply enough context to answer independently; prioritize important
questions and keep each independently answerable. Allow partial answers and
explicit uncertainty. Keep unanswered questions unresolved when decisions depend
on them. Honor the requested medium and destination without invented deadlines
or effort estimates. Drafting does not authorize sending or inbox operations.

## Review the piece

For a general-prose rewrite or style audit, read [the signs catalogue](references/signs.md).
Run `scripts/check_ai_signs.py` on completed changed local text during final
validation. Drafting alone requires neither the catalogue nor a scan. Specialist
edits use their owner's checks; load this catalogue for a requested prose-style
audit, not automatically for every technical or UI edit. Use an earlier scan only
when it will guide an audit or revision; reuse valid results.

The scanner accepts files, directories or `-` for stdin; `--summary` adds counts.
Its signals are advisory. Read the whole piece for unnecessary structure,
repetition, vague labels and missing meaning. Keep a finding when the wording is
quoted, literal, required or clearest in context. It cannot establish authorship,
factual completeness or comprehension. See [clarity evidence](references/clarity.md)
when reviewing the basis of these judgments.

Lead with finished prose or edited files. For audits, report consequential
findings, representative changes and deliberate remaining hits. Include scan
counts only when comparison was requested. Distinguish source review, exercised
behavior and human comprehension.

## Maintain the catalogue

Last source review: `2026-10-31`.

During catalogue-based rewriting or audits, read [source maintenance](references/maintenance.md)
when that date is at least 30 days old. Also use it for an explicit source-refresh
request. Ordinary drafting and developer replies do not initiate maintenance.
Use `python -B -X utf8` on Windows or `python3` on POSIX, from this skill directory
or with absolute script paths.
