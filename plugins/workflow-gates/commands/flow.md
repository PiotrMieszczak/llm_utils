---
description: Ask which skill or stage fits your current situation. A router over the llm_utils marketplace and the staged workflow.
argument-hint: "[what you are trying to do]"
disable-model-invocation: true
---

# /flow — Which skill, which stage?

You do not remember every skill. Ask.

Situation: `$ARGUMENTS`

If nothing was supplied, ask what the user is trying to do, then route.

---

## The main flow: idea → shipped

Most work travels this route. Gates (`G`) are hard conditions, not suggestions.

```
0 Explore  →  1 PRD  ─G1→  2 Spec  ─G2→  3 Plan  ─G3→  4 Tasks  ─G4→
5 Implement  →  6 Feedback  →  7 Review  ─G5→  8 Finalize
```

| Stage | Reach for | Gate to leave |
|-------|-----------|---------------|
| 0 Explore | A read-only survey. Cheap model. `Explore` subagent | none — always start cheap |
| 1 PRD | `superpowers:brainstorming` → write `docs/prd/` | **G1** PRD `approved` |
| 2 Spec | `superpowers:brainstorming`, `speckit.specify`, `speckit.clarify` | **G2** spec `ready`, no open questions |
| 3 Plan | `superpowers:writing-plans`, `speckit.plan` | **G3** plan `ready` |
| 4 Tasks | `speckit.tasks` | **G4** ADR per decision + living spec |
| 5 Implement | `superpowers:test-driven-development`, `speckit.implement` | — |
| 6 Feedback | Manual verification — a human uses it | — |
| 7 Review | **`/mr`** or `doc-aware-review` | **G5** human-confirmed approval |
| 8 Finalize | `superpowers:finishing-a-development-branch` | — |

Full detail: the `workflow-gates` skill.

---

## Route by situation

**"I have an idea and want it built"**
→ Start at stage 0. If there is a codebase, explore first — it is cheap and prevents
planning against assumptions.

**"I need to record why we chose this"**
→ `adr-from-brainstorm` if the decision was just made in conversation.
→ `adr-from-codebase` if it is already in the code and undocumented.

**"Review my branch / open a PR"**
→ **`/mr`** — audits against your ADRs and docs, fixes, commits, opens the PR.
→ `--no-fix` to audit only. `--draft` for a draft PR.

**"Is this ready to move to the next stage?"**
→ Name the gate and check its condition. The `workflow-gates` skill lists them.

**"Something is broken"**
→ `superpowers:systematic-debugging`. Build a tight failing signal before theorising.

**"Build UI from a design"**
→ `frontend-design-notw` for custom CSS (no Tailwind), `design-fidelity` to verify tokens
and breakpoints, `storybook-docs` to document the components.

**"Work on the AI layer"**
→ `llm-app-patterns` for RAG evaluation, grounding, streaming, gateway design.
→ `claude-api` for Anthropic specifics; `openai-api` for OpenAI specifics.

**"Frontend and backend types have drifted"**
→ `api-contract-sync`.

**"Huge codebase to read / screenshots / bulk refactor"**
→ `gemini-delegate`, if the `delegation` plugin is installed.

---

## Scaling down

The full nine stages fit multi-week features with real architectural weight. They are
absurd for a typo.

For small work: explore → implement → review, and keep **G4** (decisions get recorded).
The gates worth keeping even on small changes, in order:

1. **G4** — a decision made and not written down is a decision that gets re-litigated
2. **G2** — an open question carried into implementation becomes an arbitrary choice
3. **G5** — a human confirms it is actually done

---

## Context hygiene

Keep stages 1–3 in **one unbroken context window**. The PRD, spec, and plan should build
on the same thinking; compacting between them loses the reasoning that connects them.

Each implementation task, by contrast, should start **fresh** from its ticket. Carrying
the whole planning context into every task wastes it and degrades reasoning.

If a session grows long before the plan is done, hand off to a fresh session rather than
pushing on with degraded context.
