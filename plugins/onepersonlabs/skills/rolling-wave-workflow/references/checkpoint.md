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
task's existing presentation location. Deliver static, JavaScript-free HTML with
embedded CSS and an authored inline SVG graph. Do not include scripts, event
handlers, JavaScript URLs, runtime data blocks, or external dependencies.
Replace the illustrative content directly in the HTML and SVG before delivery.
Escape story text and attribute values for their HTML context. Evidence links
may use local files, HTTP, or HTTPS; reject executable link schemes.

Show only route details needed to explain the result, unfinished work, or the
next decision. Do not turn the chart into a command history or worker diary.
Update the title, summary, checkpoint, actor lanes, roadmap, graph, numbered key,
story, accounting, and next action together. Give each beat a stable story anchor,
actor, label, state, summary, story paragraphs, and available evidence links.
Match graph numbers to the numbered key and story headings. Update SVG paths,
arrowheads, accessible descriptions, and the viewBox to fit the actual graph.
Rows express narrative order, not measured time. Edges identify their source,
destination, and outcome; include only supported connections. Route edges through
lane gutters and row gaps so they do not cross unrelated nodes.

Use CSS for responsive layout. Allow ordinary document scrolling only; do not
create scrollable panels, fixed-height graph viewports, or horizontal page
overflow. Let content determine section height. Fit the entire graph to the
available width with a proportional SVG viewBox and CSS width of 100% and height
of auto. Keep graph numbers readable on phones and full labels in the adjacent
key and story. If the graph becomes too dense, split it into connected figures
with explicit continuation labels and stable beat numbers. Preserve every
supported branch and reunion; do not hide or discard the graph on narrow screens
or in print, shrink its text beyond legibility, or clip overflow to conceal it.

Use actor colors for the root and worker paths. Labels, symbols, and line styles
carry meaning independently of color. Mark abandoned and interrupted branches
at their endpoints. A repair path rejoins at the repaired result. A review that
did not finish cannot rejoin as approval. Label planned routes as proposed.
Do not fabricate branches to make the chart more interesting.

Give the broad roadmap a current position and direction. Expand only the
selected phase. Use native anchor links from graph nodes and the numbered key
to each beat's full story and evidence. Include outgoing connections as text
links so the route remains understandable without the drawing. If Plan Mode is
inactive, the next action requests the mode switch and names
only an already accepted direction; it must not contain a newly detailed plan.

Keep one chart for the review consumer and update it in place. Preserve authored
content and accepted conclusions with their existing owners. Retain temporary
captures only while they support the current visual review, then remove them.
This presentation does not authorize retaining an execution diary or copying
raw logs into project documentation.

## Inspect before delivery

Open the saved HTML file directly in the available browser. Do not start a web
server to preview or deliver the checkpoint. Check desktop and phone sizes,
long labels, branch directions and reunion points. With JavaScript disabled,
confirm that all content and the graph render. Exercise graph-to-story links,
return links, keyboard focus, story connections, and evidence links. Check that
the page has no horizontal overflow or nested scroll containers at either size.
Check that graph numbers, arrowheads, branch endpoints, and reunion points remain
legible on phones and in print. Confirm that long labels wrap and the story
remains complete. Fix observed defects and recheck
the affected behavior. Report rendered legibility separately from unobserved
human comprehension.

Deliver the concise report with a clickable Markdown link to the saved HTML file
using its absolute filesystem path. Include the next review action when needed.
Return control at the checkpoint. Plot the next leg only through the
entrypoint's actual Plan Mode gate.
