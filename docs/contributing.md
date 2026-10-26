# Contributing to OnePersonLabs

Work in the source checkout to change the plugin. The
[user guides](../plugins/onepersonlabs/README.md) describe using an installed copy;
this guide covers editing, checking, publishing, and refreshing source changes.
Read the repository's [AGENTS.md](../AGENTS.md) before starting work.

## Set up the checkout

Use Git, Node.js 24 or later, Python 3.11 or later, and a Codex CLI with plugin
and app-server support. The `last30days` research engine needs Python 3.12 or later.
On Windows, run from PowerShell:

```powershell
npm ci
python -m pip install playwright
```

On POSIX, use `python3 -m pip install playwright` in your chosen Python environment.
`npm ci` installs repository dependencies and prepares the Git hooks.
UI checks require Chromium. They can use an installed browser; to install
Playwright's development browser, run `python -m playwright install chromium`
(`python3` on POSIX). Set `ONEPERSONLABS_CHROMIUM_BIN` for a specific executable
and `PYTHON_BIN` for a different Python interpreter. Checks report missing
prerequisites rather than installing them.

## Know what ships

| Location | Responsibility |
| --- | --- |
| `plugins/onepersonlabs/` | Entire shipping plugin, including user docs, skills, hooks, scripts, and profiles. |
| `tests/` | Tests and fixtures, outside the installed package. |
| `tools/` | Repository check and installation drivers. |
| `.agents/plugins/marketplace.json` | Marketplace identity and shipping source path. |
| `docs/` | Contributor instructions and retained design/evidence records. |
| `.work/current-work.md` | Ignored local active-work, decision, and recovery checkpoint. |

Edit source, never the installed cache. Shared user guides belong inside the
plugin so their relative links work after installation. Link from both READMEs
to the owning guide; avoid maintaining copies of the same procedure.

## Make one connected change

Inspect current branch, dirty work, instructions, and the owning issue. Follow
the [workflow guide](../plugins/onepersonlabs/docs/workflow.md); this repository
uses GitHub for actionable work, existing specifications for meaning/evidence,
and the local checkpoint for recovery. Keep one primary issue through delivery.

For a skill change, edit `plugins/onepersonlabs/skills/<name>/SKILL.md` and review
its `agents/openai.yaml` activation metadata. Keep examples and references
consistent with its actual consumer. Add scripts or abstractions only for an
established need. Document changed reader actions, prerequisites, and results
with `$onepersonlabs:write-docs`.

`plugins/onepersonlabs/AGENTS.md` is the shipped instruction template. When its
content changes, increment its positive `onepersonlabs-instructions-version`
marker and stage the bump with the content. The pre-commit hook checks staged
content against `HEAD`. Ordinary guide edits do not require an instruction
revision or a timestamp version bump.

Keep separate independent writers in isolated branches/worktrees. Root owns
integration and issue writes. Stage only task-owned files, preserve unrelated
work, and checkpoint coherent verified units before moving to another concern.

## Verify the affected behavior

Run commands from the repository root. Keep successful output quiet and retain
useful diagnostics when something fails.

| Change or checkpoint | Existing command |
| --- | --- |
| Focused reproduced behavior | `npm run test:focus -- --file tests/unit/onepersonlabs/codex-hooks.test.mjs` (replace with the relevant supported test file) |
| Executable integration | `npm run test:contract -- --plugin onepersonlabs` and `npm run test:unit -- --plugin onepersonlabs` |
| MCP launcher/server metadata | `npm run test:mcp -- --plugin onepersonlabs` |
| UI code/resources | `npm run test:ui -- --plugin onepersonlabs` |
| Package-visible files | `npm run test:installed -- --plugin onepersonlabs` |
| Complete deterministic repository gate | `npm run verify` |
| Explicit release gate | `npm run release:verify` |

Review skill instructions and activation metadata against their sources and
validate package structure. For documentation, check command syntax, links,
anchors, expected results, and consequential recovery paths. Render changed
diagrams. Source inspection supports implemented intent; it does not prove the
documented runtime journey or a reader's understanding.

The installed checkpoint runs contract and unit checks, installs into a separate
persistent black-box Codex home, compares all package files, and verifies selected
hook trust through the app-server API. It does not require interactive sign-in
or manual `/hooks` confirmation. Surface discovery or trust failures.

The pre-push hook runs `npm run verify` and
`npm run test:installed -- --plugin all --package-only`. The latter validates
package/discovery/trust for every marketplace plugin without another unit run.
This is test isolation, not installation into your active homes. Reuse valid
evidence between checkpoints; preserve these required hooks.

Do not add skill invocation tests. Model-consuming evaluations require explicit
permission and a finite budget; deterministic or release checks do not grant it.
Add permanent tests only for meaningful owned contracts, not as mirrors of an edit.

## Publish and refresh

This repository defaults to checked commits on the selected branch. After a
standalone unit passes required checks, push its commits. New delivery branches
and PRs are opt-in. For selected PR delivery, review the full series against
its starting baseline, keep the builder responsible for repairs, and merge
after required checks/reviews under the existing protections. Verify landing
and synchronize the accepted base before refreshing.

Use the installed `$onepersonlabs:refresh-local-plugins` skill for the refresh:

```text
Use $onepersonlabs:refresh-local-plugins to refresh onepersonlabs from this
checkout. Follow this repository's collaboration-service pause/resume and
post-refresh checks, and report each Windows/WSL result.
```

The skill's `--dry-run` mode previews per-home selection without installation.
Normal refresh uses existing user homes and the other environment's installed
inventory; disabled installed counterparts are eligible and become enabled.
`--target-home` is for an explicit home or isolated test. Source publishing is
separate from installation.

The direct repository command is `npm run install:local -- --plugin onepersonlabs`.
It only installs and establishes selected hook trust; it does not run tests or
perform the surrounding service and post-refresh procedure for you.

Follow the [service lifecycle](../plugins/onepersonlabs/docs/collaboration-and-recovery.md):
pause before replacement and resume after the attempt, even on failure. Restore
only a previously running service and report its new pairing URL when restarted.
After a successful refresh, run installed configuration and instruction checks
in each refreshed home. This repository's standing authorization covers required
configuration fixes and outdated global-instruction updates, with backups and
no downgrade. Preserve the user-requested post-refresh rule as specified in
the repository instructions. Do not generalize this authorization to other users.

Report checked source, published commits, installed files, and fresh-session
loading separately. A refresh does not change components already loaded in the
current task. Close the issue only when its complete acceptance scope is met.

## Design and evidence records

These retain decisions and observations from their recorded baselines. Use the
current user guides for procedures; consult the records for reasons and limits.

- [Overhaul audit](onepersonlabs-overhaul.md): skill dispositions, verification,
  and delivery changes, including the 2026-10-21 follow-up.
- [Runtime research](runtime-research.md): 2026-10-20 comparison and unresolved
  unattended lifecycle requirements.
- [Local Itervox proposal](itervox-upstream-proposal.md): 2026-10-20 draft, not an
  installed runtime or an upstream submission.
- [Compound assimilation](compound-assimilation.md): 2026-10-21 capability choices
  and evidence limits.
- [WTFM assimilation](wtfm-assimilation.md): 2026-10-21 documentation discipline
  and deliberately excluded machinery.
- [Confidence steering experiment](confidence-steering-experiment.md): retained
  experimental evidence and its recorded disposition, not a current capability promise.

Instruction baseline recovery uses local history first. Remote recovery uses
the original plugin repository for revisions below 10 and this repository for
revisions 10 and later, as implemented by the existing recovery helpers.

[Back to the repository](../README.md)
