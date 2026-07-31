#!/usr/bin/env python3
"""Mark that a design or brainstorming skill ran in this session.

Fires on PostToolUse for the Skill tool. When the invoked skill is one that
produces architectural decisions, drop a marker file. The Stop hook reads that
marker to decide whether an ADR check is warranted.

Splitting detection (here) from prompting (check_adrs.py) keeps the Stop hook
cheap: it does a single file existence check on turns where nothing happened.

Always exits 0. A hook that blocks work is worse than a missed reminder.
"""

import json
import os
import sys
from pathlib import Path

# Skills whose output is typically a decision worth recording.
DESIGN_SKILLS = (
    "brainstorm",
    "brainstorming",
    "writing-plans",
    "speckit.plan",
    "speckit.specify",
    "speckit-superpowers.plan",
    "speckit-superpowers.specify",
    "adr-from-brainstorm",
)


def marker_path(session_id: str) -> Path:
    base = Path(
        os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")
    ) / "claude-adr-hook"
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")[:64] or "default"
    return base / f"{safe}.marker"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input") or {}
    skill_name = str(tool_input.get("skill", "")).lower()
    if not skill_name:
        return 0

    if not any(marker in skill_name for marker in DESIGN_SKILLS):
        return 0

    session_id = str(payload.get("session_id", "default"))
    path = marker_path(session_id)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(skill_name, encoding="utf-8")
    except OSError:
        # A marker we cannot write simply means no reminder. Never fail the turn.
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
