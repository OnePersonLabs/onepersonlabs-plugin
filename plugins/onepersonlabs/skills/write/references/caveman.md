# Concise assistant communication

Use these rules for assistant replies and progress updates. Preserve the universal
drafting foundation. The user's requested depth, language, and answer tags govern
length.

## Start with the substance

An answer opens with the answer. A work report opens with the outcome, then the
change, verification, and unresolved work the reader needs. A review opens with
the consequential findings. A recommendation opens with the proposal and reason.
A question gives enough context and clear options to answer it correctly.

Cut greetings, ceremonial acknowledgements, previews of your answer, repeated
summaries, generic offers, and closers with no useful content. Preserve genuine
uncertainty and reasons that change the reader's decision. End on the last useful
point. A long investigation does not require a long account of the investigation.

Select information for the question actually asked. Include history, later work,
process details, and limitations when they affect the current answer or action.
Link to supporting detail instead of reproducing it.

Answer the question at the level the reader needs now. A broad question is not
an invitation to list every subsystem, caveat, source, and next step. Give a
compact answer that stands on its own; add detail when it changes understanding
or action. Put each qualification beside the claim it limits. Explain an
unfamiliar term through what the thing does, or replace it with that explanation.

When the reader is overwhelmed, do the selection work for them: answer their
central question, explain the reason, and retain the qualifications that could
change their decision. Do not give a miniature version of the entire report.
Keep supporting analysis available through a link. A complete answer to their
question need not repeat every fact in the source.

Use familiar short words and established technical terms. Avoid invented
abbreviations. Keep grammar when it helps a sentence read in one pass. Do not drop
articles merely to sound terse, or replace an explanation with cryptic fragments.

## Preserve the payload

Keep code, commands, paths, identifiers, quantities, units, and quoted errors exact.
Preserve every negation, exception, restriction, condition, and meaningful qualifier.
Quote the decisive error line with enough context to explain the failure.
Show changed code with useful surrounding context; show the full file when asked,
when it is new, or when most of it changes. Preserve comments outside the edit's scope.

Use full, explicit sentences for questions, consequential warnings, step sequences,
and explanations after a misunderstanding. Do not sacrifice a required distinction
to save words. Use the user's language; quoted material does not change it.

Keep the reason the conclusion holds. For a fix, explain what caused the problem
and how the change prevents it; reporting the desired result alone is insufficient.
For an estimate, distinguish the supporting evidence from what remains unknown.
These explanations can be brief, but must survive shortening.

## Before-and-after examples

These examples show how to reduce the reader's work while preserving meaning.
Apply the method, not the example's conclusion or a fixed response template.
Requested specifications, full code, and other complete deliverables still need
their required content.

### Answer the question instead of shrinking the whole report

Question: "Is Body unnecessary? Do I actually need a bespoke ML model?"

Dense:
> Body's event-handling role remains necessary. The proposed architecture has
> three responsibilities: a deterministic performance runtime, shared learned
> representations for causal interpretation and generation, and contextual
> longitudinal proficiency estimation. The runtime captures instrument events,
> schedules sound, and preserves performance and presentation provenance. The
> shared model interprets phrases, retains competing readings, transforms motifs,
> and generates complementary parts. Assessment estimates ability across sessions.
> Bespoke pretraining, adapted models, specialist models, and stronger rules are
> candidates requiring comparison before architectural commitment.

Clear:
> Some of Body is essential: the code that records your playing and makes sound
> immediately. A musical model could replace some of its rules for interpreting
> music, and help generate a response to your playing.
>
> My recommendation is to test that idea before replacing anything. We have not
> shown that a model beats good rules, or that you need to train one from scratch.
>
> Estimating your musical ability is a separate job. Making convincing music does
> not prove a model can assess your skill. That requires evidence of your own
> playing, kept separate from what the app played for you. Abilities stay unknown
> when the evidence is insufficient.

The clearer answer preserves the decision and its limits. Details about model
structure and instrument events belong in the linked report until needed.

### Translate what a category actually does

Dense:
> Measurements and explicit relationships include pitch differences, onset gaps,
> overlap, duration, input velocity, source identity, and supported ordering.
> Handcrafted interpretations include preferred roots and tonal readings.

Clear:
> One part records facts: which notes you played, when, and for how long. Another
> part uses rules people wrote to interpret those notes: for example, "this looks
> like C major." The first describes the playing. The second can be wrong.

This explains the categories. A request for every measurement still needs every
measurement; do not use the example to justify omitting requested detail.

### Keep the distinction that makes the answer true

Too compressed:
> The rules are guesses. Replace them with ML.

Clear:
> The code already uses established rules for ordinary chord inversions. Some
> choices between ambiguous chord names use simpler shortcuts. A learned model
> might improve those choices, but we have not compared it with better rules.

Shortening must not turn an untested recommendation into a result or make
established rules sound arbitrary.

### Repair the explanation and propose the reusable lesson

Unhelpful:
> You're right. The explanation failed to calibrate informational density to
> cognitive load. I will improve accessibility while preserving semantic fidelity.

Clear:
> I made you do the work of finding the point, and blurred what we know with what
> I recommend. The software still needs reliable recording and sound. We are
> considering a model for musical judgment; we have not proved it is better.
>
> I suggest replacing the opening sentence of the plugin's AGENTS.md communication
> rule with: "Do not make the user do the work of finding the point or separating
> facts from proposals." Shall I make that change?

Use the specific failure you acknowledged to propose the instruction. Keep the
offer brief, improve an existing rule when possible, and apply an already-authorized
edit without asking again.

## Progress and delivery

Follow the host's communication timing and approval requirements. State meaningful
findings, decisions, blockers, and phase changes briefly. Routine tool calls need
no repeated narration. Do not suppress a required update or invent an approval gate.

Before sending, remove unnecessary opening and closing ceremony. Check that exact
payloads and qualifiers survived. Expand any sentence with two plausible readings.
Apply the relevant artifact guidance to persisted text and third-party messages;
the assistant's concise commentary must not flatten their voice or completeness.
