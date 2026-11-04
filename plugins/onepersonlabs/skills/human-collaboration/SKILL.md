---
name: human-collaboration
description: Prepare and integrate requested human collaboration through the shared inbox, technical reviews, questions, and feedback pinned to a running page. Draft-only questionnaires and correspondence use write.
---

# Human collaboration

The root prepares useful human contributions, continues independent work, and
integrates the responses. This is not an approval queue, a substitute for agent
review, or a way to occupy the user while agents work.

## Enter and recover

Requests only to draft questionnaires, correspondence, or review documents use
`$onepersonlabs:write`. Obtaining answers from someone else does not by itself
request inbox management. For these drafts, do not enroll a session or start the
service unless the user explicitly invokes `$onepersonlabs:human-collaboration`
or requests inbox management.

Resolve this loaded skill directory. Use its `scripts/human.py` with Python 3.11
or newer (`python` on Windows, `python3` on POSIX; honor `PYTHON_BIN`). Do not copy
the helper into the project. All global options precede the command:

```text
<python> -B -X utf8 <skill>/scripts/human.py --workspace <project> --thread <root-id> <command>
```

Use the known root thread ID or `CODEX_THREAD_ID`; never guess it. If an inbox
exists, read `INBOX.md` and use `pending` and `list` before creating more work.
Inspect only the relevant full items with `show H006`.

When the user requests substantive human collaboration beyond drafting, including
feedback on a running product or inbox management, or explicitly invokes
`$onepersonlabs:human-collaboration`, the interactive root opens the inbox before
preparing contributions:

1. Run `init --title <readable-title>` for this root. It creates or reuses the
   project inbox, enrolls the session, and registers the project in the local
   catalog. Preserve reviewed revisions, claims, and outcomes. Do not enroll
   other chats or projects, or transfer another root's work.
2. Run `connect --host lan --allow-lan` to start or reuse the service
   on the host's detected private LAN IPv4 address. Honor a user-requested bind;
   use `connect --host 127.0.0.1` for local-only access. Read
   [phone and notification delivery](references/delivery.md) for network and notification options.
3. After authenticated readiness succeeds, whether `connect` starts or reuses the
   service, deliver the pairing link as described below. If connection fails,
   report the error and evidence path; enrollment remains saved. Reconcile a
   possibly running process before retrying startup.

If the explicit request is to pause or restore the server around a local plugin
refresh, follow Local plugin refresh below instead of enrolling or connecting.

Hook-directed recovery starts by inspecting existing work. Recheck
pending input after startup, resumption or compaction, before related commitments,
and before completion. These checks do not enroll a session or start a server.
Do not run `init`, `connect`, or `serve` because a hook requests recovery or during
ordinary chat activity. If the current root is not enrolled, continue independent
work. Enroll only when the user has requested substantive collaboration as above;
a recovery hook alone does not authorize enrollment.
Workers route enrollment requests and contribution proposals to their parent.

Each contribution belongs to one root session. Independent roots can register
in the same workspace; registration does not take another root's work. Workers
propose contributions to their parent; they do not register independent roots.
`pending` with `--thread` returns that root's unresolved responses. A different
root must already be enrolled, inspect ownership, and use
`bind --from-thread <old-root> --reason` for an explicit handoff. Binding does
not enroll the receiving root, reset claims, or replay effects.

### Deliver the pairing link

After successful connection or restart, open the returned pairing URL in the
host browser and include a clickable Markdown link in the user-facing reply:
`[Open human inbox](<returned-url>)`. Use `lan_url` when present; otherwise use
`url`. Copy the complete returned URL, including its scheme, host, port, path,
`?guid=...` query and `#token=...` fragment. Do not reconstruct it from `lan_ip`,
redact its token, or replace the link with a listening-status message. A bare IP
address cannot open the inbox. Opening the browser does not replace the link in
the reply.

The pairing link grants inbox access. Give the full link to the requesting user
in this chat; keep it out of repository files, shared documents, and activity
logs. Report `lan_ip` alongside the link when present. For `local-only` access,
state that a phone cannot reach this listener. Report that the service remains
running after the turn. On Windows, its terminal shows request activity;
closing that window stops the server.

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

For feedback that needs a person to point at a running page, select
[page feedback](references/page-feedback.md), prepare the adapter, and verify its
controls before inviting the human. Keep its notes in the existing contribution
protocol and its accepted decisions with the current project owner.

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
whose consequential ambiguity requires input. Honor the user's selected question
surface. When they choose the web inbox, use it for blocking questions as well
as review invitations; leave dependent work blocked until a submitted answer
resolves it. Host-required permission or approval controls still use their
required interface. Without an established surface preference, use the host's
inline question tool when available or ordinary chat. Do not wait for a review
invitation or manufacture more work after the authorized task is complete.

When the user expects a web reply to resume an idle root, enable the existing
`connect --wake-root` delivery path and finish the current turn after independent
work. Read [delivery](references/delivery.md) first. A queued notice identifies
pending input; it is not the answer, an approval, or proof of integration. Do not
keep an agent polling for a reply. If a shared listener cannot provide the
requested notification mode, report that limitation without stopping other
sessions or silently promising automatic pickup.

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

For Conceptor projects, put accepted meaning and reasons in their existing
meaning owner and link it from the outcome. Retain generated presentation files
only while the contribution needs them; delete temporary copies after closure
and reconciliation. Preserve authored source files, human submissions, accepted
decisions, and the inbox's current views. Give any retained diagnostic evidence
a concrete consumer, validity conditions, disposal boundary, and cleanup owner.
OnePersonLabs and the native host own scheduling; Conceptor does not become a
second coordinator.

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
restart returns a new pairing URL; [deliver the complete clickable link](#deliver-the-pairing-link),
because the previous GUID and pairing link stop working after restart. If the installed helper could not
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
