# Simplified Technical English for software work

Apply the clarity principles of ASD-STE100 to eligible software prose. This skill changes expression, not product intent. It does not supply missing product decisions or certify formal ASD-STE100 compliance.

## Route by purpose and reader

- **Normative or operational:** For specifications, requirements, plans, acceptance criteria, procedures, and instructions someone must implement or follow, state one action or testable claim at a time. Put conditions before their effects. Name the actor when it matters. Reuse one term for each concept.
- **Developer-facing responses:** For answers, findings, progress and delivery reports, use direct language, clear referents, consistent terms and concise explanations of concrete behavior. Preserve the reason and limitations that change the answer.
- **Implementation guidance:** For technical explanations that guide a design or implementation, use direct verbs and short, coherent paragraphs. Retain the vocabulary needed for precision; do not force a controlled dictionary.
- **Embedded human-facing artifacts:** When the primary purpose is to explain, teach, or persuade a person, preserve the voice and structure suited to that reader. Preserve their audience and voice; developer-response guidance does not flatten delivered emails, UI or creative work.

Apply clarity principles across all branches without forcing a controlled dictionary. Concise UI labels can be fragments; procedural explanations keep complete grammar.

Purpose outranks filename. If one artifact contains different kinds of text, apply the rules to the eligible sections rather than flattening the whole artifact.

Keep the actor and referent explicit when ambiguity would change the action.
State prerequisites before dependent steps. Separate alternative conditions and
their outcomes. Prefer one instruction per sentence and coherent short paragraphs;
retain longer wording when splitting would obscure a relationship. Use complete
grammar rather than telegraphic compression. Keep distinct domain concepts distinct:
consistent terminology does not mean merging different operations into one word.

## Preserve meaning

Read the source and its governing schema or instructions before rewriting. For a
faithful rewrite or requested complete specification, keep the supplied conditions,
exceptions, numbers, units, references, defined terms and requirement strength,
including `MUST`, `SHOULD` and `MAY`.

For an answer, explanation or summary, first select the facts needed to answer the
reader's question. Preserve the accuracy and consequential conditions of those
facts; this does not require reproducing every source metric or qualification.
A request for exact detail in one artifact does not make adjacent commentary a
complete inventory. State the limits of the claims made, rather than listing
every untested property. Link measurements that support the answer when the
reader does not need their values to understand it.

When drafting from a sparse request, state only claims that follow from it. Do
not add behavior, exceptions, guarantees, implementation constraints, error details
or ancillary test requirements merely to make a requirement sound more testable.
Ask for a missing decision when it changes the required behavior. Keep domain
terms when a plain substitute would change meaning; define an unfamiliar term
when useful. Do not rewrite code, identifiers, command syntax or quotations.
When a shorter sentence would lose precision, keep the longer one.

For example, if the only source says, "Reject expired tokens without changing stored data," a complete requirement is: "If a token is expired, the service MUST reject the request and MUST NOT change stored data." Additional error formats, exceptions, and implementation steps need their own source.

## Review

After drafting an eligible Markdown artifact, run `python -B -X utf8 scripts/ste_lint.py --mode normative <path>` for normative or operational prose, or `--mode guidance` for implementation guidance. Use `python3` on POSIX. Run the script from this skill directory or pass its absolute path. It reports possible mechanical problems and never edits the artifact. Review each finding in context; fix it only when the change preserves meaning. For a mixed artifact, lint only eligible sections when they can be isolated; otherwise self-check those sections. For eligible prose not saved to a file, self-check sentence structure, terminology, and semantic preservation without creating a file only for linting.
