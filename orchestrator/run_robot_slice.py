#!/usr/bin/env python3
"""Bước D — orchestrator: robot gen + validate for one ticket."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SLICES = {
    "learn-004": {
        "requirements": "docs/requirements/learn-004-health-version-e2e.md",
        "validate_skip_robot": False,
    },
}


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), file=sys.stderr)
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False).returncode


def main() -> int:
    ticket = (sys.argv[1] if len(sys.argv) > 1 else "learn-004").lower()
    cfg = SLICES.get(ticket)
    if not cfg:
        print(f"Unknown ticket: {ticket}. Known: {', '.join(SLICES)}", file=sys.stderr)
        return 1

    py = sys.executable
    gen = REPO_ROOT / "tools/ai-robot-gen/generate.py"
    val = REPO_ROOT / "tools/ai-robot-gen/validate.py"
    req = REPO_ROOT / cfg["requirements"]

    if run([py, str(gen), "--requirements", str(req), "--template"]) != 0:
        return 1

    val_args = [py, str(val)]
    if cfg.get("validate_skip_robot"):
        val_args.append("--skip-robot")
    if run(val_args) != 0:
        return 1

    print(f"Orchestrator OK: {ticket} (robot)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
