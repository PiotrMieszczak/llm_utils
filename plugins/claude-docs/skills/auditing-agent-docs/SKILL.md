---
name: auditing-agent-docs
description: Audit everything an agent reads - CLAUDE.md, agents_docs, skills, plugins, hooks - for staleness, bloat, broken links, and invalid frontmatter. Use when documentation feels out of date, when context is being wasted, when a skill never triggers, when checking a marketplace before publishing, or when asked to audit project or agent documentation.
model-hint: opus
---

# Auditing Agent Docs

Everything an agent reads has a cost and a correctness question. This audit covers both,
across four surfaces:

| Surface | Failure mode |
|---------|--------------|
| `CLAUDE.md` | Bloat — loaded every turn |
| `agents_docs/`, `docs/` | Staleness — describes code that changed |
| Skills | Bad triggers, invalid frontmatter |
| Plugins and hooks | Broken manifests, hooks that fail closed |

Run all four, or scope to one when asked.

## 1. Always-loaded context

The most expensive documentation in the project, because it is paid on every turn.

```bash
find . -name "CLAUDE.md" -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -exec wc -l {} +
```

| Lines | Verdict |
|-------|---------|
| < 100 | Good |
| 100–400 | Acceptable if it is mostly a routing table |
| 400–800 | Bloated — restructure |
| > 800 | Almost certainly unread in practice |

Then check **content**, not just size:

```bash
# Boilerplate that costs tokens and says nothing
grep -n "provides guidance to Claude Code\|claude.ai/code\|^You are\|best practices" CLAUDE.md

# A routing table? Its absence is the main reason files grow.
grep -c "agents_docs\|docs/" CLAUDE.md

# Links that no longer resolve
grep -oE '`[^`]+\.(md|txt|json)`' CLAUDE.md | tr -d '`' | while read -r f; do
  [ -e "$f" ] || echo "BROKEN: $f"
done
```

**Verify the rules are still true.** This is the part tooling cannot do and the part that
matters most. For each rule, check the codebase actually follows it:

```bash
# e.g. a "no Tailwind" rule
grep -rn "tailwind" --include="*.json" --include="*.css" . | grep -v node_modules | head
```

A rule the code already violates is worse than no rule: it teaches the agent that this
file describes aspirations rather than reality, which discredits the rules that *are* real.

## 2. Topic documentation

```bash
wc -l agents_docs/*.md docs/*.md 2>/dev/null | sort -n
```

Check for:

- **Oversized files** (>100 lines) — split, or push detail to source
- **Orphans** — files nothing links to. Either link them or delete them
- **Staleness** — do named paths, commands, and structures still exist?

```bash
# Referenced paths that no longer exist
grep -ohE '`[a-zA-Z0-9_./-]+/`?' agents_docs/*.md | tr -d '`' | sort -u | \
  while read -r p; do [ -e "$p" ] || echo "MISSING: $p"; done
```

Documentation last touched long before the code it describes is a staleness signal:

```bash
git log -1 --format="%ar" -- agents_docs/architecture.md
git log -1 --format="%ar" -- src/
```

## 3. Skills

The frontmatter is the whole trigger mechanism, so errors there mean a skill silently
never fires.

```bash
# Fields Claude Code actually reads: name, description, allowed-tools,
# disable-model-invocation. Anything else is ignored.
for f in $(find . -name "SKILL.md" -not -path "*/node_modules/*"); do
  awk '/^---$/{n++; next} n==1' "$f" | grep -oE "^[a-z-]+:" | tr -d ':' | \
    grep -vE "^(name|description|allowed-tools|disable-model-invocation|model-hint)$" | \
    sed "s|^|  $f ignores: |"
done
```

`execution_model`, `ultrathink`, `capabilities`, and `model` are the common invented
fields. They look meaningful and do nothing.

**Then check description quality** — the actual trigger condition:

```bash
grep -A1 "^name:" $(find . -name "SKILL.md") | grep "^description:" | \
  grep -vE "Use (when|whenever|before)" 
```

A description with no "use when" clause either never fires or fires constantly. Both are
failures.

Also verify: `name` matches its directory, description is roughly 90–420 characters, and
no `${input:...}` (Copilot syntax) survives outside code blocks.

The `skill-porting` plugin's `--check` mode does all of this:

```bash
python3 scripts/port_skill.py --check path/to/**/SKILL.md
```

## 4. Plugins and hooks

```bash
# Every manifest parses
for f in $(find . -name "plugin.json" -o -name "marketplace.json" -o -name "hooks.json"); do
  python3 -c "import json;json.load(open('$f'))" || echo "INVALID: $f"
done

# Marketplace source paths resolve
python3 -c "
import json, os
m = json.load(open('.claude-plugin/marketplace.json'))
for p in m['plugins']:
    ok = os.path.isfile(os.path.join(p['source'], '.claude-plugin', 'plugin.json'))
    print(('  ok  ' if ok else '  BAD ') + p['name'])
"
```

**Hooks need behavioural checking, not just syntax.** A hook runs on every matching event;
a broken one degrades every session that installs the plugin.

```bash
# Must exit 0 and stay silent on malformed input
echo 'not json' | ./hooks/some_hook.py; echo "exit=$?"
echo '{}'       | ./hooks/some_hook.py; echo "exit=$?"
```

Any hook that errors, hangs, or exits non-zero on garbage input **fails closed** and will
eventually block real work. Blocking hooks additionally need loop protection — they must
honour `stop_hook_active` and consume their trigger before blocking.

## Reporting

Separate **cost** findings from **correctness** findings. They have different urgency:
stale documentation actively misleads, bloat merely wastes.

```
CORRECTNESS  (misleading — fix first)
  CLAUDE.md:14   "Backend: Neo4j" — no Neo4j dependency in the project
  agents_docs/architecture.md:8   references libs/chat-feature/, removed in 3f2a1b
  plugins/x/skills/y/SKILL.md   description has no trigger clause; will not fire

COST  (wasteful)
  CLAUDE.md   612 lines, no routing table — the full command list and
              directory tree belong in agents_docs/
  CLAUDE.md:3 boilerplate "provides guidance to Claude Code (claude.ai/code)"

INVALID  (silently ignored)
  skills/foo/SKILL.md   execution_model: sonnet — not a real field

ORPHANED
  agents_docs/old-setup.md   nothing links to it; last touched 8 months ago
```

Fix correctness first. A stale rule causes wrong work; a long file causes slow work.

## Judgement, not just metrics

Line counts are a signal, not a verdict. A 300-line `CLAUDE.md` that is mostly a routing
table and ten hard-won rules is fine. A 90-line one full of generic advice is not.

Ask of every line: **does the agent do something different because this is here?** If not,
it is decoration regardless of length.

Equally, do not recommend deleting content without a destination. Moving detail to
`agents_docs/` is restructuring; deleting it is data loss. Say which you are proposing.
