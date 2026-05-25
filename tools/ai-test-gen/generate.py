#!/usr/bin/env python3
"""
AI Test Agent (Bước B) — generate Jest unit tests from requirements.md.

Usage:
  python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md --template
  python tools/ai-test-gen/generate.py --requirements docs/requirements/example-feature.md  # needs OPENAI_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from schemas import AgentResponse, GeneratedUnitTest

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REQUIREMENTS = REPO_ROOT / "docs/requirements/example-feature.md"
OUTPUT_DIR = REPO_ROOT / "tests/unit/generated"


def read_requirements(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_ticket_id(content: str) -> str:
    match = re.search(r"Ticket ID\s*\|\s*([A-Z]+-\d+)", content, re.I)
    return match.group(1).lower() if match else "ticket-unknown"


def template_for_learn_001() -> GeneratedUnitTest:
    """Deterministic output for example-feature (no API). Review before commit."""
    content = """const request = require('supertest');
const app = require('../../../src/app');

describe('GET / (LEARN-001)', () => {
  it('returns service info without auth', async () => {
    const res = await request(app).get('/');
    expect(res.status).toBe(200);
    expect(res.body.message).toBe('workflow-ai-poc');
    expect(res.body.docs).toBe('/health');
  });
});
"""
    return GeneratedUnitTest(
        ticket_id="learn-001",
        file_name="learn-001-root.test.js",
        file_content=content,
        summary="Happy path for GET / root info endpoint.",
    )


def build_prompt(requirements: str) -> str:
    app_snippet = (REPO_ROOT / "src/app.js").read_text(encoding="utf-8")[:4000]
    example = (REPO_ROOT / "tests/unit/app.test.js").read_text(encoding="utf-8")[:3000]
    return f"""You are AI Test Agent for a Node.js Express POC.
Generate ONE Jest unit test file using supertest. CommonJS only. No extra dependencies.

REQUIREMENTS:
{requirements}

EXISTING APP (reference):
```javascript
{app_snippet}
```

STYLE EXAMPLE:
```javascript
{example}
```

Respond with JSON only matching this shape:
{{
  "output_format": "json_schema_v1",
  "generated_test": {{
    "ticket_id": "<from requirements>",
    "file_name": "<kebab-case>.test.js",
    "file_content": "<full file source>",
    "summary": "<one line>"
  }}
}}
"""


def call_openai(prompt: str) -> AgentResponse:
    try:
        from openai import OpenAI
    except ImportError as e:
        raise SystemExit("Install deps: pip install -r tools/ai-test-gen/requirements.txt") from e

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY not set. Use --template or add key to .env")

    client = OpenAI(api_key=api_key)
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You output only valid JSON for test generation."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)
    return AgentResponse.model_validate(data)


def write_output(generated: GeneratedUnitTest, dry_run: bool) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / generated.file_name
    header = f"// AUTO-GENERATED — ticket {generated.ticket_id}\n// REVIEW REQUIRED before merge (Bước B)\n\n"
    body = header + generated.file_content.strip() + "\n"

    if dry_run:
        print(body)
        return out_path

    out_path.write_text(body, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Test Agent — Bước B")
    parser.add_argument(
        "--requirements",
        type=Path,
        default=DEFAULT_REQUIREMENTS,
        help="Path to requirements markdown",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Use built-in template (no API) for LEARN-001 / example-feature",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print file to stdout, do not write",
    )
    args = parser.parse_args()

    req_path = args.requirements if args.requirements.is_absolute() else REPO_ROOT / args.requirements
    if not req_path.exists():
        print(f"Requirements not found: {req_path}", file=sys.stderr)
        return 1

    requirements = read_requirements(req_path)

    if args.template:
        if extract_ticket_id(requirements) != "learn-001":
            print("Warning: --template only ships LEARN-001; using that template.", file=sys.stderr)
        generated = template_for_learn_001()
        write_output(generated, args.dry_run)
        return 0

    if not os.environ.get("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY or use --template for example-feature.md", file=sys.stderr)
        return 1

    prompt = build_prompt(requirements)
    agent = call_openai(prompt)
    write_output(agent.generated_test, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
