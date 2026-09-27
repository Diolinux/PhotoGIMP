#!/usr/bin/env python3
"""Detect high-risk automation and agent-instruction patterns."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

AUTOMATION_ROOTS = (".github/", "scripts/", ".config/GIMP/3.0/plug-ins/")
AGENT_NAMES = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "COPILOT.md"}
SELF = "scripts/security_scan.py"
FORBIDDEN_BINARY_SUFFIXES = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".msi", ".dmg", ".pkg",
    ".deb", ".rpm", ".appimage", ".jar", ".class", ".wasm", ".pyc",
    ".pyo", ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2",
    ".tbz2", ".xz", ".txz",
}
PROMPT_PATTERNS = re.compile(
    r"ignore\s+(all\s+)?previous\s+instructions|"
    r"reveal\s+(the\s+)?(system\s+prompt|secrets?|tokens?)|"
    r"disable\s+(security|safety)\s+(checks?|controls?)|"
    r"override\s+(system|developer)\s+instructions?",
    re.IGNORECASE,
)
DANGEROUS_PATTERNS = re.compile(
    r"curl\b[^\n|]*\|\s*(?:ba)?sh\b|"
    r"wget\b[^\n|]*\|\s*(?:ba)?sh\b|"
    r"\beval\s+[\"']?\$|"
    r"\b(?:eval|exec)\s*\(|"
    r"permissions:\s*write-all",
    re.IGNORECASE,
)


def tracked_files() -> list[str]:
    return subprocess.check_output(["git", "ls-files"], text=True).splitlines()


def scan() -> list[str]:
    findings: list[str] = []
    for name in tracked_files():
        path = Path(name)
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES or ".so." in path.name.lower():
            findings.append(f"{name}: tracked binary or packaged artifact is not allowed")
            continue
        if name == SELF or not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        is_agent_content = path.name in AGENT_NAMES
        is_automation = name.startswith(AUTOMATION_ROOTS)
        if not (is_agent_content or is_automation):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            unsafe_prompt = is_agent_content and PROMPT_PATTERNS.search(line)
            unsafe_automation = is_automation and DANGEROUS_PATTERNS.search(line)
            if unsafe_prompt or unsafe_automation:
                findings.append(f"{name}:{line_number}: {line.strip()}")
    return findings


def main() -> None:
    findings = scan()
    if findings:
        print("Potentially unsafe automation or agent content detected:", file=sys.stderr)
        print("\n".join(findings), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
