# Codex compatibility checks

OnePersonLabs checks local Codex metadata against repository policy
for plugins, skills, and MCP servers. It reports missing requirements, conflicts,
recommendations, and discovery failures.

The checker needs Python 3.11+ and Codex CLI; discovery is tested with Codex
`0.151.0` and `0.153.4`. Windows uses `python`; POSIX uses `python3`. npm Codex
launchers also need Node.js. Review and trust OnePersonLabs hooks in Codex's `/hooks`
before expecting automatic checks.

## Repository policy

Add `codex.compatibility` to `.onepersonlabs/config.json` at the repository root. The file
is optional. An empty policy is valid and does not require capability discovery.

This example requires the project's documentation server and warns about missing
local tooling. Use constraints established by the repository, not provider loyalty.

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

`version` must be `1`. `required`, `recommended`, `disallowed`, `rules`, and
`ignoreRules` are optional arrays. `onViolation` accepts `acknowledge` (the
default) or `warn`.

| Declaration | Meaning |
| --- | --- |
| `required` | At least one matching component must be enabled. |
| `recommended` | A missing or disabled match is nonblocking information. |
| `disallowed` | Any matching enabled component is a violation. |
| `whenEnabled` inside a required or recommended entry | Apply its nested declarations only when that entry has an enabled match. |
| A top-level `rules` entry | Apply its declarations only when its `whenEnabled` selector has an enabled match. |
| `ignoreRules` | Suppress an exact rule ID, with a required explanation. |

An enabled plugin does not imply that every bundled skill or MCP server is
enabled. Use component selectors for the capabilities the repository needs.
Disabled owners do not activate their conditional rules. A conditional rule
excludes its owner from its own `disallowed` matches, so a same-name conflict
rule can detect other copies without rejecting the selected owner.

## Selectors and cherry-picking

| Kind | Identity | Optional qualification |
| --- | --- | --- |
| `plugin` | `id`, such as `onepersonlabs@onepersonlabs` | None |
| `skill` | `name`, as declared by the skill | `plugin` and an absolute `path` |
| `mcp` | `name`, as reported in server metadata | `plugin` |

Plugin IDs use the canonical `name@marketplace` form, not a display name or
cache directory. Skill and MCP selectors without `plugin` match that name
across providers. Add `plugin` to require a particular provider. For duplicate
standalone skills, add the absolute skill path reported by discovery. JSON
names omit the `$` invocation sigil. Entries can include a human-readable
`reason`; a top-level rule can also supply a shared `reason`.

Codex's `skills.config` entries are enablement overrides, not a complete
inventory. Use the diagnostic's discovered identity and path when resolving a
duplicate; a missing override does not mean a skill is absent. See the
[Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Conditional rules and exceptions

A top-level rule has an `id`, an owner selector in `whenEnabled`, and optional
constraints. Bundled rules can bind an owner path with `${PLUGIN_ROOT}/`; the
loader rejects paths escaping the plugin. Repository paths remain absolute.

`ignoreRules` suppresses a matching rule ID with a nonblank reason. An unavailable
ID produces a nonblocking warning and has no effect; it does not disable other
constraints. OnePersonLabs adds no preference for its own skill providers.

## Acknowledgment and session behavior

Checks run on `SessionStart` for startup, resume, clear, and compact. The
`UserPromptSubmit` hook rechecks detected configuration and inventory changes
and handles pending acknowledgments.

With `onViolation: "acknowledge"`, violations and discovery or policy errors
ask the agent to pause and present the findings. The original task stays in
the conversation. Reply with exactly `continue`, `ok`, `okay`, or
`continue anyway` to acknowledge the pending findings and resume that task.
Other text is not an acknowledgment. With `onViolation: "warn"`, the checker
reports findings without requesting a pause. Missing recommendations never
request acknowledgment.

This is a cooperative instruction to the agent, not a deterministic execution
or security gate. Hooks can run concurrently, and this checker cannot disable
another hook. Codex documents hook events and context delivery in its
[hooks reference](https://learn.chatgpt.com/docs/hooks).

Acknowledgments are scoped to the session, repository, policy, and inventory
fingerprint. Changes require a fresh decision; acknowledgment in one repository
does not accept another repository's findings. Session state lives under
`PLUGIN_DATA/compatibility`, falling back to `CODEX_HOME/onepersonlabs/compatibility`.
The checker does not persist user prompts.

## Run a diagnostic

From this marketplace checkout on Windows:

```powershell
python plugins/onepersonlabs/scripts/codex-compatibility-check.py --check --cwd C:/dev/my-project
python plugins/onepersonlabs/scripts/codex-compatibility-check.py --check --cwd C:/dev/my-project --json
```

On POSIX, use `python3` and a native repository path. For an installed copy,
run its `scripts/codex-compatibility-check.py`. If discovery cannot resolve the
launcher, set `CODEX_BIN` to the native executable or JavaScript entrypoint.

| Exit status | Meaning |
| --- | --- |
| `0` | Requirements satisfied; recommendations may still be reported. |
| `1` | Compatibility violations found. |
| `2` | Invalid policy, discovery error, or unverifiable inventory. |

## Discovery and troubleshooting

The adapter reads fresh local CLI metadata for the current working directory
and `CODEX_HOME`, not a running host's transient command-line or session
overrides. App Server `skills/list` supplies skills; `config/read` supplies
configuration. MCP discovery runs only when repository policy refers to MCPs:
`codex mcp list --json` supplies enablement, and plugin metadata supplies bundle
membership. It starts no MCP servers and creates no model turns. Plugin metadata
APIs are experimental. See the [App Server reference](https://learn.chatgpt.com/docs/app-server).

Unknown enablement or ownership produces `cannot_verify`, never claimed absence
or safety. Cached results, including unknowns, remain until a lifecycle recheck
or watched input change; diagnostic `--check` always reads fresh metadata.
Check the diagnostic before changing configuration:

- **No automatic report:** verify OnePersonLabs is enabled, its hooks are trusted, and the
  Python interpreter and Codex CLI are available to the hook process.
- **Cannot verify:** inspect `--json`, check `CODEX_BIN` and the Codex version,
  then rerun the diagnostic. A qualified MCP needs both enablement and plugin
  ownership metadata.
- **Unexpected skill match:** compare its plugin and absolute path. Standalone
  roots include `~/.agents/skills`, the compatibility root `~/.codex/skills`,
  and repository `.agents/skills`; `~/.codex/.agents/skills` is not the user root.
- **Policy error:** fix the reported source and JSON pointer. Unknown fields,
  malformed IDs, and relative skill paths need correction.
