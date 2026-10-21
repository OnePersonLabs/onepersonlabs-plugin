# OPL

One-Person Labs developer tooling for Codex: focused skills, shared instructions, integrations, and advisory workflow hooks.

🧭 **[Understand OPL at a glance](docs/opl-at-a-glance.md)** -- roles, work flow, choices and what is actually active.

## Install

```sh
codex plugin marketplace add https://github.com/OnePersonLabs/opl
codex plugin add opl@opl
```

Start a new Codex task after installation. Invoke skills with `$opl:<skill-name>`, such as `$opl:setup-repo-workflow`, `$opl:debug`, or `$opl:adhd`.

## Develop

Use Node.js 24 or later, Python 3, Git, and the Codex CLI.
Hooks require Python 3.11 or later. The `$opl:last30days` engine requires Python 3.12 or later.

```sh
npm ci
python -m pip install playwright
npm run verify
npm run test:installed -- --plugin opl
```

The pre-push hook runs the deterministic checks, including real-browser UI tests.
Install Playwright in the Python environment used by the checks (`PYTHON_BIN`
selects a different interpreter). The UI tests use an installed Chromium browser.
To install Playwright's development browser, run `python -m playwright install chromium`.
Set `OPL_CHROMIUM_BIN` when you need a specific browser executable.
The checks report missing prerequisites and do not install them automatically.

Shipping files live in `plugins/opl/`. Tests and fixtures live in `tests/`. Repository commands live in `tools/`.

Instruction baseline recovery uses local history first. Remote recovery uses the original OnePersonLabs plugin repository for revisions below 10 and this repository for revisions 10 and later.

When the user authorizes tests, run a focused test for the affected behavior:

```sh
npm run test:focus -- --file tests/unit/opl/codex-hooks.test.mjs
```

Review skill instructions and activation metadata against their sources and structure after changes. `npm run release:verify` runs deterministic checks and an installed-copy checkpoint.

The installed-copy checkpoint uses a separate Codex home, compares the installed files with source, and verifies hook trust. To refresh OPL in your existing Codex home:

```sh
npm run install:local -- --plugin opl
```

## Development workflow

For substantial explanations, teaching or human interaction design,
`$opl:build-understanding` helps make relationships, changes and choices easier
to grasp. Choose useful representations and worked cases; keep precise words
and simple exchanges where they serve the task best.

For consequential tool, architecture, infrastructure or integration choices,
`$opl:research-solutions` finds credible current implementations and checks their
release, integration and recovery contracts. It is automatically discoverable;
routine repairs do not require a solution survey.

Use `$opl:setup-repo-workflow` explicitly to configure one repository through its
existing instructions, GitHub conventions, local checks, review lane, and merge
policy. Default to serial work in the selected checkout and branch; new delivery
branches and PRs are opt-in. Setup explains independent workers, optional
helpers and their aggregate budget without adding another configuration schema.
Ordinary authorized work uses `$opl:github-workflow` for issue capture
and state maintenance. Projects remain independent. The builder owns PR repairs;
small checked commits make the series reviewable. Local verification is primary.
For selected PR delivery, automatic merge follows required checks and reviews,
with existing protections and explicit manual-merge overrides preserved. Native
auto-merge does not wake the builder for repairs or start the next issue. Setup
does not install unattended dispatch.

The [overhaul audit](docs/opl-overhaul.md) records package dispositions, sources
and verification. The [runtime comparison](docs/runtime-research.md) and
[local Itervox proposal](docs/itervox-upstream-proposal.md) explain the separately
tracked automation contracts. They install no runtime or worker service.

## License

OPL is MIT licensed. Bundled third-party code retains its own license notices.
