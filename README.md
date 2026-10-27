# OnePersonLabs

OnePersonLabs gives Codex reusable skills, shared instructions, and hooks for
investigating problems, making engineering decisions, collaborating with people,
and delivering checked changes.

**To use the plugin, start with the [plugin README](plugins/onepersonlabs/README.md)**
for installation, a first useful request, and the user guides. Those guides ship
with the plugin and cover everyday work, configuration, and recovery.

## Develop the plugin

This repository owns the source, development tools, and verification. Read
[AGENTS.md](AGENTS.md), then follow [Contributing](docs/contributing.md) to set up
the checkout, change source, and verify the installed package. Publishing and
refreshing active installations are separate delivery steps.

| Location | Owns |
| --- | --- |
| [`plugins/onepersonlabs/`](plugins/onepersonlabs/) | Shipping skills, instructions, hooks, scripts, profiles, and user documentation. |
| [`docs/`](docs/contributing.md) | Contributor guidance. |
| [`tools/`](tools/) and [`tests/`](tests/) | Repository drivers, checks, and fixtures; these do not ship. |

For optional GitHub issue-to-PR automation, see the separate
[Conductor plugin](https://github.com/OnePersonLabs/conductor-plugin). It is
maintained independently and does not ship with OnePersonLabs.

OnePersonLabs is [MIT licensed](LICENSE). Bundled third-party code retains its own notices.
