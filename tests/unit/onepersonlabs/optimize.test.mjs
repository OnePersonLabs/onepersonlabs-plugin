import test from "node:test"
import assert from "node:assert/strict"
import { compareObjective, decide, gatePasses, median } from "../../../plugins/onepersonlabs/skills/optimize/scripts/decide.mjs"

const base = {
  spec: {
    primary: { name: "elapsed_ms", direction: "minimize" },
    comparison: { method: "absolute", noise_threshold: 2 },
  },
  baseline: { metrics: { elapsed_ms: { samples: [100, 100, 100, 100] } } },
}

const withCandidate = (input, candidate) => decide({ ...input, candidate })

test("aggregation and correctness gates preserve numeric measurement semantics", () => {
  assert.equal(median([102, 98, 100, 101]), 100.5)
  assert.equal(gatePasses(1, "== 1"), true)
  assert.equal(gatePasses("no result", ">= 1"), false)
})

test("a gain inside observed noise stays inconclusive", () => {
  const result = withCandidate(base, { metrics: { elapsed_ms: { samples: [99, 100, 100, 101] } } })
  assert.equal(result.decision, "inconclusive")
  assert.equal(result.eligible, false)
})

test("a failed correctness gate makes an otherwise faster candidate degenerate", () => {
  const result = decide({
    ...base,
    spec: { ...base.spec, degenerate_gates: [{ name: "correctness", check: "== 1" }] },
    candidate: { metrics: { elapsed_ms: { samples: [80, 81] } }, gates: { correctness: 0 } },
  })
  assert.equal(result.decision, "degenerate")
  assert.equal(result.next_measurement, "none")
})

test("a primary win is rejected when a required objective exceeds its regression bound", () => {
  const result = decide({
    ...base,
    spec: {
      ...base.spec,
      objectives: [{ name: "memory_mb", direction: "minimize", max_regression: { value: 2 } }],
    },
    baseline: { metrics: {
      elapsed_ms: { samples: [100, 100, 100] }, memory_mb: { samples: [40, 40, 40] },
    } },
    candidate: { metrics: {
      elapsed_ms: { samples: [80, 81] }, memory_mb: { samples: [43, 44] },
    } },
  })
  assert.equal(result.decision, "revert")
  assert.deepEqual(result.violated_objectives, ["memory_mb"])
})

test("paired samples remain unresolved when observations overlap", () => {
  const result = decide({
    ...base,
    spec: { ...base.spec, comparison: { method: "paired", relative_threshold: 0.02 } },
    baseline: { metrics: { elapsed_ms: { samples: [100, 98, 101] } } },
    candidate: { metrics: { elapsed_ms: { samples: [99, 99, 100] } } },
  })
  assert.equal(result.decision, "inconclusive")
})

test("paired comparison requires a complete baseline and rejects unpaired extra candidate samples", () => {
  const result = decide({
    ...base,
    spec: { ...base.spec, comparison: { method: "paired", relative_threshold: 0.02 } },
    baseline: { metrics: { elapsed_ms: { samples: [100, 100] } } },
    candidate: { metrics: { elapsed_ms: { samples: [80, 81, 79] } } },
  })
  assert.equal(result.decision, "error")
  assert.match(result.reason, /insufficient paired baseline/)
})

test("confirmation ladder does not accept a candidate until required repeats are present", () => {
  const input = {
    ...base,
    spec: { ...base.spec, ladder: { enabled: true, exploratory_pairs: 2, confirmation_repeats: 4 } },
  }
  const first = withCandidate(input, { metrics: { elapsed_ms: { samples: [90, 91] } } })
  assert.equal(first.decision, "promising")
  assert.equal(first.eligible, true)
  assert.equal(first.next_measurement, "confirm")
  const confirmed = withCandidate(input, { metrics: { elapsed_ms: { samples: [90, 91, 89, 92] } } })
  assert.equal(confirmed.decision, "keep")
  assert.equal(confirmed.next_measurement, "none")
})

test("combined changes require their own comparison and all declared targets to be reached", () => {
  const spec = {
    primary: { name: "elapsed_ms", direction: "minimize", target: 85 },
    objectives: [{ name: "memory_mb", direction: "minimize", target: 35 }],
    comparison: { method: "absolute", noise_threshold: 2 },
  }
  const result = decide({
    spec,
    baseline: { metrics: {
      elapsed_ms: { samples: [100, 100, 100] }, memory_mb: { samples: [40, 40, 40] },
    } },
    // The combined result gets a new measurement; independent wins are not reused.
    candidate: { metrics: {
      elapsed_ms: { samples: [90, 90, 90] }, memory_mb: { samples: [36, 36, 36] },
    } },
  })
  assert.equal(result.decision, "keep")
  assert.equal(result.target_reached, false)
  assert.equal(result.next_measurement, "none")
  const composition = compareObjective({
    baselineValue: 40, candidateValue: 36, direction: "minimize",
    comparison: { method: "absolute", noise_threshold: 2, relative_threshold: 0.05 },
  })
  assert.equal(composition.verdict, "improved")
})


test("unmatched baseline tail cannot erase a paired required regression", () => {
  const result = decide({
    spec: {primary: {name: "time", direction: "minimize"},
      objectives: [{name: "memory", direction: "minimize", max_regression: {value: 2}}],
      comparison: {method: "paired", relative_threshold: 0.02}},
    baseline: {metrics: {time: {samples: [100, 100, 1000, 1000]}, memory: {samples: [100, 100, 1000, 1000]}}},
    candidate: {metrics: {time: {samples: [80, 80]}, memory: {samples: [120, 120]}}},
  })
  assert.equal(result.decision, "revert")
  assert.equal(result.comparisons.time.delta, 20)
  assert.equal(result.comparisons.memory.delta, -20)
  assert.deepEqual(result.violated_objectives, ["memory"])
})
