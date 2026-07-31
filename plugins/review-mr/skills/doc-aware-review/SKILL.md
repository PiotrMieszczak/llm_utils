---
name: doc-aware-review
description: Review code against a repository's own documented standards - its ADRs, specs, and CLAUDE.md - rather than generic best practice. Use when reviewing a diff, auditing a branch before a pull request, checking whether a change violates an architectural decision, or when asked "does this follow our conventions". Invoked automatically by the /mr command.
model-hint: opus
---

# Doc-Aware Review

Review a change against **what this repository has decided**, not against generic best
practice.

A generic reviewer says "consider adding error handling". A doc-aware reviewer says
"ADR-0002 forbids LLM calls in the ingestion path, and `parse.py:88` adds one." The second
is actionable, verifiable, and hard to argue with — it cites a decision the team already
made.

## Why this exists

Most review feedback fails for one of two reasons: it is too generic to act on, or it
relitigates a decision that was already settled. Reading the project's own documents first
solves both. Decisions already made become the standard; the review checks conformance
rather than reopening debate.

## Process

### 1. Establish the diff

```bash
BASE="${BASE:-$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || echo main)}"
git diff "$BASE"...HEAD --stat
git diff "$BASE"...HEAD --name-only
```

Note **which areas** changed — backend, frontend, docs, config. That drives which
standards apply.

### 2. Load the repository's standards

Read in this order, because later documents assume earlier ones:

| Source | What it gives you |
|--------|-------------------|
| `CLAUDE.md` (root, and nested ones covering changed paths) | Explicit project rules, often absolute |
| `docs/README.md` | Map of what documentation exists |
| `docs/adr/` (selected — see below) | Decisions that constrain implementation |
| Area docs (spec, data model, API contract) | The contract the code must satisfy |

Nested `CLAUDE.md` files override the root for their subtree. Check for them:

```bash
find . -name "CLAUDE.md" -not -path "*/node_modules/*" -not -path "*/.git/*"
```

### 3. Select relevant ADRs

**Do not read every ADR.** In a mature repo that is dozens of documents, most irrelevant
to any given diff. Select by:

```bash
# ADRs naming a changed directory
for f in $(git diff "$BASE"...HEAD --name-only); do
  d=$(dirname "$f")
  grep -l -- "$d" docs/adr/*.md 2>/dev/null
done | sort -u

# ADRs about a dependency the diff touches
git diff "$BASE"...HEAD -- package.json pyproject.toml go.mod | grep '^[+-]' | head -20
```

Match on: path overlap, topic keywords (storage, styling, streaming, auth), changed
dependencies, and any `ADR-` reference in the diff itself.

Read matched ADRs **in full**, prioritising:

- **Implementation Notes** — what must stay true, and how it is enforced
- **Negative Consequences** — costs knowingly accepted; a change "fixing" one of these may
  be reversing the decision
- **Status** — a `Superseded` ADR is not a standard; check `superseded_by`

### 4. Check the change

Priority order — report in this order, because a correctness bug outranks a style nit:

**1. Correctness.** Logic errors, unhandled cases, off-by-one, race conditions, broken
assumptions. Read the code as though it will run, not as though it will be skimmed.

**2. ADR compliance.** Does anything contradict an accepted decision? Two outcomes are
legitimate:

- The change is wrong → fix it
- The decision is outdated → the change needs a **new ADR** superseding the old one

Never let a change silently contradict an accepted ADR. That is how a codebase ends up
with documented decisions nobody follows, at which point the documents become noise.

**3. Boundary integrity.** Where an ADR names an enforcement mechanism, run it. Boundaries
that are only enforced by convention erode; a review is when that erosion is caught.

**4. Documentation drift.** If the change alters an API shape, a data model, or documented
behaviour, the corresponding document is now wrong. Flag it as a finding — many projects
require the spec to change in the same commit as the code.

```bash
# Does the diff touch anything the docs describe by name?
git diff "$BASE"...HEAD --name-only | while read -r f; do
  grep -rl "$(basename "$f")" docs/ 2>/dev/null
done | sort -u
```

**5. Test coverage.** New behaviour needs tests. Changed behaviour needs changed tests. A
bug fix with no regression test invites the same bug back.

**6. Convention.** Match the surrounding code — naming, structure, comment density. A
change that is individually fine but stylistically foreign adds friction forever.

### 5. Report on two axes, separately

Findings split along two axes that must **not** be merged:

- **Standards** — does the code follow this repo's documented decisions and conventions?
- **Spec** — does it faithfully implement what the PRD, spec, or issue asked for?

A change can pass one and fail the other:

| Situation | Standards | Spec |
|-----------|-----------|------|
| Follows every ADR, builds the wrong thing | pass | **fail** |
| Does exactly what was asked, violates a decision | **fail** | pass |

Reporting them together lets one mask the other — a diff with a clean bill on conventions
reads as "approved" even when it implements the wrong feature. Report under separate
headings and do **not** rerank across them.

If no spec, PRD, or issue can be found, say so explicitly and report the Standards axis
only. Do not silently collapse to one axis.

> **Optional parallelism.** On a large diff, run the two axes as separate subagents so
> their contexts do not pollute each other, then aggregate. Worthwhile when the diff is
> big enough that one axis would crowd out the other; unnecessary for a small change.

Within each axis, group by severity. Every finding needs three things: **location**,
**what is wrong**, and **which standard or spec line it violates**.

```
BLOCKING
  backend/app/ingestion/parse.py:88
    Calls gateway.complete() during extraction.
    ADR-0002 requires ingestion to be deterministic; this also breaks the
    import-boundary test in tests/test_architecture.py.

SHOULD FIX
  frontend/src/ui/Button.module.css:12
    Hardcoded #E8B87A.
    ADR-0004 IMP-001: tokens.css is the only file with literal color values.

CONSIDER
  backend/app/api/quests.py:45
    Repeated filter logic across four handlers; a dependency would
    centralise it. Judgement call — not a standards violation.

DOC DRIFT
  docs/api-contract.md
    Quest response gained a `parentQuestId` field (api/quests.py:34).
    Contract still shows the old shape.
```

**Severity discipline:**

| Level | Meaning |
|-------|---------|
| BLOCKING | Correctness bug, or violates an accepted ADR / explicit CLAUDE.md rule |
| SHOULD FIX | Real problem with a clear standard behind it |
| CONSIDER | Judgement call. The author may reasonably decline |
| DOC DRIFT | Code and documentation now disagree |

Do not inflate severity to force action. A reviewer who marks everything BLOCKING gets
ignored on the finding that actually matters.

## Anti-patterns

**Reviewing against generic best practice.** "You should add a repository layer" is not a
finding unless the project decided to use one. Personal preference dressed as a standard
wastes the author's time.

**Relitigating settled decisions.** If an ADR chose SQLite, a review is not the place to
argue for Postgres. Write an ADR proposing the change instead.

**Missing the superseded status.** Citing a `Superseded` ADR as a standard is
embarrassing and undermines every other finding. Check status before citing.

**Reporting only what is wrong.** If a change correctly implements a hard requirement,
say so briefly. It tells the author the reviewer actually read it.

**Claiming verification you did not do.** If you did not run the tests, do not imply they
pass. State what you ran and what you did not.

## When there are no documents

Some repositories have no ADRs and a thin `CLAUDE.md`. Then:

1. Infer conventions from the surrounding code and review for internal consistency
2. Review correctness normally — that never depends on documentation
3. **Say that standards documentation is missing.** If the change encodes a real
   architectural decision, suggest recording it — `adr-from-codebase` can backfill
   the decisions already in the code

An absence of documented standards is itself a finding worth surfacing once, without
belabouring it.
