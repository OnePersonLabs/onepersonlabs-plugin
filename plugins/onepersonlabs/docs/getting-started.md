# Getting started

Use OnePersonLabs in a Codex task opened in the repository you want to work on.
You do not need to clone or develop the plugin to use its skills.

## Before installation

- Use a Codex CLI with `codex plugin` support. Check `codex plugin --help` if
  your CLI does not recognize the commands below.
- Make Python 3.11 or later available to Codex: `python --version` on Windows,
  `python3 --version` on POSIX, including WSL. npm-based Codex launchers also
  need Node.js in that environment.
- Keep Windows and WSL paths and interpreters separate. Installing into one
  Codex home does not establish the state of the other home.

Additional requirements belong to the selected task. For example, `last30days`
uses Python 3.12 or later, GitHub operations need authenticated GitHub tools or
`gh`, and the CamoFox skills need their respective external browser runtimes.
The [skill catalog](skills.md) identifies these requirements. Contributor tools
and browser test dependencies are not general plugin prerequisites.

## Install and recognize the result

In PowerShell or a POSIX shell:

```sh
codex plugin marketplace add https://github.com/OnePersonLabs/onepersonlabs-plugin
codex plugin add onepersonlabs@onepersonlabs
codex plugin list --json
```

The list should contain an installed, enabled `onepersonlabs@onepersonlabs`
entry. A marketplace listing or leftover cache directory alone is insufficient.
If the marketplace name already points to a different checkout, inspect that
registration before changing it; see [troubleshooting](troubleshooting.md).

Start a **fresh Codex task** to load the installed components. Review and trust
OnePersonLabs hooks through Codex's `/hooks` before expecting hook behavior.
The source-refresh helper can establish selected hook trust automatically;
the plain marketplace commands above do not provide that helper's verification.

### Find the installed plugin directory

For commands that use `<installed OnePersonLabs plugin directory>`, run
`codex plugin list --json` in the affected environment. Use `source.path` from
the installed `onepersonlabs@onepersonlabs` entry. This is the installed package
directory; `marketplaceSource.source`, when present, identifies the marketplace
source instead. Use the path for that environment's Codex home.

## Try a read-only first task

Open a repository and paste this into Codex, not your terminal:

```text
Use $onepersonlabs:build-understanding to explain how this repository works.
Follow one concrete user action from its entrypoint to its result, using the
current source. Keep this read-only and identify anything you cannot verify.
```

A useful result explains the relevant components and their relationships,
follows a concrete action, and links to source. It separates implemented intent
from behavior actually exercised. If Codex reports the skill missing, follow
[the discovery checks](troubleshooting.md#the-plugin-or-skill-is-missing).
An explicit invocation makes your intent clear; it does not bypass permissions
or establish that the explanation is correct.

## Choose the next task

| Situation | Request | Expected result |
| --- | --- | --- |
| You want a repeatable repository workflow | `Use $onepersonlabs:setup-repo-workflow to inspect and configure this repository's issue, check, review, delivery, and resumption path.` | A concrete working agreement using existing repository tools and instructions. |
| A behavior is broken | `Use $onepersonlabs:debug to investigate this failure: [symptom and reproduction].` | A source-backed diagnosis; a repair and its verification when fixing is also authorized. |
| Several solutions look plausible | `Use $onepersonlabs:research-solutions to compare current implementations for [problem and constraints].` | An evidence-based comparison with integration, cost, and recovery limits. |
| You need to continue interrupted work | `Resume the existing issue and work records; reconcile current source and delivery state before continuing.` | Recovered ownership, valid evidence, outstanding work, and a next action. |

The [workflow guide](workflow.md) connects these actions in one worked session.
The [catalog](skills.md) covers every skill, including explicit-only choices.
Existing repository instructions and your task authorization determine what the
agent may change, publish, install, or run.

## Update and keep track of the copy

For a Git marketplace installation, refresh its snapshot and reinstall the
selected plugin. If the human-collaboration service is in use, apply its
[pause and resume lifecycle](collaboration-and-recovery.md) around replacement:

```sh
codex plugin marketplace upgrade onepersonlabs
codex plugin add onepersonlabs@onepersonlabs
```

Start a fresh task afterward and review hook trust if the hooks changed.
For a local source checkout, use `$onepersonlabs:refresh-local-plugins` instead;
its [source-refresh procedure](../skills/refresh-local-plugins/SKILL.md) handles
existing Windows/WSL installations and selected hook trust. Global instructions
are a separate update, described in [configuration and hooks](configuration-and-hooks.md).
Publishing source, installing it, and loading it in a task are distinct steps.
