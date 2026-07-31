---
name: writing-claude-md
description: Write or restructure a CLAUDE.md so it stays short and routes to detail instead of containing it. Use when creating a CLAUDE.md, when one has grown past a few hundred lines, when `/init` produced a bloated file, when asked to document a project for agents, or when project rules keep being ignored because they are buried.
model-hint: sonnet
---

# Writing CLAUDE.md

A `CLAUDE.md` is loaded into **every session, on every turn**. That single fact determines
everything about how it should be written.

Target: **200–400 lines**, ideally under 100. Everything else lives in files that load
only when relevant.

## The principle: progressive disclosure

Three tiers. Content belongs in the cheapest tier that can hold it.

```
CLAUDE.md              always loaded      critical rules + a routing table
   ↓ points to
docs/<topic>/*.md      loaded when needed one role per file
   ↓ points to
source, ADRs           loaded on demand   the actual truth
```

Tier 2 lives in **`docs/` at the repo root**, split by topic, with up to three roles per
topic — `overview.md` (why), `reference.md` (exact facts), and an optional `how-to.md`
(recipes). App-specific material goes in `apps/<name>/docs/` using the same pattern, and
the root index routes into it. The `project-docs` plugin owns that pattern in full.

The test for tier 1: **would violating this break something, in most sessions?** If not,
it belongs in tier 2 with a pointer from tier 1.

A rule nobody reads is not enforced. A 600-line `CLAUDE.md` costs tokens every turn *and*
buries the three rules that matter among ninety that do not — it is worse than a short one
on both dimensions.

## What belongs in CLAUDE.md

**Only these five sections.** If something does not fit one, it belongs in tier 2.

### 1. What this project is — 1–3 lines

```markdown
**Referee Assistant** — Nx monorepo for a tabletop RPG assistant with an
agent-based AI architecture.
```

Enough to orient. Not a product pitch.

### 2. Stack — a short list

Names and versions where the version matters. No rationale — that is an ADR.

### 3. Critical rules — the reason the file exists

Rules that are **non-obvious** and **costly to violate**:

```markdown
1. **No Tailwind** — custom CSS or CSS Modules only
2. **No Co-Authored-By** in commits
3. **Design system beats mock designs** when they conflict
```

Each must pass: *would an experienced developer plausibly do the wrong thing without
being told?* "Write tests" fails — everyone knows. "Design system beats mocks" passes —
unknowable without being told.

Keep this under about ten. Past that, the list stops being read as a list of imperatives
and starts being read as background.

### 4. Documentation map — the routing table

The most valuable section, and the one most often missing:

```markdown
| Topic | File |
|-------|------|
| Architecture | `docs/architecture/overview.md` |
| Retrieval | `docs/retrieval/overview.md` |
| Design tokens | `docs/design/reference.md` |
| Decisions | `docs/adr/` |
| Backend internals | `apps/api/docs/` |
```

Point at the **role** a reader needs, not just the topic. Someone looking up a token wants
`design/reference.md`; sending them to a topic folder makes them guess.

This is what makes the short file work. It does not need to *contain* the architecture; it
needs the agent to know where to look. Progressive disclosure fails without it — you get a
short file that is simply missing information.

### 5. Quick commands — the handful used constantly

```bash
nx serve ra-front      # Frontend (4200)
nx serve ra-backend    # Backend (8000)
```

Three to six. The full list goes in tier 2.

## What does not belong

| Content | Where it goes |
|---------|---------------|
| Full directory tree | `docs/architecture/overview.md` |
| Every available command | `docs/<topic>/how-to.md` |
| Coding style rules | linter config — enforce, do not document |
| API documentation | generated, or `docs/` |
| Why a decision was made | an ADR |
| Setup instructions | `README.md` |
| Long code examples | the codebase |
| Anything the code already says | nowhere — read the code |

**The strongest filter:** if a competent developer could learn it by reading the code in
under a minute, it does not belong in a file loaded every turn.

## Boilerplate to strip

`/init` and hand-written files accumulate lines that cost tokens and say nothing. Remove:

- **`This file provides guidance to Claude Code (claude.ai/code)...`** — Claude knows what
  it is reading. Pure overhead on every turn.
- **URLs to Claude documentation** — not project knowledge.
- **Generic best practice** — "write clean code", "add error handling", "follow
  conventions". Ignored because it is unactionable.
- **Workflow assumptions the project does not use** — worktrees, a branching model, or a
  CI system that is not actually in play. Stating a default nobody follows trains the
  agent to distrust the file.
- **Restated tool behaviour** — how to use Read or Grep.
- **Aspirational rules** — anything the codebase already violates. Either enforce it or
  delete it; a rule contradicted by the code is worse than no rule.

## Structuring tier 2

All project documentation lives in **`docs/` at the repo root**, split by topic. Each topic
holds up to three files, separated because they decay at different rates:

```
docs/
├── README.md                index + routing
├── adr/                     decisions — immutable, cross-cutting
├── retrieval/
│   ├── overview.md          why it works this way        (decays slowly)
│   ├── reference.md         schemas, params, fields      (decays fast)
│   └── how-to.md            recipes — optional
└── design/
    ├── overview.md
    └── reference.md         tokens, breakpoints
```

`how-to.md` exists **only** when a topic has recurring procedures. Files exist because a
topic needs them, never to complete a template — an empty `how-to.md` permanently signals
"incomplete" and trains people to ignore the directory.

App-specific documentation goes in `apps/<name>/docs/` using the same pattern. The root
index routes into it; nothing is duplicated across the two.

Name topics after **the question someone arrives with** — `retrieval/`, `design/`,
`deployment/`. Not `utils/` or `misc/`; nobody asks "how does utils work?"

The full pattern — role definitions, topic naming, and why tutorials are omitted — is
owned by the **`project-docs`** plugin. Install it for the writing and auditing skills;
`CLAUDE.md` only needs to route into the structure, not define it.

## Migrating from `agents_docs/`

Projects that kept a separate `agents_docs/` should fold it into `docs/`. The split assumes
agent-facing and human-facing documentation are different things; they are not, and
maintaining both guarantees one goes stale.

1. Map each existing file to a topic and a role — `architecture.md` becomes
   `docs/architecture/overview.md`, `styling.md` usually splits into
   `docs/design/overview.md` plus `docs/design/reference.md` (tokens are reference).
2. `git mv` so history follows the content.
3. Update the `CLAUDE.md` routing table and `docs/README.md`.
4. Verify every link resolves before removing the old directory.

Splitting one file into overview and reference is the step that adds value: the mixed file
could not be audited, because you could not tell which half was supposed to match the code.

## Nested CLAUDE.md

In a monorepo, a subdirectory may have its own `CLAUDE.md` that applies to its subtree.

Use one only when a package has rules that genuinely differ from the root. Duplicating
root content into subdirectories multiplies the always-loaded cost and creates two places
to update — which become inconsistent.

## Process

1. **Read what exists** — the current `CLAUDE.md`, plus `docs/`, `README`, and any legacy
   `agents_docs/`. Never rewrite unread.
2. **Inventory the claims.** For each, ask: critical and non-obvious (tier 1), topical
   detail (tier 2), or already-in-the-code (delete)?
3. **Verify before keeping.** Rules go stale silently. Check that named files exist,
   commands run, and stated conventions match the code. A `CLAUDE.md` describing a
   structure that was refactored away actively misleads.
4. **Write tier 1** — the five sections, nothing else.
5. **Write tier 2** — one file per topic, each linked from the routing table.
6. **Check every link resolves.** A routing table pointing at a missing file is worse than
   no table.
7. **Report the line count** before and after.

## Verification

```bash
wc -l CLAUDE.md docs/*/*.md
grep -oE '`[^`]+\.(md|txt)`' CLAUDE.md | tr -d '`' | while read -r f; do
  [ -e "$f" ] || echo "BROKEN LINK: $f"
done
```

Or use `scripts/audit_claude_md.py` from this plugin, which also flags boilerplate and
oversized sections.

## Anti-patterns

**Documenting the obvious.** "This is a React project" — the `package.json` says so.

**Rules with no teeth.** If a linter can enforce it, the linter should. Documentation is
for what tooling cannot check.

**The file as a changelog.** "Updated 2026-03: switched to Vite." Git history holds this.

**Fear-driven accumulation.** Every incident adds a line, nothing is removed, and within a
year the file is 800 lines that nobody reads and everything is buried.

**Short without routing.** Deleting content without adding pointers does not produce
progressive disclosure — it produces missing documentation.
