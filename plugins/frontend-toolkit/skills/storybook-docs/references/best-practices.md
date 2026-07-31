# Storybook Documentation Best Practices

Comprehensive guide to creating high-quality, maintainable Storybook documentation for components and design systems.

## Documentation Philosophy

Good Storybook documentation is **living, interactive, and always in sync** with components. It serves multiple audiences:

- **Developers**: Understanding component API, props, and usage
- **Designers**: Exploring visual states and variants
- **QA**: Testing component behavior and edge cases
- **Stakeholders**: Reviewing UI implementation

## Core Principles

### 1. Stories First

Write stories **while building components**, not after.

**Why**:
- Stories serve as both documentation and tests
- Forces thinking about component states upfront
- Ensures all edge cases are handled
- Documentation stays in sync with development

**Bad**:
```typescript
// Build component first, write stories later
// Result: Missing edge cases, outdated docs
```

**Good**:
```typescript
// Write stories alongside component
// Result: Comprehensive coverage, living docs
export const Primary: Story = {};
export const Disabled: Story = {};
export const Error: Story = {};
export const Loading: Story = {};
```

### 2. Comprehensive Coverage

Document **all component states**, not just happy path.

**Required States**:
- Default state
- Interactive states (hover, active, focus)
- Variant states (primary, secondary, danger)
- Edge cases (empty, error, loading, disabled)
- Boundary conditions (long text, many items)

**Example**:
```typescript
export const Default: Story = {};
export const Hover: Story = {}; // If applicable
export const Active: Story = {};
export const Focus: Story = {};
export const Disabled: Story = {};
export const Error: Story = {};
export const Loading: Story = {};
export const Empty: Story = {};
export const WithLongText: Story = {};
```

### 3. Co-location

Keep stories **next to components** they document.

**Structure**:
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.ts
│   │   ├── Button.test.ts
│   │   └── button.css
│   └── Input/
│       ├── Input.tsx
│       └── Input.stories.ts
```

**Benefits**:
- Easy to find stories when working on component
- Stories stay in sync with changes
- Clear ownership and maintenance

### 4. Autodocs by Default

Enable autodocs **globally** for consistency.

```typescript
// .storybook/preview.ts
const preview: Preview = {
  tags: ['autodocs'],
};
```

**Result**: Every component automatically gets documentation page.

### 5. Clear Naming

Use **descriptive, UpperCamelCase** names for stories.

**Good**:
```typescript
export const Primary: Story = {};
export const Disabled: Story = {};
export const WithIcon: Story = {};
export const LongText: Story = {};
export const ErrorState: Story = {};
```

**Bad**:
```typescript
export const Story1: Story = {};
export const Test: Story = {};
export const Example: Story = {};
```

## Writing Effective Stories

### Component State Coverage

### Button Component

```typescript
// Variants
export const Primary: Story = { args: { variant: 'primary' } };
export const Secondary: Story = { args: { variant: 'secondary' } };
export const Danger: Story = { args: { variant: 'danger' } };

// States
export const Disabled: Story = { args: { disabled: true } };
export const Loading: Story = { args: { loading: true } };

// Sizes
export const Small: Story = { args: { size: 'small' } };
export const Medium: Story = { args: { size: 'medium' } };
export const Large: Story = { args: { size: 'large' } };

// With Children
export const WithIcon: Story = {
  args: {
    children: <><Icon name="star" /> Click Me</>,
  },
};

// Edge Cases
export const LongText: Story = {
  args: { label: 'This is a very long button label that might wrap' },
};
```

### Input Component

```typescript
// States
export const Default: Story = {};
export const Focused: Story = { /* Simulate focus */ };
export const Disabled: Story = { args: { disabled: true } };

// With Values
export const WithValue: Story = { args: { value: 'hello@example.com' } };

// Validation States
export const WithError: Story = { args: { error: 'Invalid email' } };
export const WithSuccess: Story = { args: { success: 'Email available' } };

// With Placeholders
export const WithPlaceholder: Story = {
  args: { placeholder: 'Enter your email' },
};

// With Labels
export const WithLabel: Story = {
  args: { label: 'Email Address' },
};
```

### Data Display Components

```typescript
// Empty State
export const Empty: Story = {
  args: { items: [] },
};

// Single Item
export const SingleItem: Story = {
  args: { items: [{ id: 1, name: 'Item 1' }] },
};

// Multiple Items
export const MultipleItems: Story = {
  args: {
    items: Array.from({ length: 5 }, (_, i) => ({
      id: i,
      name: `Item ${i}`,
    })),
  },
};

// Long Text
export const WithLongText: Story = {
  args: {
    items: [{ id: 1, name: 'A'.repeat(100) }],
  },
};

// Loading State
export const Loading: Story = {
  args: { loading: true },
};

// Error State
export const Error: Story = {
  args: { error: 'Failed to load items' },
};
```

## Documentation Quality Checklist

### Story Completeness

- [ ] All component variants documented
- [ ] All interactive states shown (hover, active, focus, disabled)
- [ ] Edge cases covered (empty, error, loading)
- [ ] Boundary conditions tested (long text, many items)
- [ ] Event handlers demonstrated with actions
- [ ] Props table complete with descriptions
- [ ] Component has JSDoc description

### Story Quality

- [ ] Stories use UpperCamelCase naming
- [ ] Story names are descriptive (Primary, Disabled, WithIcon)
- [ ] Args defined using object syntax (not functions)
- [ ] Args spread onto components: `{...args}`
- [ ] No React Hooks for state (use args instead)
- [ ] Actions use `fn()` from `@storybook/test`
- [ ] Play functions test interactive components

### Documentation

- [ ] Autodocs enabled (globally or per-component)
- [ ] Component has JSDoc comment
- [ ] All props have TypeScript types or JSDoc
- [ ] Complex components have MDX documentation
- [ ] Usage examples provided
- [ ] Design guidelines documented (if applicable)

### Organization

- [ ] Stories co-located with components
- [ ] File naming follows pattern: `*.stories.@(js|jsx|ts|tsx)`
- [ ] Sidebar organized with titles
- [ ] Related components grouped together
- [ ] Design system pages use consistent hierarchy

## Design System Documentation

### Component Organization

Organize components by category in sidebar:

```typescript
// Atoms
const meta = {
  component: Button,
  title: 'Design System/Atoms/Button',
} satisfies Meta<typeof Button>;

// Molecules
const meta = {
  component: FormField,
  title: 'Design System/Molecules/FormField',
} satisfies Meta<typeof FormField>;

// Organisms
const meta = {
  component: Navigation,
  title: 'Design System/Organisms/Navigation',
} satisfies Meta<typeof Navigation>;
```

### Design Guidelines Pages

Create MDX pages for design standards:

```mdx
<!-- .storybook/docs/DesignGuidelines.mdx -->
import { Meta, Canvas } from '@storybook/addon-docs/blocks';
import * as ButtonStories from '../src/components/Button/Button.stories';

<Meta title="Design System/Guidelines/Buttons" />

# Button Guidelines

## When to Use Buttons

Use buttons for actions that change data or navigate.

### Primary Buttons

Use for main action in a section.

<Canvas of={ButtonStories.Primary />

### Secondary Buttons

Use for alternative actions.

<Canvas of={ButtonStories.Secondary />

## Do's and Don'ts

✅ Do use clear, action-oriented labels
❌ Don't use vague labels like "Submit"
✅ Do show loading state for async actions
❌ Don't disable buttons without explanation
```

### Pattern Documentation

Document common UI patterns:

```mdx
<Meta title="Design System/Patterns/Form Submission" />

# Form Submission Pattern

Forms collect user input for actions.

## Structure

1. Clear labels for all fields
2. Required fields marked with asterisk
3. Inline validation messages
4. Primary submit button
5. Cancel option (secondary button)

## Example

<Canvas of={FormStories.WithValidation />
```

## Writing MDX Documentation

### When to Use MDX vs CSF

**Use CSF for**:
- Simple component examples
- Component state variants
- Interactive explorations
- Most component documentation

**Use MDX for**:
- Design guidelines and principles
- Usage instructions and tutorials
- Pattern documentation
- Complex component explanations
- Multi-component documentation

### MDX Best Practices

✅ Use blank lines between Markdown and JSX
✅ Reference story files in Meta blocks: `<Meta of={Stories} />`
✅ Leverage doc blocks for consistency
✅ Write descriptive headings
✅ Include code examples with syntax highlighting
✅ Embed stories for live examples
❌ Don't write component logic in MDX
❌ Don't mix Markdown and JSX without blank lines
❌ Don't create deeply nested JSX in MDX

### MDX Structure Template

```mdx
import { Meta, Canvas, Controls, Stories } from '@storybook/addon-docs/blocks';
import * as ComponentStories from './Component.stories';

<Meta of={ComponentStories} />

# Component Name

Brief description of component.

## When to Use

When you need to [use case].

## Basic Usage

<Canvas of={ComponentStories.Default} />

## Variants

### Variant 1

Description of variant 1.

<Canvas of={ComponentStories.Variant1} />

### Variant 2

Description of variant 2.

<Canvas of={ComponentStories.Variant2} />

## Props

<Controls of={ComponentStories} />

## Examples

### Example 1

Description.

<Canvas of={ComponentStories.Example1} />

## Best Practices

✅ Do this
❌ Don't do this
```

## Testing with Stories

### Interaction Tests

Add play functions to test interactions:

```typescript
export const Clickable: Story = {
  args: { onClick: fn() },
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);
    expect(onClick).toHaveBeenCalled();
  },
};
```

### Visual Regression Tests

Combine with visual testing tools:

```bash
# Chromatic
npx chromatic --project-token=xxx

# Percy
npm run build-storybook
percy storybook-static
```

### Accessibility Tests

Test accessibility in stories:

```typescript
export const Accessible: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await expect(button).toHaveAccessibleName();
    await expect(button).toBeVisible();
  },
};
```

## Maintenance

### Keeping Documentation in Sync

1. **Update stories when component changes**
   - Add new stories for new features
   - Update existing stories for behavior changes
   - Remove stories for removed features

2. **Review documentation regularly**
   - Check for outdated examples
   - Verify all edge cases are covered
   - Update design guidelines as patterns evolve

3. **Automate checks**
   - Run tests on every commit
   - Fail builds if stories don't compile
   - Use visual regression tests

### Deprecation Strategy

When deprecating components or props:

```typescript
const meta = {
  component: OldButton,
  tags: ['autodocs', 'deprecated'],
  parameters: {
    docs: {
      description: {
        component: '**Deprecated**: Use `NewButton` instead.',
      },
    },
  },
} satisfies Meta<typeof OldButton>;
```

## Performance

### Lazy Loading

Load heavy components on demand:

```typescript
export const HeavyComponent: Story = {
  render: () => {
    const Heavy = lazy(() => import('./Heavy'));
    return <Suspense fallback="Loading..."><Heavy /></Suspense>;
  },
};
```

### Story Organization

Split large story files:

```typescript
// Button.stories.ts - Core stories
export const Primary: Story = {};
export const Secondary: Story = {};

// Button.interactions.stories.ts - Interactive stories
export const Clickable: Story = {};
export const Hoverable: Story = {};
```

### Disable Autodocs for Internal Components

```typescript
const meta = {
  component: InternalComponent,
  tags: ['!autodocs'], // Don't generate docs
} satisfies Meta<typeof InternalComponent>;
```

## Common Anti-Patterns

### ❌ Stories After Development

```typescript
// Build component first
const Button = () => { /* ... */ };

// Write stories later (if at all)
// Result: Missing edge cases, incomplete docs
```

**Fix**: Write stories alongside component

### ❌ Skipping Edge Cases

```typescript
// Only happy path
export const Default: Story = {};

// Missing: Empty, Error, Loading, Disabled states
```

**Fix**: Cover all component states

### ❌ Using Hooks for State

```typescript
export const Interactive: Story = {
  render: () => {
    const [count, setCount] = useState(0);
    return <Button onClick={() => setCount(count + 1)}>Clicks: {count}</Button>;
  },
};
```

**Fix**: Use args, not Hooks

### ❌ Not Spreading Args

```typescript
export const Example: Story = {
  render: (args) => <Button variant={args.variant} label={args.label} />,
};
```

**Fix**: `<Button {...args} />`

### ❌ Vague Story Names

```typescript
export const Story1: Story = {};
export const Test: Story = {};
export const Example: Story = {};
```

**Fix**: Use descriptive names (Primary, Disabled, WithIcon)

## Resources

- **Storybook Best Practices**: https://storybook.js.org/docs/best-practices
- **Design Systems with Storybook**: https://storybook.js.org/docs/design-systems
- **Testing with Storybook**: https://storybook.js.org/docs/writing-tests
