# frontend-toolkit

Frontend design, component documentation, and AG-UI protocol expertise.

```bash
/plugin install frontend-toolkit@llm-utils
```

## Skills

### `frontend-design-notw`

Distinctive, production-grade interfaces built with custom CSS, CSS Modules, or CSS-in-JS.

**The `-notw` suffix means "no Tailwind."** The name avoids colliding with Claude Code's
built-in `frontend-design` skill, and the suffix states the difference: this skill treats
utility-class frameworks as disallowed, not merely discouraged.

Covers aesthetic direction, typography beyond the default stacks, color systems with the
60-30-10 rule, orchestrated motion, and spatial composition — plus an explicit
anti-pattern list (generic fonts, blue-gradient palettes, predictable hero-then-three-columns
layouts, default shadows).

Use it when a project forbids utility classes, or when a design has a specific character
that utility classes would flatten. For general design work with no such constraint, the
built-in `frontend-design` is fine.

### `storybook-docs`

Living component documentation: Component Story Format, autodocs, MDX, controls, actions,
and interaction testing. Framework-agnostic — examples are React, but the patterns apply
to Vue, Angular, Svelte, Solid, and Web Components.

Use when building a component library, documenting a design system, or capturing component
states as stories.

### `ag-ui-expert`

AG-UI (Agent User Interaction Protocol) for connecting AI agents to user interfaces.
Covers the event system, state management (snapshots, deltas, JSON Patch), transports
(SSE, WebSocket, binary), and both the TypeScript (`@ag-ui/core`) and Python
(`ag-ui-protocol`) SDKs.

Includes decision guidance on when AG-UI is the right protocol versus MCP, A2A, or plain
REST — worth reading before adopting it, since the honest answer is sometimes "you don't
need this."

Five reference documents ship with the skill: protocol fundamentals, TypeScript and Python
implementation, architectural decisions, and troubleshooting.

## How they fit together

Building an agent-connected UI typically uses all three: `ag-ui-expert` for the protocol
and event flow, `frontend-design-notw` for the interface, `storybook-docs` to document the
components that result.

`ag-ui-expert` can optionally use `gemini-delegate` from the `delegation` plugin to fetch
large documentation sets cheaply. That is a soft reference — the skill checks rather than
assumes, so `frontend-toolkit` works standalone.
