#!/usr/bin/env python3
"""Bước C2 — minimal orchestrator: code gen + validate for one ticket."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SLICES = {
    "learn-003": {
        "requirements": "docs/requirements/learn-003-health-version.md",
        "generate_args": ["--template"],
        "validate_args": [],
    },
}


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), file=sys.stderr)
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False).returncode


def main() -> int:
    ticket = (sys.argv[1] if len(sys.argv) > 1 else "learn-003").lower()
    cfg = SLICES.get(ticket)
    if not cfg:
        print(f"Unknown ticket: {ticket}. Known: {', '.join(SLICES)}", file=sys.stderr)
        return 1

    py = sys.executable
    gen = REPO_ROOT / "tools/ai-code-gen/generate.py"
    val = REPO_ROOT / "tools/ai-code-gen/validate.py"
    req = REPO_ROOT / cfg["requirements"]

    if run([py, str(gen), "--requirements", str(req), *cfg["generate_args"]]) != 0:
        return 1
    if run([py, str(val), "--ticket", ticket, *cfg["validate_args"]]) != 0:
        return 1
    print(f"Orchestrator OK: {ticket}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
