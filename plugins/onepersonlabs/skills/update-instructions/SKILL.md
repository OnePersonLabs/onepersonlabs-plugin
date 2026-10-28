---
name: update-instructions
description: Update outdated global AGENTS.md from installed OnePersonLabs defaults under established authorization, with a verified seven-day rollback backup.
---

# Update OnePersonLabs Instructions

The user owns their global instructions. When an update is available, inspect
the effective target and installed OnePersonLabs version, then reuse applicable update authorization or ask once whether to replace
the target with the installed `AGENTS.md`. Explain that active custom rules will
be replaced and the existing file will be saved for a bounded rollback window. A clear yes
authorizes that update; do not ask the user to review a candidate or diff.

## Inspect and establish authorization

Run `scripts/instructions.py inspect` with Python, relative to this skill's
directory. The helper resolves the active Codex home and effective global file,
including override precedence, and reports `target`, `sha256`,
`bundled_sha256`, and the user and bundled versions. Use `--home PATH` only when
the user selected a home; use `--plugin-root PATH` when the intended OnePersonLabs
instructions are outside this installed plugin.

- Matching versions: report that the target is current and stop.
- User version above installed version: report that this installation is older
  and stop. Never downgrade the target.
- Missing, unversioned, or invalid target: include that state in the update
  proposal. When authorized, replace it with installed OnePersonLabs instructions and
  preserve any existing bytes in a backup.
- Older valid version: state both versions and establish authorization to update.

If update authorization already covers this target and replacement, proceed
within that scope. Otherwise, before asking, explain that replacing the target
discards active custom rules.
The user can recover them from the exact backup, but they are not merged into
the new file. If the user declines, stop without writing files.

## Apply after approval

On approval, run the helper's `apply` command. It reads the installed OnePersonLabs
`AGENTS.md` directly:

```text
python scripts/instructions.py apply --expected-sha256 HASH --expected-target TARGET --expected-bundled-sha256 BUNDLED_HASH
```

Use the `target`, `sha256`, and `bundled_sha256` returned by the initial
inspection. For a missing target, pass `missing` as its expected hash. Pass the
same `--home` and `--plugin-root` overrides used during inspection.

The helper refuses to downgrade a newer target, verifies that the target and
installed instructions have not changed since inspection, saves a byte-exact
rollback copy, and atomically replaces the target. A verified replacement keeps
that copy for seven days. An incomplete replacement preserves its recovery copy
until its state is reconciled. Backup names use
`AGENTS.md.onepersonlabs-backup-YYYYMMDD-NNN`; `NNN` starts at `001` each day and increases
to avoid overwriting an earlier backup. A failed backup or replacement is an
error; never report success unless the replacement completed and its bytes
were verified. The backup filename ends in `.pending` until verification succeeds.
Successful verification renames it with `.expires-<epoch-seconds>` for a fixed
seven-day rollback window. No separate retention ledger is created.

The next apply removes verified expired backups. Preview with
`scripts/instructions.py cleanup --preview`, then run
`scripts/instructions.py cleanup` to remove overdue backups without updating
instructions. Pass the same home override when applicable. Legacy backups require a valid later instruction
version in the current target and use their original timestamp. A failed update
or unknown ownership remains an explicit recovery obligation. Report cleanup
failures instead of silently extending retention. An inactive home is cleaned
on the next applicable invocation, not by a background timer.

Re-run inspection and confirm the effective target has the installed version
and hash. The apply helper confirms exact readback and removes expired,
helper-owned backups on the next update or explicit `cleanup` invocation. Check
cleanup output and report unresolved recovery paths. Report the new backup
location while its rollback window remains. Ask the user to start a fresh
session to load the resulting global instructions; do not claim the current
session's already-loaded instructions were replaced.
