#!/usr/bin/env python3
"""Audit agent-facing documentation for cost and correctness problems.

Checks CLAUDE.md files, topic docs, and skill frontmatter. Reports what is
mechanically detectable; judgement calls (is this rule still true? is this
content worth its tokens?) are left to a human or to the auditing-agent-docs
skill.

Usage:
    audit_claude_md.py [ROOT]           # audit a project tree
    audit_claude_md.py --skills [ROOT]  # skill frontmatter only

Exit code is 1 when correctness problems are found, 0 otherwise. Cost findings
do not fail the run - they are advisory.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

# Fields Claude Code actually reads from SKILL.md frontmatter.
VALID_SKILL_FIELDS = {"name", "description", "allowed-tools", "disable-model-invocation"}
# Marketplace convention, documented and consumed by skill-porting.
TOLERATED_SKILL_FIELDS = {"model-hint"}

BOILERPLATE = [
    (r"provides guidance to Claude Code", "generic preamble - Claude knows what it reads"),
    (r"claude\.ai/code", "link to Claude docs, not project knowledge"),
    (r"\bfollow best practices\b", "unactionable generic advice"),
    (r"\bwrite clean,? (?:readable )?code\b", "unactionable generic advice"),
    (r"\bmake sure to test\b", "unactionable generic advice"),
    (r"You are (?:an? )?(?:expert|helpful)", "persona preamble - not project knowledge"),
]

SIZE_BANDS = [(100, "good"), (400, "acceptable if mostly a routing table"),
              (800, "bloated - restructure"), (10**9, "likely unread in practice")]


def walk(root: Path, pattern: str):
    for p in root.rglob(pattern):
        if not any(part in SKIP_DIRS for part in p.parts):
            yield p


def band(lines: int) -> str:
    return next(label for limit, label in SIZE_BANDS if lines < limit)


def audit_claude_md(path: Path, root: Path) -> tuple[list[str], list[str]]:
    """Return (correctness, cost) findings for one CLAUDE.md."""
    correctness: list[str] = []
    cost: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.count("\n") + 1

    verdict = band(lines)
    if lines >= 400:
        cost.append(f"{lines} lines - {verdict}")

    # A routing table is what makes a short file viable.
    if lines > 150 and not re.search(r"agents_docs|docs/|\.md`", text):
        cost.append("no routing table - detail has nowhere to move to")

    for pattern, why in BOILERPLATE:
        for m in re.finditer(pattern, text, re.I):
            ln = text[: m.start()].count("\n") + 1
            cost.append(f"line {ln}: boilerplate - {why}")

    # Referenced files that do not exist mislead the agent.
    for ref in set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|txt|json|ya?ml))`", text)):
        for base in (path.parent, root):
            if (base / ref).exists():
                break
        else:
            correctness.append(f"broken reference: {ref}")

    return correctness, cost


def parse_frontmatter(path: Path) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8", errors="replace"), re.S)
    if not m:
        return {}
    meta, key = {}, None
    for line in m.group(1).split("\n"):
        f = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if f:
            key = f.group(1)
            meta[key] = f.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            meta[key] += " " + line.strip()
    return meta


def audit_skill(path: Path) -> list[str]:
    problems: list[str] = []
    meta = parse_frontmatter(path)
    if not meta:
        return ["no YAML frontmatter"]

    if "name" not in meta:
        problems.append("missing: name")
    elif meta["name"] != path.parent.name:
        problems.append(f"name '{meta['name']}' != directory '{path.parent.name}'")

    desc = meta.get("description", "")
    if not desc:
        problems.append("missing: description")
    else:
        if not re.search(r"\bUse (when|whenever|before)\b", desc, re.I):
            problems.append("description has no trigger clause - may never fire")
        if len(desc) > 500:
            problems.append(f"description {len(desc)} chars - likely too long")

    ignored = set(meta) - VALID_SKILL_FIELDS - TOLERATED_SKILL_FIELDS
    if ignored:
        problems.append(f"fields Claude Code ignores: {', '.join(sorted(ignored))}")

    return problems


ROLES = {"overview.md", "reference.md", "how-to.md"}
# Directories under docs/ that are not topics and take no role files:
# ADRs are immutable and cross-cutting; plans and specs are dated artifacts;
# images and assets hold no prose.
NON_TOPIC_DIRS = {"adr", "decisions", "plans", "specs", "rfcs",
                  "images", "assets", "diagrams", "mocks"}


def audit_docs_tree(root: Path) -> list[str]:
    """Check docs/ topic structure: roles, index, and legacy layouts."""
    findings: list[str] = []

    if (root / "agents_docs").is_dir():
        findings.append("agents_docs/ is legacy - fold into docs/ (one audience, one place)")

    for docs_dir in [root / "docs", *sorted((root / "apps").glob("*/docs"))]:
        if not docs_dir.is_dir():
            continue
        rel = docs_dir.relative_to(root)

        if not (docs_dir / "README.md").exists():
            findings.append(f"{rel}/: no README.md index - topics will be orphaned")

        for topic in sorted(p for p in docs_dir.iterdir() if p.is_dir()):
            # Dated or asset directories are not topics and take no roles.
            if topic.name in NON_TOPIC_DIRS:
                continue
            if not any(f.suffix == ".md" for f in topic.iterdir() if f.is_file()):
                continue                      # assets only - not a doc topic
            present = {f.name for f in topic.iterdir() if f.is_file()}
            if not present & ROLES:
                findings.append(
                    f"{rel}/{topic.name}/: no overview.md or reference.md "
                    f"(has {', '.join(sorted(present)) or 'nothing'})"
                )
            # A stub how-to signals "incomplete" and discredits the directory.
            howto = topic / "how-to.md"
            if howto.exists() and howto.read_text(encoding="utf-8",
                                                  errors="replace").count("\n") < 10:
                findings.append(f"{rel}/{topic.name}/how-to.md: stub - delete or fill it")

        # Loose .md at topic level suggests the split was never applied.
        loose = [f.name for f in docs_dir.iterdir()
                 if f.is_file() and f.suffix == ".md" and f.name != "README.md"]
        if loose:
            findings.append(
                f"{rel}/: flat files not in a topic folder: {', '.join(sorted(loose)[:4])}"
            )

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", type=Path, default=Path("."))
    ap.add_argument("--skills", action="store_true", help="audit skill frontmatter only")
    args = ap.parse_args()
    root = args.root.resolve()

    correctness: list[str] = []
    cost: list[str] = []

    if not args.skills:
        found = sorted(walk(root, "CLAUDE.md"))
        if not found:
            print("no CLAUDE.md found")
        for p in found:
            rel = p.relative_to(root)
            n = p.read_text(encoding="utf-8", errors="replace").count("\n") + 1
            print(f"  {str(rel):<46} {n:>5} lines  ({band(n)})")
            c, k = audit_claude_md(p, root)
            correctness += [f"{rel}: {x}" for x in c]
            cost += [f"{rel}: {x}" for x in k]

        correctness += audit_docs_tree(root)

    for p in sorted(walk(root, "SKILL.md")):
        if problems := audit_skill(p):
            correctness += [f"{p.relative_to(root)}: {x}" for x in problems]

    if correctness:
        print("\nCORRECTNESS (misleading - fix first)")
        for x in correctness:
            print(f"  {x}")
    if cost:
        print("\nCOST (wasteful)")
        for x in cost:
            print(f"  {x}")
    if not correctness and not cost:
        print("\nno findings")

    return 1 if correctness else 0


if __name__ == "__main__":
    sys.exit(main())
