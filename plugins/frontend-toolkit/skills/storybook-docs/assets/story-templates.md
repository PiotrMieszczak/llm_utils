# Storybook Story Templates

Ready-to-use templates for common component types. Copy and adapt these for your components.

## Basic Component Story Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

/**
 * Add component description here.
 *
 * - When to use it
 * - Key behaviors
 * - Accessibility notes
 */
const meta = {
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    // Customize controls here
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default state description
 */
export const Default: Story = {
  args: {
    prop: 'value',
  },
};

/**
 * Variant description
 */
export const VariantName: Story = {
  args: {
    prop: 'value',
  },
};
```

## Button Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button } from './Button';

const meta = {
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'radio',
      options: ['primary', 'secondary', 'danger', 'ghost'],
      description: 'Button style variant',
    },
    size: {
      control: 'radio',
      options: ['small', 'medium', 'large'],
      description: 'Button size',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable button interaction',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading spinner',
    },
    onClick: {
      action: 'clicked',
      description: 'Callback when button is clicked',
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Primary button for main actions
 */
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

/**
 * Secondary button for alternative actions
 */
export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

/**
 * Danger button for destructive actions
 */
export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Delete',
  },
};

/**
 * Ghost button for subtle actions
 */
export const Ghost: Story = {
  args: {
    variant: 'ghost',
    children: 'Cancel',
  },
};

/**
 * Disabled button state
 */
export const Disabled: Story = {
  args: {
    variant: 'primary',
    disabled: true,
    children: 'Disabled',
  },
};

/**
 * Loading state
 */
export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Loading...',
  },
};

/**
 * Small button
 */
export const Small: Story = {
  args: {
    variant: 'primary',
    size: 'small',
    children: 'Small',
  },
};

/**
 * Large button
 */
export const Large: Story = {
  args: {
    variant: 'primary',
    size: 'large',
    children: 'Large',
  },
};

/**
 * Button with icon
 */
export const WithIcon: Story = {
  args: {
    variant: 'primary',
    children: (
      <>
        <Icon name="star" />
        With Icon
      </>
    ),
  },
};

/**
 * Button with very long text
 */
export const LongText: Story = {
  args: {
    variant: 'primary',
    children: 'This is a very long button label that might wrap to multiple lines',
  },
};
```

## Input Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Input } from './Input';

const meta = {
  component: Input,
  tags: ['autodocs'],
  argTypes: {
    label: {
      control: 'text',
      description: 'Input label',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text',
    },
    value: {
      control: 'text',
      description: 'Input value',
    },
    error: {
      control: 'text',
      description: 'Error message',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable input',
    },
    required: {
      control: 'boolean',
      description: 'Mark as required',
    },
    onChange: {
      action: 'changed',
      description: 'Callback when value changes',
    },
    onFocus: {
      action: 'focused',
      description: 'Callback when input is focused',
    },
    onBlur: {
      action: 'blurred',
      description: 'Callback when input loses focus',
    },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default input state
 */
export const Default: Story = {
  args: {
    label: 'Email',
    placeholder: 'Enter your email',
  },
};

/**
 * Input with value
 */
export const WithValue: Story = {
  args: {
    label: 'Email',
    value: 'user@example.com',
  },
};

/**
 * Input with error
 */
export const WithError: Story = {
  args: {
    label: 'Email',
    value: 'invalid-email',
    error: 'Please enter a valid email address',
  },
};

/**
 * Disabled input
 */
export const Disabled: Story = {
  args: {
    label: 'Email',
    value: 'user@example.com',
    disabled: true,
  },
};

/**
 * Required input
 */
export const Required: Story = {
  args: {
    label: 'Email',
    placeholder: 'Enter your email',
    required: true,
  },
};

/**
 * Input without label
 */
export const WithoutLabel: Story = {
  args: {
    placeholder: 'Search...',
  },
};

/**
 * Input with long text
 */
export const WithLongText: Story = {
  args: {
    label: 'Description',
    value: 'This is a very long input value that might exceed the typical length',
  },
};
```

## Modal/Dialog Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Modal } from './Modal';

const meta = {
  component: Modal,
  tags: ['autodocs'],
  argTypes: {
    open: {
      control: 'boolean',
      description: 'Control modal visibility',
    },
    title: {
      control: 'text',
      description: 'Modal title',
    },
    size: {
      control: 'radio',
      options: ['small', 'medium', 'large', 'full'],
      description: 'Modal size',
    },
    onClose: {
      action: 'closed',
      description: 'Callback when modal is closed',
    },
    onConfirm: {
      action: 'confirmed',
      description: 'Callback when confirm button clicked',
    },
  },
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Open modal with content
 */
export const Open: Story = {
  args: {
    open: true,
    title: 'Confirm Action',
    children: 'Are you sure you want to proceed?',
  },
};

/**
 * Small modal
 */
export const Small: Story = {
  args: {
    open: true,
    title: 'Quick Action',
    size: 'small',
    children: 'This is a small modal for quick actions.',
  },
};

/**
 * Large modal
 */
export const Large: Story = {
  args: {
    open: true,
    title: 'Detailed View',
    size: 'large',
    children: 'This modal has more space for content.',
  },
};

/**
 * Modal with long content
 */
export const LongContent: Story = {
  args: {
    open: true,
    title: 'Terms of Service',
    size: 'large',
    children: (
      <>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        <p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        {/* Add more paragraphs */}
      </>
    ),
  },
};

/**
 * Closed modal (not visible)
 */
export const Closed: Story = {
  args: {
    open: false,
    title: 'Hidden Modal',
  },
};
```

## Table Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Table } from './Table';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const meta = {
  component: Table,
  tags: ['autodocs'],
  argTypes: {
    data: {
      control: 'object',
      description: 'Table data array',
    },
    columns: {
      control: 'object',
      description: 'Column definitions',
    },
    sortable: {
      control: 'boolean',
      description: 'Enable sorting',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading state',
    },
  },
} satisfies Meta<typeof Table<User>>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleData: User[] = [
  { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
  { id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'User' },
  { id: 3, name: 'Carol Williams', email: 'carol@example.com', role: 'User' },
];

const columns = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'role', label: 'Role', sortable: true },
];

/**
 * Table with sample data
 */
export const Default: Story = {
  args: {
    data: sampleData,
    columns,
  },
};

/**
 * Empty table
 */
export const Empty: Story = {
  args: {
    data: [],
    columns,
  },
};

/**
 * Loading table
 */
export const Loading: Story = {
  args: {
    data: [],
    columns,
    loading: true,
  },
};

/**
 * Table with many rows
 */
export const ManyRows: Story = {
  args: {
    data: Array.from({ length: 50 }, (_, i) => ({
      id: i,
      name: `User ${i}`,
      email: `user${i}@example.com`,
      role: i % 3 === 0 ? 'Admin' : 'User',
    })),
    columns,
  },
};

/**
 * Table with long content
 */
export const LongContent: Story = {
  args: {
    data: [
      {
        id: 1,
        name: 'A'.repeat(100),
        email: 'very-long-email-address@example.com',
        role: 'Administrator with extensive permissions',
      },
    ],
    columns,
  },
};
```

## Form Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Form } from './Form';

const meta = {
  component: Form,
  tags: ['autodocs'],
  argTypes: {
    onSubmit: {
      action: 'submitted',
      description: 'Callback when form is submitted',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading state',
    },
  },
} satisfies Meta<typeof Form>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default form with all fields
 */
export const Default: Story = {
  args: {
    children: (
      <>
        <FormField name="name" label="Name" required />
        <FormField name="email" label="Email" type="email" required />
        <FormField name="message" label="Message" multiline />
        <Button type="submit">Submit</Button>
      </>
    ),
  },
};

/**
 * Form with validation errors
 */
export const WithErrors: Story = {
  args: {
    children: (
      <>
        <FormField name="name" label="Name" required error="Name is required" />
        <FormField name="email" label="Email" type="email" error="Invalid email format" />
        <Button type="submit">Submit</Button>
      </>
    ),
  },
};

/**
 * Form in loading state
 */
export const Loading: Story = {
  args: {
    loading: true,
    children: (
      <>
        <FormField name="name" label="Name" />
        <FormField name="email" label="Email" type="email" />
        <Button type="submit" loading>Submit</Button>
      </>
    ),
  },
};

/**
 * Compact form with horizontal layout
 */
export const Compact: Story = {
  args: {
    layout: 'horizontal',
    children: (
      <>
        <FormField name="search" label="Search" />
        <Button type="submit">Search</Button>
      </>
    ),
  },
};
```

## List Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { List } from './List';
import { ListItem } from './ListItem';

const meta = {
  component: List,
  tags: ['autodocs'],
  subcomponents: { ListItem },
} satisfies Meta<typeof List>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * List with multiple items
 */
export const Default: Story = {
  render: (args) => (
    <List {...args}>
      <ListItem>Item 1</ListItem>
      <ListItem>Item 2</ListItem>
      <ListItem>Item 3</ListItem>
    </List>
  ),
};

/**
 * Empty list
 */
export const Empty: Story = {
  render: (args) => <List {...args} />,
};

/**
 * List with many items
 */
export const ManyItems: Story = {
  render: (args) => (
    <List {...args}>
      {Array.from({ length: 20 }, (_, i) => (
        <ListItem key={i}>Item {i}</ListItem>
      ))}
    </List>
  ),
};

/**
 * List with long content
 */
export const LongContent: Story = {
  render: (args) => (
    <List {...args}>
      <ListItem>{'A'.repeat(100)}</ListItem>
      <ListItem>Normal item</ListItem>
    </List>
  ),
};
```

## Card Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Card } from './Card';

const meta = {
  component: Card,
  tags: ['autodocs'],
  argTypes: {
    title: {
      control: 'text',
      description: 'Card title',
    },
    subtitle: {
      control: 'text',
      description: 'Card subtitle',
    },
    elevation: {
      control: 'radio',
      options: ['none', 'low', 'medium', 'high'],
      description: 'Card elevation/shadow',
    },
    clickable: {
      control: 'boolean',
      description: 'Make card clickable',
    },
  },
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default card with title and content
 */
export const Default: Story = {
  args: {
    title: 'Card Title',
    children: 'Card content goes here.',
  },
};

/**
 * Card with subtitle
 */
export const WithSubtitle: Story = {
  args: {
    title: 'Product Name',
    subtitle: '$99.99',
    children: 'Product description goes here.',
  },
};

/**
 * Clickable card
 */
export const Clickable: Story = {
  args: {
    title: 'Clickable Card',
    clickable: true,
    children: 'Click this card to trigger an action.',
  },
};

/**
 * Card with elevation
 */
export const WithElevation: Story = {
  args: {
    title: 'Elevated Card',
    elevation: 'high',
    children: 'This card has a strong shadow.',
  },
};

/**
 * Card with image
 */
export const WithImage: Story = {
  args: {
    title: 'Featured Image',
    children: (
      <>
        <img src="https://via.placeholder.com/400x200" alt="Placeholder" />
        <p>Card content with an image above.</p>
      </>
    ),
  },
};
```

## Loading Component Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Loading } from './Loading';

const meta = {
  component: Loading,
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: 'radio',
      options: ['small', 'medium', 'large'],
      description: 'Spinner size',
    },
    text: {
      control: 'text',
      description: 'Loading text message',
    },
  },
} satisfies Meta<typeof Loading>;

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Default loading spinner
 */
export const Default: Story = {};

/**
 * Small spinner
 */
export const Small: Story = {
  args: {
    size: 'small',
  },
};

/**
 * Large spinner
 */
export const Large: Story = {
  args: {
    size: 'large',
  },
};

/**
 * With loading text
 */
export const WithText: Story = {
  args: {
    text: 'Loading your data...',
  },
};
```

## Usage Instructions

1. **Copy the appropriate template** for your component type
2. **Replace placeholder names** with your actual component name
3. **Adapt props and argTypes** to match your component's API
4. **Add JSDoc comments** to describe each story
5. **Remove unnecessary stories** or add new ones as needed
6. **Add play functions** for interactive components
7. **Enable autodocs** (already included in templates)

## Customization Tips

- **Add custom decorators** for context providers or theme wrappers
- **Configure controls** to match your prop types
- **Add parameters** for backgrounds, viewport, layout
- **Include subcomponents** for composite components
- **Write play functions** for testing interactions
