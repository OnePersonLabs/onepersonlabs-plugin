---
name: camofox-cli
description: Use the redfox CamoFox CLI for terminal browser control and command lookup. Applies to the camofox executable shipped by the camofox-browser package, including navigation, snapshots, interaction, and saved sessions.
---

# CamoFox CLI

Use the redfox `camofox-browser` package's `camofox` executable. The Jo package,
`@askjo/camofox-browser`, uses `$onepersonlabs:camofox-browser` and its REST controller.

Before connecting, read [runtime guidance](references/runtime.md). Establish the
installed package, API port, authentication, and lifecycle owner. Reuse owned
sessions and keep `--user` stable. List tabs before opening another.

Use `--format json` for machine output. Take a snapshot before interaction and
refresh element references after page changes. Read the
[command reference](references/command-reference.md) for syntax, saved sessions,
authentication, tracing, downloads, and implementation limits. Check installed
`--help` when its version differs from the reviewed reference.

Close task-owned tabs when finished. Stop the server only when its lifecycle
belongs to this task. Read [UPDATE.md](references/UPDATE.md) when maintaining
this imported package.
