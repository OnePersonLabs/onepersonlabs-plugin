## Native delivery and continuation

Read the live tool schema and use the recorded recipient handle. Select transport
by the recipient's position in its native session, separate from its authority.
For any native session root, including an exec root, use the supported message
operation. In the current V2 tools, `followup_task` cannot target any root.
For other recipients, prefer an operation that delivers to a running agent and
starts an idle agent. In V2, `followup_task` does both; `send_message` only delivers.

Send one scoped question or answer through the selected operation. If delivery
cannot start an idle recipient, reconcile its state before one supported explicit
continuation. Otherwise retain BLOCKED state and report unsupported continuation.
Do not send duplicate continuations to cover uncertain delivery. Preserve
assignment, role, compute, and write ownership. Continue safe independent work,
then return a BLOCKED checkpoint if no further safe work remains. Account for
descendants. Do not wait for the parent's completion while it waits for yours.

Use native question/completion notifications or bounded waits. If a surrounding
batch does not yield a received question, use the native call outside that batch
when supported. An idle user-facing root is not guaranteed to start from a child
message. If no supported delivery or continuation exists, retain the BLOCKED
checkpoint and report that limitation; do not fabricate a tool or poll.

Before consuming an answer, check its ID, validity context, current assignment,
scope, and authority. Ignore an identical already-consumed answer. Withhold the
action on missing, stale, canceled, superseded, contradictory, or unauthorized
answers. Silence, timeout, defaults, and cleared status events are not consent.
Use subsequent progress or results as consumption evidence, without repeated
acknowledgments. A BLOCKED result never counts as successful task completion.
