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
| `docs/` | Contributor instructions and evidence for open research. |

Edit source, never the installed cache. Shared user guides belong inside the
plugin so their relative links work after installation. The root README routes
users to the plugin README and contributors here. Keep installation and usage
procedures in the plugin guides; keep checkout, verification, and publication
procedures here.

## Make one connected change

Inspect current branch, dirty work, instructions, and the task's authorization.
The [workflow guide](../plugins/onepersonlabs/docs/workflow.md) covers issue
ownership and recovery. Link relevant design and evidence when it explains
the change.

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

The repository's [test instructions](../AGENTS.md#tests) own check selection,
required gates, and test policy. Run the selected commands from the repository
root. For a focused failure, `npm run test:focus -- --file <test-file>` runs an
existing supported test file. Keep successful output quiet and retain useful
diagnostics when something fails.

Review skill instructions and activation metadata against their sources and
validate package structure. For documentation, check command syntax, links,
anchors, expected results, and consequential recovery paths. Render changed
diagrams. Source inspection supports implemented intent; it does not prove the
documented runtime journey or a reader's understanding.

For package-visible changes, the installed checkpoint is:

```sh
npm run test:installed -- --plugin onepersonlabs
```

It includes contract and unit checks, installs into a separate persistent
black-box Codex home, compares package files, and verifies discovery and selected
hook trust through the app-server API. A pass establishes that these checks
succeeded for this source snapshot; it does not refresh your active homes or
prove that a running task loaded the new package. Discovery and trust failures
need resolution, not interactive sign-in or manual `/hooks` confirmation.

The pre-push and release gates also use isolated homes. Their commands and
required scope are listed in the test instructions above.

## Publish and refresh

Use the delivery boundary authorized for the task. A verified local commit does
not authorize a push or refresh. When publication is authorized, preserve the
required pre-push checks and any selected PR review and merge requirements.
Verify remote landing before reporting publication complete. The
[workflow guide](../plugins/onepersonlabs/docs/workflow.md#follow-one-issue-through-delivery)
explains branch and PR choices.

For an authorized refresh, use the installed `$onepersonlabs:refresh-local-plugins` skill:

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

Follow the repository's
[service recovery](../AGENTS.md#human-collaboration-service-during-a-local-plugin-refresh)
and [post-refresh checks](../AGENTS.md#after-a-local-plugin-refresh). These own the
required pause/resume operations and configuration/instruction updates for this
checkout. The installed helpers retain backups and enforce their recovery and
no-downgrade checks. Report Windows and WSL outcomes separately.

Report checked source, published commits, installed files, and fresh-session
loading separately. A refresh does not change components already loaded in the
current task. Close the issue only when its complete acceptance scope is met.

## Open runtime research

[Issue #4](https://github.com/OnePersonLabs/onepersonlabs-plugin/issues/4) owns
the unresolved unattended issue-to-merge lifecycle. Two dated records support
that work. They do not set current repository workflow policy or authorize
implementation or deployment:

- [Runtime research](runtime-research.md): 2026-10-20 comparison and unresolved
  unattended lifecycle requirements.
- [Local Itervox proposal](itervox-upstream-proposal.md): 2026-10-20 draft, not an
  installed runtime or an upstream submission.

[Back to the repository](../README.md)
