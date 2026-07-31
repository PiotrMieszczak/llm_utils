# Documentation Structure

The layout that `CLAUDE.md` routes into.

## Layout

```
repo/
├── CLAUDE.md                    always loaded — rules + routing table
├── README.md                    humans arriving at the repo
├── docs/                        ALL project documentation
│   ├── README.md                the index — every topic, one table
│   ├── adr/                     decisions (separate: immutable, cross-cutting)
│   │   ├── README.md
│   │   └── adr-NNNN-*.md
│   ├── <topic>/
│   │   ├── overview.md          what it is, why it works this way
│   │   ├── reference.md         the exact facts
│   │   └── how-to.md            task recipes — optional
│   └── <topic>/
│       └── ...
└── apps/
    ├── api/docs/                backend-specific, same topic pattern
    └── web/docs/                frontend-specific, same topic pattern
```

**No `agents_docs/`.** Agent-facing and human-facing documentation are the same
documentation — an agent reading the architecture needs what a new contributor needs.
Two directories means two places to update, and one goes stale.

## The three roles

Each topic answers up to three different questions. They are separated because they have
**different audiences, different lifetimes, and different decay rates**.

| File | Question | Contains | Decays |
|------|----------|----------|--------|
| `overview.md` | *Why is it like this?* | Concepts, trade-offs, how parts relate | Slowly — rationale is stable |
| `reference.md` | *What exactly is the value?* | Schemas, parameters, tokens, event names, endpoints | **Fast** — must match code |
| `how-to.md` | *How do I do X?* | Ordered recipes for recurring tasks | Fast — breaks when steps change |

The decay column is the practical payoff. An audit can check `reference.md` aggressively
against the code while leaving `overview.md` alone. Mixed into one file, you cannot do
that — so either everything gets checked (expensive, noisy) or nothing does.

### `overview.md`

Orientation and rationale. Read once to understand a topic, revisited rarely.

- What this part of the system is and what it is for
- How the pieces relate — a diagram earns its place here
- Trade-offs and constraints that shaped it
- Links to the ADRs that decided the contentious parts

**Not here:** exact values, step-by-step procedures, exhaustive lists.

Aim for 40–120 lines. Longer usually means reference material crept in.

### `reference.md`

Lookup. Nobody reads it start to finish; they search it.

- Schemas, field names, types
- Endpoints, parameters, status codes
- Design tokens, breakpoints, event names
- Configuration keys and defaults

**Not here:** explanation of *why*, or procedures.

Structure for scanning — tables over prose, consistent ordering, no narrative. This file
must match the code exactly; when it disagrees, it is actively misleading, because it is
trusted precisely for exactness.

Length is whatever completeness requires. A reference file is allowed to be long; it is
never loaded wholesale.

### `how-to.md` — optional

Recipes for tasks people actually repeat.

- "Add a new chunker"
- "Add an endpoint with campaign scoping"
- "Debug why retrieval returns nothing"

Each recipe: a goal, ordered steps, and how to verify it worked.

**Create this file only when a topic has recurring procedures.** Most topics do not. An
empty or thin `how-to.md` permanently signals "documentation incomplete" and trains people
to ignore the whole directory.

**Not here:** one-off setup (that is `README.md`), or explanation (that is `overview.md`).

## The framework behind this

This is [Diátaxis](https://diataxis.fr/) by Daniele Procida, minus one quadrant.

You may also meet it as **[The Documentation System](https://docs.divio.com/documentation-system/)**
on Divio's site — the same framework, published earlier, sometimes called "the Grand
Unified Theory of Documentation." Diátaxis is the current canonical home, where the
two-axis model and the guidance on applying it were developed further. Same four
categories either way.

Its central claim is the reason this structure exists:

> There isn't one thing called documentation. There are four, they serve different needs,
> and they are written differently.

**Mixing them in one file is the primary failure mode.** A document that explains, lists
exact values, and gives step-by-step instructions serves all three readers badly: the
person seeking understanding wades through parameter tables, the person looking up a value
scrolls past rationale, and neither half can be audited — you cannot tell which part is
supposed to match the code.

| Diátaxis / Divio | Axis | Our file |
|------------------|------|----------|
| Explanation | theoretical, study | `overview.md` |
| Reference | theoretical, work | `reference.md` |
| How-to guide | practical, work | `how-to.md` (optional) |
| Tutorial | practical, study | **omitted** |

**Why tutorials are omitted.** A tutorial is a guided learning experience for someone new
to the domain — the most expensive type to write and maintain, and the one internal
projects almost never produce. Reserving a per-topic slot for it yields empty directories
that permanently signal "documentation incomplete," which discredits the directories that
are complete.

If a project genuinely needs onboarding material, it belongs in `README.md` or a single
`docs/getting-started.md` — not a per-topic quadrant.

## Choosing topics

Name topics after **the question someone arrives with**, not after code structure.

Good: `retrieval/`, `design/`, `ingestion/`, `deployment/`, `testing/`
Poor: `utils/`, `misc/`, `backend-v2/`, `notes/`

A topic should be something a person says out loud: "how does retrieval work?" Nobody asks
"how does utils work?"

Three to eight topics suits most projects. More than that and the index stops being
scannable; fewer and the files are doing too much each.

## Root versus app-level

**Root `docs/`** — anything cross-cutting: architecture, the data model, the API contract,
design, decisions. Its `README.md` is the single entry point and routes *into* app docs.

**`apps/<name>/docs/`** — only what is specific to that application, using the same topic
pattern. A backend's worker internals; a frontend's component conventions.

The rule: **no duplication, and root always routes.** If root and an app describe the same
thing, they will disagree within a quarter. Put it in one place and link from the other.

```markdown
<!-- docs/README.md -->
| Topic | Location |
|-------|----------|
| Architecture | [architecture/overview.md](architecture/overview.md) |
| Retrieval | [retrieval/overview.md](retrieval/overview.md) |
| Decisions | [adr/](adr/) |
| Backend internals | [../apps/api/docs/](../apps/api/docs/) |
| Frontend components | [../apps/web/docs/](../apps/web/docs/) |
```

## ADRs sit outside the topic pattern

`docs/adr/` does not take `overview`/`reference`/`how-to`, because ADRs are a different
kind of artifact:

- **Immutable** — superseded, never edited
- **Dated** — a record of what was decided when
- **Cross-cutting** — a storage decision touches retrieval, deployment, and testing at
  once, so it does not belong "under" any single topic

Topics link *to* ADRs. Overviews cite the decisions that shaped them; ADRs never move into
a topic folder.

## Worked example

```
docs/
├── README.md                     index + routing
├── adr/
│   ├── README.md
│   └── adr-0001..0006.md
├── architecture/
│   └── overview.md               system shape, boundaries — no reference needed
├── retrieval/
│   ├── overview.md               how search works, why FTS5 before vectors
│   ├── reference.md              index schema, query params, ranking fields
│   └── how-to.md                 add a chunker; debug empty results
├── design/
│   ├── overview.md               design principles, when to break the grid
│   └── reference.md              tokens, breakpoints, shadows — no how-to needed
└── api/
    ├── overview.md               contract shape, versioning, error model
    └── reference.md              every endpoint
```

Note the asymmetry: `architecture/` has only an overview, `design/` has no how-to,
`retrieval/` has all three. **That is correct.** Files exist because a topic needs them,
never to complete a template.
