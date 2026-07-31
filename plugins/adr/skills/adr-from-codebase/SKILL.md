---
name: adr-from-codebase
description: Reconstruct architectural decisions already embedded in an existing codebase and document them as ADRs. Use when adopting or inheriting a project with no decision records, when onboarding onto unfamiliar code, when asked to "document the architecture" or "backfill ADRs", or when a codebase choice keeps getting questioned because nobody wrote down why.
---

# ADR from an Existing Codebase

Recover decisions that were **made in code but never written down**, and turn them into
records.

This is archaeology, not authorship. The decision already happened; someone chose SQLite
over Postgres, or put a hard boundary between two modules, or pinned a dependency to an
old major version. The code is the evidence. The reasoning is missing, and you must
reconstruct it honestly — including admitting when you cannot.

For decisions reached in a live conversation, use `adr-from-brainstorm` instead.

## The core discipline

**Distinguish evidence from inference, and mark the difference in the record.**

The single biggest failure mode is writing a confident ADR that invents a rationale
nobody ever had. That is worse than no ADR: it fabricates authority and it will be cited
later as if it were a real decision.

Every claim you write falls into one of three buckets:

| Bucket | Basis | How to write it |
|--------|-------|-----------------|
| **Observed** | Visible in code, config, or lockfiles | State it plainly |
| **Documented** | Found in commits, PRs, issues, comments, docs | State it and cite the source |
| **Inferred** | Your reconstruction from the above | Mark it as inference |

Inferred reasoning gets explicit hedging in the record: *"No written rationale was found.
The following is reconstructed from the code and may be incomplete."*

## Process

### 1. Find what is already documented

Do not duplicate existing records.

```bash
ls docs/adr/ docs/decisions/ doc/adr/ 2>/dev/null
find . -iname "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" \
  | xargs grep -l -i "decision\|architecture\|rationale" 2>/dev/null | head -20
```

Read any `README`, `CONTRIBUTING`, `ARCHITECTURE`, or `CLAUDE.md` first. Their content is
**documented** evidence, not inference.

### 2. Survey the codebase for decision points

Look for choices that had alternatives. Signals worth investigating:

**Dependencies and stack**
```bash
cat package.json pyproject.toml go.mod Cargo.toml pom.xml 2>/dev/null
```
Pinned versions, unusual choices, a library used where the ecosystem default differs, or
a conspicuously *absent* dependency (no ORM, no state library) all mark decisions.

**Structural boundaries**
Module layout, enforced import rules, lint configs restricting cross-imports, an
architectural test asserting a boundary. A boundary someone bothered to enforce is
always a decision.

**Storage and data**
Schema files, migrations, choice of engine, denormalization, JSON columns where relational
columns would work.

**Configuration**
Feature flags, environment switching, provider abstractions. Anything with two
interchangeable implementations behind one interface is a decision about optionality.

**Conspicuous absences**
No caching layer, no queue, no auth. Absence is often a deliberate deferral, and it is the
category most often re-litigated because nobody recorded it.

### 3. Mine the history for real rationale

This is where documented evidence hides. Prioritize it over your own inference.

```bash
# Commits that touched a decision point
git log --oneline --follow -- path/to/file | head -30

# Commit bodies often carry the reasoning the code lacks
git log --format='%h %s%n%b' -20 -- path/to/file

# When a dependency arrived, and what came with it
git log --oneline -S"library-name" -- package.json | tail -5
```

If a remote exists, PR descriptions are often the richest source:

```bash
gh pr list --state merged --limit 20 --json number,title,body 2>/dev/null
```

A commit saying "switch to SQLite, Postgres was overkill for a local tool" is documented
rationale. Cite it. That single line outranks a paragraph of your own reasoning.

### 4. Confirm scope with the user

Present the decision points you found, ranked by how consequential they are, and ask which
to document. **Do not write twelve ADRs unprompted.** Backfilling every choice at once
produces a pile nobody reads, and most codebases have three to six decisions that actually
matter.

Prefer decisions that are load-bearing, surprising, or repeatedly questioned.

### 5. Write each record

Use `references/adr-template.md`, with these adjustments for reconstructed records:

- **Status** is `Accepted` — the decision is in force, whatever its provenance
- **Date** is when the decision was made if history reveals it, otherwise today's date
  with a note that the original date is unknown
- **Authors** — attribute from git history where clear; otherwise "Reconstructed from
  codebase"
- Add a **Provenance** note directly under Status stating what is observed, what is
  documented, and what is inferred

Example provenance note:

```md
> **Provenance.** Reconstructed from the codebase in 2026-07. The choice is visible in
> `backend/app/core/db.py` and the initial migration. Commit `a1b2c3d` ("use sqlite,
> no server for a local tool") supplies partial rationale. Consequences below are
> inferred and were not stated by the original author.
```

### 6. Verify before claiming

Every factual assertion must be checked against the code. If you write that all model
calls route through a gateway, grep to confirm no module bypasses it. An ADR that
misdescribes the code is actively harmful — it will be trusted over the source.

```bash
grep -rn "import anthropic\|from anthropic" --include="*.py" . | grep -v "gateway/"
```

If the check fails, that discrepancy is itself worth reporting: the intended decision and
the actual code have drifted.

### 7. Update the index

Create or update `docs/adr/README.md`. See `references/index-template.md`.

## Handling uncertainty honestly

When you cannot determine why something was chosen, say so. Acceptable and useful:

```md
## Context

- **CON-001**: The application targets single-user local operation.
- **CON-002**: No written rationale for this choice was found in commit history,
  pull requests, or documentation. The constraints below are inferred from the
  code's shape and may not reflect the original reasoning.
```

Unacceptable: inventing a plausible-sounding rationale and presenting it as fact.

Where inference is uncertain but the decision matters, flag it for the user to confirm —
someone on the team may simply remember.

## Detecting drift

Reconstruction frequently surfaces places where code and intent disagree: a boundary
documented in a README but violated in three files, a "temporary" workaround from two
years ago, a dependency that a comment says was removed.

Report drift separately from the ADRs. Do not silently document the *intended* decision as
though it were the *implemented* one — and do not quietly "fix" the code either. Surfacing
the gap is the deliverable; deciding what to do about it is the user's call.

## Writing standards

Identical to `adr-from-brainstorm`: coded bullets (`CON-001`, `POS-001`, `NEG-001`,
`ALT-001`, `IMP-001`, `REF-001`), mandatory negative consequences, and specific rejection
reasons.

One caution specific to reconstruction: **do not invent alternatives.** If history does not
reveal what else was considered, write what the plausible alternatives *were* and mark the
section as reconstructed:

```md
## Alternatives Considered

> No record of alternatives being evaluated was found. The options below are the
> realistic alternatives available at the time, with inferred rejection reasons.
```

That framing is honest and still useful to a future reader weighing a change.
