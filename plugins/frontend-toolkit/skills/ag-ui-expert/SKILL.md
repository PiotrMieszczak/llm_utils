---
name: ag-ui-expert
description: Expert guidance on AG-UI protocol for building agentic applications - architectural decisions, event-driven patterns, SDK implementation (TypeScript & Python), state management, and integration strategies. Consults official documentation when needed.
---

# AG-UI Protocol Expert

Expert consultation for implementing AG-UI protocol in agentic applications.

## Purpose

Provide authoritative guidance on AG-UI (Agent User Interaction Protocol) for building applications that connect AI agents to user-facing interfaces. Covers architectural decisions, implementation patterns, SDK usage, and best practices for both TypeScript and Python.

## When to Use This Skill

Activate when the user:
- Asks about AG-UI protocol, architecture, or concepts
- Needs help implementing AG-UI in their application
- Wants to understand when to use AG-UI vs other protocols (MCP, A2A, REST)
- Requires guidance on event streams, state management, or tool execution
- Needs SDK-specific help (JavaScript/TypeScript or Python)
- Questions about frontend-backend integration patterns
- Wants to understand AG-UI architectural decisions

## Core Expertise Areas

1. **Protocol Fundamentals**
   - Event-driven architecture and event types
   - State management (snapshots, deltas, JSON Patch)
   - Transport mechanisms (SSE, binary protocol, WebSockets)
   - Bidirectional communication patterns

2. **SDK Implementation**
   - JavaScript/TypeScript SDK (@ag-ui/core)
   - Python SDK (ag-ui-protocol)
   - HttpAgent configuration and usage
   - Event stream handling patterns

3. **Architectural Decisions**
   - When to use AG-UI vs alternatives
   - Integration patterns and secure proxies
   - Sub-agent composition strategies
   - Tool execution (frontend vs backend)
   - Human-in-the-loop design

4. **Practical Implementation**
   - Code examples in TypeScript and Python
   - Event flow design patterns
   - Debugging and troubleshooting
   - Performance optimization

## Consultation Workflow

### 1. Understand Requirements
- Identify the specific AG-UI question or implementation need
- Determine if it's conceptual, architectural, or implementation-focused
- Check which SDK language (TypeScript, Python, or both) is relevant

### 2. Assess Need for Official Documentation
- For latest API changes, new features, or specific implementation details, consult official docs
- Fetch them with WebFetch, or with the `gemini-delegate` skill if the `delegation`
  plugin is installed (it is a separate plugin in this marketplace, not a dependency —
  do not assume it is present):
  - Official docs: https://docs.ag-ui.com/
  - TypeScript SDK: https://docs.ag-ui.com/sdk/js/core/overview
  - Python SDK: https://docs.ag-ui.com/sdk/python/core/overview
  - Architecture: https://docs.ag-ui.com/concepts/architecture
  - Guides and examples: https://docs.ag-ui.com/guides/

### 3. Provide Guidance
- Start with conceptual explanation if needed
- Reference appropriate documentation from references/
- Provide code examples in requested language(s)
- Explain architectural implications
- Highlight best practices and common pitfalls

### 4. Validate Understanding
- Ensure guidance addresses the specific use case
- Offer to clarify or dive deeper into specific areas
- Suggest next steps or related considerations

## Key AG-UI Principles

1. **Event-Driven by Design** - Communication happens through discrete events, not request-response
2. **Transport Agnostic** - Works over SSE, WebSockets, binary protocols
3. **Strongly Typed** - Leverage TypeScript/Python type systems for safety
4. **Progressive Enhancement** - Events don't need exact AG-UI format, just compatibility
5. **State Efficiency** - Use snapshots for full state, deltas for incremental updates
6. **Separation of Concerns** - AG-UI handles UI interaction, MCP handles tools/context, A2A handles agent-to-agent

## Documentation Structure

### References (Detailed Technical Documentation)
- `protocol-fundamentals.md` - Core concepts, event system, architecture patterns
- `typescript-implementation.md` - JavaScript/TypeScript SDK usage and examples
- `python-implementation.md` - Python SDK usage and examples
- `architectural-decisions.md` - Decision frameworks and design patterns
- `troubleshooting.md` - Common issues and debugging strategies

### Assets (Templates and Tools)
- `event-flow-template.md` - Template for designing event streams
- `integration-checklist.md` - Pre-implementation and validation checklist

## Integration with Other Skills

- **`frontend-design-notw`** (same plugin) when implementing AG-UI in UI components
- **`storybook-docs`** (same plugin) when documenting AG-UI-connected components
- **`gemini-delegate`** (`delegation` plugin, optional) for fetching large documentation
  sets cheaply — check availability rather than assuming it
- **Reference MCP/A2A expertise** when discussing protocol ecosystem integration

## Best Practices

**DO:**
- Check official documentation for latest API changes before implementing
- Provide examples in both TypeScript and Python when relevant
- Explain the "why" behind architectural decisions
- Consider the full protocol ecosystem (AG-UI, MCP, A2A)
- Validate event stream designs against AG-UI event types
- Use custom CSS, CSS-in-JS, CSS modules, or vanilla CSS for styling components

**DON'T:**
- Assume AG-UI for all agent-app communication (consider simpler alternatives)
- Over-engineer for simple use cases
- Ignore transport mechanism implications
- Forget about state management strategies
- **Use Tailwind CSS** - Never use Tailwind for styling AG-UI components. Write custom CSS that matches the application's design system.

## Notes

- This skill has deep knowledge from AG-UI documentation fetched during creation
- For real-time updates or specific version changes, delegate to gemini-delegate skill
- Focus on practical, production-ready guidance over theoretical discussions
