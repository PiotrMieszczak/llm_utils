---
description: Audit or restructure agent-facing documentation - CLAUDE.md, agents_docs, skills, plugins - on a progressive-disclosure model.
argument-hint: "[audit|write|trim] [path]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
disable-model-invocation: true
---

# /claude-docs

Keep what the agent reads short, current, and routed.

Mode: `$ARGUMENTS` — `audit` (default), `write`, or `trim`.

## The model

```
CLAUDE.md          always loaded      critical rules + routing table
   ↓
agents_docs/*.md   loaded when needed one topic per file
   ↓
source, ADRs       loaded on demand   the truth
```

Content belongs in the cheapest tier that can hold it. `CLAUDE.md` is paid on **every
turn**, so it should route to detail rather than contain it. Target 200–400 lines,
ideally under 100.

---

## `audit` — what is wrong and what it costs

Run the mechanical pass first:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/audit_claude_md.py" .
```

It reports broken references, invalid skill frontmatter, boilerplate, and oversized files,
split into **CORRECTNESS** and **COST**.

Then do the part a script cannot: **verify the rules are still true.** For each rule in
`CLAUDE.md`, check the codebase actually follows it.

```bash
# e.g. a "no Tailwind" rule
grep -rn "tailwind" --include="*.json" --include="*.css" . | grep -v node_modules | head
```

A rule the code already violates is worse than no rule — it teaches the agent that this
file describes aspirations, which discredits the rules that are real.

Also check plugin manifests and hook safety if the repo has them:

```bash
for f in $(find . -name "plugin.json" -o -name "marketplace.json" -o -name "hooks.json"); do
  python3 -c "import json;json.load(open('$f'))" || echo "INVALID: $f"
done
echo 'not json' | ./hooks/<hook>.py; echo "exit=$?"   # must be 0 and silent
```

Report correctness before cost. Stale docs cause wrong work; long docs cause slow work.

---

## `write` — create or restructure

Follow the `writing-claude-md` skill. Five sections in tier 1, nothing else:

1. **What this project is** — 1–3 lines
2. **Stack** — names, versions where they matter
3. **Critical rules** — non-obvious and costly to violate; under ~10
4. **Documentation map** — the routing table that makes the short file work
5. **Quick commands** — three to six

Everything else moves to `agents_docs/<topic>.md`, 20–60 lines each, one topic per file,
each linked from the routing table.

**Read before rewriting.** Never replace a file you have not read — it may hold a
hard-won rule whose reason is not obvious.

---

## `trim` — strip what says nothing

Remove from `CLAUDE.md`:

- `This file provides guidance to Claude Code (claude.ai/code)...` — Claude knows what it
  is reading
- Links to Claude documentation — not project knowledge
- Generic advice: "write clean code", "follow best practices", "add error handling"
- **Workflow defaults the project does not use** — worktrees, a branching model, or a CI
  system that is not actually in play
- Restated tool behaviour — how to use Read or Grep
- Aspirational rules the codebase already violates
- Anything a competent developer learns by reading the code in under a minute

Move, do not delete, anything that is real but detailed. Deleting content without a
destination is data loss, not restructuring — say which you are doing.

---

## Verify before reporting

```bash
wc -l CLAUDE.md agents_docs/*.md
grep -oE '`[^`]+\.md`' CLAUDE.md | tr -d '`' | while read -r f; do
  [ -e "$f" ] || echo "BROKEN LINK: $f"
done
```

A routing table pointing at a missing file is worse than no table. Report line counts
before and after, and list what moved where.

## The test for every line

**Does the agent do something different because this line is here?**

If not, it is decoration — regardless of how short the file is.
