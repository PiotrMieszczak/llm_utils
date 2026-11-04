#!/usr/bin/env python3
"""After a design or brainstorming session, require a check of existing ADRs.

Fires on Stop. If mark_design_session.py flagged this session as a design
session, this hook blocks the stop once and instructs the assistant to review
existing ADRs against whatever was just decided.

The point is not to nag about writing ADRs. It is to prevent the specific
failure where a session decides something that silently contradicts a decision
already recorded and accepted - producing two ADRs pointing opposite ways, with
nothing marking which one is current.

Behaviour:
  - Not a design session          -> exit 0, silent
  - Already prompted this session -> exit 0, silent (fires at most once)
  - Design session, first stop    -> exit 2, block with instructions

Exit 2 with stderr is the documented way for a Stop hook to hand control back
to the assistant. The marker is consumed before blocking, so a failure in the
follow-up turn cannot produce a loop.
"""

import json
import os
import sys
from pathlib import Path

MAX_LISTED = 25


def marker_path(session_id: str) -> Path:
    base = Path(
        os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")
    ) / "claude-adr-hook"
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")[:64] or "default"
    return base / f"{safe}.marker"


def find_adr_dir(root: Path) -> Path | None:
    for candidate in ("docs/adr", "docs/decisions", "doc/adr", "adr", "docs/architecture/decisions"):
        path = root / candidate
        if path.is_dir():
            return path
    return None


def summarize(adr_dir: Path) -> list[str]:
    """Return 'filename - status' lines for existing records."""
    lines: list[str] = []
    for path in sorted(adr_dir.glob("*.md")):
        if path.name.lower() in {"readme.md", "template.md", "index.md"}:
            continue
        status = "unknown"
        try:
            # Status lives in frontmatter near the top; read only what we need.
            with path.open(encoding="utf-8", errors="replace") as handle:
                for _ in range(15):
                    line = handle.readline()
                    if not line:
                        break
                    if line.lower().startswith("status:"):
                        status = line.split(":", 1)[1].strip().strip("\"'")
                        break
        except OSError:
            pass
        lines.append(f"  - {path.name} [{status}]")
        if len(lines) >= MAX_LISTED:
            lines.append(f"  - ... (showing first {MAX_LISTED})")
            break
    return lines


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    # Never re-block a stop that this hook already caused.
    if payload.get("stop_hook_active"):
        return 0

    session_id = str(payload.get("session_id", "default"))
    marker = marker_path(session_id)
    if not marker.exists():
        return 0

    # Consume the marker before blocking so this fires at most once per session.
    try:
        marker.unlink()
    except OSError:
        return 0

    root = Path(payload.get("cwd") or os.getcwd())
    adr_dir = find_adr_dir(root)

    if adr_dir is None:
        message = (
            "ADR check (design session detected).\n\n"
            "This project has no ADR directory. If the discussion just settled an "
            "architectural decision - a stack choice, a boundary, a storage engine, "
            "or a deliberate deferral - record it:\n\n"
            "  1. Invoke the `adr-from-brainstorm` skill.\n"
            "  2. It will create docs/adr/ with an index and write the record.\n\n"
            "If nothing architectural was decided, say so briefly and finish. "
            "Do not invent a decision to satisfy this check."
        )
    else:
        listing = summarize(adr_dir)
        existing = "\n".join(listing) if listing else "  (directory exists but is empty)"
        message = (
            f"ADR check (design session detected).\n\n"
            f"Existing records in {adr_dir}:\n{existing}\n\n"
            "Before finishing, verify against what was just decided:\n\n"
            "  1. Does any decision from this session CONTRADICT an accepted ADR?\n"
            "     If so, the new record must set `supersedes`, and the old one must be "
            "updated to `Superseded` with `superseded_by` set. Two accepted ADRs "
            "disagreeing is the failure this check exists to prevent.\n"
            "  2. Was a decision reached that is NOT yet recorded?\n"
            "     If so, invoke `adr-from-brainstorm` to write it.\n"
            "  3. Did this session make an existing ADR obsolete?\n"
            "     If so, update its status.\n\n"
            "Read the relevant records before answering - do not assume from filenames. "
            "If nothing architectural was decided, say so briefly and finish."
        )

    print(message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
