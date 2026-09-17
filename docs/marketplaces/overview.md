# Third-party marketplaces

`llm_utils` is one marketplace among several. Others solve problems this one does not, and
a few change agent behaviour globally rather than adding a skill you invoke.

This page records the ones worth knowing, what they actually change, and where they
conflict with the conventions in the [root README](../../README.md).

## Installing another marketplace

A marketplace is a GitHub repository with a `.claude-plugin/marketplace.json`. Adding one
does not install anything:

```bash
/plugin marketplace add owner/repo
/plugin install <plugin>@<marketplace>
```

Installed marketplaces are recorded in `~/.claude/plugins/known_marketplaces.json`, and
their clones live under `~/.claude/plugins/marketplaces/`. Read a plugin's manifest there
before trusting a description — a marketplace can claim anything in its README.

## Ponytail

| | |
|---|---|
| Source | [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) |
| Install | `/plugin marketplace add DietrichGebert/ponytail` |
| Category | productivity |
| Licence | MIT |

*"Lazy senior dev mode for AI agents. The best code is the code you never wrote."*

**What it changes.** A persistent behavioural mode, not a skill you call. Once active it
governs every response until switched off, pushing each task down a ladder — does this need
to exist at all, is it already in the codebase, does the stdlib do it, can it be one line —
and stopping at the first rung that holds.

**Levels.** `lite`, `full` (default), `ultra`, set with `/ponytail <level>`. Off with
`stop ponytail` or `normal mode`.

**Skills.** `ponytail-review` (review for over-engineering only), `ponytail-audit`
(whole-repo bloat scan), `ponytail-debt` (harvest `ponytail:` comments into a ledger),
`ponytail-gain`, `ponytail-help`.

**Worth knowing.** It marks deliberate shortcuts with a `ponytail:` comment naming the
ceiling and the upgrade path, which is what makes `ponytail-debt` possible. Without that
convention the deferrals rot silently — the same reason the `adr` plugin asks a deferral to
name its revisit trigger.

## Caveman

| | |
|---|---|
| Source | [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) |
| Install | `/plugin marketplace add JuliusBrussee/caveman` |
| Category | productivity |
| Licence | MIT + BSL |

*"Ultra-compressed communication mode. Shortens prose while preserving technical terms,
code, commands, and exact errors."*

**What it changes.** Output style only, not what gets built. Drops articles, filler and
hedging; keeps code, paths, commands and error strings verbatim. Also persistent until
switched off.

**Levels.** `lite`, `full` (default), `ultra`, plus `wenyan-*` variants. Set with
`/caveman <level>`, off with `stop caveman`.

**Skills.** `caveman-review`, `caveman-commit`, `caveman-compress` (shrink a `CLAUDE.md`
or todo list), `caveman-explore`, `caveman-stats`, `caveman-help`, plus a `cavecrew`
subagent set (`investigator`, `builder`, `reviewer`) whose compressed output is the point —
main context lasts longer.

**Worth knowing.** It carves out exceptions where compression hurts: security warnings,
irreversible-action confirmations, and multi-step sequences where dropped conjunctions
change meaning. It also stays out of anything persisted for humans — commits, docs, issue
and PR bodies stay normal prose.

## How these interact with this marketplace

**They are orthogonal, and pair deliberately.** Ponytail governs *what gets built*, Caveman
governs *how it is described*. Running both is the intended combination; neither claims the
other's territory.

**Both are global modes.** Unlike everything in `llm_utils`, they are not invoked per task.
That is a real difference in kind: a skill here fires on a trigger phrase and stops, while
these persist across a whole session and shape work you did not think to scope.

**Two collisions to know about:**

1. **Ponytail versus staged workflow.** The `workflow-gates` pipeline deliberately front-
   loads PRD, spec and plan before code. Ponytail's first rung asks whether the thing needs
   to exist at all. Used together the ladder belongs *inside* a stage, not as a reason to
   skip a gate — otherwise G1–G3 become advisory.

2. **Caveman versus `project-docs`.** Caveman explicitly exempts documentation and commits
   from compression, which is the correct boundary. A terse `overview.md` would fail the
   `auditing-docs` checks in this marketplace for the same reason it reads badly: prose for
   humans is not a token sink to optimise.

**Neither declares `model-hint`.** They predate that convention and are not bound by it;
see [model routing](../model-routing/overview.md) for why the field is advisory anyway.
