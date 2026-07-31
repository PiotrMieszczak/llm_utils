---
name: writing-reference
description: Write the reference.md for a documentation topic - the exact, complete, scannable facts. Use when documenting an API, schema, configuration keys, design tokens, event names, or CLI flags, when a reference has drifted from the code, or when a document meant for lookup has filled with narrative.
model-hint: sonnet
---

# Writing Reference

`reference.md` answers **"what exactly is the value?"**

Nobody reads it start to finish. They arrive with a specific question — what type is this
field, what does this flag default to, what is the exact hex — find the answer, and leave.

Everything about how it is written follows from that.

## Two properties that matter

**Completeness.** A reference with gaps is worse than none, because a reader who finds
nine of ten fields concludes the tenth does not exist. Partial reference material actively
misleads.

**Exactness.** It is trusted *precisely* for exactness. A wrong default here is worse than
a wrong sentence in an overview, because nobody double-checks a reference against the code
— that is the whole reason they consulted it.

These make reference the fastest-decaying documentation you have, and the part an audit
should check hardest.

## Structure

Optimise for **scanning and searching**, not reading.

```markdown
# Retrieval Reference

## Chunk schema

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Primary key |
| `document_id` | int | FK to `document` |
| `ordinal` | int | Position within the document |
| `page_from` | int? | Null for non-paginated sources |
| `content` | text | Indexed text |

## Search parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `q` | string | — | Required. FTS5 syntax |
| `limit` | int | `10` | Max 100 |
```

Rules that make it usable:

- **Tables over prose.** A reader's eye can scan a column; it cannot scan a paragraph.
- **Consistent column order** across every table in the file. Varying it forces re-reading.
- **One fact per row.** Do not bundle "type and default and constraint" into a sentence.
- **Predictable ordering** — alphabetical, or the order the code defines. Pick one and
  hold it; "logical" ordering is only logical to the author.
- **Stable headings.** People link to them. Renaming a heading breaks every link.
- **Null and optional marked explicitly.** `page_from` being optional is a fact, not an
  omission.

Length is whatever completeness requires. A reference is allowed to be long — it is never
read wholesale.

## What does not belong

| Content | Belongs in |
|---------|-----------|
| Why the field exists | `overview.md` |
| How to accomplish a task | `how-to.md` |
| Migration advice | `how-to.md` or an ADR |
| Tutorials and worked walkthroughs | nowhere in this pattern |

A one-line note clarifying a non-obvious value is fine. A paragraph of rationale is
explanation leaking in.

## Keeping it true

Reference decays the moment the code changes. Two defences:

**Generate what can be generated.** An OpenAPI schema, a token file, a CLI `--help` — if a
machine can produce the table, do not hand-write it. See the `api-contract-sync` plugin for
the API case.

**Make drift detectable for the rest.** Where a table is hand-maintained, note its source
so an audit knows what to compare against:

```markdown
<!-- source: backend/app/models/chunk.py -->
```

Then a check is possible:

```bash
grep -oE "^\s+[a-z_]+:" backend/app/models/chunk.py | tr -d ' :' | sort > /tmp/code.txt
grep -oE "^\| \`[a-z_]+\`" docs/retrieval/reference.md | tr -d '|` ' | sort > /tmp/doc.txt
diff /tmp/code.txt /tmp/doc.txt
```

A hand-written reference with no stated source cannot be audited, only distrusted.

## Common cases

**API endpoints** — path, method, parameters, request shape, response shape, status codes,
errors. Group by resource, not by HTTP verb.

**Configuration** — key, type, default, required, effect. State where it is read from
(environment, file, flag) and precedence when several apply.

**Design tokens** — token name, value, and *where it is used*. That last column is what
makes a token table usable rather than a colour list.

**Events** — name, payload shape, when emitted, ordering guarantees. Ordering is the part
most often omitted and most often needed.

## Anti-patterns

**Partial coverage.** Documenting the interesting fields and skipping the boring ones. The
reader cannot tell "not documented" from "does not exist".

**Narrative reference.** "First you should set the limit parameter, which controls…" —
a reader scanning for `limit` will not find it in a sentence.

**Undated, unsourced tables.** No way to tell whether it still matches the code.

**Duplicating generated output by hand.** It will disagree with the generator within a
month, and the hand-written copy is the one people read.

**Inconsistent naming with the code.** If the field is `page_from`, the reference says
`page_from` — not "starting page". Reference is where names must be literal.
