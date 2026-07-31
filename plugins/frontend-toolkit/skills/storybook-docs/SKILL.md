---
name: storybook-docs
description: Master Storybook documentation for component development, design systems, and living documentation. Use when creating stories, autodocs, MDX documentation, or building comprehensive design system documentation.
model-hint: sonnet
---

# Storybook Documentation Mastery

Create comprehensive, living documentation for UI components using Storybook. Transform components into interactive documentation with stories, autodocs, and MDX pages.

## Core Philosophy

Storybook enables **living documentation**—interactive documentation that stays in sync with components. Stories capture component states, autodocs generate documentation automatically, and MDX provides flexible narrative documentation.

## When to Use This Skill

Activate when user mentions:
- "storybook" or "stories"
- Component documentation or design systems
- "autodocs" or "MDX"
- Writing component examples or documentation
- Building UI component libraries
- Testing component states and interactions

## Supported Frameworks

React, Vue, Angular, Svelte, Solid, Web Components, and others. Documentation examples use React syntax but apply to all frameworks.

## Core Concepts

### Component Story Format (CSF)

Stories capture rendered states of UI components:

```typescript
// Button.stories.ts
const meta = {
  component: Button,
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    label: 'Button',
  },
};
```

**Key elements**:
- Default export (meta): component metadata
- Named exports: individual story states
- Args: component inputs for that state

### Autodocs

Automatic documentation generation from stories:

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'], // Enable autodocs
} satisfies Meta<typeof Button>;
```

Generates documentation page with:
- Description and source code
- Args table (component props)
- Controls (interactive playground)
- All stories for the component

### MDX Documentation

Flexible narrative documentation combining Markdown and JSX:

```mdx
import { Meta, Canvas, Controls, Stories } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Buttons trigger actions.

<Canvas of={ButtonStories.Primary} />
<Controls of={ButtonStories} />

## Usage

Use buttons for primary actions in your interface.
```

**Best for**: Complex component explanations, design guidelines, usage patterns.

### Controls

Dynamic UI for exploring component states without coding:

```typescript
const meta = {
  component: Button,
  argTypes: {
    variant: {
      options: ['primary', 'secondary', 'danger'],
      control: 'radio',
    },
    size: {
      options: ['small', 'medium', 'large'],
      control: 'select',
    },
  },
} satisfies Meta<typeof Button>;
```

**Benefits**:
- Test component states interactively
- Explore edge cases dynamically
- Generate new stories from control states

### Actions

Test event handlers and callbacks:

```typescript
import { fn } from '@storybook/test';

const meta = {
  component: Button,
  args: {
    onClick: fn(), // Spy function
  },
} satisfies Meta<typeof Button>;
```

When button is clicked, action appears in Actions panel with arguments.

## Documentation Workflow

### 1. Write Stories First

Create comprehensive stories covering all component states:

```typescript
export const Primary: Story = {};
export const Secondary: Story = {};
export const Danger: Story = {};
export const Disabled: Story = {};
export const WithIcon: Story = {};
export const LongText: Story = {};
export const Small: Story = {};
export const Large: Story = {};
```

**Goal**: Every component state, variant, and edge case has a story.

### 2. Enable Autodocs

Add `tags: ['autodocs']` to component meta:

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'],
} satisfies Meta<typeof Button>;
```

**Result**: Automatic documentation page with args tables, stories, and controls.

### 3. Add MDX for Complex Components

For components needing detailed explanation:

```mdx
import { Meta, Canvas, Controls } from '@storybook/addon-docs/blocks';

<Meta title="Examples/Button" />

# Button Component

Buttons trigger actions. Use primary buttons for main actions.

<Canvas of={ButtonStories.Primary} />

## Best Practices

- Use one primary button per section
- Group related actions
```

### 4. Configure Controls

Define which props are editable:

```typescript
const meta = {
  component: Button,
  argTypes: {
    variant: { control: 'radio' },
    size: { control: 'select' },
    disabled: { control: 'boolean' },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Button>;
```

### 5. Test with Actions

Verify event handlers work correctly:

```typescript
export const Clickable: Story = {
  args: {
    onClick: fn(),
  },
  play: async ({ canvasElement, userEvent }) => {
    const button = canvasElement.querySelector('button');
    await userEvent.click(button);
    expect(onClick).toHaveBeenCalled();
  },
};
```

## Control Types

| Data Type | Control Types | Usage |
|-----------|---------------|-------|
| `boolean` | `boolean` | Toggle switch |
| `number` | `number`, `range` | Numeric input, slider |
| `string` | `text`, `color`, `date` | Text input, color picker, date picker |
| `enum` | `radio`, `select`, `check` | Single/multiple selection |
| `object` | `object` | JSON editor |

## File Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.ts
│   │   ├── Button.test.ts
│   │   └── Button.css
│   └── Form/
│       ├── Form.tsx
│       ├── Form.stories.ts
│       └── Form.mdx        # Complex component documentation
```

**Co-location**: Keep stories next to components.

## Design System Documentation

### Component Categories

Organize components by function in sidebar:

```typescript
// Form.stories.ts
const meta = {
  component: Form,
  title: 'Components/Forms/Form', // Sidebar grouping
} satisfies Meta<typeof Form>;
```

### Subcomponents

Document related components together:

```typescript
const meta = {
  component: List,
  subcomponents: { ListItem },
} satisfies Meta<typeof List>;
```

Autodocs shows both List and ListItem documentation.

### Documentation Pages

Create standalone MDX pages for guidelines:

```mdx
<!-- design-system/GettingStarted.mdx -->
import { Meta } from '@storybook/addon-docs/blocks';

<Meta title="Design System/Getting Started" />

# Getting Started

Learn how to use our design system components...
```

## Best Practices

### DO

- **Write stories first** while building components
- **Cover all states**: default, hover, active, disabled, error
- **Use args** instead of React Hooks for story data
- **Spread args** onto components: `<Button {...args} />`
- **Reuse story data** across component hierarchies
- **Name stories clearly**: Primary, Disabled, WithIcon
- **Enable autodocs** for automatic documentation
- **Add MDX** for complex components needing explanation

### DON'T

- Don't skip edge case stories (empty states, errors, loading)
- Don't use Hooks for component state in stories
- Don't hardcode props without using args
- Don't create stories without autodocs
- Don't write MDX for simple components (autodocs suffices)
- Don't forget action handlers for interactive components
- Don't mix component logic in story files

## Testing Integration

### Interaction Tests

Test component behavior using play functions:

```typescript
export const SubmitForm: Story = {
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.click(canvas.getByRole('button'));
    await expect(canvas.getByText('Success')).toBeInTheDocument();
  },
};
```

### Visual Regression Tests

Combine Storybook with visual testing tools (Chromatic, Percy) to catch visual changes.

## Supporting Resources

- **Writing Stories**: See `references/writing-stories.md`
- **Autodocs Guide**: See `references/autodocs-guide.md`
- **MDX Documentation**: See `references/mdx-documentation.md`
- **Controls & Actions**: See `references/controls-and-actions.md`
- **Best Practices**: See `references/best-practices.md`
- **Story Templates**: See `assets/story-templates.md`
- **Quality Checklist**: See `assets/documentation-checklist.md`

## Common Issues

**Autodocs not appearing**: Add `tags: ['autodocs']` to component meta

**Controls not working**: Add `component` to meta for automatic inference, or define argTypes manually

**Actions not firing**: Use `fn()` from `@storybook/test` instead of automatic action matching

**MDX parse errors**: Add blank lines between Markdown and JSX blocks

**Stories not in sidebar**: Check file naming matches pattern `*.stories.@(js|jsx|ts|tsx)`

## Official Resources

- Storybook Docs: https://storybook.js.org/docs
- Writing Stories: https://storybook.js.org/docs/writing-stories
- Autodocs: https://storybook.js.org/docs/writing-docs/autodocs
- MDX Format: https://storybook.js.org/docs/writing-docs/mdx
- Controls: https://storybook.js.org/docs/essentials/controls
- Actions: https://storybook.js.org/docs/essentials/actions
