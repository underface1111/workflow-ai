#!/usr/bin/env python3
"""Validate AI Code Agent changes (Bước C) — run npm test after apply."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_JS = REPO_ROOT / "src/app.js"


def check_learn_003_applied() -> list[str]:
    errors: list[str] = []
    if not APP_JS.exists():
        return ["src/app.js not found"]
    content = APP_JS.read_text(encoding="utf-8")
    if "version: '0.2.0'" not in content and 'version: "0.2.0"' not in content:
        errors.append("src/app.js: missing version 0.2.0 on /health")
    unit = REPO_ROOT / "tests/unit/app.test.js"
    if unit.exists() and "res.body.version" not in unit.read_text(encoding="utf-8"):
        errors.append("tests/unit/app.test.js: missing version assertion")
    return errors


def run_npm_test() -> int:
    print("Running npm test...", file=sys.stderr)
    return subprocess.run(["npm", "test"], cwd=REPO_ROOT, shell=True, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate code agent output")
    parser.add_argument("--skip-npm", action="store_true")
    parser.add_argument("--ticket", default="learn-003", help="Ticket checks to run")
    args = parser.parse_args()

    errors: list[str] = []
    if args.ticket == "learn-003":
        errors.extend(check_learn_003_applied())

    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("Structural checks OK (LEARN-003).")

    if args.skip_npm:
        return 0

    code = run_npm_test()
    if code != 0:
        print("npm test failed.", file=sys.stderr)
        return code
    print("Validation passed (structure + npm test).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
