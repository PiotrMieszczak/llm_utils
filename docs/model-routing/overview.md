# Model Routing

Skills in this marketplace set the model or effort they need in their frontmatter, using
fields Claude Code actually reads.

```yaml
---
name: adr-from-codebase
description: ...
effort: high
---
```

## The fields

| Field | Effect while the skill is active |
|-------|----------------------------------|
| `model` | Switches model (`sonnet`, `haiku`, `opus`, or `inherit`) |
| `effort` | Sets reasoning effort (`low` … `max`) |
| `context: fork` | Runs the skill in a forked subagent, so its reading does not fill the main context |
| `agent` | Subagent type used with `context: fork` |

Reference: <https://code.claude.com/docs/en/skills>. These fields replaced the old
`model-hint` convention, which nothing read. Outside Claude Code (claude.ai uploads, the
Skills API) only `name`, `description`, `license`, `compatibility`, `metadata` and
`allowed-tools` are allowed, so a skill meant for those surfaces should not set them.

## The routing policy

Assignment tracks **cognitive load**, not importance.

### `effort: high`, model inherited — decisions and judgment

`adr-from-codebase` · `doc-aware-review` · `rag-evaluation` · `grounded-generation` ·
`ag-ui-expert` · `auditing-agent-docs` · `auditing-docs` · `writing-explanation`

No single correct answer, trade-offs to weigh, and a wrong call that persists. These keep
the session's model (usually the strongest one you chose) and raise effort rather than
forcing a specific model.

### `model: sonnet` — execution against a known shape

`streaming-ui` · `api-contract-sync` · `storybook-docs` · `openai-api` ·
`writing-claude-md` · `writing-reference` · `writing-how-to`

Writing an SSE handler or wiring codegen has a right answer and a known route to it.

### `haiku` — mechanical survey

No skill here is mechanical end to end. Survey steps inside a skill dispatch a subagent
instead:

```
Agent(subagent_type="Explore", model="haiku",
      prompt="List every file importing the gateway module, with line numbers.")
```

## Choosing for a new skill

| Question | Setting |
|----------|---------|
| Trade-offs with no single right answer, or a wrong call that persists? | `effort: high` |
| Known shape, careful application? | `model: sonnet` |
| Reads a lot but reports a little? | add `context: fork` |
| Reading, listing, matching? | dispatch an `Explore` subagent on `haiku` from the body |

## Anti-patterns

**Forcing `model: opus` everywhere.** It overrides a user who chose a different model and
carries no routing information. Prefer `effort`.

**Inventing fields.** `model-hint`, `execution_model`, `ultrathink` look meaningful and do
nothing. `agent-docs`'s `audit_claude_md.py --skills` flags them.
