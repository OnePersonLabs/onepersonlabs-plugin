# Continue work and collaborate with people

Use this guide when work spans turns, needs a human contribution, or includes a
long local command. It shows how to restore the current state and resume with
the existing owner. Routine chat does not require an inbox service. For issue
ownership and delivery choices, see the [workflow guide](workflow.md).

## Resume an interrupted task

Start with the existing work records and the conversation that owns the task.
Reconcile the owning issue, the repository's current-work checkpoint, current
checkout and dirty files, and any unfinished external action before repeating
it. If a project uses Conceptor or another meaning owner, recover accepted
decisions and evidence there too. The current checkpoint records active
decisions, failed hypotheses, budgets, permissions, and the next safe action;
do not create a second task ledger.

Ask Codex to resume with the existing issue and evidence:

> Resume the existing work on `<issue or outcome>`. Reconcile the owning issue,
> checkpoint, and current checkout first. Preserve the original problem,
> ownership, authorization, failed hypotheses, budget, and incomplete actions;
> inspect uncertain external writes before retrying them.

If the original conversation cannot continue, use
[$onepersonlabs:handoff](../skills/handoff/SKILL.md) to prepare a compact
continuation file in the operating system's temporary directory. It links to
the issue, specification, commits, diff, checkpoint, and unresolved work rather
than copying them. Include the permission boundary, branch/revision, relevant
dirty work, verified evidence and its limits, outstanding assignments and human
submissions, and one next action. The skill checks cited repository paths,
links, and commit IDs. A handoff file helps a new conversation continue; it does
not start that conversation, transfer ownership by itself, or authorize paused
work.

### Recover earlier context when the checkpoint is incomplete

If one prior decision or exchange is missing, use
[$onepersonlabs:session-reader](../skills/session-reader/SKILL.md) for a focused
lookup. Ask it to find and show the bounded message range for the decision; for
example:

> Use `$onepersonlabs:session-reader` to search my Codex history for the
> decision about `<specific question>`, then show the messages around the best
> match. Return the session and message references so I can add verified context
> to the existing checkpoint.

The reader uses its canonical index, returns bounded excerpts, and refreshes
the index as needed. Do not read raw rollout JSONL directly or treat a search
match as proof of project ownership. Inspect the surrounding messages and
current project evidence before carrying a past statement forward.

Use [$onepersonlabs:session-history-rebuild](../skills/session-history-rebuild/SKILL.md)
only when a complete, auditable repository conversation and design history is
explicitly requested. That larger reconstruction requires a fresh
`$onepersonlabs:session-reader` index, a status check with no relevant stale
sources, and a frozen SQLite index snapshot plus explicit UTC cutoff. Inventory
every indexed session and give each candidate an inclusion or exclusion reason;
the indexed working directory is only a routing hint, and mixed sessions need
message-level inspection. Export and verify the canonical user/assistant
sequence against the frozen index and routing, retain source hashes, and cite
messages and code in the resulting baseline and history. Keep assistant
proposals separate from user decisions. This is a deliberate history project,
not the ordinary way to resume a task.

## Request a useful human contribution

Use [$onepersonlabs:human-collaboration](../skills/human-collaboration/SKILL.md)
when a specific person can improve a consequential decision, supply missing
context, review a technical choice, or give feedback on a running page. Ask for
the contribution that changes the next decision and state what can proceed
without it:

> Use `$onepersonlabs:human-collaboration` to prepare a short review for `<person>`
> about `<specific decision>`. Show the current evidence, strongest alternative,
> why the decision matters now, what can continue without an answer, and where
> to respond. Keep the open decision with the existing project owner.

When you request substantive collaboration (such as a technical review or
feedback on a running page), or explicitly invoke the skill, the root enrolls
its own session and opens the inbox service when needed. A hook or ordinary chat
does not enroll a session or start the service. The inbox is local to the
workspace and workstation; it is not cross-clone sync. Published brief
revisions and submitted replies stay with the inbox, along with any source
snapshots captured for the brief.

After authenticated readiness, the root opens and reports the pairing link.
Open that link to read the brief and respond. The usual requested collaboration
flow uses a private LAN address so a phone on the same reachable network can
connect; a requested local-only listener is accessible only on the host.
Readiness on the computer does not prove phone reachability. The link carries
the current GUID and bearer token; keep it private. The service remains running
after the agent turn, and a restart produces a new link. See
[phone and notification delivery](../skills/human-collaboration/references/delivery.md)
for network requirements, service shutdown, and optional queue notifications.

The human must explicitly send the response in the inbox or run its `submit`
command. Saving a draft is not submission. Submitted work moves to the agent for
interpretation; the root claims it, checks the reviewed revision and source
drift, and records what happened. A submission can inform a decision but does
not grant new permissions or prove code correctness. Agreement is not a test
result. The root keeps accepted meaning and evidence with the project owner.

From the installed human-collaboration skill's `scripts` directory, the human
can submit a response with this command. Use `python` on Windows or `python3`
on POSIX, and pass the item ID shown by the inbox:

```text
<python> -B -X utf8 human.py --workspace <project> submit <item-id>
```

If a brief is an invitation to comment, work continues while the person is
absent. The root may make a reversible assumption for a nonblocking question
only after independent authorized work is exhausted, and must record that
assumption and a way to recover. Never infer approval, an exception, or consent
to a destructive or consequential action from silence. Use the normal chat
question channel for a real blocker or required permission.

When handing off work with an outstanding response, preserve its brief revision,
submission ID, claim and outcome state, partly applied changes, and current
owner in the existing checkpoint. Inspect before applying a repeated response;
an inbox receipt cannot guarantee exactly-once effects in code. If ownership
needs to move to another root, use the explicit session handoff procedure in the
human-collaboration skill.

## Wait for a genuinely long local command

Use [$onepersonlabs:long-command-wakeup](../skills/long-command-wakeup/SKILL.md)
only when repository evidence or measured history supports a runtime over about
120 seconds, no native completion notification or bounded wait fits, and the
command can safely continue without supervision. It does not fit interactive,
approval-dependent, destructive, or commands that need live supervision. Batch related
finite checks when they do not require a decision between runs.

The skill starts one detached watcher and queues one continuation message. It
reports a launch receipt; that receipt says the watcher started, not that the
command succeeded or that delivery is guaranteed. Do not poll it. When the
continuation arrives, inspect the four artifacts at the reported result path
once; only `state: success` with exit code zero establishes command success.
Queue acceptance alone does not prove message delivery. If no message arrives,
inspect the artifacts only when the user later resumes the work. A timed-out
command may still be running if cleanup failed; inspect the reported process
before starting conflicting work.

The command helper requires Python 3.11 or newer and the installed skill's
`scripts/run_and_wake.py`. On Windows use `python`; on POSIX use `python3`; honor
`PYTHON_BIN` when set. Keep the existing command timeout contract: do not invent
a deadline from the runtime estimate. The skill's platform-specific invocation
is:

```text
<python> -B -X utf8 <skill>/scripts/run_and_wake.py start --cwd <working-directory> -- <program> <arguments...>
```

Use the actual loaded skill directory and pass program arguments separately.
`CODEX_THREAD_ID` must identify the current thread; pass `--thread <known-id>`
only when that ID is already known. The result artifacts remain in the reported
directory for recovery if queue submission fails.

## Restore the inbox service around a local refresh

This procedure applies only when an authorized local plugin refresh is actually
being performed. From the workspace being refreshed, use the
human-collaboration skill's `pause-for-refresh` before the installer and
`resume-after-refresh` after the attempt, even if installation fails. The pause
records whether the service was running and its bind settings, stops a running
service gracefully, and confirms both listener shutdown and process exit. If it
cannot confirm shutdown, do not refresh. Resume starts it only when it was
running before; a failed restart preserves the record for retry. A successful
restart returns a new pairing URL -- open and report it because the prior link
expires. Use the source skill to resume if the installed helper is unavailable
after a failed refresh. See the exact
[refresh procedure](../skills/human-collaboration/SKILL.md#local-plugin-refresh).

This service recovery does not change which plugin was installed or prove its
hooks are trusted. Follow the target repository's own instructions for its
installer and post-refresh checks. The
[$onepersonlabs:refresh-local-plugins](../skills/refresh-local-plugins/SKILL.md)
skill documents the plugin refresh helper and its delivery limits.

## Related skills

- [Human collaboration](../skills/human-collaboration/SKILL.md) -- explicit contribution, inbox ownership, service lifecycle, and submission recovery.
- [Handoff](../skills/handoff/SKILL.md) -- continuation file for a fresh conversation.
- [Long command wakeup](../skills/long-command-wakeup/SKILL.md) -- bounded completion notification for unattended local commands.
- [Session reader](../skills/session-reader/SKILL.md) -- focused, bounded history lookup.
- [Session history rebuild](../skills/session-history-rebuild/SKILL.md) -- explicit full-history provenance and reconstruction.
- [Local plugin refresh](../skills/refresh-local-plugins/SKILL.md) -- refresh selection, recovery lifecycle, and installed state.
- [GitHub issue procedure](../skills/github-workflow/SKILL.md) -- reconcile issue state and uncertain GitHub writes.
