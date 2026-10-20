---
name: human-collaboration
description: Open the shared human inbox for this chat and collaborate through technical reviews, optional questions, and submitted feedback.
---

# Human collaboration

The root prepares useful human contributions, continues independent work, and
integrates the responses. This is not an approval queue, a substitute for agent
review, or a way to occupy the user while agents work.

## Enter and recover

Resolve this loaded skill directory. Use its `scripts/human.py` with Python 3.11
or newer (`python` on Windows, `python3` on POSIX; honor `PYTHON_BIN`). Do not copy
the helper into the project. All global options precede the command:

```text
<python> -B -X utf8 <skill>/scripts/human.py --workspace <project> --thread <root-id> <command>
```

Use the known root thread ID or `CODEX_THREAD_ID`; never guess it. If an inbox
exists, read `INBOX.md` and use `pending` and `list` before creating more work.
Inspect only the relevant full items with `show H006`.

When the user explicitly invokes `$opl:human-collaboration`, the interactive
root opens the inbox before preparing contributions:

1. Run `init --title <readable-title>` for this root. It creates or reuses the
   project inbox, enrolls the session, and registers the project in the local
   catalog. Preserve reviewed revisions, claims, and outcomes. Do not enroll
   other chats or projects, or transfer another root's work.
2. Run `connect --host lan --allow-lan` to start or reuse the service
   on the host's detected private LAN IPv4 address. Honor a user-requested bind;
   use `connect --host 127.0.0.1` for local-only access. Read
   [phone and notification delivery](references/delivery.md) for network and notification options.
3. After authenticated readiness succeeds, whether `connect` starts or reuses the
   service, open its returned pairing URL in the host browser and report it. This
   URL contains the current GUID and bearer token. Report the host's `lan_ip` and
   render `lan_url` as a clickable Markdown
   link, such as `[Open human inbox](<returned-url>)`. For `local-only`
   access, link `url` and state that a phone cannot reach this listener. Report
   that the service remains running after the turn. On Windows, its terminal
   shows request activity; closing that window stops the server. Keep its bearer token
   private. If connection fails, report the error and evidence
   path; enrollment remains saved. Reconcile a possibly running process before
   retrying startup.

If the explicit request is to pause or restore the server around a local plugin
refresh, follow Local plugin refresh below instead of enrolling or connecting.

Hook-directed recovery starts by inspecting existing work. Recheck
pending input after startup, resumption or compaction, before related commitments,
and before completion. These checks do not enroll a session or start a server.
Do not run `init`, `connect`, or `serve` because a hook requests recovery or during
ordinary chat activity. If the current root is not enrolled, continue independent
work and tell the user to invoke this skill before publishing contributions.
Workers route enrollment requests and contribution proposals to their parent.

Each contribution belongs to one root session. Independent roots can register
in the same workspace; registration does not take another root's work. Workers
propose contributions to their parent; they do not register independent roots.
`pending` with `--thread` returns that root's unresolved responses. A different
root must already be enrolled, inspect ownership, and use
`bind --from-thread <old-root> --reason` for an explicit handoff. Binding does
not enroll the receiving root, reset claims, or replay effects.

## Select and prepare

Choose work where this particular person's contribution can improve a decision,
reduce meaningful uncertainty, or produce useful evidence. Include technical
judgment and invention, not only preferences, approval, or testing. Match their
available context, device, instruments, and interest. No worthwhile assignment
is a valid outcome. Do not manufacture busywork or delegate supervision of agent
failures.

Keep one active assignment by default, with three ordinary ready recommendations.
The index retains the rest under Later; blockers and drafts remain visible.
Priority is 0--100, lower first. Rank by consequence, likely value of human input,
and how soon commitment becomes expensive, balanced against human effort. Write
a concrete `why_now`, not an unexplained score. Top position is a recommendation,
not evidence that the human has started. Review the queue at planning boundaries:
combine overlapping questions, defer unsuitable work with reasons, and retire
obsolete items without deleting their history. Never retire an active item,
draft, or unanswered submission. Prepare candidate briefs only when justified;
do not generate a backlog of speculative two-page documents.

Maintain consequential decisions with `decision: true`, including choices the
agents consider settled. Stable H-numbers do not change with rank. Accept a
challenge to any decision; silence is not agreement. Preserve meaningful
alternatives, uncertainties and reopening assumptions in the existing project
records rather than making a competing architecture database.

## Prepare a contribution

Read [brief preparation](references/briefs.md) before publishing or revising a
technical review. Keep the decision, source snapshot, worked case, alternatives,
and return path together. Use the existing `publish`/`revise` protocol; preserve
published revisions and human drafts.

## Respond and integrate

Use optional `questions` in a published spec when specific answers will help.
Each question has a stable ID, a prompt, and three choices. Put the highest-value
recommendation first. The reader also offers a free-text answer. One brief can
contain several questions after its Markdown context. Keep architecture reviews
and other open invitations free-form when choices would distort the work.

Architecture review invitations are nonblocking. Continue authorized work while
the human is absent. For a nonblocking question, if no independent work remains,
the root can start the first recommended choice as an explicit assumption.
Before acting, use `assume H006 --question <question-id> --reason <reason>`.
State why no independent work remains and why the next step is within scope and
reversible. The question becomes `answer_assumed`; it remains visible and the
human can correct it. Preserve the assumption and recovery point in the existing
task checkpoint. A human correction requires reassessing dependent work.

Do not assume approval, a rule exception, a destructive action, or a decision
whose consequential ambiguity requires input. Use the host's inline
`request_user_input` for legitimate blockers and consequential ambiguity when
the host permits it, at the required time. Otherwise use the required chat
channel. The inbox cannot replace that channel. Do not wait for a review
invitation or manufacture more work after the authorized task is complete.

Saving a file or phone draft is not submission. The human explicitly uses Send
or `submit H006` for the Markdown reply. `submit --revision` targets an older
brief. The helper stores actual filesystem nanosecond modification stamps after
publishing, observes later stamps, and compares content. Timestamps are hints,
not the message protocol. File and phone drafts are separate; neither silently
overwrites the other.

Submissions leave Needs you immediately and remain With agent until addressed.
Use `claim <submission-id>` before applying feedback. Inspect its reviewed
revision and source drift, its existing claim, and any recorded outcome. A
repeated receipt is not another instruction to make the same code change.
`claimed_now: false` requires reconciling existing work and checkpoints, not
blind replay. Exactly-once external code effects cannot be guaranteed by an
inbox database.

Interpret the contribution in context. Identify affected decisions, dependencies
and current evidence. Preserve required approval and exception procedures; no
submission or status confers additional permissions. Continue independent work;
coordinate any work that would entrench a challenged choice. Do not treat a
human design preference as a passing runtime check or as a universal user need.

After integration, record `outcome <submission-id> <result.json>` with the actual
change or reason not adopted, relevant evidence pointers, and an explicit
`source_review`. Use `explained` for an answer that returns the item to the human,
or `follow_up` for a remaining question. Both stay in the same conversation.
Unresolved later responses keep the item With agent. Root handoffs must preserve
partly applied work in the existing task checkpoint before changing ownership.

For Projector projects, put accepted meaning, reasons, alternatives and evidence
in Projector's existing documents/checkpoint. Link them from the outcome. OPL and
the native host own scheduling; Projector does not become a second coordinator.

The human may start a contribution in the phone interface or with `contribute`.
Establish its context before promoting it to a product decision. A human does not
need an agent's invitation to question the architecture.

## Local plugin refresh

Use this lifecycle only around an explicit local plugin refresh. From the
workspace being refreshed, run `pause-for-refresh` before the installer and
`resume-after-refresh` after the installer attempt, even if refresh failed.
Both commands use the same local service catalog and workspace. The pause
command checks authenticated readiness, stores whether the service was running
and its bind settings without copying its pairing token, and stops it gracefully
only when it was running. It confirms both that the listener is unavailable and
that the recorded process exited; an unresponsive live process is an error. On
Windows it sends Ctrl+C to the service's own console; on POSIX it sends SIGINT to
the recorded service process. If it cannot confirm the stop, do not refresh.

The resume command starts the service only when the pause record says it was
running. It uses an already-registered workspace from the shared catalog, so the
workspace being refreshed does not need its own human inbox. If the service was
initially down or there is no pause record, it does not start one. A failed
restart leaves the record in place so the same command can retry. A successful
restart returns a new pairing URL; open and report it, because the previous GUID
and pairing link stop working after restart. If the installed helper could not
be updated, the source helper can consume the same record to restore service
availability.

Run the commands with the helper from the current skill directory before the
refresh and from the installed skill directory after it:

```text
<python> -B -X utf8 <skill>/scripts/human.py --workspace <project> pause-for-refresh
<python> -B -X utf8 <skill>/scripts/human.py --workspace <project> resume-after-refresh
```

## Delivery and phone access

Read [phone and notification delivery](references/delivery.md) before starting
or changing a listener, pairing a phone, enabling notifications, or diagnosing
reachability. It defines network scope, authentication, service UI, and queue
receipt limits. Use native notifications; do not poll for a human reply.
