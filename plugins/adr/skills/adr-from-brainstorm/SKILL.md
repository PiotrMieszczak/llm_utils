---
name: adr-from-brainstorm
description: Capture an architectural decision reached during a design or brainstorming conversation as an ADR. Use when a discussion has settled a technical choice - a stack, a boundary, a storage engine, a protocol, a deferral - and that choice should be recorded before it is forgotten or silently reversed. Also use when the user says "write this up as an ADR", "record this decision", or "add an ADR".
model-hint: opus
---

# ADR from a Brainstorming Session

Turn a decision that was **just reached in conversation** into a durable record.

The conversation is your source material. You were there; you have the alternatives that
were floated, the constraints that ruled them out, and the reasoning that landed on the
choice. That context evaporates when the session ends. This skill captures it while it is
still available.

For decisions already embedded in code that nobody wrote down, use `adr-from-codebase`
instead.

## When a decision deserves an ADR

Write one when **any** of these hold:

- Someone could reasonably undo the choice later without knowing why it was made
- Alternatives were genuinely considered and rejected
- The decision constrains future work (a boundary, a dependency, a data model)
- The choice will surprise a new contributor
- Something was **deferred** with a condition attached — deferrals are decisions

Do **not** write one for: reversible implementation details, choices with no alternative,
style preferences already covered by a linter, or restatements of a framework's defaults.

> A useful test: if the answer to "why is it like this?" is only in someone's head or in
> a chat log, it belongs in an ADR.

## Process

### 1. Confirm the decision is actually settled

Do not write an ADR for a discussion still in progress. If the conversation is still
weighing options, say so and offer to write it once a choice is made.

If the user asked for an ADR but the decision is genuinely still open, the honest move is
a record with `status: "Proposed"` — that is what Proposed is for.

### 2. Locate the ADR directory and next number

```bash
ls docs/adr/ 2>/dev/null || ls docs/decisions/ 2>/dev/null || ls doc/adr/ 2>/dev/null
```

Default to `docs/adr/`. Numbering is sequential four digits: find the highest existing
`adr-NNNN-*.md` and add one. If the directory does not exist, create it along with a
`README.md` index (see `references/index-template.md`).

### 3. Gather the five required inputs

Draw these from the conversation first. **Only ask about what you genuinely cannot infer** —
you were present for the discussion, so re-interrogating the user on what they just said
is a poor experience.

| Input | What it captures |
|-------|------------------|
| **Title** | The decision, stated as a decision — not a topic |
| **Context** | Forces that made a decision necessary: constraints, requirements, pressures |
| **Decision** | What was chosen, stated plainly and unambiguously |
| **Alternatives** | What else was considered, and specifically why each was rejected |
| **Consequences** | What this makes easier and what it makes harder |

If something material is missing — most often the rejection rationale for an alternative,
or the negative consequences — ask for that specific gap. One targeted question beats a
questionnaire.

**Never invent alternatives that were not discussed.** A fabricated "Alternatives
Considered" section is worse than a short one: it manufactures false confidence that
options were weighed.

### 4. Check for conflicts with existing ADRs

Before writing, read the existing records:

```bash
grep -l "status:" docs/adr/*.md 2>/dev/null | head -20
```

If the new decision contradicts an accepted ADR, you must not simply add a second record
that quietly disagrees. Instead:

- Set `supersedes: "ADR-NNNN"` in the new record
- Update the old record's status to `Superseded` and set its `superseded_by`
- Say explicitly in Context that this reverses an earlier decision, and why

Two accepted ADRs pointing opposite directions is the failure mode this check prevents.

### 5. Write the record

Use the template in `references/adr-template.md`. Follow it exactly — the structure is
what makes a set of ADRs navigable.

Save as `docs/adr/adr-NNNN-[title-slug].md`.

### 6. Update the index

Add a row to `docs/adr/README.md`. An unindexed ADR is one nobody finds.

## Writing standards

**Coded bullets.** Multi-item sections use stable identifiers: `CON-001` (context),
`POS-001` / `NEG-001` (consequences), `ALT-001` (alternatives), `IMP-001` (implementation),
`REF-001` (references). These let a later record cite one specific point —
"supersedes ADR-0005 NEG-001" — and make records greppable.

**State decisions in the past tense, consequences in the present.** "We chose SQLite"
and "Backup is a file copy."

**Negative consequences are mandatory.** An ADR with only positives is marketing, not a
record. Every real decision costs something. If you cannot name a cost, you have not
understood the decision well enough to write it up.

**Rejection reasons must be specific.** "Too complex" says nothing. "Requires the user to
run a database server for a feature whose queries are one hop deep" is a reason a future
reader can evaluate — and disagree with, if circumstances change.

**Deferrals need triggers.** If the decision is "not yet", write the observable condition
that would change the answer. A deferral without a trigger is indistinguishable from
never, and it will be re-litigated every few months.

## Status values

| Status | Meaning |
|--------|---------|
| `Proposed` | Under discussion; not yet binding |
| `Accepted` | In force; implementation should follow it |
| `Rejected` | Considered and declined; kept so it is not re-litigated |
| `Superseded` | Replaced by a later ADR named in `superseded_by` |
| `Deprecated` | No longer applies, with no direct replacement |

**Accepted records are immutable.** A changed decision is a new ADR that supersedes the
old one. Editing history away destroys the reason the record existed.

## After writing

Report the path and offer to commit. Do not commit unless asked.

If the conversation settled **several** decisions, write one ADR per decision rather than
one omnibus record. Each should be independently readable and independently supersedable.
