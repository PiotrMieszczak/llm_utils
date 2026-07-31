# llm_utils

A Claude Code plugin marketplace: architectural decision records, frontend design and
documentation, and task delegation.

## Install

```bash
/plugin marketplace add PiotrMieszczak/llm_utils
```

Then install the plugins you want:

```bash
/plugin install adr@llm-utils
/plugin install frontend-toolkit@llm-utils
/plugin install delegation@llm-utils
```

Plugins are deliberately separate so installing one does not drag in the others — in
particular, the ADR hook only runs for people who wanted ADRs.

## Plugins

### `adr` — Architectural Decision Records

Two skills for the two ways decisions arrive, plus a hook that keeps records consistent.

| Skill | Use when |
|-------|----------|
| `adr-from-brainstorm` | A design conversation just settled a choice. The reasoning is in the conversation; capture it before it evaporates. |
| `adr-from-codebase` | A decision is embedded in existing code and nobody wrote down why. Reconstruct it from the code and git history. |

**The hook.** After a brainstorming or planning session, the plugin blocks the turn once
and requires a check of existing ADRs: does anything just decided contradict an accepted
record, and was a decision reached that is not yet written down?

It exists to prevent one specific failure — two accepted ADRs pointing opposite
directions, with nothing marking which is current. It fires at most once per session and
stays silent otherwise.

See [plugins/adr/README.md](plugins/adr/README.md).

### `frontend-toolkit` — Frontend without Tailwind

| Skill | Purpose |
|-------|---------|
| `frontend-design-notw` | Distinctive interfaces with custom CSS, CSS Modules, or CSS-in-JS. Enforces a no-Tailwind rule and a list of generic-AI-aesthetic anti-patterns. |
| `storybook-docs` | Storybook stories, autodocs, MDX, controls, and interaction testing. Framework-agnostic. |
| `ag-ui-expert` | AG-UI protocol: event-driven patterns, TypeScript and Python SDKs, state management, integration strategy. |

`frontend-design-notw` is named to avoid colliding with Claude Code's built-in
`frontend-design` skill. Both can be installed; pick per task. The built-in is the
general-purpose one, this is the opinionated no-utility-classes one.

See [plugins/frontend-toolkit/README.md](plugins/frontend-toolkit/README.md).

### `delegation` — Gemini CLI delegation

| Skill | Purpose |
|-------|---------|
| `gemini-delegate` | Hand large-context ingestion, screenshot and video analysis, web research, and bulk refactoring to Gemini CLI. Reports token savings. |

Requires the `gemini` CLI on `PATH`.

See [plugins/delegation/README.md](plugins/delegation/README.md).

## Repository layout

```
llm_utils/
├── .claude-plugin/
│   └── marketplace.json          # marketplace manifest
└── plugins/
    ├── adr/
    │   ├── .claude-plugin/plugin.json
    │   ├── hooks/                # hooks.json + two Python hooks
    │   └── skills/
    │       ├── adr-from-brainstorm/
    │       └── adr-from-codebase/
    ├── frontend-toolkit/
    │   ├── .claude-plugin/plugin.json
    │   └── skills/
    │       ├── ag-ui-expert/
    │       ├── frontend-design-notw/
    │       └── storybook-docs/
    └── delegation/
        ├── .claude-plugin/plugin.json
        └── skills/gemini-delegate/
```

## Provenance

The `frontend-design-notw`, `storybook-docs`, `ag-ui-expert`, and `gemini-delegate` skills
were migrated from a personal `.claude/skills` directory and audited on the way in:

- Removed `execution_model` and `ultrathink` frontmatter keys — not valid Claude Code
  skill fields, so they were silently ignored
- Renamed `frontend-design` to `frontend-design-notw` to resolve the built-in collision,
  and rewrote its description around what actually distinguishes it
- Fixed a hard dependency in `ag-ui-expert` that assumed `gemini-delegate` was always
  present; it is now an optional, checked reference

The ADR skills are new, adapted from
[github/awesome-copilot](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md).
That original is a Copilot prompt using `${input:...}` substitution, which Claude Code
does not interpret; the coded-bullet convention and frontmatter schema were kept and the
input mechanism replaced with actual conversational elicitation.

Skills evaluated and **not** migrated, to avoid duplicating tools that already exist:
`secops` (overlaps the built-in `/security-review`), `create-skill` (superseded by
`superpowers:writing-skills`), and `github-speckit` (a wrapper around another tool's own
documentation, with no standalone value).
