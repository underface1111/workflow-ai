#!/usr/bin/env python3
"""
Bước E — Release pipeline: test → self-heal (max 3) → open PR → mentor comment.

Does NOT auto-merge. Requires branch pushed to origin for PR create on GitHub.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = REPO_ROOT / "orchestrator/out"
MAX_HEAL_ATTEMPTS = 3


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), file=sys.stderr)
    return subprocess.run(cmd, cwd=REPO_ROOT, shell=True, check=False).returncode


def npm_test() -> int:
    return run(["npm", "test"])


def build_pr_body(ticket: str, branch: str, attempts: int) -> str:
    return f"""## Summary
Automated release pipeline (Bước E) for **{ticket.upper()}**.

- Branch: `{branch}`
- Self-heal attempts: {attempts}
- **Human review required** — do not auto-merge.

## Test plan
- [ ] CI `build-test-sonar` green
- [ ] CI `e2e-robot` green
- [ ] SonarCloud Quality Gate on new code
- [ ] Peer approval

## Orchestrator
`orchestrator/run_release_pipeline.py` — template remediations only (LLM optional later).
"""


def mentor_comment(ticket: str, mentor: str) -> str:
    return (
        f"@{mentor} — Release pipeline (Bước E) opened PR for **{ticket.upper()}**.\n\n"
        "Please review when CI is green. **No auto-merge** per POC policy."
    )


def write_metrics(payload: dict) -> Path:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = METRICS_DIR / f"metrics-{payload.get('ticket', 'ticket')}-{ts}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Metrics: {path.relative_to(REPO_ROOT)}", file=sys.stderr)
    return path


def publish_pr(
    *,
    title: str,
    head: str,
    ticket: str,
    body: str,
    mentor: str,
    dry_run: bool,
) -> dict | None:
    if dry_run:
        print(f"[dry-run] PR: {title}\n  head={head}\n  comment @{mentor}", file=sys.stderr)
        return {"html_url": "(dry-run)", "number": 0}

    from github_api import add_pr_comment, create_pull_request, find_open_pr_for_branch

    existing = find_open_pr_for_branch(head)
    if existing:
        pr = existing
        print(f"Using existing PR #{pr['number']}", file=sys.stderr)
    else:
        pr = create_pull_request(title=title, head=head, body=body, draft=False)

    add_pr_comment(pr_number=int(pr["number"]), body=mentor_comment(ticket, mentor))
    return pr


def main() -> int:
    parser = argparse.ArgumentParser(description="Bước E release pipeline")
    parser.add_argument("--ticket", default="learn-005", help="Ticket id for PR title/body")
    parser.add_argument("--branch", required=True, help="Feature branch name (must exist on origin)")
    parser.add_argument("--title", default="", help="PR title override")
    parser.add_argument("--mentor", default=os.environ.get("MENTOR_GITHUB_LOGIN", "mentor"))
    parser.add_argument("--max-heal", type=int, default=MAX_HEAL_ATTEMPTS)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-pr", action="store_true", help="Only test + self-heal")
    args = parser.parse_args()

    started = datetime.now(timezone.utc).isoformat()
    title = args.title or f"feat({args.ticket}): release pipeline slice (Bước E)"

    if run(["npm", "ci"]) != 0 and not args.dry_run:
        print("npm ci failed", file=sys.stderr)
        return 1

    sys.path.insert(0, str(REPO_ROOT / "orchestrator"))
    from self_heal import self_heal_once

    passed = False
    heal_count = 0
    test_attempts = 0
    for _ in range(args.max_heal + 1):
        test_attempts += 1
        if npm_test() == 0:
            passed = True
            print(f"Tests passed (attempt {test_attempts})", file=sys.stderr)
            break
        if heal_count >= args.max_heal:
            break
        applied, fix_id = self_heal_once()
        if not applied:
            print("No template remediation matched JUnit/Sonar hints.", file=sys.stderr)
            break
        heal_count += 1
        print(f"Self-heal applied: {fix_id} (heal {heal_count}/{args.max_heal})", file=sys.stderr)
        time.sleep(0.5)

    if not passed:
        print("Tests still failing after self-heal limit.", file=sys.stderr)
        write_metrics(
            {
                "ticket": args.ticket,
                "branch": args.branch,
                "started_at": started,
                "ended_at": datetime.now(timezone.utc).isoformat(),
                "status": "failed",
                "heal_attempts": heal_count,
                "test_attempts": test_attempts,
            }
        )
        return 1

    pr_url = None
    pr_number = None
    if not args.skip_pr:
        body = build_pr_body(args.ticket, args.branch, heal_count)
        try:
            pr = publish_pr(
                title=title,
                head=args.branch,
                ticket=args.ticket,
                body=body,
                mentor=args.mentor,
                dry_run=args.dry_run,
            )
            if pr:
                pr_url = pr.get("html_url")
                pr_number = pr.get("number")
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            print("Hint: push branch to origin and set GITHUB_TOKEN.", file=sys.stderr)
            if not args.dry_run:
                return 1

    write_metrics(
        {
            "ticket": args.ticket,
            "branch": args.branch,
            "started_at": started,
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "status": "ready_for_review",
            "heal_attempts": heal_count,
            "pr_url": pr_url,
            "pr_number": pr_number,
        }
    )

    print("Release pipeline OK — PR ready for human review (no auto-merge).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
