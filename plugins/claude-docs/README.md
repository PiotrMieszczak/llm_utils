# claude-docs

Keep what the agent reads short, current, and routed.

```bash
/plugin install claude-docs@llm-utils
```

## Progressive disclosure

```
CLAUDE.md          always loaded      critical rules + routing table
   ↓ points to
agents_docs/*.md   loaded when needed one topic per file
   ↓ points to
source, ADRs       loaded on demand   the truth
```

`CLAUDE.md` is loaded on **every turn**, so it should route to detail rather than contain
it. Target 200–400 lines, ideally under 100.

The routing table is what makes this work. Without it, a short `CLAUDE.md` is not
progressive disclosure — it is missing documentation.

## Usage

```bash
/claude-docs audit      # what is wrong, and what it costs
/claude-docs write      # create or restructure
/claude-docs trim       # strip boilerplate
```

```bash
# mechanical pass, usable standalone or in CI
python3 scripts/audit_claude_md.py .
python3 scripts/audit_claude_md.py --skills .
```

Findings split into **CORRECTNESS** (misleading — fix first) and **COST** (wasteful).
Exit code is 1 only on correctness problems, so it can gate CI without failing builds over
verbosity.

## What it strips

- `This file provides guidance to Claude Code (claude.ai/code)...`
- Links to Claude documentation
- Generic advice: "write clean code", "follow best practices"
- Workflow defaults the project does not use — worktrees, branching models, CI that is not
  in play
- Aspirational rules the codebase already violates

That last one matters most. A rule contradicted by the code teaches the agent that the
file describes aspirations rather than reality, which discredits the rules that are real.

## Skills

| Skill | Use when |
|-------|----------|
| `writing-claude-md` | Creating one, or restructuring a file that has grown |
| `auditing-agent-docs` | Checking CLAUDE.md, agents_docs, skills, plugins, and hooks |

## The test for every line

**Does the agent do something different because this line is here?** If not, it is
decoration — regardless of how short the file is.
