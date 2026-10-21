#!/usr/bin/env python3
"""Local design evidence utilities. No installation, services or Projector mutations.

Run with --help. Capture requires already-installed Playwright/Chromium and Pillow;
comparison requires Pillow. Verify, episode commands and motion-fit use the stdlib.
"""

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
# Also permits a caller to load this file with importlib, as the unit runner does.
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_capture import capture, verify
from evidence_files import EvidenceError
from evidence_review import compare, fit_motion, recall_episodes, validate_episodes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("capture", help="Capture declared deterministic states to a new directory")
    command.add_argument("--manifest", required=True)
    command.add_argument("--out", required=True)
    command.add_argument("--channel", choices=("chromium", "chrome", "msedge"), default="chromium")
    command = sub.add_parser("verify", help="Fail if frozen capture inputs or artifacts changed")
    command.add_argument("--evidence", required=True)
    command = sub.add_parser("compare", help="Create a self-contained blinded gallery and separate mapping")
    command.add_argument("--manifest", required=True)
    command.add_argument("--out", required=True)
    command = sub.add_parser("episode-validate", help="Validate decisions with explicit judgment provenance")
    command.add_argument("--file", required=True)
    command = sub.add_parser("episode-recall", help="Recall exact context matches without inferring preferences")
    command.add_argument("--file", required=True)
    command.add_argument("--context", required=True)
    command = sub.add_parser("motion-fit", help="Report residuals for descriptive curves from time_ms,value CSV")
    command.add_argument("--csv", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            result = capture(args.manifest, args.out, args.channel)
            result = {"status": result["status"], "evidence": str(Path(args.out).resolve() / "evidence.json")}
        elif args.command == "verify":
            result = verify(args.evidence)
        elif args.command == "compare":
            result = compare(args.manifest, args.out)
        elif args.command == "episode-validate":
            result = {"status": "valid", "episodes": len(validate_episodes(args.file)["episodes"])}
        elif args.command == "episode-recall":
            result = recall_episodes(args.file, args.context)
        else:
            result = fit_motion(args.csv)
    except (EvidenceError, OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
