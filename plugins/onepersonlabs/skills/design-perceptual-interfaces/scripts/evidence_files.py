"""Small file contracts shared by the design evidence commands."""

import base64
import hashlib
import html
import io
import json
from pathlib import Path


class EvidenceError(ValueError):
    """A declared evidence contract was not satisfied."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def read_json(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return json.loads(raw), raw


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(paths):
    return {str(Path(p).resolve()): digest(p) for p in dict.fromkeys(paths)}


def unchanged(before):
    after = snapshot(before)
    require(before == after, "Declared input changed while evidence was being produced")
    return after


def new_output(path):
    path = Path(path).resolve()
    require(not path.exists(), f"Output already exists: {path}; choose a new directory")
    path.mkdir(parents=True)
    return path


def text(value, name):
    require(isinstance(value, str) and bool(value.strip()), f"{name} must be nonempty text")
    return value


def version_one(data):
    require(isinstance(data, dict) and data.get("version") == 1, "Expected an object with version: 1")


def image_png(path):
    """Reencode pixels, excluding filenames, EXIF, comments and other source metadata."""
    from PIL import Image
    with Image.open(path) as image:
        clean = Image.new("RGBA", image.size)
        clean.paste(image.convert("RGBA"))
        output = io.BytesIO()
        clean.save(output, format="PNG")
        return output.getvalue()


def image_tag(png, label):
    encoded = base64.b64encode(png).decode("ascii")
    return f'<img alt="{html.escape(label, quote=True)}" src="data:image/png;base64,{encoded}">'


def document(title, body):
    # No external resources, executable content, paths or condition names are needed.
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>'
            'body{font:16px system-ui;margin:2rem auto;max-width:1100px;padding:0 1rem;'
            'color:#202020;background:#fafafa}figure{margin:2rem 0;padding:1rem;'
            'border:1px solid #bbb}img{max-width:100%;height:auto}figcaption{margin:1rem 0}'
            'textarea{display:block;width:95%;min-height:5rem}label{display:block;margin:1rem 0}'
            '</style>' + body + '</html>')
