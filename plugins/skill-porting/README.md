# skill-porting

Convert agent skills between Claude Code, OpenAI Codex, GitHub Copilot, and Gemini.

```bash
/plugin install skill-porting@llm-utils
```

## Why porting is not just copying

All four platforms use Markdown with YAML metadata, so mechanical conversion gets you
most of the way. The value is in what **does not** map — and breaks quietly if ignored.

| | Claude Code | Codex | Copilot | Gemini |
|---|---|---|---|---|
| Metadata | embedded | sidecar `agents/openai.yaml` | embedded | headings |
| Arguments | `$ARGUMENTS` | positional | `${input:Name}` | prose |
| Tool limits | `allowed-tools` | per-agent | none | none |
| **Selective loading** | yes | yes | yes | **no** |

**Gemini is the outlier.** There are no discrete skills — `GEMINI.md` is one
always-loaded context file. Porting a collection there is concatenation, and every skill
becomes a permanent per-turn tax. The tool reports the token cost so the trade is visible:

```
NOTE: GEMINI.md is always loaded (~9006 tokens every turn)
WARN: 5 skills concatenated - port only broad ones
```

## Usage

```bash
# Validate skills against Claude Code's real field set
python3 scripts/port_skill.py --check plugins/*/skills/*/SKILL.md

# Port
python3 scripts/port_skill.py --to codex   path/to/SKILL.md --out ./ported
python3 scripts/port_skill.py --to copilot path/to/SKILL.md --out ./ported
python3 scripts/port_skill.py --to gemini  plugins/*/skills/*/SKILL.md --out ./ported
```

`--check` is useful on its own. It catches the frontmatter problems that are silently
ignored rather than erroring: fields Claude Code does not read, a `name` that disagrees
with its directory, a description with no trigger clause, and stray `${input:...}`
left over from a Copilot original.

## What is always lost

**Hooks.** They are Claude-specific, and they are often where the enforcement lives — the
`adr` plugin's value is its skills *plus* the hook that forces an ADR check. Port the
skills and the enforcement silently disappears.

The skill's rule: **report the losses**. A port presented as complete when enforcement was
dropped is worse than a refusal, because the user believes they still have coverage.
