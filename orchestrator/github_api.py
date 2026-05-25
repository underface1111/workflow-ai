"""GitHub REST helpers for Bước E (PR create + comment). Uses GITHUB_TOKEN."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


def _repo_slug() -> str:
    env = os.environ.get("GITHUB_REPOSITORY")
    if env:
        return env
    return "underface1111/workflow-ai"


def _request(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("Set GITHUB_TOKEN (or GH_TOKEN) for PR publish")

    url = f"https://api.github.com/repos/{_repo_slug()}{path}"
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {path} failed ({exc.code}): {detail}") from exc


def create_pull_request(
    *,
    title: str,
    head: str,
    base: str = "main",
    body: str,
    draft: bool = False,
) -> dict[str, Any]:
    return _request(
        "POST",
        "/pulls",
        {"title": title, "head": head, "base": base, "body": body, "draft": draft},
    )


def add_pr_comment(*, pr_number: int, body: str) -> dict[str, Any]:
    return _request("POST", f"/issues/{pr_number}/comments", {"body": body})


def find_open_pr_for_branch(head_branch: str, base: str = "main") -> dict[str, Any] | None:
    owner = _repo_slug().split("/")[0]
    pulls = _request("GET", f"/pulls?state=open&head={owner}:{head_branch}&base={base}")
    if isinstance(pulls, list) and pulls:
        return pulls[0]
    return None
