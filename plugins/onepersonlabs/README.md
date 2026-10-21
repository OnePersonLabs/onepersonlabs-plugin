# OnePersonLabs

One-Person Labs focused skills, shared instructions, integrations, and advisory workflow hooks for Codex.

## Runtime

Hooks use Python 3.11 or later and the standard library. Native Windows uses `python`; POSIX uses `python3`. Research through `$onepersonlabs:last30days` requires Python 3.12 or later. Provider discovery through an npm Codex launcher also requires Node.js. GitHub workflow operations use supported GitHub tools or `gh`.

Install the browser and retrieval tools used by the relevant workflows:

```sh
npm install -g agent-browser chrome-devtools-cli fetch-cli
agent-browser install
```

On Linux, use `agent-browser install --with-deps` to install Chromium system dependencies.

## Skills

Invoke a skill with `$onepersonlabs:<skill-name>`. Common starting points:

| Skill | Purpose |
| --- | --- |
| [$onepersonlabs:setup-repo-workflow](skills/setup-repo-workflow/SKILL.md) | Explicitly configure one repository using native tools. |
| [$onepersonlabs:github-workflow](skills/github-workflow/SKILL.md) | Maintain authorized issue capture and delivery status. |
| [$onepersonlabs:debug](skills/debug/SKILL.md) | Investigate and reproduce a failure. |
| [$onepersonlabs:design-perceptual-interfaces](skills/design-perceptual-interfaces/SKILL.md) | Explore consequential design and inspect implemented meaning, motion, and visual craft. |
| [$onepersonlabs:test-driven-development](skills/test-driven-development/SKILL.md) | Explicitly choose red/green development. |
| [$onepersonlabs:adhd](skills/adhd/SKILL.md) | Preserve task state and keep one active path. |
| [$onepersonlabs:configure-harness](skills/configure-harness/SKILL.md) | Compare capabilities and review a deliberate setup. |
| [$onepersonlabs:update-instructions](skills/update-instructions/SKILL.md) | Replace outdated global instructions after one approval, keeping a dated backup. |
| [$onepersonlabs:handoff](skills/handoff/SKILL.md) | Prepare a resumable task handoff. |
| [$onepersonlabs:long-command-wakeup](skills/long-command-wakeup/SKILL.md) | Run a long command and queue a bounded continuation. |
| [$onepersonlabs:refresh-local-plugins](skills/refresh-local-plugins/SKILL.md) | Refresh selected local plugins and verify hook trust. |

All shipped skills are in [skills/](skills/).

## Instructions and agents

The instruction context hook compares the installed instruction revision with the user's recorded version. Use `$onepersonlabs:update-instructions` to replace outdated instructions after one approval. It saves the previous file byte for byte in a dated backup; custom rules are not merged.

OnePersonLabs ships two domain-specific Slop Buster profiles in [agents/](agents/). Native delegation and user-authored profiles remain available. Local installation reconciles verified OnePersonLabs-owned registrations while preserving personal profiles.

## Upgrade from OPL

Pause the previous human-collaboration service with `pause-for-refresh` before
removing the previous plugin. Run `python scripts/migrate_identity.py --home
<codex-home> --backup-root <external-recovery-folder>` from this plugin directory.
Add `--rename-root <old-checkout>=<new-checkout>` for each renamed checkout.
The one-time transfer preserves collaboration identities, recovery receipts and
disabled-skill preferences, and retires manifest-verified old agent registrations.
Custom runtime paths follow `OPL_HUMAN_RUNTIME` as the source and
`ONEPERSONLABS_HUMAN_RUNTIME` as the destination. Set the new variable before
migration to retain a custom location; otherwise the new platform default is used.
It refuses destination collisions; reconcile its external progress record before
retrying an interrupted transfer. Run the same helper with `--project <repo>` for
any repository containing `.opl` or `.borg` state, using a separate backup folder.
Then replace the old native marketplace/plugin registrations and run the normal
refresh. Complete `resume-after-refresh` from the renamed workspace afterward.

## Repository policy and advisories

The [compatibility guide](compatibility/README.md) defines optional repository policy in `.onepersonlabs/config.json` . Hooks check enabled providers and report policy violations.

Slop hooks persist evidence and provide advisory steering. They do not require an immediate correction or Boolean rating. Startup configuration and instruction notices are read-only and nonblocking. Explicit update tools retain backups and recovery. No unattended issue dispatcher is installed.

## Task watchdog

The lifecycle observer records local task activity in `$CODEX_HOME/codex-watch/state.sqlite3`. To send a notification after 25 minutes without activity, set `CODEX_WATCH_NTFY_URL` to an HTTPS ntfy topic and optionally set `CODEX_WATCH_NTFY_TOKEN`. Then run:

```sh
npm run codex-watch -- run
```

From an installed plugin, run `python <plugin-root>/scripts/codex-task-watch.py run` (`python3` on POSIX). Notifications include the last completed assistant response; use an access-controlled topic when this text is private. The script also supports `status --json`, `test-notification`, and `prune --older-than 30d`.
