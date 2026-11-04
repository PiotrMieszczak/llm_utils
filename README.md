# llm_utils

Claude Code plugins for fullstack AI application development: architectural decision
records, doc-aware review and PR automation, LLM app patterns, API contract sync, and
agent/project documentation.

Planning, brainstorming and design-process plugins were retired in 4.0.0 — Claude Code's
plan mode, `/code-review`, `/security-review`, `/simplify` and the official
`frontend-design` plugin cover them. They live in [`archived/`](archived/README.md).

## Install

```bash
/plugin marketplace add PiotrMieszczak/llm_utils
```

Then install what you need — plugins are deliberately separate so one does not drag in the
others:

```bash
/plugin install review-mr@llm-utils
/plugin install adr@llm-utils
/plugin install llm-app-patterns@llm-utils
/plugin install frontend-toolkit@llm-utils
/plugin install api-contract-sync@llm-utils
/plugin install project-docs@llm-utils
/plugin install agent-docs@llm-utils
/plugin install retro@llm-utils
```

Upgrading from 3.x: after `/plugin marketplace update llm-utils`, uninstall the retired
plugins — `workflow-gates`, `user-stories`, `skill-porting`, `delegation`,
`design-fidelity`.

## Plugins

### Review and decisions

| Plugin | Contents |
|--------|----------|
| **`review-mr`** | `/mr` — audit against your ADRs, fix, commit, open a PR. Plus `doc-aware-review` |
| **`adr`** | `adr-from-codebase` — reconstruct undocumented decisions as ADRs |

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
| **`frontend-toolkit`** | `storybook-docs`, `ag-ui-expert` |

### Documentation

| Plugin | Contents |
|--------|----------|
| **`project-docs`** | `/docs` — write and audit project documentation: explanation, reference, optional how-to |
| **`agent-docs`** | `/claude-docs` — write a short routed CLAUDE.md, audit agent docs, strip boilerplate |

The two documentation plugins split by audience: **`project-docs`** is about whether the
documentation is any good; **`agent-docs`** is about what the agent reads and what it
costs. `agent-docs` decides *where* a fact belongs, `project-docs` whether it is written
well.

### Utility

| Plugin | Skills |
|--------|--------|
| **`retro`** | `/retro` — retrospective on a session; suggests changes to the agent's environment |

## Conventions used here

**Descriptions are trigger conditions.** Claude reads only a skill's frontmatter when
deciding whether to activate it — the body loads on invocation. So every description
states *what it does* and *when to use it*, with concrete trigger phrasings. A description
that lists capabilities without a "use when" clause either never fires or fires constantly.

**User-invoked commands declare `disable-model-invocation: true`.** `/mr`, `/docs`, `/claude-docs` and `/retro` are
always invoked deliberately, so they stay out of the trigger-matching pool entirely and
cost nothing until typed.

**Hooks fail open.** Every hook exits 0 on malformed input, unwritable state, or missing
paths. A hook that breaks a session is worse than a missed reminder. The blocking one (ADR
check) consumes its marker before blocking, so it cannot loop.

**Skills are as long as their content earns.** Orchestrators that delegate stay short;
skills carrying real methodology run longer. Neither padding nor artificial compression.

**Skills set `model` or `effort` in frontmatter** — `effort: high` for judgment,
`model: sonnet` for execution against a known shape; heavy-reading skills add
`context: fork`. See [docs/model-routing/overview.md](docs/model-routing/overview.md).

**Progressive disclosure runs through everything.** A skill's description is read first and
its body only when invoked; a `CLAUDE.md` should route to detail rather than contain it.
The `agent-docs` plugin applies the same idea to project documentation.

## Repository layout

```
llm_utils/
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── adr/                  1 skill
│   ├── review-mr/            commands/mr.md, skills
│   ├── llm-app-patterns/     4 skills
│   ├── frontend-toolkit/     2 skills
│   ├── api-contract-sync/    1 skill
│   ├── project-docs/         commands/docs.md, 4 skills, scripts/docs_tool.py
│   ├── agent-docs/           commands/claude-docs.md, 2 skills, scripts
│   └── retro/                commands/retro.md
└── archived/                 retired plugins and skills, not in the marketplace
```

## Credits

- The `adr` skill is an adapted version of
  [github/awesome-copilot](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md).
