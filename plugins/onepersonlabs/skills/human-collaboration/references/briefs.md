## Technical review briefs

Prepare one coherent 1--2-page review, not a compressed dump of the entire system.
Human-friendly means context-complete, not technically shallow. Include:

- The decision, its downstream consumer, why it matters now, and what work can
  continue without the answer. Distinguish a genuine blocker from an invitation.
- Grounded context: current versus proposed behavior, requirements, ownership,
  invariants, and the exact source snapshot. Explain internal terms locally.
- A mechanism-revealing diagram and concrete worked case. Show data/ownership
  flow for architecture, actual uses for patterns, or inputs/outputs, compact
  pseudocode and a troublesome trace for algorithms.
- The recommendation and strongest practical alternative, including doing less
  or postponing an abstraction. State the deciding tradeoff and reversal test.
- Evidence versus assumptions, relevant source references, an explicit invitation
  to challenge/reframe, and an easy return path. No diagnosis or formal report
  should be required from the human.

Use `publish` with a JSON spec (file or stdin `-`); see
[the protocol and examples](protocol.md). Capture only relevant
workspace-relative `sources`, never credentials or unrelated private files.
SVG/PNG/JPEG diagrams in the source snapshot render in the phone reader. Use
`![caption](source:0)` for the first source, or the workspace-relative path.
Plain Markdown stays usable in an editor. The small reader does not execute HTML
or render Mermaid; export a diagram image for the phone instead of promising a
renderer that is not present.

Published briefs end in `# Reply`. Never rewrite that file after publishing.
`revise` creates a new numbered revision when no current human work is in flight;
retain older versions. Do not silently retarget input to newer source.
