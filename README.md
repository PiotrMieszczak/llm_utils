# llm_utils

Claude Code plugins for fullstack AI application development: a staged workflow with
gates, architectural decision records, doc-aware review and PR automation, LLM app
patterns, API contract sync, and design fidelity.

## Install

```bash
/plugin marketplace add PiotrMieszczak/llm_utils
```

Then install what you need — plugins are deliberately separate so one does not drag in the
others:

```bash
/plugin install workflow-gates@llm-utils
/plugin install review-mr@llm-utils
/plugin install adr@llm-utils
/plugin install llm-app-patterns@llm-utils
/plugin install frontend-toolkit@llm-utils
/plugin install design-fidelity@llm-utils
/plugin install api-contract-sync@llm-utils
/plugin install delegation@llm-utils
```

## The workflow

Most of these plugins serve one pipeline, with hard gates between stages:

```
0 Explore  →  1 PRD  ─G1→  2 Spec  ─G2→  3 Plan  ─G3→  4 Tasks  ─G4→
5 Implement  →  6 Feedback  →  7 Review  ─G5→  8 Finalize
```

| Gate | Condition |
|------|-----------|
| **G1** | PRD approved before the spec is finalised |
| **G2** | Spec ready, open questions resolved |
| **G3** | Plan ready before tasks |
| **G4** | ADR at every significant decision; spec changes in the same commit as code |
| **G5** | Review approved, human-confirmed, before finalize |

Gates cluster around *deciding* and *shipping* — there is none between Implementation,
Feedback, and Review, because once the plan is agreed, work should flow.

Run `/flow` to ask which skill or stage fits your situation.

## Plugins

### Workflow and review

| Plugin | Contents |
|--------|----------|
| **`workflow-gates`** | `/flow` router, the staged workflow skill, and an advisory living-spec hook on commit |
| **`review-mr`** | `/mr` — audit against your ADRs, fix, commit, open a PR. Plus `doc-aware-review` |
| **`adr`** | `adr-from-brainstorm`, `adr-from-codebase`, and a hook that checks existing ADRs after design sessions |

**`/mr` in one line:** it reviews against *your repository's decisions* rather than generic
best practice, reports on two axes (Standards vs Spec) so neither masks the other, and
writes commits and PR bodies with **no AI attribution anywhere**.

### Building AI applications

| Plugin | Skills |
|--------|--------|
| **`llm-app-patterns`** | `rag-evaluation`, `grounded-generation`, `streaming-ui`, `openai-api` |
| **`api-contract-sync`** | OpenAPI → TypeScript codegen with CI drift detection |

### Frontend

| Plugin | Skills |
|--------|--------|
| **`frontend-toolkit`** | `frontend-design-notw` (no Tailwind), `storybook-docs`, `ag-ui-expert` |
| **`design-fidelity`** | Token compliance, responsive breakpoints, interaction states |

### Utility

| Plugin | Skills |
|--------|--------|
| **`delegation`** | `gemini-delegate` — hand large-context and multimodal work to Gemini CLI |

## Conventions used here

**Descriptions are trigger conditions.** Claude reads only a skill's frontmatter when
deciding whether to activate it — the body loads on invocation. So every description
states *what it does* and *when to use it*, with concrete trigger phrasings. A description
that lists capabilities without a "use when" clause either never fires or fires constantly.

**User-invoked commands declare `disable-model-invocation: true`.** `/mr` and `/flow` are
always invoked deliberately, so they stay out of the trigger-matching pool entirely and
cost nothing until typed.

**Hooks fail open.** Every hook exits 0 on malformed input, unwritable state, or missing
paths. A hook that breaks a session is worse than a missed reminder. The blocking one (ADR
check) consumes its marker before blocking, so it cannot loop.

**Skills are as long as their content earns.** Orchestrators that delegate stay short;
skills carrying real methodology run longer. Neither padding nor artificial compression.

## Repository layout

```
llm_utils/
├── .claude-plugin/marketplace.json
└── plugins/
    ├── adr/                  skills + hooks
    ├── workflow-gates/       commands/flow.md, skills, hooks
    ├── review-mr/            commands/mr.md, skills
    ├── llm-app-patterns/     4 skills
    ├── frontend-toolkit/     3 skills
    ├── api-contract-sync/    1 skill
    ├── design-fidelity/      1 skill
    └── delegation/           1 skill
```

## Provenance

`frontend-design-notw`, `storybook-docs`, `ag-ui-expert`, and `gemini-delegate` were
migrated from a personal `.claude/skills` directory and audited on the way in:

- Removed `execution_model` and `ultrathink` frontmatter keys — not valid Claude Code
  skill fields, so they were silently ignored
- Renamed `frontend-design` to `frontend-design-notw` to resolve a collision with the
  built-in skill of that name
- Rewrote descriptions that listed capabilities without a trigger condition
- Made `ag-ui-expert`'s dependency on `gemini-delegate` optional and checked

The ADR skills adapt
[github/awesome-copilot](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md).
That original is a Copilot prompt using `${input:...}` substitution, which Claude Code does
not interpret; the coded-bullet convention and frontmatter schema were kept, the input
mechanism replaced with conversational elicitation.

Two ideas are adapted from [mattpocock/skills](https://github.com/mattpocock/skills): the
two-axis review separation (Standards vs Spec, never merged) and the router-command
pattern behind `/flow`.

Evaluated and **not** migrated, to avoid duplicating existing tools: `secops` (overlaps the
built-in `/security-review`), `create-skill` (superseded by `superpowers:writing-skills`),
and `github-speckit` (a wrapper around another tool's own documentation).
