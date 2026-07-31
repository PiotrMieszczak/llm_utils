---
name: workflow-gates
description: A staged delivery workflow with hard gates - explore, PRD, spec, plan, tasks, implement, feedback, review, finalize. Use when starting a feature that needs structured progression, when asked about stage gates, when checking whether work may advance to the next stage, or when setting a PRD, spec, or plan status.
model-hint: opus
---

# Workflow Gates

A staged pipeline where **gates are hard conditions**, not suggestions. Work does not
advance until the gate for that boundary is satisfied.

```
0 Exploration  ──                     cheap survey, no gate
1 PRD          ──G1──                 PRD approved before spec is finalised
2 Spec         ──G2──                 spec ready, no open questions
3 Plan         ──G3──                 plan ready before tasks
4 Tasks        ──G4──                 ADR per decision + living spec
5 Implementation
6 Feedback (manual verification)
7 Review       ──G5──                 review approved before finalize
8 Finalize
```

## The shape of this workflow

Two properties are deliberate and worth understanding before using it.

**Gates cluster around deciding and shipping, not building.** There is no gate between
Implementation, Feedback, and Review — once the plan is agreed, work flows. The hard stops
sit where a wrong turn is expensive to undo: before a spec is locked, before a plan
becomes tasks, and before work is declared done.

**Start cheap.** Stage 0 has no gate precisely because it should be fast and disposable.
Use the cheapest capable model to map what already exists — libraries in use, existing
patterns, prior art. Exploration that costs little gets done; exploration that costs a lot
gets skipped, and then the plan is built on assumptions.

## Stages

### 0 — Exploration

**Purpose.** A cheap map of the current state before anything is planned. What libraries
are already here, what patterns exist, what has been tried.

**Do.** Survey the codebase read-only. Prefer a fast, inexpensive model or a read-only
subagent — this is breadth, not depth.

**Artifact.** A short report in-session or a handoff note. Nothing formal.

**Gate.** None. Always start cheap.

### 1 — PRD

**Purpose.** What problem is being solved, for whom, and what "done" means. Not how.

**Artifact.** `docs/prd/<feature>.md` with a `status:` field.

**Gate G1 — PRD approved before the spec is finalised.**

A spec written against an unapproved PRD encodes requirements nobody agreed to. If the PRD
status is anything but `approved`, warn loudly and require explicit confirmation to
proceed.

### 2 — Spec

**Purpose.** Precise behaviour: interfaces, data shapes, states, edge cases, acceptance
criteria.

**Artifact.** `docs/spec/<feature>.md` with `status:` and an **open questions** section.

**Gate G2 — spec `ready`, and open questions resolved.**

This is a **hard stop**. An unresolved open question in the spec becomes an arbitrary
decision during implementation, made by whoever hits it first, recorded nowhere.

Refine the spec until every open question is either answered or explicitly deferred with a
written reason. Then set `status: ready`.

### 3 — Plan

**Purpose.** How the spec will be built: sequence, structure, risks, verification.

**Artifact.** `docs/plans/<date>-<feature>.md` with `status:`.

**Gate G3 — plan `ready` before tasks and implementation.**

Plan verification is **mandatory** when the work introduces a new library or crosses
domain boundaries (frontend↔backend, service↔service). Those are where plans are most
often wrong and most expensive to correct later.

### 4 — Tasks

**Purpose.** The plan broken into ordered, individually verifiable units.

**Artifact.** `docs/tasks/<feature>.md`, or tracked task items.

**Gate G4 — ADR at every significant decision, and the spec is living.**

Two obligations that run from here through implementation:

**ADR per significant decision.** Any choice that constrains future work — a library, a
boundary, a data shape, a deliberate deferral — gets an ADR *at the moment it is made*,
not reconstructed later. Use `adr-from-brainstorm`.

**Living spec.** When implementation reveals the spec was wrong, the spec changes **in the
same commit as the code**. Not in a follow-up, not in a cleanup pass. A spec that lags the
code is worse than no spec, because it is trusted while being wrong.

### 5 — Implementation

Build the tasks in order. Use an execution-focused model; the thinking was done upstream.

Carry G4 with you: decisions get ADRs, spec corrections ship with the code that revealed
them.

### 6 — Feedback (manual verification)

**Purpose.** A human actually uses the thing. Automated tests confirm what was anticipated;
manual verification finds what was not.

**Artifact.** Verification notes — what was tried, what worked, what did not.

### 7 — Review

**Purpose.** Audit against the spec, the plan, and the project's ADRs.

Use `/mr` or the `doc-aware-review` skill — review against **this project's** documented
standards rather than generic best practice.

**Gate G5 — review approved before finalize.**

Requires **human confirmation**. A review verdict is not persisted anywhere the next
session can read; if a human has not confirmed approval, treat the gate as unmet. Do not
infer approval from a review that merely happened.

### 8 — Finalize

Merge, close out, update the index of whatever moved. Confirm the spec and ADRs reflect
what was actually built.

## Using this workflow

### Check gate status

Ask "which stage am I at, and is the gate met?" The plugin's hook answers this on demand
by reading artifact status fields.

```bash
grep -l "^status:" docs/prd/*.md docs/spec/*.md docs/plans/*.md 2>/dev/null
```

### Advance a stage

Before advancing, verify the gate explicitly and say which condition was checked:

> G2 check: `docs/spec/quest-log.md` is `status: ready`, open questions section is empty.
> Gate met — proceeding to Plan.

Not:

> Spec looks done, moving on.

### When a gate is not met

Say which gate, which condition failed, and what would satisfy it. Then stop — do not
proceed while narrating that you should not.

The user may override any gate. Record that they did:

> G2 not met — two open questions remain in §12. Proceeding at your direction; these
> will surface as arbitrary decisions during implementation.

## Artifact status conventions

| Stage | Statuses |
|-------|----------|
| PRD | `draft` → `review` → `approved` |
| Spec | `draft` → `refining` → `ready` |
| Plan | `draft` → `ready` |

Status lives in YAML frontmatter so it is machine-readable:

```yaml
---
title: "Quest log"
status: ready
updated: 2026-08-01
---
```

## Scaling down

This is a heavy workflow. It fits multi-week features with real architectural weight; it
is absurd for a typo fix.

For small work, run stages 0, 5, 6, 7 and skip the paperwork — but keep **G4**. Even a
small change can encode a decision worth recording, and the living-spec rule costs nothing
when there is no spec to update.

The gates that most reward keeping, in order: **G4** (decisions get recorded), **G2**
(no open questions into implementation), **G5** (a human confirms done).

## Related

- `adr-from-brainstorm` — satisfies the ADR half of G4
- `doc-aware-review` / `/mr` — the Review stage and G5
- `superpowers:brainstorming` — well suited to stages 1–2
- `superpowers:writing-plans` — well suited to stage 3
