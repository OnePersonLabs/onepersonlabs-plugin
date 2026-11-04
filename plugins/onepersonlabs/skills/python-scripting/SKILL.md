---
name: python-scripting
description: Create, discover, reuse, and retire generated Python utilities for agent work in the active Codex home. Use for file-based Python tools and parameterized ad hoc scripting; maintained project utilities keep their repository owner.
---

# Python scripting

Use a file when Python work needs more than a short expression, reusable arguments,
or another execution. Search for an existing utility before generating one. Keep
generated agent utilities in the active `CODEX_HOME/agent-tools` store; when
`CODEX_HOME` is unset, use `~/.codex/agent-tools`. Do not create generated utilities
inside a repository or plugin. A maintained project utility belongs with its
project and follows that project's conventions.

## Discover and run

Run this skill's `scripts/agent_tools.py` with `python -B -X utf8` on Windows or
`python3 -B -X utf8` on POSIX. The following arguments work with either command:

```text
agent_tools.py paths
agent_tools.py find csv reconcile --limit 20
agent_tools.py paths --create
agent_tools.py run reconcile_csv.py -- --input ./data.csv
agent_tools.py run inspect_json_shape.py --temp -- --path ./sample
agent_tools.py maintain --dry-run
agent_tools.py maintain
```

`paths` reports the resolved root and tier paths. `--create` creates missing
directories and never generates configuration. `find` searches names, descriptions,
and keywords using case-insensitive AND matching. Results put hot tools before
cold tools, default to 20 matches, and exclude temp. Discovery reads only a bounded
header prefix and never imports or executes a tool. Read a selected tool before
running it to confirm its behavior and permissions.

The entire discovery response is capped at 16 KiB of serialized JSON. Executable
names and paths remain complete. Counts report omitted matches and warnings, and
truncated metadata or warning text. Discovery uses the same filename and hard-link
eligibility checks as execution. A recoverable hot/cold pair appears once in hot;
other basename collisions are reported and excluded.

`run` requires an exact basename. It refreshes the tool's modification time and
promotes a cold tool to hot before execution. It preserves the caller's working
directory and standard streams, passes arguments after `--`, and uses the script
directory as the first import search path. A conflicting hot/cold basename stops
execution and preserves both files. Inspect and resolve the conflict explicitly.

## Generate a tool

Create the directories with `paths --create` when needed. Put a utility with
expected reuse after the current task in `hot/`. Use `temp/` when reuse is expected
only within the current task. Use a concise, useful
`snake_case.py` filename. Start the file with these adjacent comments, after an
optional shebang and encoding comment:

```python
# Description: Reconcile two CSV exports by their stable record identifier.
# Keywords: csv, reconcile, records
```

Use `argparse` for variable inputs, paths, and options. Keep operational inputs
out of hard-coded source. Run through the manager so execution refreshes retention
and protects tools from concurrent maintenance. Remove a temporary utility as
soon as its purpose ends; automatic cleanup is a fallback for inactive leftovers.

Generated utilities are disposable agent tools. Product code, maintained utilities,
documentation, tests, CI, and other generated scripts must not import, reference,
or invoke them. Generated scripts must not depend on one another. Manager commands
and agent selection by name are allowed. If ongoing project behavior needs the
logic, implement it as a maintained project utility with its own owner.

## Retention and maintenance

An optional `agent-tools/config.json` can override any of these defaults:

| Setting | Default | Meaning |
| --- | ---: | --- |
| `hot_age_days` | 60 | Minimum idle age before demotion |
| `hot_count` | 100 | Hot count threshold |
| `cold_age_days` | 180 | Minimum idle age before deletion |
| `cold_count` | 400 | Cold count threshold |
| `temp_age_days` | 14 | Minimum idle age before deletion |

Values must be finite nonnegative integers. Booleans and unknown keys are invalid.
The manager validates the entire configuration before changing storage.

Hot demotion requires both the age and excess-count conditions. Cold deletion
requires both conditions too. Each sweep chooses the oldest eligible files, then
filename, and changes only enough files to reach the threshold or exhaust eligible
files. Idle files below a count threshold can live indefinitely. Temp cleanup
uses age alone. Hot demotion runs before cold pruning and resets modification time,
giving each demoted tool its full cold lifetime. Editing a file also refreshes its
retention; modification time is not an exact execution history. Reading and
discovery do not refresh it.

The native asynchronous `SessionStart` hook runs maintenance on startup, resume,
clear, and compact. An absent store is a quiet no-op. Active manager executions
and concurrent maintenance make a sweep skip. Cleanup failures appear through the
hook's `systemMessage`; successful cleanup adds no context. `maintain --dry-run`
is an advisory read-only snapshot: it creates no directories, configuration, or
lock file. Real maintenance recomputes the work under locks.

The manager uses one persistent `.lock` file and OS byte-range locks. Concurrent
runners share an execution guard until each manager process exits. That guard
does not cover detached descendants or an `exec` replacement. Store paths and
flat regular `.py` candidates reject symlinks and Windows reparse points. Moves
use hard-link creation followed by unlink, without replacing a destination.
An interrupted exact two-link hot/cold pair can reconcile to hot; other collisions
and unsupported hard-link operations preserve files and report the failure.
This is cooperative filesystem safety, not a sandbox against adversarial code.
Malformed headers block discovery and execution but do not exempt regular `.py`
files from retention. Never delete or replace the stable `.lock` file.

Implementation contracts: [Python `os.link` and filesystem operations](https://docs.python.org/3/library/os.html#os.link),
[Python `runpy.run_path`](https://docs.python.org/3/library/runpy.html#runpy.run_path),
[POSIX `lockf`](https://docs.python.org/3/library/fcntl.html#fcntl.lockf),
[Windows `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex),
and [Codex asynchronous hooks](https://learn.chatgpt.com/docs/hooks).
