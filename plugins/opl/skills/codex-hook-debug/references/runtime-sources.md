# Runtime hook sources

Inspect each applicable source:

| Source | Inspect |
| --- | --- |
| User | `CODEX_HOME/hooks.json` and inline `[hooks]` in `CODEX_HOME/config.toml`. The usual home is `~/.codex`. |
| Repository | `.codex/hooks.json` and `.codex/config.toml` in active project config layers. Check the actual worktree and session subdirectory. |
| Installed plugins | Every relevant enabled plugin's installed root, `.codex-plugin/plugin.json`, manifest `hooks` entries, and default `hooks/hooks.json` when no override is present. |
| Other active layers | Session overrides and managed/system requirements when discovery or effective configuration identifies them. |

Hooks from multiple sources are additive. Higher configuration precedence does not replace lower-layer hook definitions. A layer can merge both JSON and inline TOML with a warning. Do not assume that the first command match is the only handler or that the hook file's directory is the command's working directory.

Use `/hooks` in a supported CLI or the affected runtime's read-only `hooks/list` app-server API to establish loaded definitions. An app-server client must initialize the protocol before listing hooks. Inspect returned errors and warnings, then map the failing handler by event, matcher, command or MCP tool, source path, and plugin identity. Keep its key, current hash, enabled state, managed status, and trust status when available. Preserve multiple candidates until evidence identifies the owner. File inspection alone does not prove that Codex loaded a hook.

Under normal trust enforcement, non-managed hooks with untrusted or modified definitions are listed but skipped until trusted. Check for an existing authorized trust-bypass invocation before concluding that such a handler could not run. Concurrent execution applies to eligible handlers, not every listed definition.
