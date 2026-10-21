"""Blinded reviews, explicitly scoped episode records and descriptive curve fits."""

import csv
import hashlib
import html
import math
from pathlib import Path
import secrets
import re

from evidence_files import (document, image_png, image_tag, new_output, read_json,
                            require, snapshot, text, unchanged, version_one, write_json)


def compare(manifest, output):
    path = Path(manifest).resolve()
    spec, raw = read_json(path)
    version_one(spec)
    prompt = text(spec.get("prompt"), "prompt")
    candidates = spec.get("candidates")
    require(isinstance(candidates, list) and len(candidates) >= 2, "Comparison needs at least two candidates")
    inputs = [path]
    public_text = [prompt]
    private = []
    for item in candidates:
        require(isinstance(item, dict), "Candidate must be an object")
        image = (path.parent / text(item.get("image"), "candidate image")).resolve()
        caption = text(item.get("caption"), "candidate caption")
        condition = text(item.get("condition"), "candidate condition")
        source = text(item.get("source"), "candidate source")
        inputs.append(image)
        public_text.append(caption)
        private.extend((condition, source, str(image), image.name))
    # Explicit metadata is excluded; image content itself can still reveal an approach.
    for value in private:
        pattern = r"(?<!\w)" + re.escape(value) + r"(?!\w)"
        leaks = any(re.search(pattern, p, re.IGNORECASE) if len(value) >= 3
                    else p.strip().casefold() == value.casefold() for p in public_text)
        require(not leaks,
                "Prompt/caption exposes a condition or source; use neutral review content")
    before = snapshot(inputs)
    require(before[str(path)] == hashlib.sha256(raw).hexdigest(), "Manifest changed during loading")
    prepared = [(dict(item), image_png(path.parent / item["image"])) for item in candidates]
    unchanged(before)
    secrets.SystemRandom().shuffle(prepared)
    out = new_output(output)
    mapping = {"version": 1, "inputs": before, "candidates": []}
    judgments = {"version": 1, "human_judgments": "unknown", "candidates": []}
    body = ('<h1>Compare the candidates</h1><p>' + html.escape(prompt) + '</p>'
            '<p>Record what you understood and would do before revealing intended meaning. '
            'Visual preference is a separate judgment. No responses have been submitted or saved by this page.</p>')
    for index, (candidate, png) in enumerate(prepared, 1):
        ident = f"Candidate {index}"
        mapping["candidates"].append({**candidate, "anonymous_id": ident})
        judgments["candidates"].append({"anonymous_id": ident, "interpretation": None,
            "intended_action": None, "aesthetic_preference": None, "actor": None,
            "identity": None, "evidence": [], "status": "unknown"})
        body += ('<figure>' + image_tag(png, ident) + '<figcaption><strong>' + ident +
                 '</strong> -- ' + html.escape(candidate["caption"]) + '</figcaption>'
                 '<label>What does this mean, and what would you do?<textarea></textarea></label>'
                 '<label>Separately, what works or fails visually?<textarea></textarea></label></figure>')
    (out / "gallery.html").write_text(document("Candidate comparison", body), encoding="utf-8")
    write_json(out / "mapping.json", mapping)
    write_json(out / "judgments.json", judgments)
    return {"status": "prepared", "gallery": str(out / "gallery.html"),
            "mapping": str(out / "mapping.json"), "human_judgments": "unknown",
            "limits": "Share only gallery.html. Image pixels and captions require a human blinding check."}


def context_object(value):
    require(isinstance(value, dict) and bool(value), "context must be a nonempty object")
    for key, item in value.items():
        text(key, "context key")
        require(type(item) in (str, bool, int, float) and (not isinstance(item, str) or item.strip()),
                "Context values must be nonempty text, finite numbers or booleans")
        if type(item) in (int, float):
            require(math.isfinite(item), "Context numbers must be finite")
    return value


def validate_episodes(path):
    spec, _ = read_json(path)
    version_one(spec)
    episodes = spec.get("episodes")
    require(isinstance(episodes, list), "episodes must be a list")
    ids = set()
    for episode in episodes:
        require(isinstance(episode, dict), "Episode must be an object")
        ident = text(episode.get("id"), "episode id")
        require(ident not in ids, "Duplicate episode id")
        ids.add(ident)
        text(episode.get("problem"), "problem")
        context_object(episode.get("context"))
        alternatives = episode.get("alternatives")
        require(isinstance(alternatives, list) and len(alternatives) >= 2, "Record at least two alternatives")
        alternative_ids = set()
        for alternative in alternatives:
            require(isinstance(alternative, dict), "Alternative must be an object")
            aid = text(alternative.get("id"), "alternative id")
            require(aid not in alternative_ids, "Duplicate alternative id")
            alternative_ids.add(aid)
            require(alternative.get("status") in ("selected", "rejected", "considered"), "Invalid alternative status")
            text(alternative.get("reason"), "alternative reason")
        require(sum(a["status"] == "selected" for a in alternatives) == 1, "Exactly one alternative must be selected")
        judgments = episode.get("judgments")
        require(isinstance(judgments, list) and bool(judgments), "Record judgment provenance")
        for judgment in judgments:
            require(isinstance(judgment, dict), "Judgment must be an object")
            require(judgment.get("actor") in ("user", "model"), "Judgment actor must be user or model")
            text(judgment.get("identity"), "judgment identity")
            text(judgment.get("statement"), "judgment statement")
            require(judgment.get("basis") in ("stated", "observed", "inferred"), "Invalid judgment basis")
            evidence = judgment.get("evidence")
            require(isinstance(evidence, list) and bool(evidence), "Judgment needs source evidence references")
            for reference in evidence:
                text(reference, "judgment evidence")
            require(not (judgment["actor"] == "user" and judgment["basis"] == "inferred"),
                    "An inferred preference belongs to the model, not the user")
        limits = episode.get("limits")
        require(isinstance(limits, list) and bool(limits), "Record explicit episode limits")
        for limit in limits:
            text(limit, "episode limit")
        require(episode.get("confidence") in ("low", "medium", "high"), "Invalid episode confidence")
    return spec


def recall_episodes(path, context_path):
    spec = validate_episodes(path)
    query, _ = read_json(context_path)
    context_object(query)
    # Type-sensitive equality avoids treating JSON true as the number 1.
    matches = [episode for episode in spec["episodes"] if all(
        key in episode["context"] and type(episode["context"][key]) is type(value)
        and episode["context"][key] == value for key, value in query.items())]
    return {"version": 1, "matching_context": query, "episodes": matches,
            "limits": "Exact requested context matches only. Recorded judgments are not global user preferences."}


def fit_motion(path):
    """Endpoint-normalized descriptive candidates; no physical parameter inference."""
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames is not None and {"time_ms", "value"} <= set(reader.fieldnames),
                "CSV requires time_ms,value columns")
        samples = [(float(row["time_ms"]), float(row["value"])) for row in reader]
    require(len(samples) >= 3 and all(math.isfinite(v) for row in samples for v in row),
            "Need at least three finite samples")
    require(all(b[0] > a[0] for a, b in zip(samples, samples[1:])), "Sample times must strictly increase")
    t0, y0 = samples[0]
    duration = samples[-1][0] - t0
    delta = samples[-1][1] - y0
    require(delta != 0, "Equal endpoints cannot define these normalized curve candidates")
    curves = {"linear": ("u", lambda u: u), "ease-in-quadratic": ("u*u", lambda u: u*u),
              "ease-out-quadratic": ("1-(1-u)^2", lambda u: 1-(1-u)**2),
              "smoothstep": ("3*u^2-2*u^3", lambda u: 3*u*u-2*u*u*u)}
    results = []
    for name, (formula, curve) in curves.items():
        residuals = [value - (y0 + delta * curve((t - t0) / duration)) for t, value in samples]
        results.append({"curve": name, "formula": formula,
                        "rmse": math.sqrt(sum(r*r for r in residuals) / len(samples)),
                        "max_abs_residual": max(abs(r) for r in residuals), "residuals": residuals})
    return {"version": 1, "source": snapshot([path]), "samples": len(samples),
            "normalization": {"start_time_ms": t0, "duration_ms": duration, "start_value": y0, "delta": delta},
            "candidates": sorted(results, key=lambda r: r["rmse"]),
            "limits": "Descriptive endpoint-normalized curves only; residuals use original value units. "
                      "No spring, physical model, intent or perceptual quality is inferred."}
