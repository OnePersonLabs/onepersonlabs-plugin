# WTFM documentation assimilation

Decision, 2026-10-21: retain the documentation judgment, not the article engine.
[Issue #16](https://github.com/OnePersonLabs/onepersonlabs-plugin/issues/16)
owns delivery. The native owner is
[$onepersonlabs:write-docs](../plugins/onepersonlabs/skills/write-docs/SKILL.md),
with a short maintenance trigger in the shipping instructions.

## Source and examined scope

Donor: [SupportPages-io/wtfm](https://github.com/SupportPages-io/wtfm/tree/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2),
package version 0.5.7. Inspected its repository inventory, README, package manifest,
writer workflow, label-evidence contract, copy-lint implementation, writer entry
and completion handling, run acknowledgements, repository-benefit prompts, LICENSE
and NOTICE. The large writer workflow was reviewed selectively; renderer internals,
platform-specific assets, installer internals and most tests were not examined.
No donor automation was executed. Source-backed mechanisms are not runtime trials.

The donor's [LICENSE](https://github.com/SupportPages-io/wtfm/blob/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2/LICENSE)
is Apache-2.0; its NOTICE identifies Surface Layer Limited and separately licensed
assets. This integration contains original instructions inspired by the mechanisms,
not copied donor code, prose, assets, branding or package dependencies.

## Capability decisions

| Capability and source | Value retained and native mechanism | Boundary |
| --- | --- | --- |
| [Writer workflow](https://github.com/SupportPages-io/wtfm/blob/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2/engine/generate-illustrated-article/SKILL.md): topic-to-entrypoint grounding, reader actions, reusable context | The skill follows the actual user journey and reads only dependencies that can alter instructions. | No fixed search quota that forces a guess; uncertainty remains explicit. |
| [Label evidence](https://github.com/SupportPages-io/wtfm/blob/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2/engine/generate-illustrated-article/contracts/label-evidence.md) and [copy lint](https://github.com/SupportPages-io/wtfm/blob/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2/engine/generate-illustrated-article/scripts/lint_article_copy.js) | Verify commands and controls at their sources; preserve unresolved dynamic labels and runtime limits. | Do not import the article schema, specialized resolver, or lexical matching as proof of semantic correctness. |
| Writer's selective illustration and copyable terminal instructions | Use visuals when recognition needs them; keep commands as text. | Reject mandatory UI-action screenshots and mockups presented as runtime evidence. |
| README and [repository-benefit prompts](https://github.com/SupportPages-io/wtfm/blob/1ab355b7d77b9d9f8b8f666bef2222c5d5325aa2/src/repository-benefits.ts) describe hosted change tracking | Native adaptation: the active implementation agent updates affected reader claims using its existing change context. | Hosted diff analysis is an advertised external capability, not verified local machinery. No service, account, scheduler or recurring model work. |

WTFM explicitly targets end-user help rather than READMEs. README orientation,
project-specific voice, qualification boundaries and change-scoped maintenance
are recipient adaptations. Existing build-understanding guidance supplies complex
explanation; the new skill owns the independently discoverable documentation task.

## Survival cases and evidence standard

- A new README must let its intended reader choose a first useful task and
  recognize the result without first learning internal architecture.
- A renamed command or changed permission must update its entry page and linked
  instructions. A stale example is a failure even if the new paragraph is correct.
- An internal refactor with identical reader behavior must not trigger a cosmetic
  rewrite or corpus-wide scan.
- An unresolved dynamic control name must remain unresolved or be checked through
  an authorized observation; a plausible guess is not evidence.
- A reconstructed screenshot must be labeled and cannot establish that the app
  executes the depicted action. A consequential failure needs useful recovery.

Instruction review checks these cases against the procedure and its routing. Existing
package checks verify structure and installation, not agent selection or improved
writing. No invocation tests or AI evaluations are authorized. Project documentation
applications provide source-reviewed examples; human comprehension and token savings
remain unmeasured.

## Cost and reconsideration

One compact skill and its discovery metadata, plus a short always-loaded trigger,
replace the need to load the donor's roughly 11,000-word writer workflow. That is
an instruction-size comparison, not measured usage savings. No runtime dependencies,
hooks, automation, new validators or evidence stores are introduced. Use existing
project checkpoints for application evidence. Reconsider if real documentation
work misses affected instructions, repeatedly duplicates investigation, or cannot
preserve a necessary reader journey within this shape.
