# CamoFox CLI Command Reference

## Quick Reference Table

### Core Commands (5)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `open` | Open new tab | `--user`, `[url]` |
| `close` | Close active tab or specified tab | `--user`, `[tabId]` |
| `snapshot` | Capture accessibility snapshot with refs | `--user`, `[tabId]` |
| `click` | Click element by ref/selector | `--user`, `<ref>`, `[tabId]` |
| `type` | Type into element by ref/selector | `--user`, `<ref>`, `<text>`, `[tabId]` |

### Navigation Commands (4)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `navigate` | Navigate tab to URL | `--user`, `<url>`, `[tabId]` |
| `screenshot` | Save screenshot PNG | `--user`, `[tabId]`, `--output`, `--full-page` |
| `go-back` | Go back in history | `--user`, `[tabId]` |
| `go-forward` | Go forward in history | `--user`, `[tabId]` |

### Content Commands (8)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `get-text` | Extract visible text | `--user`, `[tabId]`, `--selector` |
| `get-url` | Get current URL | `--user`, `[tabId]` |
| `get-links` | Get links from page | `--user`, `[tabId]` |
| `get-tabs` | List open tabs | `--user` |
| `eval` | Evaluate JavaScript expression | `--user`, `<expression>`, `[tabId]` |
| `wait` | Wait for condition/selector/navigation | `--user`, `<condition>`, `[tabId]`, `--timeout` |
| `search` | Search using built-in engines | `--user`, `<query>`, `[tabId]`, `--engine` |
| `extract-structured` | Extract content against a JSON schema | `--user`, `<schemaOrFile>`, `[tabId]` |

### Interaction Commands (5)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `fill` | Fill multiple fields | `--user`, `<assignments>`, `[tabId]` |
| `scroll` | Scroll page | `--user`, `[direction]`, `[tabId]`, `--amount` |
| `select` | Select dropdown value | `--user`, `<ref>`, `<value>`, `[tabId]` |
| `hover` | Hover over element | `--user`, `<ref>`, `[tabId]` |
| `press` | Press key | `--user`, `<key>`, `[tabId]` |

### Console & Error Capture (2)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `console` | Get console logs | `--user`, `[tabId]`, `--type`, `--limit`, `--clear` |
| `errors` | Get captured page errors | `--user`, `[tabId]`, `--limit`, `--clear` |

### Tracing Commands (5)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `trace start` | Start trace recording | `--user`, `--screenshots`, `--snapshots` |
| `trace stop` | Stop trace and save ZIP | `--user`, `--output` |
| `trace chunk-start` | Start trace chunk | `--user` |
| `trace chunk-stop` | Stop trace chunk and save ZIP | `--user`, `--output` |
| `trace status` | Show tracing status | `--user` |

### Session Commands (4)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `session save` | Save session | `--user`, `<name>`, `[tabId]` |
| `session load` | Restore session | `--user`, `<name>`, `[tabId]` |
| `session list` | List saved sessions | `--format` |
| `session delete` | Delete saved session | `<name>`, `--force` |

### Download/Cookie Commands (4)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `cookie export` | Export cookies to JSON | `--user`, `[tabId]`, `--path` |
| `cookie import` | Import cookies from JSON | `--user`, `<file>`, `[tabId]` |
| `download` | Registered command; returns `ok:false` in 2.4.8 because its direct endpoint is unavailable | `--user`, `[url]`, `--path` |
| `downloads` | List tracked downloads | `--user`, `--format` |

### Auth Commands (5)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `auth save` | Save encrypted credentials profile | `<profile-name>`, `--url`, `--notes` |
| `auth load` | Load credentials / inject into page | `<profile-name>`, `--inject`, `--username-ref`, `--password-ref`, `--user` |
| `auth list` | List auth profiles | `--format` |
| `auth delete` | Delete auth profile | `<profile-name>` |
| `auth change-password` | Rotate profile master password | `<profile-name>` |

### Server Commands (3)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `server start` | Start local server | `--port`, `--background`, `--idle-timeout` |
| `server stop` | Stop local server | *(none)* |
| `server status` | Show server status | `--format` |

### Advanced Commands (4)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `annotate` | Screenshot with element refs | `--user`, `[tabId]`, `--output`, `--format` |
| `health` | Health check | `--format` |
| `version` | Show CLI/server version info | `--format` |
| `info` | Show runtime configuration | `--format` |

### Pipeline Command (1)

| Command | Description | Key Options |
|---------|-------------|-------------|
| `run` | Execute script of CLI commands | `<script-file>`, `--continue-on-error` |

## Command syntax and implementation limits

## 2. Core Commands (5)

```bash
camofox open <url> [--user <user>] [--viewport <WxH>] [--geo <preset>]
camofox close [tabId] [--user <user>]
camofox snapshot [tabId] [--user <user>]
camofox click <ref> [tabId] [--user <user>]
camofox type <ref> <text> [tabId] [--user <user>]
```

## 3. Navigation Commands (4)

```bash
camofox navigate <url> [tabId] [--user <user>]
camofox screenshot [tabId] [--path <file>] [--output <file>] [--full-page] [--user <user>]
camofox go-back [tabId] [--user <user>]
camofox go-forward [tabId] [--user <user>]
```

## 4. Content Commands (8)

```bash
camofox get-text [tabId] [--selector <selector>] [--user <user>]
camofox get-url [tabId] [--user <user>]
camofox get-links [tabId] [--user <user>]
camofox get-tabs [--user <user>]
camofox eval <expression> [tabId] [--user <user>]
camofox wait <condition> [tabId] [--timeout <ms>] [--user <user>]
camofox search <query> [tabId] [--engine <engine>] [--user <user>]
camofox extract-structured <schemaOrFile> [tabId] [--user <user>]
```

Search engines: `google`, `youtube`, `amazon`, `bing`, `reddit`, `duckduckgo`, `github`, `stackoverflow`.

## 5. Interaction Commands (5)

```bash
camofox fill '<assignments>' [tabId] [--user <user>]
camofox scroll [direction] [tabId] [--amount <N>] [--user <user>]
camofox select <ref> <value> [tabId] [--user <user>]
camofox hover <ref> [tabId] [--user <user>]
camofox press <key> [tabId] [--user <user>]
```

Assignment format for `fill`:

```text
[e1]="value1" [e2]="value2"
```

## 6. Console & Error Capture (2)

```bash
camofox console [tabId] [--user <user>] [--type <type>] [--limit <N>] [--clear]
camofox errors [tabId] [--user <user>] [--limit <N>] [--clear]
```

## 7. Tracing Commands (5)

```bash
camofox trace start [--user <user>] [--screenshots] [--snapshots]
camofox trace stop [--user <user>] [--output <file>]
camofox trace chunk-start [--user <user>]
camofox trace chunk-stop [--user <user>] [--output <file>]
camofox trace status [--user <user>]
```

## 8. Session Commands (4)

```bash
camofox session save <name> [tabId] [--user <user>]
camofox session load <name> [tabId] [--user <user>]
camofox session list [--format <format>]
camofox session delete <name> [--force]
```

## 9. Download/Cookie Commands (4)

```bash
camofox cookie export [tabId] [--path <file>] [--user <user>]
camofox cookie import <file> [tabId] [--user <user>]
camofox download [url] [--path <dir>] [--user <user>]
camofox downloads [--user <user>] [--format <format>]
```

In the reviewed 2.4.8 implementation, `download` is registered but returns `ok:false` because the direct-download endpoint is unavailable. Use `downloads` to list tracked downloads. For batch downloads, inspect the package's supported API and task scope before calling it.

## 10. Auth Commands (5)

```bash
camofox auth save <profile-name> [--url <url>] [--notes <notes>]
camofox auth load <profile-name> [--inject [tabId]] [--username-ref <ref>] [--password-ref <ref>] [--user <user>]
camofox auth list [--format <format>]
camofox auth delete <profile-name>
camofox auth change-password <profile-name>
```

## 11. Server Commands (3)

```bash
camofox server start [--port <port>] [--background] [--idle-timeout <minutes>]
camofox server stop
camofox server status [--format <format>]
```

## 12. Advanced Commands (4)

```bash
camofox annotate [tabId] [--user <user>] [--output <file>] [--format <format>]
camofox health [--format <format>]
camofox version [--format <format>]
camofox info [--format <format>]
```

## 13. Pipeline Command (1)

```bash
camofox run <script-file> [--continue-on-error]
```

`run` executes sequential CLI command scripts (file path or `-` for stdin). It does not execute JavaScript/TypeScript source files.

## 14. Global Options

```bash
--user <user>
--port <port>
--format <format>    # json|text|plain
--local              # reserved for v2
-V, --version
-h, --help
```
