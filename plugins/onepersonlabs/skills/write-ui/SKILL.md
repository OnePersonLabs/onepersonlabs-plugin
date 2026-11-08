---
name: write-ui
description: Write or revise application interface text: headings, buttons, labels, descriptions, onboarding, confirmations, empty states, and errors. Match the wording to the actual state, surrounding controls, and available actions.
---

# Write copy that supports the action

Apply the shared drafting foundation in the applicable OnePersonLabs AGENTS.md.
Inspect the user's task, actual state, surrounding controls, available action and
recovery before choosing wording. A label can change a promise about behavior,
persistence, timing, privacy or accessibility. Check that promise against the
product and its governing requirements; do not infer equivalence from a small edit.
Keep accepted meaning and design changes with their existing owner.

Name the action and its consequence before internal architecture. Use informative
titles, understandable descriptions and short labels. Fragments are appropriate
for buttons and fields. Keep terminology consistent and preserve meaningful
distinctions between states. Remove copy or sections that do not help complete
the task, while keeping limits that change what the user can do.

Distinguish pending work, edits retained in the current view, durably saved data
and completed operations. Use "saved" only when persistence is established. An
error explains what failed, its effect on the user's work and the known recovery
action. Do not invent recovery steps, guarantees or success. An unavailable
action must not be described as available.

Use $onepersonlabs:write-technical for procedural instructions and precise
explanations; do not turn concise control labels into full sentences. For rendered
fit, accessibility and interaction meaning, use the existing product design and
testing workflow. Inspect the changed text in its surrounding interface, including
relevant narrow layouts and failure states. Rendered legibility does not prove
human comprehension.

Guides use $onepersonlabs:write-documentation. Editorial or persuasive prose uses
$onepersonlabs:write. A report keeps its existing report owner; being HTML does
not make the whole report application UI. Developer-facing commentary follows
$onepersonlabs:write-technical. Do not run a prose scanner for every UI edit.
