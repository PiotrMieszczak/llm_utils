# Investigation Guide

Concrete techniques for recovering decisions from a codebase. Use alongside `SKILL.md`;
this file is the mechanical detail.

## Where decisions hide

### Dependency manifests

The clearest record of choices anyone made.

```bash
cat package.json pyproject.toml go.mod Cargo.toml Gemfile pom.xml 2>/dev/null
```

Look for:

- **Ecosystem-atypical picks** — a Vite SPA where the ecosystem defaults to Next.js
- **Pinned or held-back versions** — `"react": "18.2.0"` exact, or a major version behind.
  Something forced that pin
- **Conspicuous absences** — no ORM, no state library, no HTTP client. Deliberate
  minimalism is a decision
- **Two libraries doing one job** — usually a migration frozen midway

```bash
# When did this dependency arrive, and in what commit?
git log --oneline -S'"library-name"' -- package.json | tail -5
```

### Enforced boundaries

A boundary someone bothered to enforce is always a decision.

```bash
# Import restrictions in lint config
grep -rn "no-restricted-imports\|import/no-restricted-paths" \
  --include=".eslintrc*" --include="eslint.config.*" . 2>/dev/null

# Architectural tests
grep -rln "import.*forbidden\|must not import\|architecture" \
  --include="*test*" --include="*spec*" . 2>/dev/null | head
```

An architectural test is a decision someone cared enough about to defend mechanically.
That is a strong ADR candidate.

### Storage and schema

```bash
find . -path ./node_modules -prune -o \
  \( -name "*.sql" -o -path "*migration*" -o -name "schema*" \) -print 2>/dev/null | head -20
```

Signals: engine choice, JSON columns where relational ones would serve, denormalization,
absent indexes on obvious lookup paths, a table that exists but is never written.

### Abstraction layers

Any interface with two interchangeable implementations encodes a decision about
optionality — someone paid for a seam to keep a choice open.

```bash
grep -rn "class.*Provider\|interface.*Adapter\|ABC\|Protocol" \
  --include="*.py" --include="*.ts" . 2>/dev/null | head -20
```

### Configuration and flags

```bash
cat .env.example 2>/dev/null
grep -rn "getenv\|process\.env\|os\.environ" --include="*.py" --include="*.ts" . \
  2>/dev/null | head -20
```

Every switchable behaviour is a decision that both paths must be supported.

## Mining history

Commit bodies carry the reasoning that code cannot.

```bash
# Full messages, not just subjects - the body is where the "why" lives
git log --format='%h %an %ad%n%s%n%b%n---' --date=short -25 -- path/to/file

# Follow a file across renames
git log --oneline --follow -- path/to/file | head -30

# When a string first appeared or disappeared
git log --oneline -S"SearchTerm" | tail -10

# Who last touched each line, and when
git blame -w --date=short path/to/file | head -40
```

Merge commits often reference PR numbers. If a remote exists:

```bash
gh pr list --state merged --limit 25 --json number,title,body,mergedAt 2>/dev/null
gh pr view 42 --json title,body,comments 2>/dev/null
```

PR discussion is the single richest source of rejected alternatives, because that is where
people argue.

### Reading commit messages critically

| Message | Value |
|---------|-------|
| `switch to SQLite - no server for a local tool` | **Documented rationale.** Cite it. |
| `fix build` | Nothing. Ignore. |
| `revert 3f2a1b - broke streaming on Ollama` | **Strong signal.** A reverted approach is a real rejected alternative. |
| `WIP` / `updates` | Nothing. |

Reverts deserve particular attention: they are the clearest evidence that an alternative
was tried and failed, which is exactly what "Alternatives Considered" wants.

## In-code evidence

```bash
# Comments explaining a choice
grep -rn "# because\|// because\|# NOTE\|// NOTE\|# WHY\|// WHY" \
  --include="*.py" --include="*.ts" . 2>/dev/null | head -20

# Known compromises
grep -rn "TODO\|FIXME\|HACK\|XXX\|workaround" \
  --include="*.py" --include="*.ts" . 2>/dev/null | head -20
```

A comment saying *"do not use the async client here, it deadlocks under the worker"* is
documented rationale for a decision that looks arbitrary in the code.

## Verification

Before asserting anything in a record, confirm it against the code. If an ADR will claim
a boundary holds, prove it:

```bash
# Claim: all model calls go through the gateway
grep -rn "import anthropic\|from anthropic\|import ollama" --include="*.py" . \
  | grep -v "gateway/"
# Empty output supports the claim. Any hit disproves it.
```

If verification fails, that gap is a finding. Report the drift; do not document the
intended decision as though it were implemented, and do not quietly change the code to
match the story.

## Ranking what to document

Present findings ranked, and let the user choose. Rank by:

1. **Load-bearing** — much of the system depends on it
2. **Surprising** — a newcomer would ask "why is it like this?"
3. **Contested** — the same question keeps resurfacing
4. **Costly to reverse** — data model, storage engine, protocol
5. **Deferred** — deliberate absences, which are re-litigated most often

Three to six well-chosen records beat twenty exhaustive ones. Backfilling everything
produces a pile nobody reads, which defeats the purpose.
