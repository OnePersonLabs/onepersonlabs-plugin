---
name: restart-codex-desktop
description: Restart or reload Codex Desktop after plugin, skill, instruction, or configuration changes, with optional reopening and a scoped continuation in an existing thread. Use when a fresh Desktop session is needed; installing or editing configuration alone does not authorize quitting the app.
---

# Restart Codex Desktop

Prepare a restart without losing the next action. This skill works without
Conductor. Automatic discovery does not authorize an immediate restart.

## Establish the restart boundary

Discover the available Desktop tools first. Prefer a supported native restart
operation if its current contract covers graceful exit and reopening. The
currently exposed app tools have no restart operation. On native Windows, use
the bundled helper below. Other platforms and non-Appx installations need a
verified platform route or a manual Quit and reopen; do not adapt the Windows
helper by guessing executable names.

Finish the current coherent edit batch and its required checks before restarting.
Preserve unfinished work and its next authorized action in the existing work owner.
Reconcile active
writers, child agents, commands, pending approvals, and unsaved authored content.
Tell the user which application will close and which work will be interrupted.
Use existing restart authorization when it applies. If the user only requested
configuration changes, prepare the restart command and leave execution optional.

Resolve an optional thread/session identifier to an exact local UUID on the
correct host. Use available thread tools to confirm its title and current state.
Use `CODEX_THREAD_ID` only when the request means this chat. Do not select the
most recent session or infer another chat from a title match. A remote host or
WSL home is outside the helper's native Windows continuation route.

## Inspect and prepare

Use Python 3.11 or newer and the helper from this loaded skill directory:

```powershell
python -B -X utf8 '<skill>/scripts/restart_desktop.py' inspect
```

Inspection reads the installed `OpenAI.Codex` Appx manifest, verifies its Desktop
entrypoint and resources, and reports only the matching UI process identities.
The app's root UI may be `Codex.exe` or `ChatGPT.exe`; the bundled
`resources/codex.exe` is a CLI runner. A process name alone cannot distinguish
them. Inspection does not close, launch, or message anything.

Prepare one command for an **external PowerShell terminal that survives Desktop
exit**. Replace `<skill>` with the absolute loaded skill directory. Run it before
the user uses the application's **Quit** action:

```powershell
python -B -X utf8 '<skill>/scripts/restart_desktop.py' wait-and-reopen --timeout-seconds 60
```

Add `--thread '<UUID>'` to reopen an existing chat. Quote actual PowerShell
arguments with single quotes and double any embedded single quote. Do not launch
the helper from a Desktop-owned terminal or tool process whose survival after
Quit has not been established. If no surviving external terminal is available,
give the user the command or use a fully manual restart.

On Windows, closing a window can leave the application running in the tray.
Use the application's Quit action. The helper never sends forceful termination
or kills a process by name. It waits at most the selected timeout for all observed
UI processes at the manifest path to exit, then launches that exact UI executable.
It stops if the installation changes, new UI processes appear before exit, or the
timeout expires. A timeout leaves the app alone and sends no continuation.
After launch, it waits up to 30 seconds for a new UI process. Process observation
does not establish UI readiness, thread navigation, or configuration receipt.

## Optional continuation

A thread ID alone requests navigation. When the user also requests that work
continue after restart, prepare one short prompt stating the authorized next
action, constraints, and unresolved checks. Show that prompt before execution.
The restart request does not authorize deployments, messages to other people,
additional evaluations, or wider task scope.

Add these arguments to the same external-terminal command:

```powershell
--thread '<UUID>' --codex-home '<native-Windows-Codex-home>' --message '<reviewed continuation prompt>'
```

The helper verifies the package's native CLI supports `queue --resume` before
waiting for Quit. After observing a new UI process, it calls
`codex queue --thread <UUID> --message <prompt> --resume` exactly once using the
selected `CODEX_HOME`. It preserves the thread's model and permissions. This
submits an AI prompt and can start another turn; omit `--message` when only
reopening was requested. Never enqueue a second copy through an app tool.

Queue acceptance and resumed work are different results. The CLI can exit zero
while warning that resume failed. The helper therefore reports `accepted` with
the CLI output and `resume_confirmed: false`. Any failed or timed-out submission
is `unknown`, because acceptance may already have happened. It never retries.
Keep the external terminal result and the reviewed prompt visible. On an unknown
result or missing turn, reconcile the original submission and pending state using
supported evidence before sending another prompt. No visible turn does not prove
that a queued prompt is absent. If the original submission remains unresolved,
report that uncertainty and do not resend. No persistent service, queue
ledger, or recovery sidecar is created.

In the resumed chat, check the pending work and actual loaded capabilities before
continuing. Reopening an existing chat does not prove that changed skills or
startup instructions entered that chat's context. Use a fresh chat when the
change requires new initial context. A received continuation establishes delivery;
only completed work and its required checks establish task completion.

## Evidence and limits

The [official Desktop command reference](https://developers.openai.com/codex/app/commands/)
documents `codex://threads/<thread-id>` for navigation. The
[official CLI reference](https://learn.chatgpt.com/docs/cli/reference) documents
queueing to an existing session. Inspect installed `queue --help` for the local
`--resume` behavior. The current Windows package's manifest and installed app
source establish its executable and its window-close/tray-Quit distinction;
recheck those sources if the installed behavior changes.

Report inspection, helper launch, old-process exit, new-process observation,
queue acceptance, delivery, and loaded capability separately. Source review and
simulated process checks do not qualify an actual restart. If the native route
cannot meet the request, state that limit and leave a concrete manual recovery
path; do not add an app-server, unsupported IPC, SQLite writes, or a daemon.
