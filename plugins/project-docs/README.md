# project-docs

Project documentation on the [Diátaxis](https://diataxis.fr/) model — also published as
Divio's [Documentation System](https://docs.divio.com/documentation-system/) — **without
tutorials**.

```bash
/plugin install project-docs@llm-utils
```

## The pattern

One topic per folder, up to three roles per topic:

```
docs/
├── README.md            the index
├── adr/                 decisions — immutable, cross-cutting
├── retrieval/
│   ├── overview.md      why it works this way        (decays slowly)
│   ├── reference.md     schemas, params, fields      (decays fast)
│   └── how-to.md        recipes — optional
└── design/
    ├── overview.md
    └── reference.md
```

| Diátaxis | Our file | Question | Included |
|----------|----------|----------|----------|
| Explanation | `overview.md` | Why is it like this? | always |
| Reference | `reference.md` | What exactly is the value? | always |
| How-to guide | `how-to.md` | How do I do X? | when the topic has recipes |
| Tutorial | — | Teach me the domain | **omitted** |

**Tutorials are omitted deliberately.** They are the most expensive type to write and the
one internal projects almost never produce. A reserved per-topic slot yields empty
directories that permanently signal "documentation incomplete," which discredits the
directories that are complete.

## Why split at all

Because the three roles **decay at different rates**, and that determines how hard each
should be audited:

| File | Audit | Why |
|------|-------|-----|
| `reference.md` | Hardest — field by field | Trusted for exactness; nobody double-checks it |
| `how-to.md` | Run the steps | Breaks silently; a failed step destroys trust |
| `overview.md` | Lightly | Rationale is stable; churn here is noise |

Mixed into one file, you cannot tell which half is supposed to match the code — so either
everything gets checked, or nothing does. In practice, nothing does.

This is Diátaxis's central claim: *there isn't one thing called documentation. There are
four, they serve different needs, and they are written differently.*

## Usage

```bash
/docs init                    # create docs/ with an index
/docs add-topic retrieval     # overview.md + reference.md, index updated
/docs audit                   # structural + judgement passes
/docs write retrieval         # fill or revise one topic
```

```bash
# structural pass, usable in CI
python3 scripts/docs_tool.py audit
python3 scripts/docs_tool.py index    # rebuild docs/README.md
```

`add-topic` **never scaffolds `how-to.md`.** Templates are near-empty by design — rich
templates become filler nobody replaces, and half-filled headings read as abandoned rather
than absent.

## Skills

| Skill | Use when |
|-------|----------|
| `writing-explanation` | Writing `overview.md` — the hardest role, no completeness test |
| `writing-reference` | Writing `reference.md` — complete, exact, scannable |
| `writing-how-to` | Writing `how-to.md` — and deciding whether the topic needs one |
| `auditing-docs` | Role confusion, staleness, gaps, orphans |

## Relationship to `claude-docs`

Different audiences, no overlap:

| Plugin | Concern |
|--------|---------|
| **`claude-docs`** | What the agent reads and what it costs — CLAUDE.md size, routing tables, skill and hook audits |
| **`project-docs`** | Whether the documentation is any good — roles, completeness, staleness |

`claude-docs` decides *where* a fact belongs; `project-docs` decides whether it is
written well.
