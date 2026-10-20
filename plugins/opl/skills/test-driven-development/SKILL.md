---
name: test-driven-development
description: Use an optional red-green-refactor loop to develop a meaningful observable contract.
---

# Test-driven development

Use test-first development when a failing example can guide the next change.
Choose coverage under the project's test policy; this skill does not require a
new permanent test for every behavior or change.

Inspect the existing test surface and caller-visible contract. Prefer a public
boundary that catches a plausible production failure with little setup. Reuse
repository commands and independently derived expectations.

1. **Red:** Write a small example and observe its assertion fail because the
   requested behavior is absent or wrong. Import, syntax, and fixture errors
   do not establish this evidence.
2. **Green:** Make the smallest coherent change and run the focused check.
   Revise an expectation only when the intended contract changes.
3. **Refactor:** Improve the design while the check stays green. Continue only
   with slices for which another example adds useful protection.

Preserve existing and concurrent work. If implementation already exists, test it
as found and report tests-after honestly. Do not revert someone else's work,
manufacture a failure, or weaken an assertion to claim a test-first sequence.
A passing new test establishes current behavior, not prior failure.

For test doubles, process boundaries, side effects, or nontrivial expected values,
read [test quality](references/test-quality.md). Use real collaborators when
practical and isolate only the external or nondeterministic boundary.

Run affected checks after the final relevant edit. Reuse valid evidence while
inputs remain unchanged. Report observed failures and passes, whether tests came
before or after implementation, and skipped or unavailable checks. A one-time
probe or manual observation can be sufficient when the project's policy permits
it; state its limits rather than promising regression protection.
