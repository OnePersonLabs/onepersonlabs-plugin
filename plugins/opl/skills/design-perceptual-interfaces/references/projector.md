# Projector compatibility

Use this reference only when the project already uses Projector. Follow the
installed Projector skill and native root. This capability does not activate
Projector, schedule work, invent status, or write its cache receipts.

## Attach evidence to existing ownership

| Design material | Owner and location |
| --- | --- |
| Accepted communication meaning, invariants, reasons | Existing Concept under `.projector/meaning/` |
| Participants and repeated technical checks | Existing or root-approved Lens |
| Proposals, inspected states, images, contact sheets, judgments | Project's normal artifact/design path |
| Current decision, assignment, unresolved judgment, evidence links | Existing `.projector/work/ID.md` checkpoint body |
| Reusable mechanism with alternatives and limits | Root-reviewed Pattern Candidate where useful |

Return proposed changes to the owner unless the exact surface is assigned to you.
Preserve Concept/Lens identities when their meaning stays the same. Do not create
records for a literal label edit whose action, state, ownership, persistence, and
accessibility meaning are unchanged.

Projector's evidence kinds are `static` and `runtime`. Keep semantic correctness,
comprehension/control, and aesthetic preference as separate claims in the design
evidence. A receipt from a capture validator establishes only its technical
condition. It does not establish beauty or user comprehension.

## Capture, then verify

Capture through the application's native boundary. Put source and artifacts in
normal project paths. `.projector/cache/**` and `.projector/work/**` are excluded
from discovery; they are not suitable inputs for reusable visual proof.

For a repeatable technical condition, give its Lens check a real command and
separate arguments, input paths, target, and explicit coverage. For example,
after putting the observation helper in a project-owned tools path:

```yaml
checks:
  - id: current-render-evidence
    command: python
    args: [-B, tools/design_evidence.py, verify, --evidence, artifacts/design/run/evidence.json]
    selectors: [changed-view]
    conditions: [view#current-render-evidence]
    evidence: runtime
    coverage: [src/view.js]
    inputs:
      - tools/design_evidence.py
      - artifacts/design/capture.json
      - artifacts/design/run/**
```

This fragment belongs in an existing Lens with a real `changed-view` selector and
`view#current-render-evidence` condition. Substitute actual paths and coverage;
do not paste identifiers into an unrelated project. Include all source, style,
data, configuration, helper, and artifact dependencies used by this observation.
The capture manifest binds the inputs actually declared there. Missing dependencies
remain outside its claim. Use the installed helper path when appropriate and bind
its revision through the project's established input mechanism.

Run capture before the Lens check. A check that rewrites its own declared inputs
can become unresolved because Projector fingerprints inputs before and after.
The frozen-artifact verifier reads only; it rejects changed source or missing or
changed artifacts. Separate browser interaction tests establish control behavior.
Check exit status has no aesthetic interpretation.

Use Projector's normal reconcile operation for receipts. Its runtime writes
`.projector/cache/checks/<id>/receipt.json`, stdout, and stderr. Do not manufacture
those files or count a wildcard selector as coverage of all future participants.
Link one-time native evidence with checked source, target, and limits when a
permanent check adds no useful protection.

## Tested boundary and continuing work

The adapter was exercised through native `activate`, `writeCheckpoint`, `focus`,
`reconcile`, and `resume` operations against the revision recorded in
[sources](sources.md). A supported technical check became unresolved after a
source change; fresh execution reported mismatch against the old artifact.
Inactive reconciliation created no Projector state. These observations establish
the existing technical route, not a visual or model-effectiveness result.

Keep visual and human gaps in the existing checkpoint. The root decides whether
accepted meaning or a Pattern Candidate should change. A source plugin edit does
not update installed bundles or guidance already loaded by another session.
