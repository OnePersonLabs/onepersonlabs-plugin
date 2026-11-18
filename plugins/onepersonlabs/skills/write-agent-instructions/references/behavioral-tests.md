# Bounded instruction comparisons

Use a comparison when material uncertainty about the default behavior or a
proposed instruction can change an instruction decision. Existing checks and
source inspection come first. Necessary task-specific
verification and test-and-fix rounds have standing authorization under the
plugin's `AGENTS.md`; do not request separate permission for each run. Respect
explicit user budgets. Do not create permanent invocation tests or a mandatory
evaluation gate. An explicitly requested evaluation follows its stated scope
without requiring a prior failure.

Choose representative software tasks with independently checkable outcomes.
Include the original failure scenario when changing debugging guidance. Freeze
the baseline and candidate, then keep task input, environment, tools, model,
effort, and evaluator criteria equal. Use disposable repositories and isolated
Codex homes outside the target checkout, supported authentication, and no unrelated
plugins or hooks. Do not expose private logs or credentials in the result.

Use one comparison for as many changes as have distinct, independently checkable
outcomes. If two changes can affect the same outcome, compare them separately.
After accepting changes on separate evidence, check the combined instructions for
interactions that could undo a required behavior. Use an additional model run
only when the interaction is materially uncertain.

Before attributing a difference to changed instructions, measure repeated runs
of the same frozen build under the same conditions (A/A). Verify that the runner
actually loaded the intended source, instructions, and build selector. Record
that identity with the observations; selecting a label is not proof of loading.
Choose the success criterion before inspecting candidate results. If identical
build variation can explain the apparent gain, report the result as inconclusive
or gather more evidence within any explicit user budget. Do not impose a universal
sample count or buy more model runs to rescue a preferred result.

Use explicit model/effort settings and record the actual context and command.
Keep observations separate from inference: accepted behavior, missing requirements,
repairs, elapsed time, model usage, and cache observations. A cache hit requires a
matching prefix; a file reread does not establish a charge or a saving. Subscription
allowance cannot be derived directly from API token prices.

Report the sample's limits. Repeat when a remaining verification question needs
evidence, and stop when the required behavior is verified. Respect any explicit
user budget. For explicitly requested profile discovery or
instrumentation recovery, use $onepersonlabs:configure-harness and its diagnostic reference.
