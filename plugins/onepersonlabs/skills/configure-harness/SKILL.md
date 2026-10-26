---
name: configure-harness
description: Configure or diagnose a Codex harness by inventorying capabilities, preparing reversible configuration changes, and optionally measuring routing or profile receipt. Use for personal harness setup, profile probes, or host input failures.
---

# Configure Harness

Build a usable, user-owned harness from the capabilities actually available in the selected Codex home. Treat a skill, plugin, tool, and instruction rule as different objects. Availability, eligibility, activation, and task success each need their own evidence. Keep choices and test results under `<selected Codex home>/onepersonlabs/harness/` so an interrupted run can resume.

Target one curated default setup. Introduce separate task profiles only when
evidence shows a conflict that conditional guidance cannot resolve cleanly.

## Establish scope and inventory

Resolve the selected Codex home and working directory from the request. For a first setup, inspect the effective global instructions, repository instructions, enabled and disabled installed plugins, installed and cached skill packages, configured MCP tools, callable CLIs, and discoverable catalog entries. Run `python scripts/harness.py init --home PATH`, then `discover --home PATH --cwd PATH`; pass `--marketplace PATH` for each known marketplace and `--cli NAME` for each relevant CLI probe. The script is relative to this skill. Complete paginated skill and plugin listings. Read the inventory and confirm the effective state before advising a change. A catalog listing does not prove that a tool is installed, enabled, authenticated, callable, or free to use.

Use the inventory as one source of truth, including the enabled/disabled distinction and provenance. Check current primary sources for material claims about capability, supported configuration, eligibility, price, recurring free access, time-limited trials, self-hosting, and limits. Record the source and observation date. For the default free baseline, exclude paid-only and trial-only operating modes and routes with required paid dependencies; recurring free quotas and suitable self-hosted modes remain eligible. Do not label a trial, promotional credit, or self-hosted software as a recurring free hosted service. Mark an unverified claim unknown. Read [references/workflow.md](references/workflow.md) when comparing candidates, interviewing the user, or preparing changes.

## Choose capability by capability

Group real user needs into small capability categories. For each category, show a short card for each viable option: exact name, what it enables, current availability, material cost or eligibility, and evidence quality. The inventory's description summary is at most 256 characters per item; keep the exact name in its own field and do not treat the summary as the full instruction text. Present one category at a time, collect unresolved choices under the host's question timing rules, and write each settled choice and reason through `decide --home PATH --decision PATH`. Reuse recorded choices when resuming; revisit one only when the user changes it or new evidence makes it stale.

Compare the current route and the strongest alternative before adding a capability. Prefer disabling a redundant route before adding another overlapping instruction. Choose the narrowest supported scope: per-skill invocation policy when that owns activation; plugin enablement when the whole plugin is at issue; task-specific instructions where no supported control exists. Never patch installed caches as configuration. An inventory or recommendation alone does not authorize installation, external account creation, payment, or changes to the user's live profile.

## Optional measurement and diagnosis

Use deterministic inventory and existing evidence first. Model evaluation is
optional and requires an explicit finite budget and authorization for AI usage.
For an explicitly requested live profile probe or interrupted instrumentation,
read [profile probe and restoration](references/profile-probe.md). Discovery and
restoration do not require running the model probe. For an observed host question
tool failure, read [host input diagnosis](references/host-input.md).

For authorized model measurements, read [evaluation](references/evaluation.md).
The existing bounded evaluation engine uses a Luna executor and Sol judge;
choose it only when that separate judgment can change the decision. Record its
explicit budget before sampling. Deterministic probes and local evidence do not
require two agents or a model evaluation. Report unmeasured routing as unknown.

## Review, apply, and recover

Show the concrete proposed state, ownership of each change, evidence, remaining uncertainty, and expected effects. Use `prepare --home PATH --files PATH --output PATH` with a JSON list of reviewed `target` and `candidate` files to prepare file changes. Use `apply --home PATH --plan PATH` only after the reviewed change is authorized. Reuse existing authorization within its scope; do not ask again for an already approved transaction. Retain the returned receipt before proceeding to another change; use `rollback --home PATH --receipt PATH` for a failed or rejected application. The managed section may be absent on first setup: review its placement, then create exactly one. Stop on duplicate headings or ambiguous ownership rather than guessing where text belongs.

For OnePersonLabs startup configuration, present the discovered OnePersonLabs roles and each
required setting from the plugin-root `config.defaults.toml` file before
preparing a transaction. Reconcile only role registrations whose `config_file` provenance establishes
OnePersonLabs ownership, and that documented startup baseline. A name prefix alone does
not establish ownership. Preserve custom registrations and unrelated configuration. Root model and reasoning preferences are outside this
features/agents transaction contract; inspect them without adding them to a
harness apply plan.

For a global instruction change outside the harness-owned `Harness Policies (managed by $onepersonlabs:configure-harness)` section, use `$onepersonlabs:update-instructions` to update the full file. It replaces outdated instructions under established authorization and saves the old file byte for byte in a dated backup; it does not merge custom rules. Put essential, unmeasured constraints inline. Add compact conditional pointers to category policies and procedures only when their targets resolve and their route can be verified; avoid circular pointers. Add a runtime recovery hook only after measured failures show a hook is needed; no hook is part of the default setup. When an authorized evaluation tests routing, verify the root route, a relevant documentation event, and subagent behavior separately in fresh contexts. Otherwise report routing as unmeasured. Give the user the durable run location and any remaining uncertainty.
