# frontend-toolkit

Component documentation and AG-UI protocol expertise.

```bash
/plugin install frontend-toolkit@llm-utils
```

## Skills

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

Building an agent-connected UI: `ag-ui-expert` for the protocol and event flow,
`storybook-docs` to document the components that result. For the interface design itself
use the official `frontend-design` plugin; the former no-Tailwind `frontend-design-notw`
skill is in `archived/frontend-toolkit/`.
