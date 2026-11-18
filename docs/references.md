# Project reference catalog

## Qualify open-source projects with evidence, not a single score

**Scope:** The project-health comparison in the
[`research-solutions` skill](../plugins/onepersonlabs/skills/research-solutions/SKILL.md)
and its [qualification guidance](../plugins/onepersonlabs/skills/research-solutions/references/evaluate-and-record.md#evaluate-open-source-projects).

**Sources and fit (checked 2026-11-18):**
[Linux Foundation LFX Insights](https://insights.linuxfoundation.org/docs/metrics/health-score/)
identifies available project trends; the
[CHAOSS viability guide](https://www.chaoss.community/practitioner-guide-viability/)
helps interpret health signals against the intended use;
[OpenSSF Scorecard's checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
identify supply-chain security signals and limits. The combination helps distinguish
maintenance and community activity from risks that affect adopting a project.

**Adaptation:** Use only signals that could change the choice and verify them
against release, issue, or advisory evidence. The plugin does not run these
services or combine their results into a score. This keeps the workflow usable
when coverage is incomplete or additional checks would not change the decision.
