#!/usr/bin/env python3
"""Port Claude Code skills to Codex, Copilot, or Gemini format.

Handles the mechanical part: frontmatter reshaping, directory layout, and the
argument-syntax rewrites that are pure substitution. Everything judgement-shaped
is reported as a warning for a human to resolve - this script never pretends a
lossy conversion was clean.

Usage:
    port_skill.py --to codex   SKILL.md [SKILL.md ...] --out DIR
    port_skill.py --to copilot SKILL.md [...]          --out DIR
    port_skill.py --to gemini  SKILL.md [...]          --out DIR
    port_skill.py --check      SKILL.md [...]

No third-party dependencies: the frontmatter subset used by skills is simple
enough to parse directly, and requiring PyYAML would make the script harder to
run than the task warrants.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Fields Claude Code actually reads. Everything else in frontmatter is ignored
# by the loader (see docs/model-routing.md).
CLAUDE_FIELDS = {"name", "description", "allowed-tools", "disable-model-invocation"}

# Features with no equivalent on the target platform.
LOSSES = {
    "codex": {"allowed-tools": "Codex configures tools per agent, not per skill."},
    "copilot": {
        "allowed-tools": "Copilot has no per-skill tool restriction.",
        "disable-model-invocation": (
            "Copilot cannot mark a skill slash-only; it becomes automatically "
            "triggerable."
        ),
    },
    "gemini": {
        "allowed-tools": "No equivalent.",
        "disable-model-invocation": "No equivalent; GEMINI.md is always loaded.",
        "description": (
            "Gemini does not match descriptions - converted to an explicit "
            "'When to use' line."
        ),
    },
}


def parse_skill(path: Path) -> tuple[dict[str, str], str]:
    """Split a SKILL.md into (frontmatter dict, body)."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: no YAML frontmatter found")

    raw, body = match.group(1), match.group(2)
    meta: dict[str, str] = {}
    key = None
    for line in raw.split("\n"):
        field = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if field:
            key = field.group(1)
            meta[key] = field.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            meta[key] += " " + line.strip()          # folded continuation
    return meta, body.lstrip("\n")


def title_case(slug: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_]", slug))


def lead_clause(description: str) -> str:
    """First sentence before the trigger clause - Codex wants a picker label."""
    return re.split(r"\s+Use (when|whenever|before)\b", description, 1)[0].strip().rstrip(".")


def trigger_clause(description: str) -> str:
    """The 'Use when ...' half, for platforms that do not match descriptions."""
    parts = re.split(r"\s+(?=Use (?:when|whenever|before)\b)", description, 1)
    return parts[1].strip() if len(parts) > 1 else ""


def warn(name: str, target: str, meta: dict[str, str]) -> list[str]:
    out = [
        f"    lost: {field} - {why}"
        for field, why in LOSSES.get(target, {}).items()
        if field in meta
    ]
    if target == "claude" and "${input:" in name:
        out.append("    rewrite: ${input:...} has no Claude equivalent")
    return out


def to_codex(meta: dict, body: str, out: Path) -> list[str]:
    d = out / meta["name"]
    (d / "agents").mkdir(parents=True, exist_ok=True)

    front = "\n".join(f"{k}: {meta[k]}" for k in ("name", "description") if k in meta)
    (d / "SKILL.md").write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")

    (d / "agents" / "openai.yaml").write_text(
        "interface:\n"
        f'  display_name: "{title_case(meta["name"])}"\n'
        f'  short_description: "{lead_clause(meta.get("description", ""))}"\n',
        encoding="utf-8",
    )
    return warn(meta["name"], "codex", meta)


def to_copilot(meta: dict, body: str, out: Path) -> list[str]:
    d = out / meta["name"]
    d.mkdir(parents=True, exist_ok=True)

    # Copilot uses typed inputs rather than a single argument string.
    converted = body.replace("$ARGUMENTS", "${input:Arguments}")

    front = f'name: {meta["name"]}\ndescription: \'{meta.get("description", "")}\''
    (d / "SKILL.md").write_text(f"---\n{front}\n---\n\n{converted}", encoding="utf-8")

    notes = warn(meta["name"], "copilot", meta)
    if "$ARGUMENTS" in body:
        notes.append("    rewrote: $ARGUMENTS -> ${input:Arguments} (review the name)")
    return notes


def to_gemini(skills: list[tuple[dict, str]], out: Path) -> list[str]:
    """Gemini has no discrete skills - concatenate into one always-loaded file."""
    out.mkdir(parents=True, exist_ok=True)
    parts = [
        "# Project Context\n",
        "> Ported from Claude Code skills. This file is loaded on every turn, so it "
        "should hold only skills that apply broadly to this repository.\n",
    ]
    for meta, body in skills:
        parts.append(f"\n## Skill: {title_case(meta['name'])}\n")
        if trig := trigger_clause(meta.get("description", "")):
            parts.append(f"\n**When to use:** {trig}\n")
        parts.append(f"\n{body.strip()}\n")

    (out / "GEMINI.md").write_text("\n".join(parts), encoding="utf-8")

    total = sum(len(b) for _, b in skills)
    notes = [f"    NOTE: GEMINI.md is always loaded (~{total // 4} tokens every turn)"]
    if len(skills) > 3:
        notes.append(f"    WARN: {len(skills)} skills concatenated - port only broad ones")
    return notes


def check(meta: dict, path: Path) -> list[str]:
    """Validate a skill against Claude Code's real field set."""
    problems = []
    if "name" not in meta:
        problems.append("missing required field: name")
    elif meta["name"] != path.parent.name:
        problems.append(f"name '{meta['name']}' != directory '{path.parent.name}'")

    desc = meta.get("description", "")
    if not desc:
        problems.append("missing required field: description")
    else:
        if not re.search(r"\bUse (when|whenever|before)\b", desc, re.I):
            problems.append("description has no trigger clause ('Use when ...')")
        if len(desc) > 500:
            problems.append(f"description is {len(desc)} chars - likely too long")

    unknown = set(meta) - CLAUDE_FIELDS - {"model-hint"}
    if unknown:
        problems.append(f"fields Claude Code ignores: {', '.join(sorted(unknown))}")

    # Only flag ${input:...} outside code blocks - a skill may legitimately
    # document the syntax as an example (this one does).
    prose = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    prose = re.sub(r"`[^`]*`", "", prose)
    if "${input:" in prose:
        problems.append("contains ${input:...} - Copilot syntax, not substituted here")

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skills", nargs="+", type=Path)
    ap.add_argument("--to", choices=["codex", "copilot", "gemini"])
    ap.add_argument("--out", type=Path, default=Path("./ported"))
    ap.add_argument("--check", action="store_true", help="validate only, do not convert")
    args = ap.parse_args()

    if not args.check and not args.to:
        ap.error("one of --to or --check is required")

    parsed, failed = [], 0
    for path in args.skills:
        try:
            parsed.append((path, *parse_skill(path)))
        except (ValueError, OSError) as exc:
            print(f"  SKIP {path}: {exc}", file=sys.stderr)
            failed += 1

    if args.check:
        for path, meta, _ in parsed:
            problems = check(meta, path)
            status = "ok" if not problems else "PROBLEMS"
            print(f"  {meta.get('name', path.name):<28} {status}")
            for p in problems:
                print(f"    - {p}")
            failed += bool(problems)
        print(f"\n{len(parsed)} checked, {failed} with problems")
        return 1 if failed else 0

    if args.to == "gemini":
        for note in to_gemini([(m, b) for _, m, b in parsed], args.out):
            print(note)
        print(f"\nwrote {args.out / 'GEMINI.md'} from {len(parsed)} skills")
        return 0

    convert = {"codex": to_codex, "copilot": to_copilot}[args.to]
    for _, meta, body in parsed:
        print(f"  {meta['name']} -> {args.to}")
        for note in convert(meta, body, args.out):
            print(note)
    print(f"\nwrote {len(parsed)} skills to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
