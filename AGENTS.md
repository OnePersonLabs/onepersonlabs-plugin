# Repository Instructions

## Issue and recovery ownership

Use `$onepersonlabs:github-workflow` to keep actionable work, decisions, recovery
and delivery status in the owning GitHub issue in OnePersonLabs/onepersonlabs-plugin.
Use `$onepersonlabs:setup-repo-workflow` only for explicit setup or migration.
Keep one primary issue through landing and up to two useful bounded helpers.
Do not create another task ledger. New product or runtime scope needs its own
authorization; the repository's publication default below covers finished
authorized tooling units only.

## Local plugin development

This repository uses the source-first workflow in `README.md`. The plugin root
under `plugins/onepersonlabs/` contains only shipping files. Tests live under `tests/`.
Repository drivers live under `tools/`.

Create and update skills under `plugins/onepersonlabs/skills/` unless the user explicitly
specifies another location.
Interpret an unqualified reference to `AGENTS.md` as `plugins/onepersonlabs/AGENTS.md`
unless the user explicitly specifies another file.

During authorized implementation, make small, coherent, verified task-owned
checkpoint commits before moving into another concern. Do not blanket-stage,
force broken splits, or push/refresh after each checkpoint.

Work in the selected checkout and branch by default. New delivery branches and
PRs are opt-in; parallel independent writers still need separate worktrees and
branches. Preserve small, coherent commits that are understandable and reviewable
on their own, and leave working states.

After completing a standalone unit and its required checks, push its checkpoint
commits to the selected branch. If PR delivery is selected, review the full series
against its frozen starting baseline, repair findings, and merge automatically
once required checks and reviews pass. Preserve checkpoint history; do not squash
unrelated units together. Use native auto-merge for outstanding GitHub requirements;
complete required local checks and reviews before an immediately available merge.
Keep branch protections and explicit manual-merge requirements in force.

After landing, synchronize the accepted base and run `$onepersonlabs:refresh-local-plugins`
with the service recovery and post-refresh checks below. A task-specific delivery
boundary can override this default.

OnePersonLabs's `plugins/onepersonlabs/AGENTS.md` has an independent positive integer instruction
revision in its `onepersonlabs-instructions-version` marker. Increment and stage that
revision whenever changing instruction content. The pre-commit hook compares
the staged file with `HEAD` and rejects changed content without a staged bump;
an unstaged bump does not satisfy the check. Initial version adoption uses 1
in an existing repository. The first standalone commit preserves the inherited
revision 10.

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

Before refreshing a local plugin, use `$onepersonlabs:human-collaboration`'s
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

After a successful `$onepersonlabs:refresh-local-plugins` refresh, run the OnePersonLabs checks used
at session startup. Check configuration and global instructions in each refreshed
user-level Codex home. The user has approved the update question: apply required
OnePersonLabs agent TOML configuration and documented defaults with the installed
`scripts/codex-config-check.py fix`, and update outdated global instructions with
`$onepersonlabs:update-instructions`. Do not ask for that approval again.

Keep the safety checks and dated backups from the update helpers. Do not downgrade.
If homes share an instruction file, update its resolved target once. After a
global-instruction replacement, restore this user-requested post-refresh rule in
the user-level file. Keep the rule in this repository's `AGENTS.md` and the
user-level file; do not add it to `plugins/onepersonlabs/AGENTS.md`.

## Tests

Apply the shared [Verification and experiments](plugins/onepersonlabs/AGENTS.md#verification-and-experiments)
policy to all repository work, including `tests/` and `tools/`.
Run commands from the repository root. Select affected checks below and complete
all required gates.

| Change or checkpoint | Check |
| --- | --- |
| Executable integration | `npm run test:contract -- --plugin <plugin-name>` and `npm run test:unit -- --plugin <plugin-name>` |
| Skill instructions or activation metadata | Review the changed package against its sources and validate its structure. |
| MCP launcher or server metadata | `npm run test:mcp -- --plugin <plugin-name>` |
| UI code or resources | `npm run test:ui -- --plugin <plugin-name>` |
| Package-visible files at a coherent checkpoint | `npm run test:installed -- --plugin <plugin-name>` |

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

Do not add timestamp cachebusters to plugin versions and do not restore the
retired all-plugin reinstall script. Codex's installed cache is tested only at
the black-box checkpoint or used by the explicit installation command.
