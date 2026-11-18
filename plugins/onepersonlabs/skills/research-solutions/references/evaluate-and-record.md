# Evaluate and record solution references

## Evaluate open-source projects

Compare realistic alternatives that solve the same problem at a similar level.
Use comparable ecosystem, project maturity, scope, and time windows. Distinguish
observations from judgments and comparable signals from incomplete data. Use only
the checks that could change the decision:

- **Fit and currency.** Verify the relevant behavior in the published version or
  pinned source. Compare its design or API pattern with current primary guidance.
  A recently patched project can still use an outdated approach; an older project
  can still use a current one. Check stack and platform support, operating costs,
  license, and any constraints that could rule it out.
- **Maintenance and issue severity.** Check release and support history, who can
  maintain or release the project, and how maintainers respond to and resolve
  issues affecting the intended version and use. Read representative serious
  bugs, regressions, and breaking changes. A large backlog does not tell you
  whether the project fixes important issues.
- **Adoption and momentum.** Look for downstream dependents, meaningful usage
  case studies, or other direct adoption evidence. If you use download counts,
  say what they measure and what they cannot show. Compare trends in substantive
  releases, contributor activity, or adoption over the same period. Account for
  bots, stable maintenance-only projects, and missing data. Stars measure
  interest, not adoption.
- **Security.** For adoption or code reuse with a material security impact, check
  advisories for the intended version, release and dependency practices, and how
  the project fixes and discloses vulnerabilities. Interpret specific automated
  findings in context; missing results or a passing score do not establish safety.

When these sources can change the choice, use
[Linux Foundation LFX Insights](https://insights.linuxfoundation.org/docs/metrics/health-score/)
for comparison data on covered projects, the
[CHAOSS viability guide](https://www.chaoss.community/practitioner-guide-viability/)
to choose and interpret health metrics, and the
[OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
for supply-chain security signals and their limits. Check decisive signals against
releases, issue threads, advisories or other primary evidence. These are aids,
not separate gates, mandatory tools, or inputs to a homegrown score.

## Maintain the project reference catalog

Use the repository's declared catalog or extend its existing decision index.
If neither exists, create `docs/references.md` only when there is a durable entry
to add. Do not create a second copy of an ADR or a per-task research log. Use one
short entry per consequential decision:

- **Decision and scope:** What the project adopted or adapted. Link to the
  existing decision if there is one, and name relevant files, modules or symbols.
- **Source and fit:** Link directly to the relevant specification, docs or source.
  Include the version or revision when available and the date checked. Say what
  it informed, why it fits, and the conditions under which it applies.
- **Deviation:** Name any meaningful departure from the source, why the project
  needs it, and any constraint that would make the decision worth revisiting.

A link alone is not an entry. Do not add decorative or unverifiable sources.
On later work, search the catalog by the affected area and decision before
changing the code. Update the same entry when the reference, scope or rationale
changes; mark a superseded entry when that history still helps a reader.
