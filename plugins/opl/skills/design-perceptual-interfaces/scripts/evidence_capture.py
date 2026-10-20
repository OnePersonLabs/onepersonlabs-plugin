"""Capture declared browser states and verify their frozen file provenance.

A page's state attribute is self-reported evidence, not a measurement of motion.
Browser clock brackets are measured; a requested seek time is only a request.
"""

import hashlib
import html
import math
import os
from pathlib import Path
import re
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from evidence_files import (EvidenceError, digest, document, image_png, image_tag,
                            new_output, read_json, require, snapshot, text,
                            version_one, write_json)


def capture_spec(manifest):
    manifest = Path(manifest).resolve()
    spec, raw = read_json(manifest)
    version_one(spec)
    target = text(spec.get("target"), "target")
    parts = urlsplit(target)
    local = None
    if parts.scheme in ("http", "https"):
        require(bool(parts.netloc), "target URL must have a host")
        url = target
    else:
        require(not parts.scheme and not Path(parts.path).is_absolute(),
                "target must be http(s) or a relative local HTML path")
        local = (manifest.parent / parts.path).resolve()
        require(local.is_file(), f"Local target is missing: {local}")
        url = local.as_uri() + ("?" + parts.query if parts.query else "")
        if parts.fragment:
            url += "#" + parts.fragment
    sources = spec.get("source_files")
    require(isinstance(sources, list) and bool(sources), "source_files must declare at least one source file")
    sources = [(manifest.parent / text(p, "source file")).resolve() for p in sources]
    inputs = [manifest, *sources, *sorted(Path(__file__).parent.glob("*.py"))]
    if local:
        inputs.append(local)
    before = snapshot(inputs)
    require(before[str(manifest)] == hashlib.sha256(raw).hexdigest(), "Manifest changed during loading")
    text(spec.get("ready_selector"), "ready_selector")
    text(spec.get("state_attribute", "data-evidence-state"), "state_attribute")
    viewport = spec.get("viewport")
    require(isinstance(viewport, dict) and all(type(viewport.get(k)) is int and 1 <= viewport[k] <= 8192
                                             for k in ("width", "height")), "viewport requires width/height in 1..8192")
    require(spec.get("reduced_motion") in ("reduce", "no-preference"), "Declare reduced_motion")
    timeout = spec.get("timeout_ms", 10000)
    require(type(timeout) is int and 1 <= timeout <= 120000, "timeout_ms must be 1..120000")
    frames = spec.get("frames")
    require(isinstance(frames, list) and bool(frames), "frames must be a nonempty list")
    ids = set()
    for frame in frames:
        require(isinstance(frame, dict), "Each frame must be an object")
        ident = text(frame.get("id"), "frame id")
        folded = ident.casefold()
        # Frames share a directory with generated sheets; Windows also aliases
        # case variants and reserves device names even when an extension is added.
        reserved = (folded == "contact-sheet" or folded in {"con", "prn", "aux", "nul"}
                    or re.fullmatch(r"(?:com|lpt)[1-9]", folded) is not None)
        require(re.fullmatch(r"[A-Za-z0-9_-]+", ident) is not None and len(ident) <= 251
                and folded not in ids and not reserved,
                "Frame IDs must be unique ignoring case, Windows-safe, and not reserved for generated artifacts")
        ids.add(folded)
        query = frame.get("query", {})
        require(isinstance(query, dict) and all(isinstance(k, str) and isinstance(v, (str, int, float))
                                              for k, v in query.items()), "query must map names to scalar values")
        if "reduced_motion" in frame:
            require(frame["reduced_motion"] in ("reduce", "no-preference"), "Invalid frame reduced_motion")
        if "requested_time_ms" in frame:
            value = frame["requested_time_ms"]
            require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                    "requested_time_ms must be finite and nonnegative")
        if "expected_state" in frame:
            text(frame["expected_state"], "expected_state")
    return spec, url, before, local is None


def frame_url(url, query):
    parts = urlsplit(url)
    values = dict(parse_qsl(parts.query, keep_blank_values=True))
    values.update({k: str(v) for k, v in query.items()})
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(values), parts.fragment))


def contact_sheet(out, frames):
    from PIL import Image, ImageDraw
    sizes = []
    for frame in frames:
        with Image.open(out / frame["artifact"]) as image:
            sizes.append(image.size)
    scale = min(1, 640 / max(size[0] for size in sizes))
    width = max(1, round(max(size[0] for size in sizes) * scale))
    height = max(1, round(max(size[1] for size in sizes) * scale))
    columns = min(3, len(frames))
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (columns * width, rows * (height + 36)), "white")
    draw = ImageDraw.Draw(sheet)
    body = '<h1>Declared states</h1><p>State labels are reported by the page. Seek requests are not measured time.</p>'
    for i, frame in enumerate(frames):
        x, y = (i % columns) * width, (i // columns) * (height + 36)
        with Image.open(out / frame["artifact"]) as image:
            thumbnail = image.convert("RGB")
            thumbnail.thumbnail((width, height), Image.Resampling.LANCZOS)
            sheet.paste(thumbnail, (x, y + 36))
        label = frame["id"]
        draw.text((x + 8, y + 8), label, fill="black")
        body += ('<figure>' + image_tag(image_png(out / frame["artifact"]), label) +
                 '<figcaption>' + html.escape(label + " -- " + frame["declared_state"]) + '</figcaption></figure>')
    sheet.save(out / "contact-sheet.png")
    (out / "contact-sheet.html").write_text(document("State evidence", body), encoding="utf-8")


def capture(manifest, output, channel="chromium"):
    spec, url, before, remote = capture_spec(manifest)
    # Import only at the capture boundary: all record validation works without a browser.
    from playwright.sync_api import Error as BrowserError, sync_playwright
    out = new_output(output)
    record = {"version": 1, "kind": "capture", "status": "failed", "inputs_before": before,
              "inputs_after": {}, "artifacts": {}, "frames": [], "viewport": spec["viewport"],
              "reduced_motion": spec["reduced_motion"], "target": url,
              "limitations": ["Page-declared states are not independent measurements of visual correctness.",
                              "Frozen frames do not establish smoothness, comprehension or aesthetic quality."]}
    if remote:
        record["limitations"].append("Remote deployment correspondence to declared local sources is unverified.")
    started = time.perf_counter()
    try:
        with sync_playwright() as playwright:
            executable = os.environ.get("OPL_CHROMIUM_BIN")
            if executable:
                require(Path(executable).is_file(), "OPL_CHROMIUM_BIN does not name an existing browser")
            launch = ({"executable_path": executable} if executable else
                      ({} if channel == "chromium" else {"channel": channel}))
            with playwright.chromium.launch(headless=True, **launch) as browser:
                record["browser"] = {"version": browser.version, "channel": channel, "executable_path": executable}
                context = browser.new_context(viewport=spec["viewport"], device_scale_factor=1,
                                              reduced_motion=spec["reduced_motion"])
                context.set_default_timeout(spec.get("timeout_ms", 10000))
                for frame in spec["frames"]:
                    page = context.new_page()
                    motion = frame.get("reduced_motion", spec["reduced_motion"])
                    page.emulate_media(reduced_motion=motion)
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    frame_start = time.perf_counter()
                    address = frame_url(url, frame.get("query", {}))
                    page.goto(address, wait_until="load", timeout=spec.get("timeout_ms", 10000))
                    selector = spec["ready_selector"]
                    page.wait_for_selector(selector, state="visible", strict=True)
                    page.wait_for_function("document.fonts.status === 'loaded'")
                    attribute = spec.get("state_attribute", "data-evidence-state")
                    time_attribute = spec.get("declared_time_attribute")
                    sample = """([selector, attribute, timeAttribute]) => ({state:document.querySelector(selector).getAttribute(attribute),
                        declared_time:timeAttribute ? document.querySelector(selector).getAttribute(timeAttribute) : null,
                        browser_time_ms:performance.now(), browser_epoch_ms:Date.now(),
                        ready:!!document.querySelector(selector), fonts:document.fonts.status})"""
                    first = page.evaluate(sample, [selector, attribute, time_attribute])
                    text(first["state"], "Page-declared state attribute")
                    if time_attribute:
                        text(first["declared_time"], "Page-declared time attribute")
                    if "expected_state" in frame:
                        require(first["state"] == frame["expected_state"], f"Declared state mismatch for {frame['id']}")
                    artifact = frame["id"] + ".png"
                    page.screenshot(path=str(out / artifact), animations="allow", caret="initial", scale="css")
                    last = page.evaluate(sample, [selector, attribute, time_attribute])
                    require(first["state"] == last["state"] and first["declared_time"] == last["declared_time"]
                            and last["ready"], "Page state changed during screenshot")
                    require(not errors, "Browser page errors: " + "; ".join(errors))
                    record["frames"].append({"id": frame["id"], "artifact": artifact, "url": address,
                        "requested_time_ms": frame.get("requested_time_ms"), "declared_state": first["state"],
                        "ready_selector": selector, "state_attribute": attribute, "reduced_motion": motion,
                        "declared_time_attribute": time_attribute,
                        "before_screenshot": first, "after_screenshot": last,
                        "host_elapsed_ms": (time.perf_counter() - frame_start) * 1000})
                    page.close()
                context.close()
        contact_sheet(out, record["frames"])
        record["inputs_after"] = snapshot(before)
        require(record["inputs_after"] == before, "Declared input changed while evidence was being produced")
        record["status"] = "complete"
    except (EvidenceError, BrowserError, OSError) as exc:
        record["error"] = str(exc)
        raise EvidenceError(f"Capture failed; inspect {out / 'evidence.json'}: {exc}") from exc
    finally:
        if not record["inputs_after"]:
            record["inputs_after"] = {name: digest(name) if Path(name).is_file() else None for name in before}
        record["host_elapsed_ms"] = (time.perf_counter() - started) * 1000
        record["artifacts"] = {p.name: digest(p) for p in sorted(out.iterdir()) if p.is_file()}
        write_json(out / "evidence.json", record)
    return record


def verify(evidence):
    path = Path(evidence).resolve()
    record, _ = read_json(path)
    version_one(record)
    require(record.get("kind") == "capture" and record.get("status") == "complete", "Capture is incomplete or failed")
    before = record.get("inputs_before")
    require(isinstance(before, dict) and bool(before), "Missing frozen input inventory")
    require(record.get("inputs_after") == before, "Input hashes changed during capture")
    require(snapshot(before) == before, "Declared source or tool changed since capture")
    artifacts = record.get("artifacts")
    require(isinstance(artifacts, dict) and bool(artifacts), "Missing artifact inventory")
    frames = record.get("frames")
    require(isinstance(frames, list) and bool(frames), "Missing captured frames")
    required = {"contact-sheet.png", "contact-sheet.html", *(f["artifact"] for f in frames)}
    require(required <= artifacts.keys(), "Capture inventory omits required artifacts")
    for name, expected in artifacts.items():
        item = (path.parent / name).resolve()
        require(item.parent == path.parent and item.name == name, "Artifact must be a direct child of evidence directory")
        require(digest(item) == expected, f"Artifact changed: {name}")
    return {"status": "verified", "frames": len(frames), "artifacts": len(artifacts),
            "limits": "File identity only; does not establish semantic, human or aesthetic acceptance."}
