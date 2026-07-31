---
name: auditing-docs
description: Audit project documentation for role confusion, staleness, gaps, and orphans. Use when documentation feels out of date, when a doc set has grown organically without structure, before onboarding someone new, when checking whether reference material still matches the code, or when asked to review or reorganise documentation.
model-hint: opus
---

# Auditing Documentation

Documentation fails in four distinct ways, and they need different checks.

| Failure | Symptom | Cost |
|---------|---------|------|
| **Role confusion** | One file explaining, listing, and instructing | Nothing is auditable |
| **Staleness** | Describes code that changed | Actively misleads |
| **Gaps** | A topic nobody wrote | Silent — nobody knows to look |
| **Orphans** | Files nothing links to | Wasted, and rot unnoticed |

Structure is in `references/doc-structure.md`. This skill is about judging what is there.

## 1. Role confusion

The most consequential and least visible problem.

The pattern splits each topic into `overview.md` (why), `reference.md` (exact facts), and
optional `how-to.md` (recipes) because **they decay at different rates**. Mixed into one
file, you cannot tell which half is supposed to match the code — so either everything gets
checked, or nothing does. In practice, nothing does.

Detect it:

```bash
# Explanation carrying reference material: tables of fields or values
grep -c "^|" docs/*/overview.md 2>/dev/null

# Reference carrying narrative: long prose paragraphs
awk 'length > 200 {c++} END {print FILENAME, c+0}' docs/*/reference.md 2>/dev/null

# Explanation carrying procedures
grep -ln "^[0-9]\. \|^Step " docs/*/overview.md 2>/dev/null
```

An `overview.md` with a dozen table rows is a reference wearing a disguise. Move the tables
and see what remains — if nothing does, it was never an explanation.

## 2. Staleness — audit each role differently

**This is the payoff of splitting roles.** Apply rigour where it belongs:

| File | How hard to check | Why |
|------|-------------------|-----|
| `reference.md` | **Hardest** — field by field | Trusted for exactness; nobody double-checks it |
| `how-to.md` | Run the steps | Breaks silently; failure destroys trust |
| `overview.md` | Lightly | Rationale is stable; churn here is noise |

For reference material, compare against its source:

```bash
# Fields the code defines vs the reference documents
grep -oE "^\s+[a-z_]+:" backend/app/models/chunk.py | tr -d ' :' | sort > /tmp/code.txt
grep -oE "^\| \`[a-z_]+\`" docs/retrieval/reference.md | tr -d '|` ' | sort > /tmp/doc.txt
diff /tmp/code.txt /tmp/doc.txt
```

A reference with no stated source cannot be audited, only distrusted. Flag that as a
finding in itself.

Timing is a cheap staleness signal:

```bash
git log -1 --format="%ar" -- docs/retrieval/reference.md
git log -1 --format="%ar" -- backend/app/retrieval/
```

Reference untouched for months while its subject changed weekly is almost certainly wrong.

For how-to files, the verification steps are runnable:

```bash
grep -A6 "^Verify:" docs/*/how-to.md | grep -E "^\s*(npm|pytest|make|python3|nx)"
```

## 3. Gaps

Harder than staleness, because nothing signals absence.

**Compare topics against the system.** List the significant subsystems, then check which
have documentation:

```bash
ls docs/*/ -d 2>/dev/null | sed 's|docs/||;s|/||'
ls apps/*/src/*/ -d 2>/dev/null | sed 's|.*/||'
```

**Look for questions answered repeatedly** in commit messages, PR discussion, or chat. A
question asked twice is a missing document.

**Check the roles per topic.** A topic with only `reference.md` and no `overview.md` tells
readers *what* without ever telling them *why* — common, and it is why people keep asking
the same design questions.

Do **not** report a missing `how-to.md` as a gap. It is optional by design; only flag one
when the topic clearly has repeated procedures.

## 4. Orphans

```bash
# Files nothing links to
for f in docs/*/*.md; do
  base=$(basename "$f")
  grep -rq "$base" docs/README.md CLAUDE.md docs/*/*.md 2>/dev/null || echo "ORPHAN: $f"
done
```

Also check the reverse — the index promising files that do not exist:

```bash
grep -oE '\]\(([^)]+\.md)\)' docs/README.md | sed 's/](\(.*\))/\1/' | while read -r f; do
  [ -e "docs/$f" ] || [ -e "$f" ] || echo "BROKEN: $f"
done
```

An index pointing at a missing file is worse than no index, because it is trusted.

## Reporting

Group by failure type; order by cost.

```
STALE  (misleading — fix first)
  docs/retrieval/reference.md
    `chunk.heading` documented, removed from the model in 3f2a1b
    Source not stated; cannot be checked automatically.

ROLE CONFUSION
  docs/design/overview.md
    38 table rows of token values. Move to design/reference.md;
    what remains should be the design principles.

GAPS
  docs/ingestion/  has reference.md but no overview.md
    Readers learn the chunk schema but never why chunking works this way.

ORPHANED
  docs/deployment/how-to.md
    Nothing links to it. Last touched 8 months ago.
    Either link it from docs/README.md or delete it.
```

**Stale before structural.** A wrong value causes wrong work today; a misfiled explanation
causes slow work eventually.

## Judgement

**Do not enforce the template.** A topic with only `overview.md` is complete if that is all
it needs. Files exist because a topic needs them, never to fill a pattern — flagging every
missing `how-to.md` produces stub files, which is the outcome the optional rule exists to
prevent.

**Do not recommend deleting without a destination.** Moving detail is restructuring;
deleting it is data loss. Say which you are proposing.

**Weigh the reader, not the author.** The question is never "is this well written" but
"does someone arriving with a question find the answer?" A terse table that answers it
beats an elegant paragraph that does not.
