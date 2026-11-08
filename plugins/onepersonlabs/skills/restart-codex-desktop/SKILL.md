---
name: restart-codex-desktop
description: Automatically quit and relaunch Codex Desktop when a restart is requested or needed to load changed plugins, skills, instructions, or configuration. Optionally continue an existing chat; choose a fresh chat when a clean initial context is the actual goal. Configuration edits alone do not authorize interrupting unrelated work.
---

# Restart Codex Desktop

Perform the restart, including graceful Quit, independent relaunch and any
authorized continuation. The agent runs the helper; the user does not need to
open a terminal or close the app.

## Choose what needs to restart

Distinguish the running application from the conversation context. Restarting
Desktop reloads its processes and configuration; reopening an old chat retains
its history and does not establish a fresh initial skill/instruction context.

Continue the existing chat when its history is useful and the changed runtime
settings are the concern. Choose a fresh chat when new initial instructions,
skill discovery or an unnecessarily large history make that the intended result.
Use native thread tools for an authorized fresh chat. When creation is only
available to a running agent, resume this chat after restart solely to verify
recovery and create the fresh chat with the agreed handoff. Never start a second
writer before the first owner has stopped. A new-chat URL only prefills the
composer; it does not submit the prompt.

Inspect the active host's restart and thread tools first. Prefer a native restart
operation if its current contract covers the outcome. The Windows helper below
supports the installed OpenAI.Codex Appx package. For another platform or package,
verify its native route before acting; do not substitute a manual procedure and
claim automatic restart is complete.

## Reach a safe checkpoint

Finish the current coherent edit batch and its required checks. Preserve remaining
work, accepted decisions, evidence, current ownership and the next authorized
action with the existing issue or handoff owner. Reconcile active writers, child
agents, commands, pending approvals and unsaved authored content. Tell the user
that Desktop will close and which chat or next action will resume.

Reuse existing restart authorization. A request to configure a plugin alone does
not authorize interrupting unrelated work. Resolve any target chat to its exact
local UUID using native thread tools; never select the most recent chat. Honor
its model and permissions. A remote host or WSL chat is outside this helper's
native Windows continuation route.

## Inspect, arm and quit

Run this loaded skill's helper with Python 3.11 or newer:

```powershell
python -B -X utf8 '<skill>/scripts/restart_desktop.py' inspect
```

It reads the installed Appx manifest's App entrypoint, verifies Desktop resources
and reports process identities. The root UI can be ChatGPT.exe or Codex.exe;
resources/codex.exe is the CLI. A process name alone is insufficient.

Use supported computer-use to select the matching app window and locate its
actual Quit control before arming. Inspect the File menu or tray menu as exposed
by the installed app. Use the observed control, not a remembered shortcut.
Windows Desktop can remove its native menu while retaining a custom menu;
the source's Ctrl+Q definition does not establish a working accelerator.
Closing the window can leave the app in the tray. Do not force-kill processes
or invoke undocumented IPC. If no supported Quit route is available, report
that blocker before arming.

Start the independent recovery helper from the agent's own tool:

```powershell
python -B -X utf8 '<skill>/scripts/restart_desktop.py' arm --thread '<UUID>' --message '<authorized next action>'
```

Omit --thread to restart without continuing work. A thread ID without --message
uses a short continuation of that chat's authorized work. --codex-home defaults
to the active native Windows Codex home. Quote real PowerShell arguments with
single quotes, doubling embedded single quotes. Do not pass a shell command as
the message. --timeout-seconds defaults to 60 for app exit.

The helper starts a hidden, finite process through local Windows WMI. It verifies
that the worker is outside the parent's process job before reporting armed. This
matters because merely detaching a console can leave a child in a job that dies
with Desktop. No service, scheduled task or recurring process is installed.

After the helper reports armed, immediately use supported computer-use to invoke
the verified Quit control. The agent performs this step; do not ask the user to
open a terminal or quit the app. Handle a visible quit confirmation only within
the existing restart authorization and settled work checkpoint. A confirmation
that reveals unrelated active work requires reconciliation before proceeding.
Arming is an intermediate result: do not end the turn before invoking Quit.

The worker tracks the original main process separately from renderer turnover.
After confirmed exit, it launches the exact manifest executable with the selected
CODEX_HOME and waits for a new process. An external replacement or changed
installation stops the operation. The worker sends no UI input. If the Quit action
fails, its finite wait expires without launch or continuation. A launch failure
remains in the receipt for recovery. Process observation alone does not prove UI
readiness or loaded settings.

The command returns a receipt path, worker PID, target identity and exit deadline.
Match that identity to the selected UI window. Once armed, do only the Quit
interaction and its recovery; do not start more edits or another restart. If
readiness or input delivery is uncertain, inspect the receipt before any retry.
An existing receipt blocks another arm until its operation is reconciled and the
receipt is removed. The original worker may still be waiting. The exclusive claim
prevents repeated workers for the same operation.

## Continue and reconcile

With a target chat, the worker calls its verified native CLI's queue --resume
exactly once after relaunch. It preserves the chat's model and permissions. The
message must stay within existing authority; restart adds no deployment, outreach
or evaluation permission. The worker appends the receipt path for its resumed owner.

Queue acceptance and resumed work are separate results. The CLI can exit zero
while warning that resume failed. Failed or timed-out submission is unknown,
because acceptance may already have happened. Never resend while the original
submission remains unresolved; no visible turn is not proof of an empty queue.

Read the receipt directly or run:

```powershell
python -B -X utf8 '<skill>/scripts/restart_desktop.py' status --receipt '<returned-path>'
```

Receipts live under <Codex home>/onepersonlabs/desktop-restarts. Each has one
matching .claimed file. The resumed root owns reconciliation and removes both
after confirming restart and continuation delivery, or resolving a failed
operation. Preserve unresolved submission state and report it. On later restart
maintenance, inspect inactive receipts older than seven days and remove only
those whose operations are reconciled; reading them does not renew retention.
These are temporary recovery records, not a task ledger or evidence archive.

Verify the intended loaded configuration or skill availability in the resumed
context. If a fresh chat was chosen, pass the checkpoint and source/issue pointers
through the native create-thread tool and confirm that work starts. Distinguish
app restart, queue acceptance, message delivery and fresh-context loading. Do not
close the owning work because package tests or mocked process checks passed.

## Mechanism sources

Electron documents [Quit roles](https://www.electronjs.org/docs/latest/tutorial/menus#roles)
and [window menu removal](https://www.electronjs.org/docs/latest/api/browser-window#winremovemenu-linux-windows).
The installed Windows app uses a custom menu after removing the native window
menu. Inspect the exposed controls and their actual result; a menu definition or
successful input injection alone does not establish that Quit ran.

Microsoft documents [job inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
and [local WMI process creation](https://learn.microsoft.com/en-us/windows/win32/wmisdk/creating-processes-remotely).
Local creation can remain in the interactive session while avoiding the caller's
job; the worker verifies independence rather than assuming launch success proves it.

The [Desktop command reference](https://developers.openai.com/codex/app/commands/)
documents existing-chat navigation and new-chat composer links. Inspect the
installed queue --help for --resume behavior. Use supported native routes;
do not mutate session databases or invent app IPC to manufacture continuation.
