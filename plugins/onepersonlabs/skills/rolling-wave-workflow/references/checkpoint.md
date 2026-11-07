# Deliver a checkpoint

Use this reference after a phase or when reporting existing work. Recover the
result and consequential evidence from the current conversation, commits,
results, and existing work records. Use bounded history lookup only when an
unresolved historical fact changes the report. Do not reconstruct every command.

## Write a concise report

Use [$onepersonlabs:write](../../write/SKILL.md#concise-report-mode)'s
concise-report mode for the report and chart text. Explain what was built or
changed through what it does. Then say whether it worked and what remains
unfinished. The reader must understand the result without the conversation's
internal labels or history.

Retain causes and decisions only when they explain the result or next action.
Separate completed work, experiments, interrupted reviews, and proposed work.
An exhausted allowance or
interrupted check is not a passing check. Keep qualifications beside the claims
they limit; omit those that do not affect the takeaway. Link supporting detail
instead of narrating the work process.

Account for preparation, implementation, verification, coordination, rework, and
waiting when these distinctions affect the next action. Parallel durations
overlap. Compare equivalent work; do not turn different workloads into a speedup
claim. State unknown intervals or usage directly. Reuse the account produced by
$onepersonlabs:optimize-workflow rather than creating a separate ledger.

## Draw the route

Copy [the standalone template](../assets/navigation.html) into the current
task's existing presentation location. Replace its illustrative `application/json`
data block with the task's observed story. The file has no external dependencies.
Serialize data as JSON and escape `<` as `\u003c` before inserting it into HTML.
Do not insert untrusted story text as HTML. Retain the renderer and its validation.

Show only route details needed to explain the result, unfinished work, or the
next decision. Do not turn the chart into a command history or worker diary.
The data contains title, summary, checkpoint, actors, roadmap, nodes, edges,
accounting, and next. Each node has a stable ID, actor, grid row, label, state,
summary, story paragraphs, and optional evidence links. Actor order selects lanes.
Rows express narrative order, not measured time. Edges identify their source,
destination, and outcome; include only supported connections. The example shows
the complete shape. Add only fields the renderer consumes.

Use actor colors for the root and worker paths. Labels, symbols, and line styles
carry meaning independently of color. Mark abandoned and interrupted branches
at their endpoints. A repair path rejoins at the repaired result. A review that
did not finish cannot rejoin as approval. Label planned routes as proposed.
Do not fabricate branches to make the chart more interesting.

Give the broad roadmap a current position and direction. Expand only the
selected phase. Include selectable beats, their evidence, and an equivalent
linear story. If Plan Mode is inactive, `next` requests the mode switch and names
only an already accepted direction; it must not contain a newly detailed plan.

Keep one chart for the review consumer and update it in place. Preserve authored
content and accepted conclusions with their existing owners. Retain temporary
captures only while they support the current visual review, then remove them.
This presentation does not authorize retaining an execution diary or copying
raw logs into project documentation.

## Inspect before delivery

Open the saved HTML file directly in the available browser. Do not start a web
server to preview or deliver the checkpoint. Check desktop and phone sizes,
long labels, branch directions and reunion points. Exercise node selection,
previous/next controls, keyboard focus, story links, and evidence links. Check
that the map scrolls without clipping the page and that the phone story remains
readable without interpreting the wide map. Fix observed defects and recheck
the affected behavior. Report rendered legibility separately from unobserved
human comprehension.

Deliver the concise report with a clickable Markdown link to the saved HTML file
using its absolute filesystem path. Include the next review action when needed.
Return control at the checkpoint. Plot the next leg only through the
entrypoint's actual Plan Mode gate.
