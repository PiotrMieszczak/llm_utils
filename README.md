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
/plugin install project-docs@llm-utils
/plugin install claude-docs@llm-utils
/plugin install skill-porting@llm-utils
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

### Documentation and interop

| Plugin | Contents |
|--------|----------|
| **`project-docs`** | `/docs` — write and audit project documentation: explanation, reference, optional how-to |
| **`claude-docs`** | `/claude-docs` — write a short routed CLAUDE.md, audit agent docs, strip boilerplate |
| **`skill-porting`** | Convert skills to Codex, Copilot, or Gemini; `--check` validates frontmatter |

The two documentation plugins split by audience: **`project-docs`** is about whether the
documentation is any good; **`claude-docs`** is about what the agent reads and what it
costs. `claude-docs` decides *where* a fact belongs, `project-docs` whether it is written
well.

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

**Every skill declares a `model-hint`** (`opus` / `sonnet` / `haiku`) reflecting cognitive
load — judgment, execution, or mechanical survey. The field is advisory: Claude Code does
not read it, but it documents intent, drives subagent dispatch, and maps onto formats that
do support model selection. See [docs/model-routing/overview.md](docs/model-routing/overview.md).

**Progressive disclosure runs through everything.** A skill's description is read first and
its body only when invoked; a `CLAUDE.md` should route to detail rather than contain it.
The `claude-docs` plugin applies the same idea to project documentation.

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
    ├── project-docs/         commands/docs.md, 4 skills, scripts/docs_tool.py
    ├── claude-docs/          commands/claude-docs.md, 2 skills, scripts
    ├── skill-porting/        1 skill, scripts/port_skill.py
    └── delegation/           1 skill
```

## Credits

- `/flow` is inspired by [mattpocock/skills](https://github.com/mattpocock/skills).
- The `adr` skills are an adapted version of
  [github/awesome-copilot](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md).
