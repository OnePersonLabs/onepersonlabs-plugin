---
name: last30days
description: Research what people have said about a topic in the last 30 days across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web. Use for recent reactions, recommendations, comparisons, source-health checks, and configuration diagnosis; do not use for generic timeless web research.
---

# Last 30 Days

Run the bundled research engine and synthesize its evidence. Web research
improves planning, but it never substitutes for the engine.

## Locate this installation

Codex provides the selected skill's `SKILL.md` path. Set `SKILL_ROOT` to the
directory containing that exact file and use its sibling engine:

In PowerShell, set `$SKILL_ROOT` to that directory and use
`$ENGINE = Join-Path $SKILL_ROOT 'scripts/last30days.py'`; verify it
with `Test-Path -LiteralPath $ENGINE -PathType Leaf`. In POSIX, set
`SKILL_ROOT="<directory containing the selected SKILL.md>"`, use
`ENGINE="$SKILL_ROOT/scripts/last30days.py"`, and verify with
`test -f "$ENGINE"`. If the engine is missing, report the exact expected
path and stop.

Do not scan `~/.codex`, compare cache versions, search for another copy, or
substitute a repository checkout. The selected skill path is the authority;
this keeps instructions, scripts, and references from the same installation.

## Route the request

- If the user asks to configure sources, fix a source, inspect permissions, or
  diagnose configuration, read [references/setup-and-diagnostics.md](references/setup-and-diagnostics.md).
- If the user provided no topic, ask one short question for it and wait.
- Recognize `--days=N`, `--quick`, and `--deep` when the user supplies them.
- Classify the request as general/news, recommendations, or comparison.
  Comparisons include `X vs Y`, `X versus Y`, and direct compare requests.
- If the topic is too broad to retrieve meaningfully (for example a single
  common noun), ask for the angle before running anything. For demographic or
  numeric shopping queries, ask for relationship, interests, and budget rather
  than searching the literal age phrase.

## Run the engine

Read [engine execution](references/run-engine.md) before research. Resolve a
supported interpreter, check source health, build the query plan, and run this
installation's engine. Keep authentication, network scope, user-selected depth,
source coverage, and failures visible. Configuration and health-only requests
use the diagnostics branch and stop after reporting its result.

## Synthesize

After the engine completes, read
[references/synthesis.md](references/synthesis.md). Use the entire compact
output, including evidence clusters, community comments, uncertainty markers,
source coverage, and the engine-reported saved paths.

The final response must:

- distinguish evidence from inference;
- cite only URLs present in engine output or fetched during this run;
- reflect actual source coverage and uncertainty;
- include the engine-reported raw artifact path when one was saved; and
- omit engine scratchpad, planner JSON, internal scoring tuples, and
  secrets.

Do not add a generated version badge. Runtime version reporting, when needed by
diagnostics, is owned by the executable and its nearest `.codex-plugin/plugin.json`.

## Follow-ups

Answer follow-up questions from the completed research while it remains current
for the user's requested window. Run new research when the user changes the
topic, changes the time window, requests a refresh, or asks for evidence the
existing report did not collect.
