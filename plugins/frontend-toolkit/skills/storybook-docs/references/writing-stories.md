# Writing Stories in Storybook: Comprehensive Guide

Complete guide to creating effective component stories using Component Story Format (CSF).

## What Is a Story?

A **story** captures a rendered state of a UI component. Think of it as a screenshot with code—a reusable, testable, and interactive example of how a component looks and behaves with specific arguments.

### Story Definition

"A story captures the rendered state of a UI component. It's an object with annotations that describe the component's behavior and appearance given a set of arguments."

**Key Characteristics**:
- **Reusable**: Stories can be embedded in docs, tests, and design tools
- **Testable**: Stories work with interaction testing and visual regression tools
- **Interactive**: All stories are live-editable via Controls addon

## Component Story Format (CSF)

CSF is the standard for writing stories in Storybook, based on ES6 modules.

### Basic Structure

Every story file requires:

1. **Default export** (meta): Component metadata
2. **Named exports** (stories): Individual component states

```typescript
// Button.stories.ts
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

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

### Anatomy of a Story File

```typescript
// 1. Imports
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

// 2. Meta (default export)
const meta = {
  component: Button,
  title: 'Components/Button', // Optional: overrides auto title
  tags: ['autodocs'],          // Enable autodocs
  argTypes: {                  // Customize controls
    variant: { control: 'radio' },
  },
} satisfies Meta<typeof Button>;

export default meta;

// 3. Story type
type Story = StoryObj<typeof meta>;

// 4. Story exports (named exports)
export const Primary: Story = {
  args: { variant: 'primary', label: 'Button' },
};

export const Secondary: Story = {
  args: { variant: 'secondary', label: 'Button' },
};
```

## File Organization

### Naming Convention

Story files use the `.stories.` extension followed by the language extension:

```
*.stories.js
*.stories.jsx
*.stories.ts
*.stories.tsx
*.stories.mdx
```

### Co-location Pattern

Keep stories next to components:

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.ts
│   │   ├── Button.test.ts
│   │   └── button.css
│   ├── Form/
│   │   ├── Form.tsx
│   │   └── Form.stories.ts
│   └── index.ts
```

**Benefits**:
- Easy to find stories when working on components
- Stories stay in sync with component changes
- Clear ownership and maintenance

### Alternative: Stories Directory

For large projects, organize stories in dedicated directory:

```
src/
├── components/
│   └── Button/
│       └── Button.tsx
└── stories/
    └── components/
        └── Button.stories.ts
```

Use this when:
- Component directories are crowded
- Multiple story sets per component
- Shared story utilities

## Story Export Types

### Named Exports (Recommended)

```typescript
export const Primary: Story = {
  args: { variant: 'primary' },
};

export const Secondary: Story = {
  args: { variant: 'secondary' },
};
```

**Default naming**: UpperCamelCase (Primary, Secondary, Disabled)

### Custom Names

Add a `name` property to customize sidebar display:

```typescript
export const VeryLongStateName: Story = {
  name: 'Default', // Shows as "Default" in sidebar
  args: { variant: 'primary' },
};
```

### Arrow Function Stories

For computed or dynamic args:

```typescript
export const DynamicState = () => ({
  args: {
    label: `Button ${Math.random()}`,
  },
});
```

**Use sparingly**: Prefer object syntax for better addon compatibility.

## Args: Component Arguments

### What Are Args?

Args are the input data passed to components. They represent the component's state for that story.

### Defining Args

```typescript
export const Primary: Story = {
  args: {
    variant: 'primary',
    label: 'Click me',
    disabled: false,
    onClick: fn(),
  },
};
```

### Default Args at Meta Level

Reuse args across all stories:

```typescript
const meta = {
  component: Button,
  args: {
    label: 'Default Label',
    disabled: false,
  },
} satisfies Meta<typeof Button>;

export const Primary: Story = {
  args: {
    ...meta.args, // Inherit defaults
    variant: 'primary',
  },
};
```

### Args Composition

Reuse and extend args from other stories:

```typescript
export const Primary: Story = {
  args: { variant: 'primary', label: 'Button' },
};

export const PrimaryWithIcon: Story = {
  args: {
    ...Primary.args,
    icon: '<StarIcon />',
  },
};
```

### Template Pattern

Create reusable render functions:

```typescript
const Template: Story = {
  render: (args) => <Button {...args} />,
};

export const Primary = Template.bind({});
Primary.args = { variant: 'primary' };

export const Secondary = Template.bind({});
Secondary.args = { variant: 'secondary' };
```

**Modern alternative**: Use object syntax (simpler and preferred).

## Custom Rendering

### Render Functions

Override default component rendering:

```typescript
export const WrappedInAlert: Story = {
  args: { variant: 'primary', label: 'Delete' },
  render: (args) => (
    <Alert type="warning">
      <p>Are you sure you want to delete?</p>
      <Button {...args} />
    </Alert>
  ),
};
```

**Use cases**:
- Wrap component in layout providers
- Add context providers
- Render multiple components together
- Test component in specific scenarios

### Render at Meta Level

Apply custom rendering to all stories:

```typescript
const meta = {
  component: Button,
  render: (args) => (
    <div style={{ margin: '2em' }}>
      <Button {...args} />
    </div>
  ),
} satisfies Meta<typeof Button>;
```

### Multi-Component Stories

For components with children, use custom render:

```typescript
export const ManyItems: Story = {
  render: (args) => (
    <List {...args}>
      <ListItem>Item 1</ListItem>
      <ListItem>Item 2</ListItem>
      <ListItem>Item 3</ListItem>
    </List>
  ),
};
```

## Decorators: Wrapping Components

### What Are Decorators?

Decorators wrap stories in arbitrary markup, enabling themes, layouts, or context providers.

### Story-Level Decorators

```typescript
export const WithTheme: Story = {
  args: { variant: 'primary' },
  decorators: [
    (Story) => (
      <ThemeProvider theme={darkTheme}>
        <Story />
      </ThemeProvider>
    ),
  ],
};
```

### Component-Level Decorators

Apply to all stories in a file:

```typescript
const meta = {
  component: Button,
  decorators: [
    (Story) => (
      <div style={{ padding: '3em', background: '#f5f5f5' }}>
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Button>;
```

### Global Decorators

Apply to all stories in `.storybook/preview.js|ts`:

```typescript
export const decorators = [
  (Story) => (
    <Provider store={store}>
      <Story />
    </Provider>
  ),
];
```

### Multiple Decorators

Decorators compose in order (outermost to innermost):

```typescript
decorators: [
  (Story) => <ThemeProvider><Story /></ThemeProvider>,
  (Story) => <div style={{ padding: '20px' }}><Story /></div>,
],
// Renders: <ThemeProvider><div style={{ padding: '20px' }}><Story /></div></ThemeProvider>
```

## Parameters: Addon Configuration

### What Are Parameters?

Parameters are static metadata for addons (backgrounds, viewport, layout, etc.).

### Story-Level Parameters

```typescript
export const OnDarkBackground: Story = {
  args: { variant: 'primary' },
  parameters: {
    backgrounds: {
      default: 'dark',
    },
  },
};
```

### Component-Level Parameters

```typescript
const meta = {
  component: Button,
  parameters: {
    layout: 'centered', // centered, fullscreen, padded
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#333333' },
      ],
    },
  },
} satisfies Meta<typeof Button>;
```

### Global Parameters

Configure in `.storybook/preview.js|ts`:

```typescript
const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on.*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
};
```

## Play Functions: Interaction Testing

### What Are Play Functions?

Play functions execute code after story renders, enabling interaction testing and component validation.

### Basic Play Function

```typescript
export const Clickable: Story = {
  args: {
    onClick: fn(),
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    await userEvent.click(button);
    expect(button).toHaveFocus();
  },
};
```

### Testing Library Integration

Storybook integrates with Testing Library:

```typescript
import { within, expect } from '@storybook/test';

export const FormSubmission: Story = {
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);

    // Fill form
    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(canvas.getByLabelText('Password'), 'password123');

    // Submit
    await userEvent.click(canvas.getByRole('button', { name: 'Submit' }));

    // Assert
    await expect(canvas.getByText('Success')).toBeInTheDocument();
  },
};
```

### Step Library for Complex Interactions

```typescript
export const MultiStepWorkflow: Story = {
  play: async ({ canvasElement, step }) => {
    const canvas = within(canvasElement);

    await step('Enter email', async () => {
      await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    });

    await step('Enter password', async () => {
      await userEvent.type(canvas.getByLabelText('Password'), 'password123');
    });

    await step('Submit form', async () => {
      await userEvent.click(canvas.getByRole('button'));
    });
  },
};
```

## Story Composition

### Reusing Story Data

Import and use story data from child components:

```typescript
// Form.stories.ts
import * as InputStories from './Input.stories';
import * as ButtonStories from './Button.stories';

export const PopulatedForm: Story = {
  render: (args) => (
    <Form {...args}>
      <Input {...InputStories.Valid.args} />
      <Button {...ButtonStories.Primary.args} />
    </Form>
  ),
};
```

### Story Building Blocks

Create base stories to extend:

```typescript
export const Base: Story = {
  args: {
    label: 'Button',
    disabled: false,
  },
};

export const Primary = {
  ...Base,
  args: { ...Base.args, variant: 'primary' },
};

export const Disabled = {
  ...Base,
  args: { ...Base.args, disabled: true },
};
```

## Framework-Specific Patterns

### React

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = { component: Button };
export default meta;

export const Primary: StoryObj<typeof Button> = {
  args: { variant: 'primary' },
};
```

### Vue

```typescript
import type { Meta, StoryObj } from '@storybook/vue3';
import MyButton from './Button.vue';

const meta: Meta<typeof MyButton> = {
  component: MyButton,
};

export default meta;
type Story = StoryObj<typeof MyButton>;

export const Primary: Story = {
  args: { label: 'Button', primary: true },
};
```

### Angular

```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { Button } from './button.component';

const meta: Meta<Button> = {
  component: Button,
  title: 'Button',
};

export default meta;
type Story = StoryObj<Button>;

export const Primary: Story = {
  args: {
    label: 'Button',
    variant: 'primary',
  },
};
```

### Web Components

```typescript
import type { Meta, StoryObj } from '@storybook/web-components';
import './my-button';

const meta: Meta = {
  title: 'Button',
  component: 'my-button',
};

export default meta;
type Story = StoryObj;

export const Primary: Story = {
  args: {
    label: 'Button',
    variant: 'primary',
  },
};
```

## Best Practices

### DO

✅ Write stories while building components (not after)
✅ Cover all component states (default, hover, active, disabled, error, loading)
✅ Use args instead of Hooks for story data
✅ Spread args onto components: `<Component {...args} />`
✅ Name stories clearly: Primary, Disabled, WithIcon
✅ Co-locate stories with components
✅ Enable autodocs for automatic documentation
✅ Add play functions for interactive components
✅ Reuse story data across component hierarchies

### DON'T

❌ Skip edge case stories (empty states, error states, loading states)
❌ Use React Hooks for component state in stories
❌ Hardcode props without using args
❌ Create deeply nested story structures
❌ Mix component logic in story files
❌ Forget to test event handlers with actions
❌ Write stories without autodocs

## Common Patterns

### Button Component Stories

```typescript
export const Primary: Story = {};
export const Secondary: Story = {};
export const Danger: Story = {};
export const Disabled: Story = { args: { disabled: true } };
export const WithIcon: Story = { args: { icon: '<Star />' } };
export const Small: Story = { args: { size: 'small' } };
export const Large: Story = { args: { size: 'large' } };
export const Loading: Story = { args: { loading: true } };
```

### Form Input Stories

```typescript
export const Default: Story = {};
export const WithValue: Story = { args: { value: 'hello@example.com' } };
export const WithError: Story = { args: { error: 'Invalid email' } };
export const Disabled: Story = { args: { disabled: true } };
export const WithPlaceholder: Story = { args: { placeholder: 'Enter email' } };
export const WithLabel: Story = { args: { label: 'Email Address' } };
```

### Data Display Stories

```typescript
export const Empty: Story = { args: { items: [] } };
export const SingleItem: Story = { args: { items: [{ id: 1, name: 'Item' }] } };
export const MultipleItems: Story = {
  args: { items: Array.from({ length: 5 }, (_, i) => ({ id: i, name: `Item ${i}` })) },
};
export const LongText: Story = {
  args: { items: [{ id: 1, name: 'A'.repeat(100) }] },
};
```

## Troubleshooting

### Story Not Showing in Sidebar

**Cause**: File doesn't match stories pattern
**Solution**: Ensure file matches `*.stories.@(js|jsx|ts|tsx)`

### Args Not Updating Component

**Cause**: Not spreading args onto component
**Solution**: Always use `<Component {...args} />`

### Play Function Failing

**Cause**: Testing Library queries incorrect
**Solution**: Use `within(canvasElement)` and verify selectors

### Decorator Not Applying

**Cause**: Decorator order incorrect
**Solution**: Outermost decorator first in array

### TypeScript Errors

**Cause**: Missing type imports
**Solution**: Import `Meta` and `StoryObj` from `@storybook/react`

## Advanced Topics

### Storybook Compositor

Combine multiple stories into composite pages:

```typescript
export const AllButtons: Story = {
  render: () => (
    <div>
      <Primary />
      <Secondary />
      <Danger />
    </div>
  ),
};
```

### Dynamic Story Generation

Generate stories programmatically:

```typescript
const sizes = ['small', 'medium', 'large'] as const;

export const Small: Story = { args: { size: 'small' } };
export const Medium: Story = { args: { size: 'medium' } };
export const Large: Story = { args: { size: 'large' } };
```

### Story Hierarchy

Organize stories with titles:

```typescript
const meta = {
  component: Button,
  title: 'Design System/Atoms/Button', // → Design System/Atoms/Button
} satisfies Meta<typeof Button>;
```

## Resources

- **Official Docs**: https://storybook.js.org/docs/writing-stories
- **CSF Documentation**: https://storybook.js.org/docs/api/csf
- **Testing Library**: https://storybook.js.org/docs/writing-tests/testing-library
