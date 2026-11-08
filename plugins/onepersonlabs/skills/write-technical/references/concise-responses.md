# Concise developer response examples

Read these examples for developer-facing replies and progress updates. Apply the
method to the actual question, not the example conclusion or a fixed template.
The shared rules live in AGENTS.md; exact payloads, causal meaning and requested
depth survive shortening.

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

### Replace an empty heading with the useful fact

Empty:
> ## The important bit
> You can recover a saved draft after reopening the app.

Clear:
> ## Recover your saved draft
> Reopen the app and select the draft from History.

The second heading tells the reader which task the section covers. The steps
still need to match the product's actual controls; a heading cannot supply missing
behavior.

### Do not simplify a partial capability into a finished one

Misleading:
> Notifications work when the app is closed.

Clear:
> Notifications work while the app is open. Delivery after you close it is still
> unimplemented.

Use this distinction only when the evidence supports those states. A shorter
claim must not erase the unfinished part of the user's goal.

### Correct the explanation and offer steering

Question: "I cannot tell what you mean by usable inference machinery."

Clear response when supported by the supplied evidence:
> The code can calculate probabilities and generate candidate note events. We
> have not yet shown that it can make a useful musical response to your playing.
>
> 💡 In the report skill, replace "Describe the inference machinery" with
> "Explain what the tested code can do for the musical task and what remains unproven."

Correct the answer first, then briefly propose the exact change at the actual
owner. Follow AGENTS.md authorization rules. Do not invent an explanation or
repeat a steering proposal already accepted or applied. Ordinary factual errors
do not automatically require a standing instruction.
