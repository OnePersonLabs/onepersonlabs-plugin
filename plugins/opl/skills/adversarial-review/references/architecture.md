# Architectural and acceptance questions

Read when a proposal changes responsibility, state, boundaries, or delivery.
Select questions that can change the decision; this is not an all-task checklist.

- Which user-visible outcome must hold through the actual consumer?
- Who owns each state transition, and can two actors claim the same authority?
- Which producer/consumer contracts change, including recovery and interruption?
- Is a local success hiding a dependency that changes the system-level decision?
- Does the design correct the cause or add machinery around a faulty premise?
- Can a maintainer explain the main path and diagnose a failed one without
  reconstructing this conversation?
- Which checks establish the acceptance scope, and which claims remain untested?
- Does completion mean local behavior, merged delivery, release, or human/device
  qualification? What evidence belongs to each?

Report supported failure scenarios and their consequence. Do not turn unanswered
questions into defects without evidence or demand ceremony where none is needed.
