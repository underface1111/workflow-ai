#!/usr/bin/env python3
"""Validate AI-generated Robot suites (Bước D)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from pydantic import ValidationError

from schemas import GeneratedRobotSuite

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = REPO_ROOT / "tests/e2e-robot/suites/generated"


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix != ".robot":
        errors.append(f"{path.name}: must be *.robot")
        return errors

    content = path.read_text(encoding="utf-8")
    if "AUTO-GENERATED" not in content:
        errors.append(f"{path.name}: missing AUTO-GENERATED header")
    if "REVIEW REQUIRED" not in content:
        errors.append(f"{path.name}: missing REVIEW REQUIRED (D3)")

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("Force Tags") and re.search(r"\bcritical\b", stripped, re.I):
            errors.append(f"{path.name}: generated suite must not use Force Tag critical")

    ticket = "learn-004"
    for line in content.splitlines():
        if "ticket learn-" in line.lower():
            m = re.search(r"learn-\d+", line, re.I)
            if m:
                ticket = m.group(0).lower()

    try:
        GeneratedRobotSuite(
            ticket_id=ticket,
            file_name=path.name,
            file_content=content,
            summary="validated from file",
        )
    except ValidationError as exc:
        errors.append(f"{path.name}: schema — {exc}")

    return errors


def collect_files() -> list[Path]:
    if not GENERATED_DIR.exists():
        return []
    return sorted(GENERATED_DIR.glob("*.robot"))


def run_robot_generated() -> int:
    print("Running robot --include generated ...", file=sys.stderr)
    return subprocess.run(
        [
            "robot",
            "--outputdir",
            "robot-results-generated",
            "--include",
            "generated",
            "tests/e2e-robot/suites/generated",
        ],
        cwd=REPO_ROOT,
        shell=True,
        check=False,
    ).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated Robot suites")
    parser.add_argument("--skip-robot", action="store_true", help="Structure only")
    args = parser.parse_args()

    files = collect_files()
    if not files:
        print("No generated suites (tests/e2e-robot/suites/generated/*.robot).")
        return 0

    all_errors: list[str] = []
    for path in files:
        errs = validate_file(path)
        all_errors.extend(errs)
        if not errs:
            print(f"OK  {path.relative_to(REPO_ROOT)}")

    if all_errors:
        print("\nValidation failed:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.skip_robot:
        print("Structural validation passed.")
        return 0

    code = run_robot_generated()
    if code != 0:
        print("robot run failed (is API running on :3000?).", file=sys.stderr)
        return code
    print("Validation passed (structure + robot generated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
