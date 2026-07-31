#!/usr/bin/env python3
"""Scaffold and audit a Diataxis-without-tutorials documentation tree.

Each topic gets overview.md (why) and reference.md (exact facts). how-to.md is
NOT scaffolded - it is optional by design, and a stub how-to permanently signals
"documentation incomplete", which is the outcome the optional rule exists to
prevent. Create it by hand when a topic has two real recipes.

Templates are deliberately minimal. Rich templates become filler nobody replaces,
and half-filled headings read as abandoned rather than absent.

Usage:
    docs_tool.py init [--root DIR]              create docs/ with an index
    docs_tool.py add-topic NAME [--root DIR]    add a topic with overview+reference
    docs_tool.py audit [--root DIR]             structural audit
    docs_tool.py index [--root DIR]             rebuild docs/README.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROLES = ("overview.md", "reference.md", "how-to.md")
REQUIRED = ("overview.md", "reference.md")

# Not topics: ADRs are immutable and cross-cutting, plans and specs are dated
# artifacts, asset directories hold no prose.
NON_TOPIC = {"adr", "decisions", "plans", "specs", "rfcs",
             "images", "assets", "diagrams", "mocks"}

OVERVIEW = """# {title}

<!-- Why is it like this? Read once to understand; rarely revisited. -->

## The problem

## How it works

## Why this way

## What this does not do
"""

REFERENCE = """# {title} Reference

<!-- Exact facts, for lookup. Tables over prose. State the source so it can be audited. -->
<!-- source:  -->

##
"""

INDEX = """# Documentation

| Topic | What it covers |
|-------|----------------|
{rows}

## Layout

Documentation is split by topic. Each topic holds up to three roles:

- `overview.md` — why it works this way
- `reference.md` — the exact facts, for lookup
- `how-to.md` — recipes for recurring tasks (only when a topic has them)

Files exist because a topic needs them, never to complete a template.
"""


def title_of(slug: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_]", slug))


def topics(docs: Path) -> list[Path]:
    if not docs.is_dir():
        return []
    return sorted(
        p for p in docs.iterdir()
        if p.is_dir() and p.name not in NON_TOPIC
        and any(f.suffix == ".md" for f in p.iterdir() if f.is_file())
    )


def summary_of(topic: Path) -> str:
    """First non-heading, non-comment line of overview.md, for the index."""
    ov = topic / "overview.md"
    if not ov.exists():
        return ""
    for line in ov.read_text(encoding="utf-8", errors="replace").split("\n"):
        line = line.strip()
        if line and not line.startswith(("#", "<!--", "|")):
            return line[:90]
    return ""


def write_index(docs: Path) -> None:
    rows = []
    for t in topics(docs):
        target = "overview.md" if (t / "overview.md").exists() else "reference.md"
        rows.append(f"| [{title_of(t.name)}]({t.name}/{target}) | {summary_of(t)} |")
    if (docs / "adr").is_dir():
        rows.append("| [Decisions](adr/) | Architectural decision records |")
    (docs / "README.md").write_text(
        INDEX.format(rows="\n".join(rows) or "| | |"), encoding="utf-8"
    )


def cmd_init(root: Path) -> int:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    write_index(docs)
    print(f"  created {docs}/README.md")
    print("  next: docs_tool.py add-topic <name>")
    return 0


def cmd_add_topic(root: Path, name: str) -> int:
    slug = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    if not slug:
        print(f"  invalid topic name: {name!r}", file=sys.stderr)
        return 1

    topic = root / "docs" / slug
    if topic.exists():
        print(f"  {topic} already exists", file=sys.stderr)
        return 1

    topic.mkdir(parents=True)
    (topic / "overview.md").write_text(OVERVIEW.format(title=title_of(slug)), encoding="utf-8")
    (topic / "reference.md").write_text(REFERENCE.format(title=title_of(slug)), encoding="utf-8")
    write_index(root / "docs")

    print(f"  created docs/{slug}/overview.md")
    print(f"  created docs/{slug}/reference.md")
    print("  updated docs/README.md")
    print("  note: how-to.md is not scaffolded - add it only when the topic has")
    print("        two or more recipes people actually repeat")
    return 0


def cmd_audit(root: Path) -> int:
    findings: list[str] = []

    for docs in [root / "docs", *sorted((root / "apps").glob("*/docs"))]:
        if not docs.is_dir():
            continue
        rel = docs.relative_to(root)

        if not (docs / "README.md").exists():
            findings.append(f"{rel}/: no README.md index - topics will be orphaned")

        loose = [f.name for f in docs.iterdir()
                 if f.is_file() and f.suffix == ".md" and f.name != "README.md"]
        if loose:
            findings.append(f"{rel}/: not in a topic folder: {', '.join(sorted(loose)[:4])}")

        for t in topics(docs):
            present = {f.name for f in t.iterdir() if f.is_file()}
            missing = [r for r in REQUIRED if r not in present]
            if set(present) & set(ROLES) == set():
                findings.append(f"{rel}/{t.name}/: no role files")
            elif missing:
                # Only overview missing is a real signal; reference-only topics
                # tell readers what without ever telling them why.
                if "overview.md" in missing:
                    findings.append(
                        f"{rel}/{t.name}/: reference without overview - "
                        "readers learn what, never why")

            ov = t / "overview.md"
            if ov.exists():
                text = ov.read_text(encoding="utf-8", errors="replace")
                rows = sum(1 for ln in text.split("\n") if ln.startswith("|"))
                if rows > 12:
                    findings.append(
                        f"{rel}/{t.name}/overview.md: {rows} table rows - "
                        "reference material in an explanation")

            ht = t / "how-to.md"
            if ht.exists():
                n = ht.read_text(encoding="utf-8", errors="replace").count("\n")
                if n < 10:
                    findings.append(
                        f"{rel}/{t.name}/how-to.md: stub - delete it "
                        "(how-to is optional; a stub signals 'incomplete')")

        # Index promising files that do not exist.
        readme = docs / "README.md"
        if readme.exists():
            for link in re.findall(r"\]\(([^)]+\.md)\)",
                                   readme.read_text(encoding="utf-8", errors="replace")):
                if not (docs / link).exists():
                    findings.append(f"{rel}/README.md: broken link -> {link}")

    if findings:
        print("STRUCTURE")
        for f in findings:
            print(f"  {f}")
    else:
        print("no structural findings")

    print("\nNot checked here (needs judgement - see the auditing-docs skill):")
    print("  staleness against the code, gaps, and whether explanations explain")
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "add-topic", "audit", "index"])
    ap.add_argument("name", nargs="?", help="topic name, for add-topic")
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args()
    root = args.root.resolve()

    if args.command == "init":
        return cmd_init(root)
    if args.command == "add-topic":
        if not args.name:
            ap.error("add-topic requires a topic name")
        return cmd_add_topic(root, args.name)
    if args.command == "index":
        docs = root / "docs"
        if not docs.is_dir():
            print("  no docs/ directory", file=sys.stderr)
            return 1
        write_index(docs)
        print("  rebuilt docs/README.md")
        return 0
    return cmd_audit(root)


if __name__ == "__main__":
    sys.exit(main())
