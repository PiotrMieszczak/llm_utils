#!/usr/bin/env python3
"""G4 living-spec check: warn when code is staged without its spec.

Fires on PreToolUse for Bash commands that look like `git commit`. If the staged
changes touch code covered by a spec, but no spec or ADR file is staged alongside,
emit a warning.

This is advisory, not blocking. Exit code 0 always: a heuristic that cannot know
whether a given change actually alters documented behaviour must not stop a
commit. It surfaces the question; the human answers it.

The rule it supports (workflow gate G4): when implementation reveals the spec was
wrong, the spec changes in the same commit as the code - not in a follow-up.
"""

import json
import re
import subprocess
import sys

CODE_SUFFIXES = (
    ".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte",
    ".go", ".rs", ".java", ".rb", ".kt", ".swift", ".cs",
)

DOC_MARKERS = ("docs/", "spec/", "adr/", "decisions/", ".md")

# Paths whose changes rarely alter documented behaviour.
NOISE = re.compile(
    r"(^|/)(tests?|__tests__|spec|e2e|fixtures?|mocks?|\.storybook|"
    r"migrations?|node_modules|dist|build)(/|$)"
)


def staged_files() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    command = str((payload.get("tool_input") or {}).get("command", ""))
    # Only real commits; ignore --amend (spec may already be in the commit)
    # and anything that merely mentions the word.
    if not re.search(r"\bgit\s+(-[^\s]+\s+)*commit\b", command):
        return 0
    if "--amend" in command:
        return 0

    files = staged_files()
    if not files:
        return 0

    code = [
        f for f in files
        if f.endswith(CODE_SUFFIXES) and not NOISE.search(f)
    ]
    docs = [f for f in files if any(m in f for m in DOC_MARKERS)]

    if code and not docs:
        preview = ", ".join(code[:4]) + (f" (+{len(code) - 4} more)" if len(code) > 4 else "")
        print(
            "G4 living-spec check\n"
            f"  Staged code with no doc or ADR change: {preview}\n"
            "  If this alters documented behaviour, update the spec in THIS commit.\n"
            "  If it encodes an architectural decision, write an ADR now.\n"
            "  If neither applies, continue - this is advisory only.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
