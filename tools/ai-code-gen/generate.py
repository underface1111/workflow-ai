#!/usr/bin/env python3
"""
AI Code Agent (Bước C) — apply code changes from requirements.md.

Usage:
  python tools/ai-code-gen/generate.py --requirements docs/requirements/learn-003-health-version.md --template
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from schemas import CodeAgentResponse, GeneratedSourceFile

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REQUIREMENTS = REPO_ROOT / "docs/requirements/learn-003-health-version.md"

HEALTH_JSON_OLD = "res.json({ status: 'ok', service: 'workflow-ai-poc' });"
HEALTH_JSON_NEW = "res.json({ status: 'ok', service: 'workflow-ai-poc', version: '0.2.0' });"


def read_requirements(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_ticket_id(content: str) -> str:
    match = re.search(r"Ticket ID\s*\|\s*([A-Z]+-\d+)", content, re.I)
    return match.group(1).lower() if match else "ticket-unknown"


def _read_repo_file(relative: str) -> str:
    path = REPO_ROOT / relative
    return path.read_text(encoding="utf-8")


def template_learn_003() -> CodeAgentResponse:
    """Deterministic LEARN-003: add version to /health + update tests."""
    app_path = "src/app.js"
    app_content = _read_repo_file(app_path)
    if HEALTH_JSON_NEW in app_content:
        print("LEARN-003 already applied in src/app.js", file=sys.stderr)
    elif HEALTH_JSON_OLD not in app_content:
        raise SystemExit("src/app.js: expected health handler snippet not found")
    else:
        app_content = app_content.replace(HEALTH_JSON_OLD, HEALTH_JSON_NEW, 1)

    unit_path = "tests/unit/app.test.js"
    unit_content = _read_repo_file(unit_path)
    if "res.body.version" not in unit_content:
        unit_content = unit_content.replace(
            "      expect(res.body.status).toBe('ok');\n    });",
            "      expect(res.body.status).toBe('ok');\n"
            "      expect(res.body.version).toBe('0.2.0');\n    });",
            1,
        )

    gen_path = "tests/unit/generated/learn-002-health.test.js"
    gen_content = _read_repo_file(gen_path)
    if "res.body.version" not in gen_content:
        gen_content = gen_content.replace(
            "    expect(res.body.service).toBe('workflow-ai-poc');\n  });",
            "    expect(res.body.service).toBe('workflow-ai-poc');\n"
            "    expect(res.body.version).toBe('0.2.0');\n  });",
            1,
        )

    ticket = "learn-003"
    files = [
        GeneratedSourceFile(
            ticket_id=ticket,
            relative_path=app_path,
            file_content=app_content,
            summary="Add version 0.2.0 to GET /health response.",
        ),
        GeneratedSourceFile(
            ticket_id=ticket,
            relative_path=unit_path,
            file_content=unit_content,
            summary="Assert health version in app.test.js.",
        ),
        GeneratedSourceFile(
            ticket_id=ticket,
            relative_path=gen_path,
            file_content=gen_content,
            summary="Align generated LEARN-002 test with new health shape.",
        ),
    ]
    return CodeAgentResponse(output_format="json_schema_v1", files=files)


def write_files(response: CodeAgentResponse, dry_run: bool) -> None:
    for item in response.files:
        out = REPO_ROOT / item.relative_path
        if dry_run:
            print(f"--- {item.relative_path} ({item.summary}) ---")
            print(item.file_content[:500] + ("..." if len(item.file_content) > 500 else ""))
            continue
        out.write_text(item.file_content, encoding="utf-8")
        print(f"Wrote {item.relative_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Code Agent — Bước C")
    parser.add_argument("--requirements", type=Path, default=DEFAULT_REQUIREMENTS)
    parser.add_argument("--template", action="store_true", help="Built-in template (no API)")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes only")
    args = parser.parse_args()

    req_path = args.requirements if args.requirements.is_absolute() else REPO_ROOT / args.requirements
    if not req_path.exists():
        print(f"Requirements not found: {req_path}", file=sys.stderr)
        return 1

    requirements = read_requirements(req_path)

    if not args.template:
        print("LLM mode not implemented yet; use --template (LEARN-003).", file=sys.stderr)
        return 1

    ticket = extract_ticket_id(requirements)
    if ticket != "learn-003":
        print(f"Warning: --template only supports learn-003; got {ticket}", file=sys.stderr)

    response = template_learn_003()
    write_files(response, args.dry_run)
    if not args.dry_run:
        print("Run: npm run ai:code-validate", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
