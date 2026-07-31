# Model Routing

Every skill in this marketplace declares a `model-hint` in its frontmatter.

```yaml
---
name: adr-from-brainstorm
description: ...
model-hint: opus
---
```

## What `model-hint` is, honestly

**It is advisory metadata, not an instruction Claude Code executes.**

Claude Code reads only four fields from `SKILL.md` frontmatter: `name`, `description`,
`allowed-tools`, and `disable-model-invocation`. Anything else — including `model-hint` —
is ignored by the loader.

This is worth stating plainly, because the opposite belief is common and produces
cargo-cult frontmatter. Skills migrated into this marketplace arrived carrying
`execution_model: sonnet` and `ultrathink: true`, both of which looked meaningful and did
nothing. They were removed.

So why declare `model-hint` at all?

1. **It is machine-readable.** The `skill-porting` plugin maps it onto formats that *do*
   support model selection.
2. **It documents intent.** A reader can see whether a skill was written for careful
   reasoning or mechanical execution.
3. **It drives subagent dispatch**, which is the mechanism that genuinely works — see
   below.

## Where model selection actually takes effect

| Mechanism | Model selectable? |
|-----------|-------------------|
| `SKILL.md` frontmatter | **No** — advisory only |
| Subagent definitions (`agents/*.md`) | **Yes** — `model:` is read |
| `Agent` tool invocation | **Yes** — `model` parameter |
| The user's session model | Yes — `/model`, or the app's picker |

A skill cannot change the model it runs under. It *can* dispatch expensive or cheap work
to a subagent on a chosen model, and that is the lever these hints inform.

```
Task tool → subagent with model: haiku    ← cheap, parallel, mechanical
Task tool → subagent with model: opus     ← one hard reasoning pass
```

## The routing policy

Assignment tracks **cognitive load**, not importance. It mirrors the staged workflow in
`workflow-gates`: cheap survey, expensive decisions, mid-tier execution.

### `opus` — decisions and judgment

Work where being wrong is expensive and the reasoning is genuinely hard.

`adr-from-brainstorm` · `adr-from-codebase` · `workflow-gates` · `doc-aware-review` ·
`rag-evaluation` · `grounded-generation` · `ag-ui-expert` · `frontend-design-notw`

What these share: no single correct answer, trade-offs to weigh, and a wrong call that
persists. Reconstructing why a codebase chose SQLite, or deciding whether keyword
retrieval is failing, is not mechanical.

### `sonnet` — execution against a known shape

The task is understood; the work is applying it carefully.

`streaming-ui` · `api-contract-sync` · `design-fidelity` · `storybook-docs` ·
`gemini-delegate` · `openai-api` · `fastapi-patterns` · `sqlalchemy-async` ·
`background-jobs` · `chunking-strategies` · `skill-porting`

Writing an SSE handler or wiring codegen has a right answer and a known route to it.

### `haiku` — mechanical survey and lookup

Breadth over depth. Reading, listing, matching, extracting.

`pdf-extraction` (the survey parts) · exploration passes · file inventories

The workflow's stage 0 has no gate by design — always start cheap. Exploration that costs
little gets done; exploration that costs a lot gets skipped, and then plans rest on
assumptions.

## Using the hints

### Dispatching to a cheaper model

When a skill's work is mechanical breadth, delegate it:

```
Agent(subagent_type="Explore", model="haiku",
      prompt="List every file importing the gateway module, with line numbers.")
```

Sweeping fifty files to build an inventory does not need a frontier model. Doing it on one
wastes budget that the subsequent reasoning pass actually needs.

### Dispatching to a stronger model

When the session is on a fast model but the task needs judgment:

```
Agent(subagent_type="general-purpose", model="opus",
      prompt="Read ADRs 0001-0006 and this diff. Does anything contradict an accepted
              decision? Cite the ADR and the specific bullet.")
```

### Splitting a task by phase

The highest-value pattern, and the one the hints exist to support:

```
1. haiku   survey the codebase, list candidate files          (breadth, cheap)
2. opus    decide which decisions matter and why              (judgment, expensive)
3. sonnet  write the records                                  (execution, mid-tier)
```

`adr-from-codebase` is `opus` overall because step 2 dominates — but its step 1 is exactly
the kind of survey that should not run on a frontier model.

## Choosing a hint for a new skill

Ask what the skill's *hardest* step requires:

| Question | Hint |
|----------|------|
| Are there trade-offs with no single right answer? | `opus` |
| Does being wrong here persist and cost a lot? | `opus` |
| Is the shape known and the work is applying it? | `sonnet` |
| Is it reading, listing, matching, or extracting? | `haiku` |

When torn between two, pick the cheaper one and note in the body which step warrants
escalation. A skill that claims `opus` for one hard paragraph in an otherwise mechanical
procedure is mis-hinted; say so in the body instead.

## Anti-patterns

**Treating the hint as enforcement.** It is not read by the loader. If a skill genuinely
requires a specific model for a step, say so in the body and dispatch a subagent.

**Hinting `opus` for everything.** If every skill claims maximum capability, the field
carries no information and nothing gets routed cheaply.

**Adding other invented frontmatter fields.** `model-hint` is documented here as a
marketplace convention with a known consumer (`skill-porting`). Inventing further fields
that nothing reads recreates the `execution_model` problem.
