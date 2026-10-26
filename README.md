# OnePersonLabs

OnePersonLabs gives Codex reusable skills for investigating problems, making
engineering decisions, collaborating with people, and delivering checked changes.
It also supplies shared instructions and hooks for configuration, task continuity,
and advisory feedback.

## Install and try it

Use a Codex CLI with plugin support and Python 3.11 or later for the hooks.
Run these commands in PowerShell or a POSIX shell:

```sh
codex plugin marketplace add https://github.com/OnePersonLabs/onepersonlabs-plugin
codex plugin add onepersonlabs@onepersonlabs
```

Start a fresh Codex task in a repository you want to understand, then ask:

```text
Use $onepersonlabs:build-understanding to explain how this repository works.
Follow one concrete user action from its entrypoint to its result, using the
current source. Keep this read-only and identify anything you cannot verify.
```

Expect an explanation tied to the repository, a worked case, and explicit gaps.
The [getting-started guide](plugins/onepersonlabs/docs/getting-started.md) covers
installation checks, hook trust, and the next useful task. Installing the plugin
does not configure your repository workflow or start an unattended worker.

## Find your path

| You want to… | Start here |
| --- | --- |
| Install and complete a first task | [Getting started](plugins/onepersonlabs/docs/getting-started.md) |
| Find the right skill | [All 32 skills by task](plugins/onepersonlabs/docs/skills.md) |
| Set up a repository or follow an issue through delivery | [Workflow and worked session](plugins/onepersonlabs/docs/workflow.md) |
| Understand settings, global instructions, and hooks | [Configuration and hooks](plugins/onepersonlabs/docs/configuration-and-hooks.md) |
| Request human input, resume work, or recover a session | [Collaboration and recovery](plugins/onepersonlabs/docs/collaboration-and-recovery.md) |
| Diagnose a missing skill, failed hook, or refresh | [Troubleshooting](plugins/onepersonlabs/docs/troubleshooting.md) |
| Change, test, and publish the plugin | [Contributing](docs/contributing.md) |

The guides ship with the plugin. Each links to the skill or implementation that
owns the detailed behavior. Skills can use tools already available to Codex;
external accounts, browser runtimes, and optional services have their own prerequisites.

Assimilation is maintained by the independent
[All Your Base plugin](https://github.com/OnePersonLabs/all-your-base-are-belong-to-us-plugin),
invoked as `$all-your-base:assimilate` after installing it. Conceptor is optional;
OnePersonLabs also works with a repository's existing specifications and decisions.

## Project records and license

[Design and evidence records](docs/contributing.md#design-and-evidence-records)
retain dated audits, experiments, and proposals. They distinguish historical
results from current user instructions.

OnePersonLabs is [MIT licensed](LICENSE). Bundled third-party code retains its own notices.
