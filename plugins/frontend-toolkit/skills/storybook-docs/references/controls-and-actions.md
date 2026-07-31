# Storybook Controls and Actions: Interactive Documentation

Complete guide to using Controls for dynamic component exploration and Actions for event handler testing.

## Controls: Dynamic Component Exploration

### What Are Controls?

Controls provide a **graphical interface** for dynamically interacting with component arguments without coding. Edit story inputs through the Controls panel and see results in real-time.

### Key Benefits

- **Interactive Exploration**: Test component states dynamically
- **Edge Case Discovery**: Find unexpected behaviors by tweaking inputs
- **Story Generation**: Create new stories from control states
- **Documentation**: Live examples of component behavior

## How Controls Work

### Automatic Control Generation

Controls automatically generate UI based on component props:

```typescript
const meta = {
  component: Button,
  // No argTypes needed - auto-inferred from component
} satisfies Meta<typeof Button>;
```

**Requirements**: Add `component` to meta for automatic inference. Storybook uses tools like `react-docgen` to extract prop types.

### Manual Control Definition

Define controls explicitly:

```typescript
const meta = {
  component: Button,
  argTypes: {
    variant: {
      control: 'radio',
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
    disabled: {
      control: 'boolean',
    },
  },
} satisfies Meta<typeof Button>;
```

## Control Types

### Boolean Control

Toggle switch for boolean values:

```typescript
disabled: {
  control: 'boolean',
}
```

**UI**: Toggle switch

### Number Control

Numeric input with optional min/max/step:

```typescript
const meta = {
  component: Slider,
  argTypes: {
    value: {
      control: 'number',
      min: 0,
      max: 100,
      step: 5,
    },
  },
} satisfies Meta<typeof Slider>;
```

**UI**: Number input field

### Range Control

Slider for numeric values:

```typescript
value: {
  control: 'range',
  min: 0,
  max: 100,
  step: 1,
}
```

**UI**: Slider with drag handle

### Text Control

Text input for strings:

```typescript
label: {
  control: 'text',
}
```

**UI**: Text input field

### Color Control

Color picker with optional preset swatches:

```typescript
backgroundColor: {
  control: 'color',
  presetColors: ['#ff0000', '#00ff00', '#0000ff'],
}
```

**UI**: Color picker with swatches

### Date Control

Date picker for date values:

```typescript
dueDate: {
  control: 'date',
}
```

**UI**: Date input field

### Object Control

JSON editor for complex objects:

```typescript
user: {
  control: 'object',
}
```

**UI**: JSON editor with validation

### Enum Controls

For predefined options, use enum controls:

#### Radio

```typescript
variant: {
  control: 'radio',
  options: ['primary', 'secondary', 'danger'],
}
```

**UI**: Radio buttons (horizontal)

#### Inline Radio

```typescript
variant: {
  control: 'inline-radio',
  options: ['primary', 'secondary', 'danger'],
}
```

**UI**: Radio buttons (compact horizontal)

#### Select

```typescript
size: {
  control: 'select',
  options: ['small', 'medium', 'large'],
}
```

**UI**: Dropdown select

#### Multi-Select

```typescript
tags: {
  control: 'multi-select',
  options: ['tag1', 'tag2', 'tag3'],
}
```

**UI**: Multi-select dropdown

#### Check

```typescript
features: {
  control: 'check',
  options: ['feature1', 'feature2', 'feature3'],
}
```

**UI**: Checkboxes (vertical)

#### Inline Check

```typescript
flags: {
  control: 'inline-check',
  options: ['flag1', 'flag2'],
}
```

**UI**: Checkboxes (compact horizontal)

## Control Type Mapping

Storybook automatically chooses control types based on data:

| Initial Value | Inferred Control | Override To |
|---------------|------------------|-------------|
| `true`/`false` | boolean | - |
| `42` | number | number, range |
| `'text'` | text | text, color, date |
| `['a', 'b']` | check/select | radio, select, check |
| `{ a: 1 }` | object | object, file |

## Custom Control Matchers

Automatically match controls to arg names using regex:

```typescript
// .storybook/preview.ts
const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,    // Ends with "background" or "color"
        date: /Date$/,                    // Ends with "Date"
      },
    },
  },
};
```

**Result**: Props matching patterns get appropriate controls automatically.

## Control Configuration

### Per-Arg Configuration

```typescript
const meta = {
  component: Button,
  argTypes: {
    variant: {
      control: 'radio',
      options: ['primary', 'secondary', 'danger'],
      description: 'Button style variant',
      table: {
        category: 'Appearance',
        defaultValue: { summary: 'primary' },
      },
    },
  },
} satisfies Meta<typeof Button>;
```

### Global Configuration

Configure Controls addon behavior:

```typescript
// .storybook/preview.ts
const preview: Preview = {
  parameters: {
    controls: {
      expanded: true,          // Show full documentation
      presetColors: [         // Custom color swatches
        '#FF0000',
        '#00FF00',
        '#0000FF',
        { color: '#FFFFFF', title: 'White' },
      ],
      include: [/^on[A-Z]/],  // Only show matching args
      exclude: ['internal'],  // Hide specific args
      sort: 'alpha',          // 'none' | 'alpha' | 'requiredFirst'
      disableSaveFromUI: false, // Prevent creating stories from controls
    },
  },
};
```

### Sort Options

- **'none'**: Preserve definition order
- **'alpha'**: Alphabetical by name
- **'requiredFirst'**: Required props first, then alphabetical

## Conditional Controls

Show/hide controls based on other control values:

```typescript
const meta = {
  component: Form,
  argTypes: {
    showAdvanced: {
      control: 'boolean',
    },
    advancedOption: {
      control: 'text',
      if: { arg: 'showAdvanced' }, // Show only when showAdvanced is truthy
    },
  },
} satisfies Meta<typeof Form>;
```

### Query Operators

- **`truthy`**: Control shows when arg is truthy
- **`exists`**: Control shows when arg exists
- **`eq`**: Control shows when arg equals value
- **`neq`**: Control shows when arg doesn't equal value

### Complex Conditions

```typescript
settings: {
  control: 'object',
  if: { arg: 'mode', eq: 'advanced' },
}
```

## Actions: Event Handler Testing

### What Are Actions?

Actions verify when event handlers (callbacks) are invoked and inspect their arguments. The Actions panel displays callback invocations with arguments.

### Using fn() Spies (Recommended)

Create mock functions from `@storybook/test`:

```typescript
import { fn } from '@storybook/test';

const meta = {
  component: Button,
  args: {
    onClick: fn(), // Spy function
  },
} satisfies Meta<typeof Button>;
```

**Benefits**:
- Works with interaction tests (play functions)
- Spy functions available in test code
- Integrates with Testing Library

### Automatic Argument Matching

Auto-create actions for matching arg names:

```typescript
// .storybook/preview.ts
const preview: Preview = {
  parameters: {
    actions: {
      argTypesRegex: '^on.*', // Match all props starting with "on"
    },
  },
};
```

**Result**: `onClick`, `onSubmit`, `onChange` all become actions automatically.

**⚠️ Not Recommended**: For stories with play functions, automatically inferred args aren't available as spies. Use `fn()` instead.

### Action() Function

Legacy method (not recommended):

```typescript
import { action } from '@storybook/addon-actions';

const meta = {
  component: Button,
  args: {
    onClick: action('clicked'), // Deprecated
  },
} satisfies Meta<typeof Button>;
```

**Use `fn()` instead**: Better integration with modern testing.

## Action Configuration

### Per-Story Actions

```typescript
export const WithActions: Story = {
  args: {
    onClick: fn(),
    onChange: fn(),
    onSubmit: fn(),
  },
};
```

### Meta-Level Actions

Apply to all stories:

```typescript
const meta = {
  component: Form,
  args: {
    onSubmit: fn(),
    onCancel: fn(),
  },
} satisfies Meta<typeof Form>;
```

### Global Actions

Configure in `.storybook/preview.ts`:

```typescript
const preview: Preview = {
  parameters: {
    actions: {
      argTypesRegex: '^on.*', // Auto-create actions for all "on*" props
      disable: false,         // Toggle actions panel
    },
  },
};
```

## Testing with Actions

### Play Function Integration

Test that callbacks fire correctly:

```typescript
import { fn } from '@storybook/test';
import { within, expect } from '@storybook/test';

export const Clickable: Story = {
  args: {
    onClick: fn(),
  },
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);

    // Assert callback was called
    expect(onClick).toHaveBeenCalled();
    expect(onClick).toHaveBeenCalledTimes(1);
  },
};
```

### Inspect Action Arguments

Verify callback received correct arguments:

```typescript
export const FormSubmit: Story = {
  args: {
    onSubmit: fn(),
  },
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);

    await userEvent.type(canvas.getByLabelText('Email'), 'test@example.com');
    await userEvent.click(canvas.getByRole('button', { name: 'Submit' }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
    });
  },
};
```

### Multiple Actions

```typescript
export const MultipleHandlers: Story = {
  args: {
    onFocus: fn(),
    onBlur: fn(),
    onChange: fn(),
  },
  play: async ({ canvasElement, userEvent }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByLabelText('Email');

    await userEvent.click(input);
    expect(onFocus).toHaveBeenCalled();

    await userEvent.type(input, 'test@example.com');
    expect(onChange).toHaveBeenCalled();

    await userEvent.tab();
    expect(onBlur).toHaveBeenCalled();
  },
};
```

## Non-Story Function Monitoring

Monitor functions that aren't component props:

### Using spyOn()

```typescript
import { spyOn } from '@storybook/test';

const preview: Preview = {
  async beforeEach() {
    spyOn(console, 'log').mockName('console.log');
  },
};
```

### Filtered Actions

Conditionally log function calls:

```typescript
import { action } from '@storybook/actions';
import { spyOn } from '@storybook/test';

const preview: Preview = {
  async beforeEach() {
    spyOn(console, 'log')
      .mockImplementation((...args) => {
        if (args[0] === 'IMPORTANT') {
          action('console.log')(args);
        }
      });
  },
};
```

## Best Practices

### Controls

✅ Use `component` in meta for automatic inference
✅ Define argTypes for complex props
✅ Use appropriate control types (radio for few options, select for many)
✅ Add description and table metadata for clarity
✅ Configure matchers for color, date props
✅ Use conditional controls for advanced options
✅ Set min/max/step for numeric controls

❌ Don't manually define simple controls (let Storybook infer)
❌ Don't use 'object' control for simple data (use individual args)
❌ Don't forget to add useful descriptions

### Actions

✅ Use `fn()` from `@storybook/test` for all new stories
✅ Name action handlers clearly: `onClick`, `onSubmit`
✅ Test actions in play functions
✅ Verify action arguments with `expect().toHaveBeenCalledWith()`
✅ Monitor important non-story functions with `spyOn()`

❌ Don't use automatic `argTypesRegex` for stories with play functions
❌ Don't use deprecated `action()` function
❌ Don't forget to assert action calls in tests

## Common Patterns

### Button Component

```typescript
const meta = {
  component: Button,
  argTypes: {
    variant: { control: 'radio', options: ['primary', 'secondary'] },
    size: { control: 'radio', options: ['small', 'medium', 'large'] },
    disabled: { control: 'boolean' },
    onClick: { action: 'clicked' }, // Or fn()
  },
} satisfies Meta<typeof Button>;
```

### Form Component

```typescript
const meta = {
  component: Form,
  args: {
    onSubmit: fn(),
    onCancel: fn(),
  },
  argTypes: {
    showAdvanced: { control: 'boolean' },
    apiKey: {
      control: 'text',
      if: { arg: 'showAdvanced' },
    },
  },
} satisfies Meta<typeof Form>;
```

### Data Table Component

```typescript
const meta = {
  component: Table,
  argTypes: {
    data: { control: 'object' },
    sortBy: {
      control: 'select',
      options: ['name', 'date', 'status'],
    },
    sortOrder: {
      control: 'inline-radio',
      options: ['asc', 'desc'],
    },
  },
} satisfies Meta<typeof Table>;
```

## Troubleshooting

### Controls Not Appearing

**Cause**: Component not referenced in meta
**Solution**: Add `component: Button` to meta

### Wrong Control Type Inferred

**Cause**: Initial value doesn't match desired type
**Solution**: Define argTypes explicitly with correct control type

### Action Not Firing

**Cause**: Using automatic matching with play functions
**Solution**: Use `fn()` from `@storybook/test`

### Can't Access Action Spy in Play Function

**Cause**: Automatic action matching creates wrappers
**Solution**: Define args explicitly with `fn()`

### Controls Panel Too Large

**Cause**: Too many props shown
**Solution**: Use `include`/`exclude` to filter props

## Resources

- **Controls Docs**: https://storybook.js.org/docs/essentials/controls
- **Actions Docs**: https://storybook.js.org/docs/essentials/actions
- **Testing Library**: https://storybook.js.org/docs/writing-tests/testing-library
