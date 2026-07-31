# workflow-gates

A staged delivery workflow where gates are hard conditions.

```bash
/plugin install workflow-gates@llm-utils
```

```
0 Explore  →  1 PRD  ─G1→  2 Spec  ─G2→  3 Plan  ─G3→  4 Tasks  ─G4→
5 Implement  →  6 Feedback  →  7 Review  ─G5→  8 Finalize
```

## The gates

| Gate | Condition |
|------|-----------|
| **G1** | PRD `approved` before the spec is finalised |
| **G2** | Spec `ready`, open questions resolved — a hard stop |
| **G3** | Plan `ready` before tasks; verification mandatory for a new library or cross-domain work |
| **G4** | ADR at every significant decision, and the spec changes in the same commit as the code |
| **G5** | Review approved, human-confirmed, before finalize |

## Why gates sit where they do

There is **no gate** between Implementation, Feedback, and Review. Once the plan is
agreed, work flows. The hard stops cluster around *deciding* and *shipping* — where a
wrong turn is expensive to undo.

Stage 0 has no gate deliberately: exploration should be cheap and disposable. Exploration
that costs little gets done; exploration that costs a lot gets skipped, and then the plan
rests on assumptions.

## `/flow`

Router over the workflow and the marketplace. Ask what fits your situation:

```bash
/flow I need to review my branch
/flow starting a new feature
```

## The living-spec hook

Advisory `PreToolUse` hook on `git commit`. When staged changes touch code but no doc or
ADR, it asks whether documented behaviour changed.

Never blocks — a heuristic cannot know whether a given change alters a documented
contract, so it surfaces the question and lets you answer. Exits 0 always.

## Scaling down

Nine stages fit multi-week features with architectural weight, and are absurd for a typo.
For small work run explore → implement → review, and keep **G4**. The gates worth keeping
even then, in order: **G4** (decisions get recorded), **G2** (no open questions into
implementation), **G5** (a human confirms done).
