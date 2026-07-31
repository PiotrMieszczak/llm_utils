# Storybook Autodocs: Complete Guide

Comprehensive guide to automatic documentation generation in Storybook.

## What Is Autodocs?

Autodocs transforms your stories into **living documentation** by automatically generating comprehensive documentation pages for UI components. It extracts metadata like `args`, `argTypes`, and `parameters` to create documentation pages positioned at the root-level of your component tree in the sidebar.

### Key Benefits

- **Zero configuration**: Works out of the box with CSF stories
- **Always in sync**: Documentation updates automatically as components change
- **Interactive**: Users can explore component states live
- **Comprehensive**: Extracts props, descriptions, stories, and controls

## Enabling Autodocs

### Global Enablement (Recommended)

Enable autodocs for all components by adding the `autodocs` tag in `.storybook/preview.js|ts`:

```typescript
// .storybook/preview.ts
const preview: Preview = {
  tags: ['autodocs'],
};

export default preview;
```

**Result**: Every component with stories gets an auto-generated documentation page.

### Per-Component Enablement

Add the `autodocs` tag to individual component metadata:

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'],
} satisfies Meta<typeof Button>;
```

**Use case**: When only certain components need autodocs.

### Disabling Autodocs

For components where autodocs aren't needed:

```typescript
const meta = {
  component: Page,
  tags: ['!autodocs'], // Negation syntax
} satisfies Meta<typeof Page>;
```

**Common exclusions**:
- Layout/page components
- Internal utility components
- Deprecated components

## What Autodocs Generates

### Documentation Page Structure

For a component with autodocs enabled, Storybook generates a page with:

1. **Title**: Component name from meta
2. **Description**: Component description (extracted from JSDoc or source)
3. **Source Code**: Rendered component code
4. **Args Table**: All component props with types and descriptions
5. **Controls**: Interactive playground for exploring states
6. **Stories**: All stories for the component rendered inline

### Example Output

For a `Button` component, autodocs generates:

```
# Button

Buttons trigger actions. Use for primary actions in your interface.

## Source

<Button variant="primary" label="Click me" />

## Args Table

| Name | Description | Default | Control |
|------|-------------|---------|---------|
| variant | Button style variation | 'primary' | Radio |
| label | Button text | 'Button' | Text |
| disabled | Disable interaction | false | Boolean |
| size | Button size | 'medium' | Select |

## Stories

- Primary
- Secondary
- Danger
- Disabled

## Controls

[Interactive controls panel]
```

## Configuration Options

### Main Configuration

Configure autodocs in `.storybook/main.js|ts`:

```typescript
const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    {
      name: '@storybook/addon-docs',
      options: {
        defaultName: 'Docs', // Rename documentation page
        docsMode: false,     // Enable docs-only sidebar mode
      },
    },
  ],
};
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `defaultName` | string | 'Docs' | Renames the auto-generated documentation page |
| `docsMode` | boolean | false | Toggles documentation-only mode in the sidebar |

### Docs Mode

Enable `docsMode: true` to show only documentation pages in the sidebar (hides individual stories):

```typescript
{
  name: '@storybook/addon-docs',
  options: {
    docsMode: true, // Only show Docs pages, not individual stories
  },
}
```

**Use case**: When you want documentation-first navigation.

## Customizing Autodocs

### Custom Page Templates

Override the default autodocs template in `.storybook/preview.js|ts`:

```typescript
import { Title, Subtitle, Description, Primary, Controls, Stories } from '@storybook/blocks';

const preview: Preview = {
  parameters: {
    docs: {
      page: () => (
        <>
          <Title />
          <Subtitle />
          <Description />
          <Primary />
          <Controls />
          <Stories />
        </>
      ),
    },
  },
};
```

### Available Doc Blocks

Storybook provides pre-built blocks:

| Block | Description |
|-------|-------------|
| `Title` | Component name |
| `Subtitle` | Component subtitle |
| `Description` | Component description from JSDoc or description parameter |
| `Primary` | Primary story (first story) |
| `Controls` | Interactive controls playground |
| `Stories` | All stories rendered inline |
| `Canvas` | Render story in canvas iframe |

### Conditional Block Rendering

Show/hide blocks based on metadata:

```typescript
import { Meta, Canvas, Controls, Story } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Custom Button Layout

<Canvas of={ButtonStories.Primary} />

<Controls of={ButtonStories} />

{ButtonStories.parameters?.includeActions && (
  <div>
    <h3>Actions</h3>
    <Canvas of={ButtonStories.WithActions} />
  </div>
)}
```

## Table of Contents

### Enable TOC

Add table of contents to documentation pages:

```typescript
const preview: Preview = {
  parameters: {
    docs: {
      toc: true, // Enable table of contents
    },
  },
};
```

### TOC Customization

Configure TOC behavior:

```typescript
parameters: {
  docs: {
    toc: {
      contentsSelector: '.sbdocs', // CSS selector for heading container
      headingSelector: 'h2, h3',    // Headings to include
      ignoreSelector: '.sb-ignore', // Headings/stories to exclude
      title: 'Contents',             // TOC caption
      disable: false,               // Hide TOC
    },
  },
}
```

### Exclude Headings

Mark headings to exclude from TOC:

```html
<h2 class="sb-ignore">Internal Notes</h2>
```

## Subcomponents

### Documenting Related Components

Use the `subcomponents` property to document related components together:

```typescript
import { List } from './List';
import { ListItem } from './ListItem';

const meta = {
  component: List,
  subcomponents: { ListItem },
} satisfies Meta<typeof List>;
```

**Result**: Autodocs shows both List and ListItem documentation on the same page.

### Nested Subcomponents

Document hierarchies:

```typescript
const meta = {
  component: Menu,
  subcomponents: {
    MenuItem,
    MenuSeparator,
    MenuGroup,
  },
} satisfies Meta<typeof Menu>;
```

### When to Use Subcomponents

**Good use cases**:
- Parent-child components (List/ListItem, Menu/MenuItem)
- Component families (Table/TableCell/TableRow)
- Composite components (Form/Input/Label/Select)

**Avoid**:
- Unrelated components
- Components used across multiple contexts
- Utility components

## Docs Container Customization

### Custom Container Component

Replace the default docs container:

```typescript
import CustomDocsContainer from './CustomDocsContainer';

const preview: Preview = {
  parameters: {
    docs: {
      container: CustomDocsContainer,
    },
  },
};
```

**Custom container example**:

```typescript
import { DocsContainer as BaseContainer } from '@storybook/addon-docs';

export const DocsContainer = ({ children, context }) => {
  return (
    <div style={{ background: context?.theme?.base === 'dark' ? '#333' : '#fff' }}>
      <BaseContainer context={context}>{children}</BaseContainer>
    </div>
  );
};
```

## Theme Override

### Apply Custom Theme

Override docs theme for specific stories:

```typescript
import { themes, ensure } from '@storybook/theming';

const meta = {
  component: Button,
  parameters: {
    docs: {
      theme: ensure(themes.dark), // Force dark theme
    },
  },
} satisfies Meta<typeof Button>;
```

### Custom Theme Configuration

Create custom theme:

```typescript
import { create } from '@storybook/theming';

const customTheme = create({
  base: 'light',
  brandTitle: 'My Storybook',
  brandUrl: 'https://example.com',
  brandImage: '/logo.png',
  // ... other theme properties
});

const preview: Preview = {
  parameters: {
    docs: {
      theme: customTheme,
    },
  },
};
```

## Description Sources

Autodocs extracts component descriptions from multiple sources:

### 1. JSDoc Comments (Recommended)

```typescript
/**
 * Buttons trigger actions. Use for primary actions in your interface.
 *
 * Supports multiple variants: primary, secondary, danger.
 */
export const Button = ({ variant, label, ...props }) => {
  return <button className={`btn btn-${variant}`} {...props}>{label}</button>;
};
```

### 2. Description Parameter

```typescript
const meta = {
  component: Button,
  parameters: {
    docs: {
      description: {
        component: 'Buttons trigger actions. Use for primary actions.',
      },
    },
  },
} satisfies Meta<typeof Button>;
```

### 3. Story Descriptions

```typescript
export const Primary: Story = {
  args: { variant: 'primary' },
  parameters: {
    docs: {
      description: {
        story: 'Primary button for main actions',
      },
    },
  },
};
```

### 4. MDX Imports

For MDX files, the first paragraph becomes the description:

```mdx
import { Meta } from '@storybook/addon-docs/blocks';

<Meta title="Example/Button" />

# Button

Buttons trigger actions. Use this for primary actions.

The primary button should be used sparingly for the most important action.
```

## Args Table

### What Is the Args Table?

The args table displays component props with:
- **Name**: Prop name
- **Description**: Prop description (from JSDoc or argTypes)
- **Default**: Default value
- **Control**: Interactive control type

### Customizing Args Table

Control which props appear in the table:

```typescript
const meta = {
  component: Button,
  argTypes: {
    // Include specific props
    variant: { table: { category: 'Appearance' } },
    label: { table: { category: 'Content' } },

    // Exclude props
    internalProp: { table: { disable: true } },

    // Custom description
    onClick: {
      description: 'Callback when button is clicked',
      table: { type: { summary: 'function' } },
    },
  },
} satisfies Meta<typeof Button>;
```

### Args Table Configuration

```typescript
argTypes: {
  variant: {
    control: 'radio',
    options: ['primary', 'secondary', 'danger'],
    description: 'Button style variant',
    table: {
      category: 'Appearance',
      defaultValue: { summary: 'primary' },
      type: { summary: 'string' },
    },
  },
}
```

## Monorepo Configuration

### Import Components Directly

In monorepos, import components directly rather than through package index files:

```typescript
// ❌ Avoid (may have type inference issues)
import { Button } from '@my-org/ui-kit';

// ✅ Preferred (direct import)
import { Button } from '@my-org/ui-kit/src/components/Button';
```

### TypeScript Configuration

Add to `tsconfig.json` if needed:

```json
{
  "compilerOptions": {
    "reactDocgen": "react-docgen",
    "check": false
  }
}
```

## Best Practices

### DO

✅ Enable autodocs globally for consistency
✅ Write JSDoc comments for components and props
✅ Use `subcomponents` for related component groups
✅ Customize doc blocks for complex components
✅ Provide descriptions for all args
✅ Enable TOC for long documentation pages
✅ Use proper TypeScript types for better argTypes inference

### DON'T

❌ Disable autodocs without good reason
❌ Create manual docs when autodocs suffices
❌ Document unrelated components together
❌ Skip JSDoc comments (improves autodocs quality)
❌ Over-customize template (standard is good)

## Common Patterns

### Simple Component

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'],
} satisfies Meta<typeof Button>;
```

### Component with Custom Description

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Buttons trigger actions in your interface.',
      },
    },
  },
} satisfies Meta<typeof Button>;
```

### Component with Subcomponents

```typescript
const meta = {
  component: Select,
  tags: ['autodocs'],
  subcomponents: { SelectOption, SelectGroup },
} satisfies Meta<typeof Select>;
```

## Troubleshooting

### Autodocs Not Appearing

**Cause**: `tags: ['autodocs']` not added
**Solution**: Add tag to meta or enable globally in preview

### Args Table Empty

**Cause**: Component missing type annotations or JSDoc
**Solution**: Add TypeScript types or JSDoc comments

### Incorrect Type Inference

**Cause**: Complex types or generics
**Solution**: Manually define argTypes

### Subcomponents Not Showing

**Cause**: Subcomponents not imported or defined
**Solution**: Import and add to `subcomponents` property

### TOC Not Generating

**Cause**: No headings or incorrect heading selector
**Solution**: Add `h2`/`h3` headings or configure `headingSelector`

## Advanced Topics

### Programmatic Doc Block Usage

Use doc blocks in MDX for fine-grained control:

```mdx
import { Canvas, Controls, Title, Description } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Title />
<Description />

## Examples

<Canvas of={ButtonStories.Primary} />
<Canvas of={ButtonStories.Secondary} />

## Props

<Controls />
```

### Multiple Component Docs

Document multiple components in one MDX file:

```mdx
import { Meta, Canvas, Story } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';
import * as LinkStories from './Link.stories';

<Meta title="Design System/Actions" />

# Action Components

Buttons and links for user interactions.

## Buttons

<Canvas of={ButtonStories.Primary} />

## Links

<Canvas of={LinkStories.Default} />
```

## Resources

- **Official Autodocs Docs**: https://storybook.js.org/docs/writing-docs/autodocs
- **Doc Blocks Reference**: https://storybook.js.org/docs/writing-docs/doc-blocks
- **Docs Page Customization**: https://storybook.js.org/docs/writing-docs/docs-page
