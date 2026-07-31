# MDX Documentation in Storybook

Complete guide to writing narrative documentation with MDX (Markdown + JSX) in Storybook.

## What Is MDX?

MDX combines Markdown and JavaScript/JSX to create **interactive documentation**. You can write readable Markdown syntax while embedding components, stories, and interactive examples using JSX.

### MDX vs CSF

Storybook splits documentation into two complementary formats:

| Format | Best For | Example |
|--------|----------|---------|
| **CSF** (Component Story Format) | Defining component examples with type safety | `Button.stories.ts` |
| **MDX** | Narrative documentation, design guidelines, tutorials | `DesignGuidelines.mdx` |

**Key Insight**: CSF for component examples, MDX for explanations and patterns.

## Basic MDX Structure

### Minimal MDX File

```mdx
import { Meta } from '@storybook/addon-docs/blocks';

<Meta title="Design System/Getting Started" />

# Getting Started

Welcome to our design system documentation.
```

### Complete MDX File

```mdx
import { Meta, Canvas, Controls, Stories, Description } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button Component

Buttons trigger actions in your interface.

<Description of={ButtonStories} />

## Examples

<Canvas of={ButtonStories.Primary} />
<Canvas of={ButtonStories.Secondary} />

## Props

<Controls of={ButtonStories} />

## All Stories

<Stories of={ButtonStories} />
```

## File Organization

### MDX File Locations

MDX files can live anywhere in your stories directory:

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.stories.ts
│   └── Form/
│       ├── Form.tsx
│       ├── Form.stories.ts
│       └── Form.mdx          # Component-specific docs
└── docs/
    ├── Introduction.mdx      # Standalone documentation
    └── Patterns.mdx          # Pattern library
```

### Configure Storybook to Find MDX

```typescript
// .storybook/main.ts
const config: StorybookConfig = {
  stories: [
    '../src/**/*.mdx',                    // MDX files
    '../src/**/*.stories.@(js|jsx|ts|tsx)', // CSF files
  ],
  addons: ['@storybook/addon-docs'],
};

export default config;
```

## Meta Block

### What Is the Meta Block?

The Meta block controls sidebar placement and title for MDX pages.

### Referencing Story Files

Use `of` prop to reference existing stories:

```mdx
import { Meta } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button Component

...
```

**Result**: MDX page appears in same sidebar location as Button stories.

### Standalone MDX Pages

For standalone documentation (not tied to a component), omit `of`:

```mdx
import { Meta } from '@storybook/addon-docs/blocks';

<Meta title="Design System/Introduction" />

# Introduction

Welcome to our design system!
```

**Result**: Page appears at `Design System/Introduction` in sidebar.

### Custom Titles

Override auto-generated titles:

```mdx
<Meta title="Design System/Guidelines/Buttons" />
```

## Doc Blocks

Storybook provides pre-built components for displaying stories and component metadata.

### Meta

Controls sidebar placement and title:

```mdx
import { Meta } from '@storybook/addon-docs/blocks';

// Reference stories
<Meta of={ButtonStories} />

// Or standalone
<Meta title="Design System/Introduction" />
```

### Canvas

Render story in isolated canvas with code and controls:

```mdx
import { Canvas } from '@storybook/addon-docs/blocks';

<Canvas of={ButtonStories.Primary} />
```

**Options**:
- `of`: Story to render
- `state`: Initial state (from Controls)
- `sourceState`: Show/hide source code ('hidden', 'shown')

### Story

Render story without canvas frame:

```mdx
import { Story } from '@storybook/addon-docs/blocks';

<Story of={ButtonStories.Primary} />
```

**Use case**: Embed stories inline in documentation flow.

### Controls

Display interactive args table:

```mdx
import { Controls } from '@storybook/addon-docs/blocks';

<Controls of={ButtonStories} />
```

**Options**:
- `of`: Component or story to show controls for
- `sort`: Sort order ('alpha', 'requiredFirst', 'none')

### Stories

Render all stories for a component:

```mdx
import { Stories } from '@storybook/addon-docs/blocks';

<Stories of={ButtonStories} />
```

**Use case**: Show all component variants in one place.

### Title, Subtitle, Description

Display component metadata:

```mdx
import { Title, Subtitle, Description } from '@storybook/addon-docs/blocks';

<Title />
<Subtitle />
<Description of={ButtonStories} />
```

### Primary

Show primary (first) story:

```mdx
import { Primary } from '@storybook/addon-docs/blocks';

<Primary of={ButtonStories} />
```

## Markdown Syntax

### Standard Markdown

All standard Markdown syntax works:

```mdx
# Heading 1
## Heading 2
### Heading 3

**Bold text** and *italic text*

- List item 1
- List item 2
  - Nested item

1. Numbered list
2. Another item

[Link text](https://example.com)

`Inline code`

```
Code block
```

> Blockquote
```

### GitHub Flavored Markdown (GFM)

Enable tables and strikethrough:

```bash
npm install -D remark-gfm
```

Configure in `.storybook/main.ts`:

```typescript
import { remarkGfm } from 'remark-gfm';

const config: StorybookConfig = {
  addons: [
    {
      name: '@storybook/addon-docs',
      options: {
        mdxPluginOptions: {
          mdxCompileOptions: {
            remarkPlugins: [remarkGfm],
          },
        },
      },
    },
  ],
};
```

**Now you can use**:

```mdx
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

~~Strikethrough text~~
```

## Embedding Components

### Embed React Components

Import and use React components directly:

```mdx
import { Alert } from '../components/Alert';

<Alert type="info">
  This is an info alert embedded in MDX.
</Alert>
```

### Embed Stories

Reference stories by name:

```mdx
import { Story } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Story of={ButtonStories.Primary} />
<Story of={ButtonStories.Secondary} />
<Story of={ButtonStories.Danger} />
```

### Embed Multiple Components

```mdx
import { Button } from '../components/Button';
import { Icon } from '../components/Icon';

<Button variant="primary">
  <Icon name="star" />
  Primary Button
</Button>
```

## Code Blocks

### Syntax Highlighting

Storybook uses Prism for syntax highlighting:

````mdx
```javascript
function hello() {
  console.log('Hello, world!');
}
```
````

### With Titles

````mdx
```jsx title="Button.tsx"
export const Button = ({ children }) => {
  return <button>{children}</button>;
};
```
````

### Highlighted Lines

````mdx
```jsx {1,3-5}
const Primary = () => <Button variant="primary">Click</Button>;
const Secondary = () => <Button variant="secondary">Click</Button>;
const Danger = () => <Button variant="danger">Click</Button>;
```
````

## MDX Best Practices

### DO

✅ Use blank lines between Markdown and JSX blocks
✅ Reference story files (not components) in Meta blocks
✅ Leverage doc blocks for consistent UI
✅ Write descriptive headings and subheadings
✅ Enable GFM for tables and advanced Markdown
✅ Import components from relative paths
✅ Keep MDX files focused on narrative documentation

### DON'T

❌ Mix Markdown and JSX without blank lines
❌ Reference components directly in Meta blocks (use story files)
❌ Write component logic in MDX (keep in story files)
❌ Create deeply nested JSX in MDX
❌ Forget to import doc blocks
❌ Use MDX for simple component examples (use CSF)

## Block Separation

**Critical Rule**: MDX requires blank lines between blocks to distinguish where one language ends and another begins.

### Good Example

```mdx
import { Canvas } from '@storybook/addon-docs/blocks';

# Heading

This is markdown.

<Canvas of={ButtonStories.Primary} />

More markdown text.

<Canvas of={ButtonStories.Secondary} />
```

### Bad Example (Missing Blank Lines)

```mdx
import { Canvas } from '@storybook/addon-docs/blocks';
# Heading
This is markdown.
<Canvas of={ButtonStories.Primary} />
More markdown.
<Canvas of={ButtonStories.Secondary} />
```

**Result**: Parse errors, unexpected rendering.

## Common Patterns

### Component Documentation

```mdx
import { Meta, Canvas, Controls, Stories } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button Component

Buttons trigger actions in your interface.

## Basic Usage

<Canvas of={ButtonStories.Primary} />

## Variants

<Canvas of={ButtonStories.Secondary} />
<Canvas of={ButtonStories.Danger} />

## Props

<Controls of={ButtonStories} />

## All States

<Stories of={ButtonStories} />
```

### Design Guidelines

```mdx
import { Meta, Canvas } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta title="Design System/Buttons" />

# Button Guidelines

## When to Use Buttons

Use buttons for actions that change data or navigate.

<Canvas of={ButtonStories.Primary} />

### Primary Buttons

Use primary buttons for the main action in a section.

### Secondary Buttons

Use secondary buttons for alternative actions.

## Do's and Don'ts

✅ Do use clear, action-oriented labels
❌ Don't use vague labels like "Submit" without context
```

### Pattern Documentation

```mdx
import { Meta, Canvas } from '@storybook/addon-docs/blocks';
import * as FormStories from './Form.stories';

<Meta title="Patterns/Form Submission" />

# Form Submission Pattern

Forms collect user input for actions.

## Structure

1. Required fields marked with asterisk
2. Clear validation messages
3. Primary submit button
4. Cancel option

## Example

<Canvas of={FormStories.WithValidation} />
```

### Tutorial Documentation

```mdx
import { Meta, Canvas } from '@storybook/addon-docs/blocks';
import * as ButtonStories from './Button.stories';

<Meta title="Tutorials/Creating Buttons" />

# Creating Buttons

Learn how to use our Button component.

## Step 1: Import

```tsx
import { Button } from '@my-org/ui-kit';
```

## Step 2: Use

<Canvas of={ButtonStories.Primary} />

```tsx
<Button variant="primary">Click me</Button>
```

## Step 3: Customize

Try changing the variant:

<Canvas of={ButtonStories.Secondary} />
```

## Advanced Usage

### Custom Components in MDX

```mdx
import { Callout } from '../components/Callout';

<Callout type="warning">
  **Warning**: This is a custom callout component.
</Callout>
```

### Conditional Rendering

```mdx
import { useState } from 'react';

export const Example = () => {
  const [show, setShow] = useState(false);

  return (
    <>
      <button onClick={() => setShow(!show)}>Toggle</button>
      {show && <div>Conditional content</div>}
    </>
  );
};

<Example />
```

### Importing External Markdown

```mdx
import { Markdown } from '@storybook/addon-docs/blocks';

<Markdown>
# Content from external file

You can include markdown from other files.
</Markdown>
```

## Framework-Specific Notes

### React

MDX files in React Storybook render in React. All JSX works:

```mdx
import { MyComponent } from './MyComponent';

<MyComponent prop="value" />
```

### Vue

Vue components require special syntax:

```mdx
import { Meta, Canvas, Story } from '@storybook/addon-docs/blocks';
import MyButton from './MyButton.vue';

<Meta title="Example/Button" />

# Button Component

<Canvas>
  <Story name="Primary">
    {{ template: '<MyButton variant="primary">Click</MyButton>' }}
  </Story>
</Canvas>
```

### Angular

Angular components use similar template syntax:

```mdx
import { Meta, Canvas, Story } from '@storybook/addon-docs/blocks';
import { MyButton } from './MyButton.component';

<Meta title="Example/Button" />

<Canvas>
  <Story name="Primary">
    {{ template: '<app-my-button variant="primary">Click</app-my-button>' }}
  </Story>
</Canvas>
```

**Note**: MDX implementation renders documentation in React even for Vue/Angular stories.

## Troubleshooting

### Parse Error: "Unexpected token"

**Cause**: Missing blank line between Markdown and JSX
**Solution**: Add blank line before and after JSX blocks

### Component Not Rendering

**Cause**: Component not imported or incorrect path
**Solution**: Verify import path and component export

### Meta Block Not Working

**Cause**: Not referencing story file correctly
**Solution**: Use `import * as Stories from './Component.stories'`

### Doc Blocks Not Showing

**Cause**: Doc blocks not imported
**Solution**: Import from `@storybook/addon-docs/blocks`

### Tables Not Rendering

**Cause**: GFM plugin not installed
**Solution**: Install and configure `remark-gfm`

## Performance Tips

### Lazy Load Stories

Load stories only when needed:

```mdx
import { lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

### Split Large MDX Files

Break into smaller files with links:

```mdx
For more details, see [Advanced Usage](./AdvancedUsage.mdx).
```

### Avoid Heavy Components

Don't embed complex interactive demos in MDX. Use stories instead.

## Resources

- **Official MDX Docs**: https://storybook.js.org/docs/writing-docs/mdx
- **Doc Blocks Reference**: https://storybook.js.org/docs/writing-docs/doc-blocks
- **MDX Syntax**: https://mdxjs.com/docs/syntax
