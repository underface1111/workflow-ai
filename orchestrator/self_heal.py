"""Bước E3 — self-heal from JUnit (and optional Sonar hints), max N attempts."""

from __future__ import annotations

import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
JUNIT_PATH = REPO_ROOT / "coverage/junit.xml"
SONAR_HINTS = REPO_ROOT / "orchestrator/in/sonar-hints.json"


@dataclass
class TestFailure:
    test_name: str
    message: str
    suite: str


def parse_junit(path: Path = JUNIT_PATH) -> list[TestFailure]:
    if not path.exists():
        return []
    failures: list[TestFailure] = []
    root = ET.parse(path).getroot()
    for case in root.iter("testcase"):
        fail = case.find("failure")
        if fail is None:
            continue
        failures.append(
            TestFailure(
                test_name=case.get("name", ""),
                message=(fail.get("message") or fail.text or "").strip(),
                suite=case.get("classname", ""),
            )
        )
    return failures


def load_sonar_hints() -> list[str]:
    if not SONAR_HINTS.exists():
        return []
    import json

    data = json.loads(SONAR_HINTS.read_text(encoding="utf-8"))
    return [str(x) for x in data.get("hints", [])]


def run_cmd(cmd: list[str]) -> int:
    print("+", " ".join(cmd), file=sys.stderr)
    return subprocess.run(cmd, cwd=REPO_ROOT, shell=False, check=False).returncode


def apply_remediation(failures: list[TestFailure], sonar_hints: list[str]) -> str | None:
    """Return remediation id if a template fix was applied."""
    text = " ".join(f.message.lower() for f in failures) + " " + " ".join(sonar_hints).lower()
    version_failure = any(
        "version" in f.message.lower() or "0.2.0" in f.message for f in failures
    ) or "version" in text

    if version_failure:
        py = sys.executable
        gen = REPO_ROOT / "tools/ai-code-gen/generate.py"
        req = REPO_ROOT / "docs/requirements/learn-003-health-version.md"
        if run_cmd([py, str(gen), "--requirements", str(req), "--template"]) == 0:
            return "apply_learn_003_health_version"

    if "learn-004" in text and "robot" in text:
        py = sys.executable
        gen = REPO_ROOT / "tools/ai-robot-gen/generate.py"
        req = REPO_ROOT / "docs/requirements/learn-004-health-version-e2e.md"
        if run_cmd([py, str(gen), "--requirements", str(req), "--template"]) == 0:
            return "regenerate_learn_004_robot"

    return None


def self_heal_once() -> tuple[bool, str | None]:
    failures = parse_junit()
    sonar_hints = load_sonar_hints()
    if not failures and not sonar_hints:
        return False, None
    fix_id = apply_remediation(failures, sonar_hints)
    return fix_id is not None, fix_id
