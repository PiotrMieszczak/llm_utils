# Storybook Documentation Quality Checklist

Use this checklist to validate Storybook documentation quality before considering it complete. Think of this as quality gates for your documentation.

## Usage

1. Complete component stories and documentation
2. Review each section of this checklist
3. Mark items as complete only when truly satisfied
4. Resolve all failures before merging documentation
5. Re-run checklist when component changes significantly

---

## Section 1: Story Completeness

### Component Variants
- [ ] All component variants documented (primary, secondary, danger, ghost, etc.)
- [ ] All sizes shown (small, medium, large)
- [ ] All styles/themes covered

### Component States
- [ ] Default state documented
- [ ] Disabled state shown
- [ ] Error state demonstrated (if applicable)
- [ ] Loading state shown (if applicable)
- [ ] Empty state documented (if applicable)
- [ ] Hover state demonstrated (if interactive)
- [ ] Active/focus state shown (if interactive)

### Edge Cases
- [ ] Long text/content handled
- [ ] Many items shown (for lists/tables)
- [ ] Single item shown (for lists/tables)
- [ ] No items/empty state (for data display)
- [ ] Special characters handled
- [ ] Maximum values tested
- [ ] Boundary conditions documented

### Interactive Components
- [ ] All event handlers demonstrated with actions
- [ ] Click/tap interactions shown
- [ ] Form input/output demonstrated
- [ ] Keyboard interactions documented
- [ ] Accessibility features shown (ARIA labels, roles)

---

## Section 2: Story Quality

### Naming Conventions
- [ ] Stories use UpperCamelCase naming
- [ ] Story names are descriptive (Primary, Disabled, WithIcon)
- [ ] No generic names (Story1, Test, Example)
- [ ] Names follow team conventions (if established)

### Code Quality
- [ ] Stories use object syntax (not arrow functions)
- [ ] Args defined using object properties
- [ ] Args spread onto components: `<Component {...args} />`
- [ ] No React Hooks for component state (use args instead)
- [ ] No complex logic in story files (keep in component)
- [ ] TypeScript types properly defined
- [ ] Proper imports (no barrel file imports in monorepos)

### Event Handlers
- [ ] Actions use `fn()` from `@storybook/test`
- [ ] All callbacks have action handlers
- [ ] Action names are descriptive (clicked, changed, submitted)
- [ ] Play functions test interactive components
- [ ] Play functions assert behavior with `expect()`

### Metadata
- [ ] Component properly referenced in meta
- [ ] Title set for sidebar organization
- [ ] Autodocs enabled (globally or per-component)
- [ ] Tags configured appropriately
- [ ] Parameters defined for addons (backgrounds, layout)

---

## Section 3: Documentation Content

### Component Documentation
- [ ] Component has JSDoc comment
- [ ] Component description is clear and concise
- [ ] When to use component is documented
- [ ] Key behaviors and features explained
- [ ] Accessibility notes included (if applicable)

### Props Documentation
- [ ] All props have TypeScript types or JSDoc
- [ ] All props have descriptions
- [ ] Default values documented
- [ ] Required props marked
- [ ] Prop types are accurate
- [ ] Complex props have examples
- [ ] Enum options listed with descriptions

### Usage Examples
- [ ] Basic usage provided
- [ ] Common use cases shown
- [ ] Code examples are copy-pasteable
- [ ] Code examples have syntax highlighting
- [ ] Examples are current and accurate
- [ ] Advanced usage documented (if needed)

### Design Guidelines (if applicable)
- [ ] When to use component explained
- [ ] When NOT to use component explained
- [ ] Do's and don'ts provided
- [ ] Design tokens documented (spacing, colors)
- [ ] Layout guidelines included
- [ ] Content guidelines provided

---

## Section 4: Autodocs Configuration

### Autodocs Enabled
- [ ] Autodocs enabled globally OR per-component
- [ ] Docs page generates correctly
- [ ] Args table displays
- [ ] Controls panel works
- [ ] Stories render in docs page

### Description Quality
- [ ] Component description appears in docs
- [ ] Prop descriptions show in args table
- [ ] Default values display correctly
- [ ] Control types are appropriate
- [ ] No "undefined" or missing descriptions

### Customization (if applicable)
- [ ] Custom doc blocks configured (if needed)
- [ ] TOC enabled for long docs
- [ ] Theme configured (if needed)
- [ ] Subcomponents documented together (if related)

---

## Section 5: MDX Documentation (if used)

### MDX Structure
- [ ] Meta block references story file (not component)
- [ ] Blank lines between Markdown and JSX
- [ ] Proper imports (doc blocks, stories)
- [ ] Headings follow hierarchy (h1, h2, h3)
- [ ] No deeply nested JSX

### Content Quality
- [ ] Clear, concise descriptions
- [ ] Proper grammar and spelling
- [ ] Consistent formatting
- [ ] Code examples work correctly
- [ ] Embedded stories render properly
- [ ] Links are valid

### MDX Best Practices
- [ ] Doc blocks used consistently
- [ ] Stories embedded with Canvas or Story blocks
- [ ] Controls block included (if applicable)
- [ ] GFM enabled if tables used
- [ ] No component logic in MDX

---

## Section 6: Design System Documentation

### Organization
- [ ] Components grouped by category (Atoms, Molecules, Organisms)
- [ ] Sidebar follows clear hierarchy
- [ ] Related components linked
- [ ] Design guidelines pages exist (if applicable)
- [ ] Pattern documentation included (if applicable)

### Consistency
- [ ] Naming conventions consistent across components
- [ ] Story structure consistent
- [ ] Documentation style consistent
- [ ] Code style consistent
- [ ] Example style consistent

### Navigation
- [ ] Component names are clear
- [ ] Categories make sense
- [ ] Search would find relevant components
- [ ] Cross-references between related components

---

## Section 7: Testing

### Interaction Tests
- [ ] Play functions test key interactions
- [ ] Click/tap actions tested
- [ ] Form input/output tested
- [ ] State changes verified
- [ ] Actions assertions included
- [ ] Tests use Testing Library queries

### Visual Regression
- [ ] Visual tests configured (Chromatic, Percy, etc.)
- [ ] All states captured visually
- [ ] Baselines established
- [ ] Tests run in CI/CD

### Accessibility
- [ ] Accessibility attributes documented (ARIA)
- [ ] Keyboard navigation tested
- [ ] Screen reader friendly
- [ ] Color contrast adequate
- [ ] Focus indicators visible

---

## Section 8: File Organization

### File Placement
- [ ] Stories co-located with components
- [ ] File naming follows pattern: `*.stories.@(js|jsx|ts|tsx)`
- [ ] Directory structure makes sense
- [ ] No orphaned or misplaced files

### Imports
- [ ] Component imports use relative paths
- [ ] No barrel/index imports (in monorepos)
- [ ] Import aliases configured (if used)
- [ ] No circular dependencies

---

## Section 9: Performance

### Optimization
- [ ] No unnecessary re-renders in stories
- [ ] Lazy loading used for heavy components (if needed)
- [ ] Story files aren't excessively large
- [ ] No heavy computations in story files

### Build Performance
- [ ] Storybook builds without errors
- [ ] Build time is reasonable
- [ ] No memory issues during build
- [ ] HMR works during development

---

## Section 10: Accessibility

### ARIA Attributes
- [ ] Components have proper roles
- [ ] Labels provided for interactive elements
- [ ] ARIA attributes documented
- [ ] State announcements work

### Keyboard Navigation
- [ ] All interactive elements keyboard accessible
- [ ] Tab order is logical
- [ ] Focus indicators visible
- [ ] Keyboard shortcuts documented (if any)

### Screen Reader
- [ ] Component announcements are clear
- [ ] Icon-only elements have labels
- [ ] Form inputs have associated labels
- [ ] Error messages are announced

---

## Section 11: Internationalization

### i18n Support (if applicable)
- [ ] Translatable strings identified
- [ ] Date/number formats locale-aware
- [ ] Text direction handled (LTR/RTL)
- [ ] Character encoding correct

### Locale-Specific Content
- [ ] Examples use generic/neutral content
- [ ] No hardcoded dates/times without locale
- [ ] Currency symbols handled
- [ ] Phone number formats documented

---

## Section 12: Maintenance

### Documentation Freshness
- [ ] Documentation reflects current implementation
- [ ] No outdated examples
- [ ] No deprecated props shown without warning
- [ ] Version compatibility documented

### Deprecation Strategy
- [ ] Deprecated components marked
- [ ] Migration path provided
- [ ] Removal timeline documented
- [ ] Alternatives suggested

---

## Section 13: User Experience

### Discoverability
- [ ] Components easy to find in sidebar
- [ ] Search terms would find component
- [ ] Related components cross-referenced
- [ ] Examples are compelling

### Usability
- [ ] Docs answer common questions
- [ ] Examples are realistic
- [ ] Code is copy-pasteable
- [ ] Learning curve is gentle

---

## Section 14: Quality Gates

### Pre-Merge Checks
- [ ] All stories render without errors
- [ ] TypeScript compiles without errors
- [ ] ESLint/Prettier checks pass
- [ ] Tests pass
- [ ] Visual regression tests pass
- [ ] No console errors or warnings

### Review Checklist
- [ ] Peer review completed
- [ ] Designer review completed (if applicable)
- [ ] QA review completed (if applicable)
- [ ] Accessibility review completed
- [ ] Documentation review completed

---

## Quick Validation Commands

```bash
# Build Storybook to check for errors
npm run build-storybook

# Type check
npm run type-check

# Lint
npm run lint

# Run tests
npm test

# Start Storybook for manual review
npm run storybook
```

---

## Passing Criteria

**Minimum Requirements**:
- All items in Section 1 (Story Completeness) must pass
- All items in Section 2 (Story Quality) must pass
- All items in Section 3 (Documentation Content) must pass
- Autodocs must work (Section 4)

**Recommended**:
- >90% completion in all sections
- Zero failing critical items (marked with ⚠️)

**Exception Process**:
- Document why item was skipped
- Note impact on documentation quality
- Create issue for future improvement

---

## Version History

- **v1.0** (2024-01-15): Initial checklist created

---

## Customization

Add project-specific items to these sections:
- Section 1: Add component-specific variants
- Section 12: Add project-specific maintenance tasks
- Section 14: Add CI/CD specific gates

---

**End of Documentation Quality Checklist**
