---
name: frontend-design-notw
description: Create distinctive, production-grade frontend interfaces using custom CSS, CSS Modules, or CSS-in-JS - never Tailwind. Use when building web components, pages, or applications in a project that forbids utility-class frameworks, or when a design calls for a bold, specific aesthetic that utility classes would flatten. Enforces a no-Tailwind rule and a list of generic-AI-aesthetic anti-patterns.
---

# Frontend Design Skill

Create production-ready frontend interfaces with distinctive aesthetics that transcend generic AI-generated patterns.

## Core Principle

**Avoid predictable design.** Each project should have intentional, memorable character. Generic patterns kill differentiation.

## Workflow

### 1. Context Analysis (MANDATORY - Before Any Code)

Ask yourself:
- **Purpose**: What is this interface for? Who will use it?
- **Tone**: Professional? Playful? Experimental? Editorial?
- **Constraints**: Framework requirements, browser targets, accessibility needs?
- **Differentiator**: What makes THIS different from similar interfaces?

**DO NOT skip to code.** Context drives aesthetic decisions.

### 2. Aesthetic Direction

**Choose a bold direction** - avoid middle-ground defaults:

Examples:
- Brutally minimal (negative space, stark contrasts, single accent)
- Maximalist chaos (overlapping elements, multiple typefaces, vibrant colors)
- Retro-futuristic (grid systems, neon accents, terminal aesthetics)
- Organic/natural (fluid shapes, earth tones, asymmetry)
- Editorial (magazine-style layouts, strong typography hierarchy)

**Key insight**: "Bold maximalism and refined minimalism both work - the key is intentionality, not intensity."

### 3. Implementation Focus Areas

Execute with precision across these four pillars:

#### Typography
- **NO defaults**: Avoid Arial, Roboto, Inter, Helvetica unless specifically justified
- Use distinctive, characterful fonts (Google Fonts, system-ui alternatives)
- Establish clear hierarchy: display, heading, body, caption scales
- **Use modular scales** (e.g., Major Third 1.250) for font sizing to ensure mathematical harmony
- Consider variable fonts for dynamic sizing
- Set explicit line-height, letter-spacing for readability

#### Color & Theme
- Define CSS variables for cohesive theming:
  ```css
  :root {
    --color-primary: /* dominant brand color */;
    --color-accent: /* sharp contrast for CTAs */;
    --color-surface: /* backgrounds */;
    --color-text: /* body copy */;
  }
  ```
- Avoid cliched schemes: blue gradients, purple/pink, generic pastels
- **Apply the 60-30-10 rule**: 60% dominant, 30% secondary, 10% accent to balance the palette
- Consider: monochrome + single accent, analogous harmony, unexpected pairings
- Dark mode: intentional, not inverted

#### Motion & Animation
- **Prioritize high-impact animations**: page-load reveals, interaction feedback
- Use orchestrated timing (staggered delays) for element reveals:
  ```css
  .item:nth-child(1) { animation-delay: 0ms; }
  .item:nth-child(2) { animation-delay: 100ms; }
  .item:nth-child(3) { animation-delay: 200ms; }
  ```
- Prefer `transform` and `opacity` for performance (GPU-accelerated)
- Respect `prefers-reduced-motion` for accessibility
- Timing: ease-out for entrances, ease-in for exits, custom cubic-bezier for character

#### Spatial Composition
- **Break the grid**: Asymmetry, overlap, diagonal flow create visual interest
- Use negative space intentionally (minimalism) or reject it entirely (maximalism)
- Consider: split-screen layouts, fixed headers with parallax, card-based grids with varied sizes
- Responsive design: mobile-first, but ensure desktop isn't just stretched mobile

### 4. Code Quality Standards

Generate production-ready code:
- **Semantic HTML**: Proper heading hierarchy, landmarks, ARIA where needed
- **CSS Organization**: Logical grouping (layout → typography → colors → effects)
- **Performance**: Lazy-load images, minimize reflows, optimize animations
- **Accessibility**: Color contrast ratios, keyboard navigation, screen reader support
- **Modularity**: Component-based structure, reusable utilities
- **CRITICAL - NO TAILWIND**: Never use Tailwind CSS. Write custom CSS or use CSS-in-JS, CSS modules, or vanilla CSS. This ensures unique, maintainable styling that matches the distinctive design vision.

### 5. Output Format

Deliver complete, runnable code:
- Single HTML file with embedded CSS/JS (unless framework specified)
- External assets via CDN (fonts, icons) or inline SVG
- Comments explaining key design decisions
- Clear instructions for customization

## Anti-Patterns (NEVER DO THIS)

1. **Generic fonts**: Arial, Roboto, Inter without justification
2. **Cliched colors**: Blue gradients, purple/pink combos, generic pastels
3. **Predictable layouts**: Centered hero → three-column features → footer
4. **Default shadows**: `box-shadow: 0 2px 4px rgba(0,0,0,0.1)` everywhere
5. **Tailwind CSS**: NEVER use Tailwind. It produces generic, verbose HTML and discourages custom design thinking. Use custom CSS, CSS-in-JS, CSS modules, or vanilla CSS instead.
6. **Bootstrap defaults**: Avoid Bootstrap unless heavily customized beyond recognition
7. **Rigid 8pt grid**: Blindly following 8px/16px/24px steps without optical adjustment
8. **Copy-paste patterns**: Card grids that look like every other card grid

## Complexity Matching

**Match code complexity to design vision:**
- Elaborate designs demand elaborate code (custom animations, SVG, advanced CSS)
- Minimal designs demand restraint and precision (every pixel intentional)

## Examples of Good Aesthetic Directions

- **Brutalist**: Monospace fonts, stark black/white, exposed structure, raw HTML elements
- **Neumorphism evolved**: Soft shadows with unexpected color shifts (not just gray)
- **Terminal UI**: Monospace, green/amber text, scan-line effects, glitch animations
- **Swiss design**: Grid-based, limited color, Helvetica justified, mathematical spacing
- **Y2K revival**: Gradients, metallics, bubbly shapes, playful cursors
- **Editorial bold**: Large type, columns, pull quotes, magazine-style layouts

## Tool Usage

Use Claude Code tools effectively:
- **Read**: Review existing design systems or style guides in the project
- **Write**: Create complete HTML/CSS/JS files
- **Edit**: Refine based on user feedback
- **WebFetch**: Research design trends, color palettes, font pairings (if needed)

## Success Criteria

The design is successful when:
1. It has a **memorable differentiator** (user can describe it uniquely)
2. It **avoids generic AI patterns** (doesn't look like every other AI-generated UI)
3. It's **production-ready** (accessibility, performance, responsiveness)
4. It **matches the brief** (tone, purpose, constraints all satisfied)

## Final Reminder

**No two designs should look the same.** Vary your approach. Experiment. Commit to bold choices. The goal is distinctiveness AND quality.
