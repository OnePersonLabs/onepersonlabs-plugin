# Local observation tools

Use the application's current capture/test tooling first. The optional helper
`scripts/design_evidence.py` provides portable artifact operations when needed.
It creates no service, workflow database, Projector records, or global settings.
Use `python` on Windows and `python3` where that is the installed interpreter.
Run `--help` and the relevant subcommand's help for the current interface.

Capture needs Python Playwright, Pillow, and an available Chromium browser.
Other image operations use Pillow. The tool reports missing prerequisites; it
does not install software or call a model/API. Use an already installed browser
channel or the existing `OPL_CHROMIUM_BIN` convention where supported.

## Capture a meaningful state set

Example manifest, with paths relative to the manifest:

```json
{
  "version": 1,
  "target": "../../src/specimen.html",
  "source_files": ["../../src/specimen.html", "../../src/specimen.js", "../../src/specimen.css"],
  "ready_selector": "[data-capture-ready='true']",
  "state_attribute": "data-capture-state",
  "declared_time_attribute": "data-time-ms",
  "viewport": {"width": 1280, "height": 900},
  "reduced_motion": "no-preference",
  "frames": [
    {"id": "before", "query": {"scene": "regroup", "phase": "before"}, "expected_state": "regroup:before", "requested_time_ms": 0},
    {"id": "mid", "query": {"scene": "regroup", "phase": "mid"}, "expected_state": "regroup:mid", "requested_time_ms": 600},
    {"id": "settled", "query": {"scene": "regroup", "phase": "settled"}, "expected_state": "regroup:settled", "requested_time_ms": 1200}
  ]
}
```

Adapt the native URL/state seam rather than imposing these query names on a
product. The shipped [specimens](../specimens/index.html) implement this example.
The ready element must expose a nonempty actual state attribute.
The optional `declared_time_attribute` records the page-reported frozen time.
A frame can override `reduced_motion` with `reduce` or `no-preference`. The helper records
it as self-reported application evidence, not independent proof of semantics.
The optional `declared_time_attribute` retains a frozen application time separately
from browser clocks. A frame can override `reduced_motion` for matched captures.
Include the relevant helper and configuration among source inputs when they can
alter the result. Remote URLs need equivalent source/deployment binding; local
hashes alone cannot prove which build a remote server served.

```text
python scripts/design_evidence.py capture --manifest capture.json --out run-01
python scripts/design_evidence.py verify --evidence run-01/evidence.json
```

Use a new output directory. Inspect the actual PNGs and contact sheet. Keep the
manifest and source bindings. Capture records readiness, browser/host time brackets,
viewport, motion setting, and requested frame labels. Requested time is not measured
animation phase. Missing readiness, a wrong reported state, or changed declared
inputs makes the capture fail. A partial output is not completed evidence.

Add first response, early/late trajectory, interruption, reversal, and reduced-motion
states when they matter. Also exercise live controls, keyboard/focus, rapid input,
and recovery. Frozen frame capture and successful file verification do not replace
those tests. Use representative viewports and actual content.

## Present comparable alternatives

```json
{
  "version": 1,
  "prompt": "What changed? What stayed the same? Which treatment would you choose, and why?",
  "candidates": [
    {"image": "a.png", "caption": "Same task and state", "condition": "private condition A", "source": "private source"},
    {"image": "b.png", "caption": "Same task and state", "condition": "private condition B", "source": "private source"}
  ]
}
```

Run `compare --manifest comparison.json --out comparison-01`. Share `gallery.html`
for judgment; retain `mapping.json` separately. Images are embedded and reencoded.
Review pixels and captions for condition clues. Keep user responses with the
comparison's actual mapping. Initial unknown judgments are not scores or votes.
This gallery supports still images/contact sheets; use matched clips or live
interactions as additional evidence for temporal experience and control.

## Retain and retrieve an episode

Use `episode-validate --file episodes.json` before reusing a meaningful correction.
The file has `version: 1` and an `episodes` array. Each episode has an `id`,
`problem`, `context` object, alternatives with IDs/status/reason, judgments with
actor/identity/basis/statement/evidence, `limits`, and `confidence`. Exactly one
alternative is selected; a composed selection can name its contributing sources.
User-attributed judgments require actual evidence and cannot use an inferred basis.

Use `episode-recall --file episodes.json --context context.json`. Context is a
nonempty object; all requested key/value pairs must match. Choose fields that
preserve the relevant problem, surface, task, and audience. Inspect applicability
before using a match. An unmatched context returns no learned preference.

## Measure a demonstrated trace

Run `motion-fit --csv samples.csv` for columns `time_ms,value`. Retain units,
sampling method, and original recording elsewhere in the same evidence packet.
The tool normalizes endpoints and compares simple curve candidates, reporting
residuals in value units. It cannot recover hidden physics or establish intent.
Use [motion guidance](motion.md) to decide whether the measured mechanism fits.
