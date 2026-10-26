# Troubleshooting

Start with the observed failure and the copy or environment involved. Preserve
the original error and any recovery receipt before retrying. Use
`$onepersonlabs:codex-hook-debug` for hook failures and
`$onepersonlabs:configure-harness` for capability or configuration problems.

## The plugin or skill is missing

1. Run `codex plugin list --json` in the affected environment. Confirm the
   installed entry is `onepersonlabs@onepersonlabs` and enabled.
2. Run `codex plugin marketplace list --json` to inspect the source registration.
   A cache folder or available marketplace entry is not an installed plugin.
3. Start a fresh task after installation or refresh. Check the skill's exact
   name in the [catalog](skills.md) and invoke it explicitly.
4. If still missing, ask `$onepersonlabs:configure-harness` to inspect that
   Codex home and working directory. Its discovery distinguishes disabled,
   unavailable, duplicated, and unverifiable capabilities.

Do not fix discovery by editing the installed cache. Local source-refresh
conflicts need the intended marketplace mapping resolved first.

## A hook gives no report or fails

Verify the plugin is enabled, its current hooks are trusted in `/hooks`, and
the hook process can find Python and Codex. Windows uses `python`; POSIX uses
`python3`. A working interpreter in another terminal or WSL distribution does
not prove the hook can use it.

```text
Use $onepersonlabs:codex-hook-debug to investigate this hook failure.
Here is the event, exact error, affected environment, and expected behavior: …
```

The skill inspects registration, payload, execution, and evidence. An absence
of warnings can also be normal: configuration notices are advisory and some
checks report only changes. See [hook behavior](configuration-and-hooks.md).

## Startup reports a configuration or instruction mismatch

Startup notices inspect state; they do not repair it. Use
`$onepersonlabs:configure-harness` to inspect and prepare supported configuration
changes. Use `$onepersonlabs:update-instructions` for outdated global instructions.
The latter replaces the effective file under established authorization, saves a
dated byte-exact backup, and does not merge custom rules. Never downgrade a newer
instruction revision. Start a new task after an update.

## Compatibility asks for acknowledgment or cannot verify a capability

Read the reported policy source and diagnostic first. The
[compatibility reference](compatibility.md#run-a-diagnostic) gives the
read-only command and exit statuses. `cannot_verify` means discovery lacks
decisive evidence; it does not establish that a component is absent.

With the policy's default `acknowledge` mode, after reviewing the findings you
can reply exactly `continue`, `ok`, `okay`, or `continue anyway` to resume the
pending task. This accepts the current findings; it does not repair configuration.
Policy or inventory changes can require another acknowledgment. `warn` mode
reports without requesting a pause. The checker is cooperative guidance, not a
security boundary.

## A refresh failed or only one environment updated

Read the per-environment report. A Windows failure does not undo a successful
WSL refresh, or vice versa. Resolve the reported source, preparation, inventory,
or installer error before retrying the failed route. A same-name marketplace
pointing elsewhere requires a deliberate mapping decision.

If automatic hook trust fails, finish the other reachable refreshes, then open
a fresh session in each affected environment, review and trust the selected
plugin's hooks with `/hooks`, and return to the agent for verification. Installation
is incomplete until the failed trust check is reconciled.

Run `resume-after-refresh` even after a failed installer attempt if the service
was paused. Use the source helper if the installed helper is unavailable. A
failed restart retains its pause record for retry; do not delete that record.
The [refresh lifecycle](collaboration-and-recovery.md) explains process shutdown
and the replacement pairing URL.

## Human feedback or task continuation seems lost

A saved draft is not a submitted response. Reopen the existing inbox and inspect
the item's status before creating another request. The root must reconcile
pending submissions and ownership when it resumes. Phone reachability, submission
receipt, agent continuation, and integration of the answer are separate states.

For interrupted issue work, resume the existing conversation and checkpoint where
possible. Inspect remote state before retrying an uncertain GitHub write. See
[collaboration and recovery](collaboration-and-recovery.md) and the
[workflow session](workflow.md). Auto-merge does not wake an agent or select its
next issue.

## Migrating an old OPL installation

This is a one-time migration, not the normal update path. Have the old home or
project path, the new destination, and a separate recovery folder available.
Ask Codex to inspect the [migration helper](../scripts/migrate_identity.py) and
the relevant installations before changing registrations.

1. Run the previous collaboration service's `pause-for-refresh` operation and
   confirm listener shutdown and process exit before removing the old plugin.
2. From the new plugin directory, run the home migration with Python 3.11+.
   Replace the paths below with actual paths; on POSIX use `python3`:

   ```text
   python scripts/migrate_identity.py --home <codex-home> --backup-root <external-recovery-folder>
   ```

3. Add `--rename-root <old-checkout>=<new-checkout>` for each renamed checkout.
   Quote arguments containing spaces. For a repository containing `.opl` or
   `.borg` state, run the helper with `--project <repo>` and a separate backup folder.
4. Replace the old marketplace/plugin registrations, refresh OnePersonLabs, and
   complete `resume-after-refresh` from the renamed workspace.

The helper preserves collaboration identities, recovery receipts, and disabled
skill preferences, and retires manifest-verified old agent registrations.
For custom runtime locations, `OPL_HUMAN_RUNTIME` selects the source and
`ONEPERSONLABS_HUMAN_RUNTIME` the destination. Set the new variable before
migration to retain a custom location; otherwise the platform default applies.
Destination collisions stop the transfer. After interruption, reconcile the
external progress record before retrying. Keep backups until the migrated
consumer and its recovery state have been verified.

[Back to OnePersonLabs](../README.md) · [Getting started](getting-started.md)
