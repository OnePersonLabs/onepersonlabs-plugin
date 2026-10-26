---
name: optimize
description: Improve a working system against measured objectives when the winning change is unknown and noise, trade-offs, or composition could mislead.
---

# Optimize a working system

Select this workflow when the system already works and the task is to improve a measurable property, but it is not yet known which change wins. Start it without waiting for the user to name the skill. Use the existing implementation workflow for ordinary requested changes; use debugging when the main need is to explain a failure, and use `$onepersonlabs:solve-novel-software` when a risky technical assumption needs a falsifying probe. Route back here when the decision is which candidate performs better.

## Establish a trustworthy comparison

Name the current best, the primary metric, every required trade-off, and any correctness or safety gates before editing. Choose a workload and oracle that represent the consumer. A faster result that violates correctness or a required memory, cost, quality, or latency bound is not a win. Use an existing project objective when one exists; otherwise report measurements without inventing an acceptance threshold.

Record the baseline in the project's existing work record, such as its owning issue or checkpoint. Include source state and dirty changes, environment and configuration, exact workload and command, raw samples, correctness result, and the decision. Keep the experiment budget within the task's existing authorization and resource limits. Do not add approval steps when the work is already authorized, or assume that authorization for measurement permits unrelated side effects.

Check attribution before making speculative edits. For a claimed speedup, first compare repeated runs of the same build and workload; when identical-build variation can explain the gain, measure that variation and do not credit a change that remains inside it. Preserve raw observations and label missing, failed, or censored measurements rather than turning them into zeros or successes.

## Change, measure, decide

Change one meaningful factor where practical. Run the same correctness oracle and workload against the current best and candidate. Include all required objectives in each comparison. Use the deterministic helper when uncertainty, multiple objectives, paired observations, or confirmation would affect the decision:

```powershell
$skillDir = "<absolute loaded optimize skill directory>"
node "$skillDir/scripts/decide.mjs" "<path to comparison JSON file>"
```

The JSON file follows this compact shape (samples are raw numeric observations):

```json
{
  "spec": {
    "primary": { "name": "elapsed_ms", "direction": "minimize" },
    "objectives": [
      { "name": "memory_mb", "direction": "minimize", "max_regression": { "value": 4 } }
    ],
    "degenerate_gates": [{ "name": "correctness", "check": "== 1" }],
    "comparison": { "method": "absolute", "noise_threshold": 2 },
    "ladder": { "enabled": true, "exploratory_pairs": 2, "confirmation_repeats": 4 }
  },
  "baseline": {
    "metrics": { "elapsed_ms": { "samples": [100, 102, 99, 101] }, "memory_mb": { "samples": [40, 41, 40, 40] } }
  },
  "candidate": {
    "metrics": { "elapsed_ms": { "samples": [95, 96] }, "memory_mb": { "samples": [41, 42] } },
    "gates": { "correctness": 1 }
  }
}
```

Use the output as a measurement decision, not a substitute for engineering judgment. `degenerate` means the candidate failed a correctness gate or smoke check; `revert` means it regressed or did not improve a required objective; `inconclusive` means the evidence does not separate the outcomes; `promising` requests confirmation. Follow `next_measurement` and append each new raw sample and result to the same task checkpoint before deciding again. Keep a candidate only when it is eligible and `next_measurement` is `none`. Do not claim the target was reached unless the helper reports it and the consumer-level checks pass.

For paired comparison, provide aligned samples from the same workload conditions for both baseline and candidate; gather a complete baseline before interpreting additional candidate samples. The helper supports absolute, relative, and paired comparison, aggregation, required objectives, degeneracy gates, a confirmation ladder, and optional futility bounds. Missing required measurements are errors, not evidence of a win.

Compare every candidate to the current best, retain its exact source and measurement record, and rerun the full combined change against a fresh baseline. Individual wins need not compose. If confirmation is unavailable within the authorized budget, keep the result unresolved and the current best intact. Finish by exercising the selected change through its real consumer and correctness oracle, then update the existing project checkpoint with the result and remaining limits.
