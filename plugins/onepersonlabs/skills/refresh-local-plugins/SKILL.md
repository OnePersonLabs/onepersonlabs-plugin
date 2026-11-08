---
name: refresh-local-plugins
description: Refresh plugins from a source checkout in the current user’s default Codex home. Use after local edits or pulls, for stale installed copies, or to preview an installation. Publishing is separate.
---

# Refresh Local Plugins

Prepare and refresh changed shipping bundles from the source checkout through
Codex's native installer. The bundled helper works across local marketplace
repositories; shipping-source checkouts need no build setup.

## Select the source and Codex home

Resolve the source checkout from the request and session context. Run the helper
from this **loaded skill's actual directory**, including when this skill is in
Codex's installed cache. Never use the installed cache as the source checkout.

Run the helper in the environment where the plugin is needed. By default, it
uses that environment's existing user-level `~/.codex` and selects previously
installed marketplace plugins whose bundles differ from their cached copies.
The comparison includes committed changes after a pull and uncommitted edits.
Honor explicit plugin selections. Use `--plugin all` only when the user requests
the whole marketplace.

## Preserve collaboration service availability

When the workspace requires the human-collaboration refresh lifecycle, use
`$onepersonlabs:human-collaboration`'s `pause-for-refresh` from that workspace before
installation. Continue only after it proves both listener shutdown and process
exit, or reports the service was not running. An unresponsive live service
blocks refresh. Do not add repeated service probes.

After the installation attempt, run installed `resume-after-refresh` from the
same workspace even if installation failed. Use the source helper if the
installed helper is unavailable. It restarts only a previously running service;
retain its pause record on failure. When it returns a new pairing URL, follow
[$onepersonlabs:human-collaboration](../human-collaboration/SKILL.md#deliver-the-pairing-link)
to open it and give the user the complete clickable link.

## Run the bundled helper

Use `--repo` when the checkout is outside the current directory. This command
refreshes modified plugins in the current user's default Codex home:

```text
node <loaded-skill-directory>/scripts/install-local.mjs --repo <source-checkout>
```

Repeat `--plugin <name>` to select specific plugins. Use `--dry-run` for discovery
or a read-only preview. Use `--target-home <absolute-path>` when the user names
a Codex home or when running an isolated test. `CODEX_BIN` can select a native
Codex executable or JavaScript entrypoint.

The helper validates selected sources and existing marketplace registration
before installation. If the marketplace name is registered to a different
checkout, report the conflict. Use the registered checkout or resolve the
registration before retrying.

If the checkout declares `scripts["plugin:prepare-local"]` in `package.json`,
the helper runs that script with the declared package manager (npm by default)
before comparing bundles with installed copies. That command owns compilation
and bundle assembly. If preparation fails, stop the installation.
Repositories without this script install their shipping sources directly.
`--dry-run` never builds: it reports required preparation and marks plugin
selection pending when a build is needed. Use the helper for the whole refresh;
do not separately run the preparation command first.

The helper calls native `codex plugin add` to atomically refresh and enable
each selected plugin, including unchanged versions. Do not add uninstall steps,
version cachebusters, or verification commands. Run tests separately only when
requested or required by a development task.

## Hook trust and handoff

An authorized refresh also authorizes trusting the refreshed plugins' current
installed hooks in the selected home. The helper uses the Codex app-server API to save only selected hook hashes and verify trusted status. It
preserves unrelated hooks and sandbox settings. A hook trust failure does not
stop later selected plugins from refreshing. Do not ask for sign-in, sandbox
setup, or manual hook approval when automatic trust succeeds.

If automatic hook trust fails, report the home and plugins that need manual
trust. Ask the user to open a fresh Codex session in that home, review and trust
the affected hooks with `/hooks`, and reply `done`. Verify trust after the reply
before reporting the refresh complete.

## Report the result

Report the selected home, refreshed plugin IDs, and installed paths. For a
dry run, report the preflight result. Surface failures with completed progress. Tell the user to
start a fresh Codex session to load updated components. Installation and trust
verification do not prove that plugin tests pass or hooks execute correctly.
