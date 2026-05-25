#!/usr/bin/env python3
"""
Validate AI-generated unit tests (Bước B4).

Structural checks (no API). Optional npm test. LLM generation is separate (generate.py).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from pydantic import ValidationError

from schemas import GeneratedUnitTest

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = REPO_ROOT / "tests/unit/generated"
HEADER_TICKET_RE = re.compile(r"//\s*AUTO-GENERATED\s*—\s*ticket\s+(\S+)", re.I)


def strip_generated_header(content: str) -> str:
    lines = content.splitlines()
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("//"):
            continue
        body_start = i
        break
    return "\n".join(lines[body_start:]).strip() + "\n"


def extract_ticket_id(content: str) -> str:
    for line in content.splitlines():
        match = HEADER_TICKET_RE.search(line)
        if match:
            return match.group(1).lower()
    return "unknown"


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix != ".js" or not path.name.endswith(".test.js"):
        errors.append(f"{path.name}: must be *.test.js")
        return errors

    content = path.read_text(encoding="utf-8")
    if "AUTO-GENERATED" not in content:
        errors.append(f"{path.name}: missing AUTO-GENERATED header")
    if "REVIEW REQUIRED" not in content:
        errors.append(f"{path.name}: missing REVIEW REQUIRED marker (B5)")

    body = strip_generated_header(content)
    ticket_id = extract_ticket_id(content)

    try:
        GeneratedUnitTest(
            ticket_id=ticket_id,
            file_name=path.name,
            file_content=body,
            summary="validated from file",
        )
    except ValidationError as exc:
        errors.append(f"{path.name}: schema validation failed — {exc}")

    return errors


def collect_generated_files() -> list[Path]:
    if not GENERATED_DIR.exists():
        return []
    return sorted(GENERATED_DIR.glob("*.test.js"))


def run_npm_test() -> int:
    print("Running npm test...", file=sys.stderr)
    result = subprocess.run(
        ["npm", "test"],
        cwd=REPO_ROOT,
        shell=True,
        check=False,
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated unit tests (no API)")
    parser.add_argument(
        "--skip-npm",
        action="store_true",
        help="Only structural validation, do not run npm test",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Validate a single file instead of all in tests/unit/generated/",
    )
    args = parser.parse_args()

    files = [args.file] if args.file else collect_generated_files()
    if not files:
        print("No generated tests found (tests/unit/generated/*.test.js). OK if none expected.")
        return 0

    all_errors: list[str] = []
    for path in files:
        resolved = path if path.is_absolute() else REPO_ROOT / path
        if not resolved.exists():
            all_errors.append(f"File not found: {resolved}")
            continue
        file_errors = validate_file(resolved)
        all_errors.extend(file_errors)
        if not file_errors:
            print(f"OK  {resolved.relative_to(REPO_ROOT)}")

    if all_errors:
        print("\nValidation failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if args.skip_npm:
        print("Structural validation passed.")
        return 0

    code = run_npm_test()
    if code != 0:
        print("npm test failed.", file=sys.stderr)
        return code

    print("Validation passed (structure + npm test).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
