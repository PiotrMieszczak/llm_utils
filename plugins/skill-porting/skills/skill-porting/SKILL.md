---
name: skill-porting
description: Convert agent skills between Claude Code, OpenAI Codex, GitHub Copilot, and Gemini formats. Use when asked to port a skill to another AI tool, to make a skill work in Codex or Copilot, to export a skill collection for a different agent, or when writing a skill that must run on more than one platform.
model-hint: sonnet
---

# Skill Porting

Move a skill between agent platforms without silently losing what it does.

The formats are more alike than different — Markdown instructions with YAML metadata — so
mechanical conversion gets you most of the way. The value of this skill is in the parts
that **do not** map, which are the parts that break quietly if you ignore them.

## Format map

| | Claude Code | OpenAI Codex | GitHub Copilot | Gemini |
|---|---|---|---|---|
| Unit | `skills/<name>/SKILL.md` | skill dir + `agents/openai.yaml` | `.github/skills/<name>/SKILL.md` | one `GEMINI.md` |
| Metadata | embedded frontmatter | sidecar YAML | embedded frontmatter | headings |
| Trigger | `description` | `short_description` | `description` | prose |
| Arguments | `$ARGUMENTS` | positional | `${input:Name}` | prose |
| Tool limits | `allowed-tools` | per-agent config | none | none |
| Model choice | not supported | supported | not supported | n/a |
| Discrete skills | yes | yes | yes | **no** |

That last row is the important one. Claude, Codex, and Copilot all load skills
*selectively* — the model picks one based on its description. Gemini's `GEMINI.md` is a
single always-loaded context file. Porting a collection there is **concatenation**, not
translation, and it changes the economics completely.

## Porting out of Claude Code

### To Codex

Keep `SKILL.md` as-is and add a sidecar:

```
skills/my-skill/
├── SKILL.md                 # unchanged
└── agents/
    └── openai.yaml          # generated
```

```yaml
interface:
  display_name: "My Skill"
  short_description: "One line, under ~60 chars"
```

`display_name` is title-cased from `name`; `short_description` is the **first clause** of
the description — everything before "Use when". Codex shows it in a picker, so the trigger
phrasings that matter to Claude are noise there.

Use `scripts/port_skill.py` for this — it is purely mechanical.

### To Copilot

Copilot reads embedded frontmatter like Claude, so the file is nearly portable. Two
changes:

**1. Arguments.** Claude interpolates `$ARGUMENTS`; Copilot uses typed inputs:

```markdown
Claude:   Review the branch: $ARGUMENTS
Copilot:  Review the branch: ${input:BranchName}
```

**2. Drop `allowed-tools` and `disable-model-invocation`.** Copilot has no equivalent.
Losing `disable-model-invocation` matters: a skill you deliberately kept out of automatic
triggering becomes automatically triggerable. Say so when you port it.

### To Gemini

There are no discrete skills. Concatenate into `GEMINI.md` under headings:

```markdown
# Project Context

## Skill: ADR from Brainstorming
<When to use: a design conversation just settled a technical choice.>

<body>

## Skill: Doc-Aware Review
...
```

**This is always loaded**, so it costs tokens on every turn. Three consequences:

- Port only the few skills that genuinely apply to most work in that repo
- Convert each `description` into an explicit "When to use:" line, since nothing is
  matching descriptions for you any more
- A 300-line skill that Claude loads occasionally becomes a 300-line permanent tax

If a collection is large, port the two or three highest-frequency skills and leave the
rest.

## Porting into Claude Code

### From Copilot

Mostly a rename plus a rewrite of the input mechanism.

`${input:DecisionTitle}` has **no Claude equivalent** and is the most common porting bug.
Claude does not substitute it, so the literal string reaches the model and it either asks
about a variable name or invents a value. Replace with conversational elicitation:

```markdown
Copilot:  Create an ADR for ${input:DecisionTitle} with ${input:Context}.

Claude:   Gather these from the conversation. Ask only about what you
          genuinely cannot infer:
          - Title: the decision, stated as a decision
          - Context: the forces that made a decision necessary
```

This is exactly what the `adr` plugin's skills did when adapted from
`github/awesome-copilot` — the coded-bullet convention was worth keeping, the
`${input:...}` mechanism was not.

### From Codex

Take `SKILL.md` directly. Fold `short_description` into the Claude `description`, then
**add a trigger clause** — Codex descriptions are picker labels and usually lack one.

```yaml
# Codex
short_description: "Research from high-trust sources"

# Claude — needs the "use when"
description: Investigate a question against primary sources and capture findings
  as a Markdown file. Use when the user wants a topic researched, docs or API
  facts gathered, or reading legwork delegated.
```

## What does not survive a port

Check each of these explicitly and report what was lost:

| Feature | Ports? |
|---------|--------|
| Instructions and examples | Yes |
| `name`, `description` | Yes, with reshaping |
| `references/` files | Yes, if paths are relative |
| `allowed-tools` | Claude only |
| `disable-model-invocation` | Claude only |
| Hooks | **No** — Claude-specific, and often the enforcement |
| Slash commands | Partially; syntax and argument handling differ |
| `model-hint` | Advisory in Claude; maps to real config in Codex |
| Selective loading | Lost entirely when porting to Gemini |

**Hooks are the biggest silent loss.** The `adr` plugin's value is not only its two skills
but the hook that forces an ADR check after design sessions. Port the skills and the
enforcement disappears while everything still *looks* complete. Say so.

## Process

1. **Read the source skill fully.** Do not transform what you have not read.
2. **Identify non-portable features** from the table above.
3. **Convert mechanically** — `scripts/port_skill.py` handles the frontmatter and layout.
4. **Rewrite what cannot be mechanical**: argument syntax, trigger phrasing, tool
   references.
5. **Report the losses.** A port that silently drops enforcement is worse than a refusal,
   because the user believes they have working coverage.

```bash
python3 scripts/port_skill.py --to codex   path/to/SKILL.md --out ./ported
python3 scripts/port_skill.py --to copilot path/to/SKILL.md --out ./ported
python3 scripts/port_skill.py --to gemini  plugins/*/skills/*/SKILL.md --out ./ported
```

## Writing skills that port well

If a skill is meant to run on more than one platform:

- **Do not rely on `$ARGUMENTS`.** Ask conversationally instead; that works everywhere.
- **Do not assume Claude-specific tools by name.** "Search the codebase" ports; "use Grep
  with `--include`" does not.
- **Keep enforcement separate from instruction.** If a rule matters, state it in the body
  *as well as* wiring a hook. The body survives the port; the hook does not.
- **Front-load the trigger.** A description whose first clause stands alone becomes a
  usable Codex `short_description` with no rewriting.

## Anti-patterns

**Porting a whole collection to Gemini.** Every skill becomes permanent context. Pick the
few that apply broadly.

**Leaving `${input:...}` in a Claude skill.** Nothing substitutes it; the literal reaches
the model.

**Copying `allowed-tools` to platforms that ignore it.** It reads as a guarantee that is
not being enforced.

**Reporting a port as complete when hooks were dropped.** Name what was lost.
