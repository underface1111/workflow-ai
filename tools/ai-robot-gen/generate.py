#!/usr/bin/env python3
"""AI Robot Agent (Bước D) — generate Robot suites from requirements.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from schemas import GeneratedRobotSuite, RobotAgentResponse

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REQUIREMENTS = REPO_ROOT / "docs/requirements/learn-004-health-version-e2e.md"
OUTPUT_DIR = REPO_ROOT / "tests/e2e-robot/suites/generated"


def read_requirements(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_ticket_id(content: str) -> str:
    match = re.search(r"Ticket ID\s*\|\s*([A-Z]+-\d+)", content, re.I)
    return match.group(1).lower() if match else "ticket-unknown"


def template_learn_004() -> GeneratedRobotSuite:
    content = """*** Settings ***
Documentation    AUTO-GENERATED — ticket learn-004
...              REVIEW REQUIRED before merge (Bước D)
...              API E2E: GET /health includes version (LEARN-003)
Resource           ../../resources/api_keywords.robot
Variables          ../../variables/env/local.yaml
Suite Setup        API Session Is Ready
Force Tags         generated    learn-004

*** Test Cases ***
Health Returns API Version
    [Tags]    generated    learn-004    smoke
    ${resp}=    GET On Session    app    /health    expected_status=200
    Should Be Equal As Strings    ${resp.json()}[status]    ok
    Should Be Equal As Strings    ${resp.json()}[service]    workflow-ai-poc
    Should Be Equal As Strings    ${resp.json()}[version]    0.2.0
"""
    return GeneratedRobotSuite(
        ticket_id="learn-004",
        file_name="learn-004-health-version.robot",
        file_content=content,
        summary="E2E assert /health returns version 0.2.0 (generated, not critical).",
    )


def write_output(generated: GeneratedRobotSuite, dry_run: bool) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / generated.file_name
    body = generated.file_content.strip() + "\n"

    if dry_run:
        print(body)
        return out_path

    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Robot Agent — Bước D")
    parser.add_argument("--requirements", type=Path, default=DEFAULT_REQUIREMENTS)
    parser.add_argument("--template", action="store_true", help="Built-in template (no API)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    req_path = args.requirements if args.requirements.is_absolute() else REPO_ROOT / args.requirements
    if not req_path.exists():
        print(f"Requirements not found: {req_path}", file=sys.stderr)
        return 1

    if not args.template:
        print("LLM mode not implemented yet; use --template (LEARN-004).", file=sys.stderr)
        return 1

    ticket = extract_ticket_id(read_requirements(req_path))
    if ticket != "learn-004":
        print(f"Warning: --template only supports learn-004; got {ticket}", file=sys.stderr)

    generated = template_learn_004()
    write_output(generated, args.dry_run)
    if not args.dry_run:
        print("Run: npm run ai:robot-validate", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
