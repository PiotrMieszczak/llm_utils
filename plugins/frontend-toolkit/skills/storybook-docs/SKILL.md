---
name: storybook-docs
description: Write Storybook stories and component documentation that stay useful as a design system grows. Use when creating or reviewing stories, deciding which component states need covering, choosing between autodocs and MDX, organising a component library's documentation, or when a Storybook has become a wall of examples nobody reads.
model-hint: sonnet
---

# Storybook Documentation

Stories are **executable documentation**. Their value is not that they render a component —
it is that they pin the states a component can be in, so those states cannot silently break.

This skill covers the judgement calls. For API detail — every control type, decorator
argument, config option — read [storybook.js.org/docs](https://storybook.js.org/docs) or the
`references/` files in this skill. Restating a framework's own reference inline goes stale
and is worse than the source.

## What deserves a story

The most common failure is a Storybook full of examples that all look the same: one happy
path per component, nothing else.

Cover states that **differ in behaviour**, not just appearance:

| State | Why it matters |
|-------|----------------|
| Default | The baseline |
| Each variant | `primary`, `secondary`, `ghost` — one story each |
| **Empty** | What a new user sees before data exists. Almost always missing |
| **Loading** | Async feedback; frequently unstyled because nobody looked |
| **Error** | Failure often renders as nothing at all |
| **Disabled** | Frequently styled but still clickable |
| Edge content | Long labels, missing images, overflowing text |

**Empty, loading, and error earn their place.** They are the states nobody opens the app to
check, and the ones users hit first when something goes wrong.

The test: **would a reviewer notice if this state broke?** If a state is only reachable
through three clicks in the running app, the story is the only place it will ever be seen.

## Autodocs or MDX

| Use | When |
|-----|------|
| **Autodocs** | The props explain themselves. The default choice |
| **MDX** | The component needs prose — usage rules, composition guidance, do and don't |

Autodocs is generated from stories and types, so it cannot drift on its own. MDX is
hand-written and will. Reach for MDX only when the explanation cannot be expressed as a
story, and expect to maintain it.

A `Button` needs autodocs. A `DataTable` with six composition patterns and rules about when
to paginate needs MDX.

## Stories that survive

**Args, not hardcoded props.** Args are why controls work, why stories compose, and why a
change to defaults propagates.

```tsx
// works with controls, reusable
export const Primary: Story = { args: { variant: "primary", label: "Save" } };

// a screenshot with extra steps
export const Primary = () => <Button variant="primary" label="Save" />;
```

**No hooks for story state.** Component state belongs in the component. A story reaching for
`useState` usually means the component should accept that state as a prop — the story just
found a design problem.

**Name for the state, not the appearance.** `Disabled` and `WithLongLabel` say what is being
tested. `Example2` and `BlueVersion` do not.

**Compose from a base story** when a variant differs by one prop, so changes propagate
instead of being copied.

## Organisation

Colocate stories with components (`Button/Button.stories.tsx`). Separate directories drift
apart and make deletion incomplete.

Group by **what a person is looking for**, not by internal structure:

```
Design System / Foundations   tokens, typography, colour
Design System / Components    Button, Input, Card
Patterns                      composed, multi-component examples
```

Someone opening Storybook wants a component by name or by job. A tree mirroring `src/`
serves the author, not the reader.

## Interaction tests

A play function turns a story into a test that runs where the component is documented.
Worth it for **multi-step interactions** — a form, a dialog flow, search-and-select. Not
worth it for "the button renders"; the story already proves that.

See `references/controls-and-actions.md` for the API.

## In a design system

Two rules matter more than the rest:

**Every state the design spec claims gets a story.** Otherwise "we support a loading state"
is a claim nobody can check.

**Stories use design tokens, never literals.** A story hardcoding `#E8B87A` documents a
component that has already drifted. The `design-fidelity` skill covers enforcement.

## Anti-patterns

**One story per component.** Documents that it renders, nothing more.

**Missing empty, loading, and error.** The states that matter most when things go wrong.

**MDX for simple components.** Hand-written prose that autodocs would have generated and
kept current.

**Stories as a scratchpad.** Half-finished examples named `Test` and `Foo` accumulate and
train people to distrust the whole Storybook.

**Restating props in prose.** Autodocs generates that table from types; writing it again by
hand guarantees the two disagree.

## Reference

Detail lives beside this file, loaded only when needed:

| File | Covers |
|------|--------|
| `references/writing-stories.md` | CSF structure, args, composition |
| `references/autodocs-guide.md` | Autodocs setup and customisation |
| `references/mdx-documentation.md` | MDX blocks and layout |
| `references/controls-and-actions.md` | Control types, argTypes, play functions |
| `references/best-practices.md` | Extended guidance |
| `assets/story-templates.md` | Starting points |
| `assets/documentation-checklist.md` | Review checklist |

Official: [Storybook docs](https://storybook.js.org/docs) ·
[CSF](https://storybook.js.org/docs/api/csf) ·
[Interaction testing](https://storybook.js.org/docs/writing-tests/interaction-testing)
