# Optional instruction comparisons

Use a comparison only when an instruction decision needs evidence and the user
has authorized a finite AI budget. Existing checks and source inspection come
first. Do not create permanent invocation tests or a mandatory evaluation gate.

Choose representative software tasks with independently checkable outcomes.
Include the original failure scenario when changing debugging guidance. Freeze
the baseline and candidate, then keep task input, environment, tools, model,
effort, and evaluator criteria equal. Use disposable repositories and isolated
Codex homes outside the target checkout, supported authentication, and no unrelated
plugins or hooks. Do not expose private logs or credentials in the result.

Before attributing a difference to changed instructions, measure repeated runs
of the same frozen build under the same conditions (A/A). Verify that the runner
actually loaded the intended source, instructions, and build selector. Record
that identity with the observations; selecting a label is not proof of loading.
Choose the success criterion before inspecting candidate results. If identical
build variation can explain the apparent gain, report the result as inconclusive
or gather more evidence within the authorized budget. Do not impose a universal
sample count or buy more model runs to rescue a preferred result.

Use explicit model/effort settings and record the actual context and command.
Keep observations separate from inference: accepted behavior, missing requirements,
repairs, elapsed time, model usage, and cache observations. A cache hit requires a
matching prefix; a file reread does not establish a charge or a saving. Subscription
allowance cannot be derived directly from API token prices.

Report the sample's limits. Repeat only within the authorized budget when the
remaining decision needs it. For explicitly requested profile discovery or
instrumentation recovery, use $onepersonlabs:configure-harness and its diagnostic reference.
