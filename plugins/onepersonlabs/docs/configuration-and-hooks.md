# Codex configuration and hooks

This guide is for people who want to understand what OnePersonLabs changes in
Codex, tune their setup, or diagnose a startup notice. OnePersonLabs provides
skills and several local hooks. Its compatibility check is advisory guidance,
not a security boundary or a deterministic command gate.

## Choose the right configuration owner

- Use **[$onepersonlabs:configure-harness](../skills/configure-harness/SKILL.md)** to inventory the selected Codex home and prepare or diagnose user-level Codex settings. It distinguishes plugins, skills, tools, instructions, and effective configuration. It does not automatically install a capability or change an external account.
- Use **[$onepersonlabs:setup-repo-workflow](../skills/setup-repo-workflow/SKILL.md)** for a repository's issue tracker, checks, review, merge, parallel work, and resumption path. It does not configure personal Codex capabilities.
- Use **[$onepersonlabs:update-instructions](../skills/update-instructions/SKILL.md)** to check and update OnePersonLabs' global `AGENTS.md` instructions. It does not configure `config.toml`.
- Use **[$onepersonlabs:codex-hook-debug](../skills/codex-hook-debug/SKILL.md)** when a particular hook is missing, untrusted, fails, or returns unexpected output. It identifies the active host, Codex home, event, matcher, and owning definition before recommending a repair.

Treat a listed or installed capability as different from an enabled capability.
An available tool can still be unauthenticated, unavailable to the current
host, or unusable for a particular task.

## Inspect or repair OnePersonLabs' managed Codex defaults

The installed plugin provides a read-only check and an explicit repair command.
Run them with Python 3.11 or newer and the `scripts` directory from the
installed plugin copy. In PowerShell:

```powershell
$pluginRoot = "<installed OnePersonLabs plugin directory>"
python "$pluginRoot/scripts/codex-config-check.py" check
```

Inspect the report before changing settings. When the repair is authorized, run:

```powershell
python "$pluginRoot/scripts/codex-config-check.py" fix
```

On POSIX, use `python3` and the installed plugin path. By default, the checker
uses the active `CODEX_HOME`, or the standard user Codex home when it is unset.
Use `--home PATH` only when you intend to inspect or repair that specific home.
The commands print a JSON report. `check` reports whether the managed baseline
matches. `fix` explicitly reconciles it and verifies the result; it does not
perform an install or load the changed settings into an already-running task.

The managed baseline is defined in
[`config.defaults.toml`](../config.defaults.toml). It covers the
`apply_patch_preserve_line_endings` feature, enables agents, and sets the
default subagent model and reasoning effort to Luna/high when those values are
absent. A user's explicit subagent model or effort is preserved.

The package ships two Codex agent profiles for Slop Buster:

- [`onepersonlabs-slop-reader`](../agents/onepersonlabs-slop-reader.toml) uses Luna/medium for bounded source-evidence review.
- [`onepersonlabs-slop-analyst`](../agents/onepersonlabs-slop-analyst.toml) uses Sol/high for an assigned failure-pattern question.

The checker registers profiles from the installed package and checks their
source paths. It only replaces or removes a profile entry when its `config_file`
path proves OnePersonLabs ownership; a matching name by itself is not enough.
User profiles and unrelated settings remain in place.

An explicit configuration transaction keeps its receipt and any prior bytes
under `<CODEX_HOME>/onepersonlabs/harness/transactions/`, or under
`~/.codex/onepersonlabs/harness/transactions/` when `CODEX_HOME` is unset. Keep
the returned receipt if you may need to roll back. The transaction helper restores only
files that still match the transaction's written version; it preserves files
that changed afterward and reports a conflict for inspection.

## Know which copy changed

| State | What it establishes |
| --- | --- |
| Written and checked | The source checkout contains the change and its stated verification. |
| Published | The commits are available remotely; an open PR still awaits landing. |
| Landed | The accepted branch contains the change, with required checks and review complete. |
| Installed | The selected Codex home has a refreshed plugin copy and its reported trust state. |
| Loaded in a fresh task | That new task can discover the installed components; earlier tasks retain already-loaded context. |

Each transition needs its own evidence. A source edit does not update an installed
copy, and plugin installation does not replace global instructions. Use the
[refresh skill](../skills/refresh-local-plugins/SKILL.md) for source installations
and the procedure below for the instruction file.

## Update global instructions

At session start, a read-only hook checks the installed OnePersonLabs version
against the version marker in the effective global `AGENTS.md`. It can report
that instructions are missing, outdated, invalid, or newer than the installed
plugin. This notice does not edit the file or stop the pending task. If the
installed plugin is older than the user's instructions, update the plugin
instead of downgrading the instructions.

When an update is wanted, name `$onepersonlabs:update-instructions`. It inspects
the effective instruction file and installed plugin, then replaces the complete
file with the installed baseline when an update is authorized. A dated,
byte-exact backup is written beside the target as
`AGENTS.md.onepersonlabs-backup-YYYYMMDD-NNN`. Custom rules are not merged into
the new baseline; recover them from that backup if needed. Start a fresh Codex
task to load changed global instructions.

## Set repository compatibility expectations

The optional repository policy lives in `.onepersonlabs/config.json`. It checks
Codex plugins, skills, and MCP servers against declared repository needs; it
does not install or enable them. For example:

```json
{
  "codex": {
    "compatibility": {
      "version": 1,
      "onViolation": "warn",
      "required": [{ "kind": "mcp", "name": "project-docs" }],
      "recommended": [{ "kind": "skill", "name": "project-build" }]
    }
  }
}
```

The policy can declare `required`, `recommended`, `disallowed`, conditional
`rules`, and documented `ignoreRules`. Plugin IDs use `name@marketplace`;
skill names omit the `$` invocation prefix. Add provider qualification when a
specific plugin or duplicate skill matters. A missing enabled-skill override
does not prove that the skill is absent; use discovered identity and path.
The full selector, conditional-rule, and exception behavior is in the
[compatibility reference](compatibility.md).

From the marketplace checkout on Windows, inspect the current repository with:

```powershell
python plugins/onepersonlabs/scripts/codex-compatibility-check.py --check --cwd C:/dev/my-project
python plugins/onepersonlabs/scripts/codex-compatibility-check.py --check --cwd C:/dev/my-project --json
```

On POSIX, use `python3` and the repository's native path. For an installed
copy, use its `scripts/codex-compatibility-check.py`. The checker requires
Python 3.11+ and the Codex CLI; npm-based Codex launchers also need Node.js.
If Codex discovery cannot resolve the launcher, set `CODEX_BIN` to its native
executable or JavaScript entrypoint. Exit code `0` means no required policy
violation, `1` means a violation, and `2` means invalid policy or incomplete
discovery. Missing recommendations may still be reported with exit code `0`.

The plugin runs the compatibility check at session start and again when a user
prompt is submitted. With the default `onViolation: "acknowledge"`, the hook
asks the agent to present policy or discovery findings. The user can continue
that task by replying exactly `continue`, `ok`, `okay`, or `continue anyway`.
With `onViolation: "warn"`, findings are reported without that pause. This is
a cooperative instruction to the agent; it is not an execution or security
gate. Unknown ownership or enablement is reported as unverifiable, not absent
or safe. The diagnostic `--check` always reads fresh local metadata. See the
[compatibility guide](compatibility.md) for discovery details and
failure recovery.

## Know what the installed hooks do

The plugin's [hook definitions](../hooks/hooks.json) define these event
behaviors. Codex must have the plugin enabled and its current hook definitions
trusted for the hooks to run.

| Hook family | What it does | What it does not establish |
| --- | --- | --- |
| Session start and user prompt | Reports managed configuration or instruction notices; checks repository compatibility and handles its pending acknowledgments. | It does not silently repair settings or replace instructions. |
| Prompt, pre-tool, and stop lifecycle | Slop Buster can add advisory steering and persist findings for later review. | It does not force an apology, stop continuation, or require a Boolean rating. |
| Tool and task lifecycle | The task watchdog records local activity events for later status or optional notification. | Recording activity does not start the notification process or prove that a stalled task is complete. |
| Human-collaboration events | Reads relevant local collaboration state and supplies pending context when available. | It does not enroll a session, start the service, or submit a human contribution. |
| Bash pre-tool use | Applies a conservative check to common destructive shell-command shapes. | It is not a complete shell parser or general command safety system. |

The [Bash guard](../scripts/codex-dangerous-shell-gate.py) recognizes certain
force-push forms, `git reset --hard`, recursive removal aimed at root, home,
the current directory, or a path glob. It also recognizes parent-directory
traversal in removal paths and `rm --no-preserve-root`. It rejects
recognized input with a diagnostic and exit status 2. It does not analyze
other tool types or guarantee that an unrecognized command is safe. Narrow,
quoted paths remain easier to review.

Review and trust the plugin's current hook definitions in Codex before relying
on hook behavior. A trust record alone does not prove that a particular event
matched or that a hook produced the intended result. For diagnosis, preserve
the event, triggering action, host, Codex version, and relevant output, then
use `codex-hook-debug` to trace the active definition and handler.

## Run optional task-watch notifications

The [lifecycle hook](../scripts/codex-task-watch.py) records active-session
events locally under
`$CODEX_HOME/codex-watch/state.sqlite3`, or under the standard user Codex home
when `CODEX_HOME` is unset. Notifications are optional and require a separate
foreground process. The default idle threshold is 25 minutes. To send a message,
configure an HTTPS ntfy topic URL in `CODEX_WATCH_NTFY_URL` and, if
the topic requires it, `CODEX_WATCH_NTFY_TOKEN`. From this repository checkout,
for example, use PowerShell:

```powershell
$env:CODEX_WATCH_NTFY_URL = "https://ntfy.example.com/<private-topic>"
$env:CODEX_WATCH_NTFY_TOKEN = "<optional-token>"
npm run codex-watch -- run
```

From an installed plugin, use Python 3.11+ with its script. On Windows, use
`python`; on POSIX, use `python3`.

```text
python <plugin-root>/scripts/codex-task-watch.py run
```

The process stays in the foreground; press Ctrl+C to stop it. The notification
includes the last completed assistant response. Use an access-controlled topic
and treat its contents as private.
Do not put the topic token in shared shell history or reports.

Use `status` or `status --json` to inspect recorded sessions. Use
`test-notification` to send a real message to the configured topic, and
`prune --older-than 30d` to delete old session records. `run` and
`test-notification` require `CODEX_WATCH_NTFY_URL`; status and prune do not.
If no activity appears, first check that OnePersonLabs is enabled, its hooks
are trusted, and the relevant Codex task loaded the current plugin. If delivery
fails, the process reports the final error; correct the URL, token, or topic
access, then restart it.
