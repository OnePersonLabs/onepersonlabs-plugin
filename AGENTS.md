# Repository Instructions

## Local plugin development

This repository uses the source-first workflow in `README.md`. The plugin root
under `plugins/onepersonlabs/` contains only shipping files. Tests live under `tests/`.
Repository drivers live under `tools/`.

Create and update skills under `plugins/onepersonlabs/skills/` unless the user explicitly
specifies another location.
Interpret an unqualified reference to `AGENTS.md` as `plugins/onepersonlabs/AGENTS.md`
unless the user explicitly specifies another file.

`npm run install:local -- --plugin <plugin-name>` is an
installation-only consumer operation. It never runs unit tests, contract
checks, installed checks, or skill evaluations. An authorized local refresh
also trusts the selected installed plugins' current hooks through the shared
installer; leave unrelated hooks and sandbox settings unchanged. Use
`--plugin all` only when the user explicitly asks to install every marketplace
plugin. For a normal `$onepersonlabs:refresh-local-plugins` invocation, use the current
user's existing default Codex home or homes without asking for a path. Use an
explicit `--target-home` when the user names a home or the task clearly targets
one, including isolated tests.

## Human-collaboration service during a local plugin refresh

Before refreshing the local plugin, use `$onepersonlabs:human-collaboration`'s
`pause-for-refresh` operation from the workspace being refreshed. It checks
authenticated readiness, records whether the service was running and its bind
settings, and stops it gracefully only when it was running. The operation must
confirm both listener shutdown and process exit; an unresponsive live service
blocks refresh. Do not run separate repeated service checks. Continue only when
the operation reports the service stopped or not running.

After the refresh attempt, use the installed `$onepersonlabs:human-collaboration` skill's
`resume-after-refresh` operation from the same workspace, even if the installer
failed. It starts the service only when the pause record says it was running.
If the installed helper is unavailable because refresh failed, use the source
skill to resume it. A failed restart keeps the record for retry; report the
failure and do not clear it. When the service restarts, open and report the new
pairing URL returned by the operation.

## After a local plugin refresh

After a successful `$onepersonlabs:refresh-local-plugins` refresh targeting this `onepersonlabs-plugin` repo:

- Run the OnePersonLabs checks used
  at session startup.
- Apply required OnePersonLabs agent TOML configuration and documented defaults with the installed `scripts/codex-config-check.py fix`.
- Update outdated global instructions with
  `$onepersonlabs:update-instructions`.

## Tests

Apply the shared [Verification and experiments](plugins/onepersonlabs/AGENTS.md#verification-and-experiments)
policy to all repository work, including `tests/` and `tools/`.
Run commands from the repository root. Select affected checks below and complete
all required gates.

| Change or checkpoint                           | Check                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Executable integration                         | `npm run test:contract -- --plugin <plugin-name>` and `npm run test:unit -- --plugin <plugin-name>` |
| Skill instructions or activation metadata      | Review the changed package against its sources and validate its structure.                          |
| MCP launcher or server metadata                | `npm run test:mcp -- --plugin <plugin-name>`                                                        |
| UI code or resources                           | `npm run test:ui -- --plugin <plugin-name>`                                                         |
| Package-visible files at a coherent checkpoint | `npm run test:installed -- --plugin <plugin-name>`                                                  |

`test:installed` includes contract and unit checks. When it is required at the
same checkpoint, use it instead of first running those suites separately.
The installed checkpoint verifies package files, discovery and hook trust
without manual sign-in, sandbox onboarding or `/hooks` confirmation. Surface
failures rather than skipping the checkpoint. See the
[contributor guide](docs/contributing.md#verify-the-affected-behavior) for its isolated-home procedure.

`npm run verify` runs the full deterministic repository gate without model
evaluations. The pre-push hook runs it followed by
`npm run test:installed -- --plugin all --package-only`. Package-only mode skips
unit checks but still runs contract checks. Preserve these required hooks.

The explicit `npm run release:verify` gate runs verification and clean installed
checks for every plugin. The full skill corpus is not a routine update check.
