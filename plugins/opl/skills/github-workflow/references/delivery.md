# Delivery and native automation

Read this branch when Projects, review, PR repair, or merge affects status.
Use the repository's configured lane and merge policy. Keep local completion,
merged delivery, release, and human qualification distinct.

Native Project auto-add does not backfill the existing matching issue set.
Reconcile that set when adopting a workflow. Use native Done automation only
when its trigger matches complete acceptance. Preserve existing fields and
filters; use ordinary root-owned GitHub tools for remaining authorized writes.
See [auto-add](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)
and [built-in automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations).

Keep the same builder for PR repair rounds and make small checked commits.
Review the complete series from a frozen baseline. Batch broader affected checks
once at an integration boundary; rerun evidence invalidated by repairs.
A closed unmerged PR is not done.

When choosing a review surface or interpreting its usage, read
[review lane](../../setup-repo-workflow/references/native-workflow.md#review-lane).
That reference records local versus GitHub usage categories and the dated
0.160.1 native fresh-delegate behavior. Inline presentation does not guarantee
shared history or cache savings.
