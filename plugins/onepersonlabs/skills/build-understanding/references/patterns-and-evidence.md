# Choose a representation that does useful work

Read this when selecting a medium, designing exploration or checking the research
basis. Use only the patterns that help the current task. Availability and a
polished presentation do not establish comprehension.

## Match the representation to the question

| Needed understanding | Useful representation | Keep clear |
| --- | --- | --- |
| Parts, responsibilities or dependencies | A labeled map with grouping and connections | What an edge means; actual ownership versus a proposed relationship |
| Alternatives or tradeoffs | Aligned comparisons with the same scale and criteria | Different units, assumptions and uncertainty |
| Change over time | Before/after, a sequence, timeline or controlled motion | Object identity, causality and inspectable states |
| Cause and effect | A worked case or adjustable example | Which input changed, what responded and the model's limits |
| Exact instructions or constraints | Concise text, values and nearby labels | Every required condition, exception and permission |
| Sound, language or timing | Listening, speech, replay or an audio comparison | User control, captions/transcripts and the actual sound capability |
| Movement, assembly or tactile distinctions | A demonstration or user-performed action with feedback; haptics when supported | Safe actions, orientation and an equivalent route when touch or movement is unavailable |
| Human intent or judgment | Concrete choices, direct manipulation or a shared example | The decision being requested, consequences and a way to correct it |

A map helps when its organization exposes something the person needs. More
icons, colors, panels or motion can add decoding work instead. Use short words
when they remove ambiguity. Put the most useful overview first, with detail
available at the point of need; do not hide a condition required for safe action.

## Examples across human input and output

**Explain a workflow.** Show the main path and who owns each transition. Then
trace one failed check through repair and back to review. Link exact commands
from the existing procedure. A long arrow does not imply automatic execution.

**Teach a sound distinction.** If playback is available and wanted, let the person
compare the actual sounds and replay the relevant change. Pair it with a concise
description or notation. A static picture cannot establish what was heard; a
listener's preference does not prove discrimination or transfer to another case.

**Explore a model.** Start with a meaningful example, then expose an input whose
change makes a useful relationship visible. Keep the assumptions and reset path
available. The example should still explain something before interaction. A
simulation illustrates its model; it is not evidence that the model fits reality.

**Elicit a decision.** Place each option beside its consequence. Let the person
choose or correct the shared example using the available input method. Ask for
free-form explanation when the distinction cannot be represented faithfully by
the choices. Do not turn every exchange into a form or an interview.

## Use the actual delivery surface

For static relationships, use Mermaid where the reader supports it. Include an
accessible title and description, labeled nodes and a short equivalent reading.
For unsupported readers, use a rendered image and text alternative. Follow
$onepersonlabs:human-collaboration's existing image-export protocol for its phone reader.

For meaningful dynamics or exploration, use available visualization tools or the
product's native components. Respect keyboard, screen-reader, touch, reduced-motion
and audio needs. Preserve meaning without color alone or a transient effect.
Use text when it communicates the task more directly; do not build an app merely
to demonstrate the method.

## Evidence and limits

| Primary basis | What it contributes | Limit of the inference |
| --- | --- | --- |
| [Larkin and Simon, diagrammatic reasoning](https://doi.org/10.1111/j.1551-6708.1987.tb00863.x), 1987 | Spatial organization can make information and needed inferences explicit, reducing search or reconstruction in the analyzed problems. | A diagram's advantage depends on its structure, the problem and the reader; visual decoration is not the mechanism. |
| [Çeken and Taşkın, multimedia-learning review](https://doi.org/10.1186/s40561-022-00200-2), 2022 | Examines principles including signaling, coherence, contiguity and segmentation across learning environments. | Results depend on learner and context. They do not validate this skill or guarantee lower effort in every human interaction. |
| [Bret Victor, Explorable Explanations](https://worrydream.com/ExplorableExplanations/), 2011, with 2024 postscript | Concrete reactive documents, guided examples and contextual information show how interaction can support questioning and intuition. | These are design references, not a universal controlled performance result. |
| [W3C text alternatives](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html), [color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) and [motion](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | Equivalent access, redundant cues and control of nonessential motion. | Rendering and conformance checks do not establish human comprehension. |
| [Mermaid accessibility](https://mermaid.js.org/config/accessibility.html) | Supported `accTitle` and `accDescr` metadata for rendered diagrams. | A renderer can preserve metadata without making the diagram understandable or legible at the target size. |

Perceptual scaffolding is the working name for this reusable design stance.
The individual references support specific mechanisms and examples, not a new
scientific theory, a sensory-bandwidth claim or a measured learning improvement.
