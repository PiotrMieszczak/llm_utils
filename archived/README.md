# Archived

Retired in 4.0.0. Not listed in the marketplace, kept for reference. Each was superseded
by something built into Claude Code or maintained elsewhere.

| Item | Replaced by |
|------|-------------|
| `workflow-gates` (`/flow`, staged gates, living-spec hook) | Plan mode and the built-in task list; the hook ran on every Bash call |
| `user-stories` | Plan mode; `product-management:write-spec` |
| `adr/skills/adr-from-brainstorm`, `adr/hooks` (Stop-blocking ADR check) | Write the ADR from the plan with `adr-from-codebase`'s template |
| `skill-porting` | The [Agent Skills](https://agentskills.io) standard — Codex, Gemini CLI and Copilot read `SKILL.md` natively |
| `delegation` (`gemini-delegate`) | 1M-token context, `Explore` subagents, `WebFetch` |
| `frontend-toolkit/skills/frontend-design-notw` | Official `frontend-design` plugin |
| `design-fidelity` | `impeccable` audit / finish review, `design:design-handoff` |

To use one anyway, add its folder as a local plugin; it is unmaintained.
