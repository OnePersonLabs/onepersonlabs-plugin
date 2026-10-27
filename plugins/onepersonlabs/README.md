# OnePersonLabs

Skills, shared instructions, and hooks that help you direct Codex from a question
or failure to clearer understanding or a checked change. Use it to understand
code, investigate problems, make decisions, and collaborate with people.

## Start here

Install with a Codex CLI that supports plugins:

```sh
codex plugin marketplace add https://github.com/OnePersonLabs/onepersonlabs-plugin
codex plugin add onepersonlabs@onepersonlabs
```

Hooks require Python 3.11 or later (`python` on Windows, `python3` on POSIX).
Start a fresh Codex task in your repository and try:

```text
Use $onepersonlabs:build-understanding to explain how this repository works.
Follow one concrete user action from its entrypoint to its result, using the
current source. Keep this read-only and identify anything you cannot verify.
```

Expect a source-grounded explanation and a worked case, with uncertainty stated.
See [getting started](docs/getting-started.md) for installation checks and hook
trust. Installation adds skills and hooks; it does not run repository work.

## Guides

| Reader task | Guide |
| --- | --- |
| First installation and useful request | [Getting started](docs/getting-started.md) |
| Choose among all 30 shipped skills | [Skills by task](docs/skills.md) |
| Inspect settings, instructions, policies, and notifications | [Configuration and hooks](docs/configuration-and-hooks.md) |
| Declare repository capability requirements and diagnose conflicts | [Compatibility](docs/compatibility.md) |
| Work with people, recover history, and hand off | [Collaboration and recovery](docs/collaboration-and-recovery.md) |
| Diagnose failures or migrate from OPL | [Troubleshooting](docs/troubleshooting.md) |
| Extend, verify, and publish the plugin | [Contributor guide on GitHub](https://github.com/OnePersonLabs/onepersonlabs-plugin/blob/main/docs/contributing.md) |

Individual [skill instructions](skills/) own detailed procedures and
conditional dependencies. Availability and automatic discovery do not guarantee
that a skill will be selected or complete a particular task.

For optional GitHub issue-to-PR automation, see the separately installed
[Conductor plugin](https://github.com/OnePersonLabs/conductor-plugin). It is
not included in OnePersonLabs.
