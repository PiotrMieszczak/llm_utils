---
name: design-fidelity
description: Verify an implemented UI matches its design spec - design-token compliance, responsive breakpoints, and interaction states. Use when reviewing UI code, after building a component from a design, when checking for hardcoded colors or spacing, when a design system is drifting, or when asked whether an implementation matches the design.
model-hint: sonnet
---

# Design Fidelity

Check that what was built matches what was designed — mechanically where possible, so it
does not depend on someone remembering to look.

Three checks, in order of how cheaply they catch real problems:

1. **Token compliance** — are design values referenced, or retyped?
2. **Responsive behaviour** — does it work at every specified breakpoint?
3. **Interaction states** — do hover, focus, disabled, loading, empty, and error exist?

## 1. Token compliance

The check that keeps a design system alive. One hardcoded hex is harmless; two hundred mean
the accent color can never change again.

### Find violations

```bash
# Literal hex outside the token definition file
grep -rn --include="*.css" --include="*.scss" --include="*.module.css" \
  -E "#[0-9a-fA-F]{3,8}\b" frontend/src \
  | grep -v "tokens.css" \
  | grep -v "^\s*/\*"
```

```bash
# Literal colors in JS/TS (inline styles, styled-components)
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(#[0-9a-fA-F]{6}|rgba?\([0-9]+,)" frontend/src | grep -v "\.test\."
```

```bash
# Suspicious raw pixel values where spacing tokens exist
grep -rn --include="*.module.css" -E ":\s*[0-9]+px" frontend/src \
  | grep -vE "1px|0px|100%" | head -30
```

Not every match is a violation. Legitimate exceptions:

- `1px` borders and hairlines
- Values inside `tokens.css` itself
- Genuinely dynamic values — a computed graph node position, a progress bar width
- Third-party overrides where a library demands a literal

The point is not zero matches. It is that **every match is deliberate and reviewed**.

### Enforce it

A grep that nobody runs is not enforcement. Wire it into lint:

```jsonc
// .stylelintrc.json
{
  "rules": {
    "color-no-hex": true,
    "declaration-property-value-allowed-list": {
      "/^(color|background|border-color)/": ["/^var\\(--/", "transparent", "inherit", "currentColor"]
    }
  },
  "overrides": [
    { "files": ["**/tokens.css"], "rules": { "color-no-hex": null,
        "declaration-property-value-allowed-list": null } }
  ]
}
```

Now a hardcoded color fails CI rather than depending on a reviewer noticing.

### Verify tokens match the spec

Compliance means nothing if the tokens themselves are wrong. Compare `tokens.css` against
the design's token table:

```bash
grep -oE "^\s*--[a-z-]+:\s*[^;]+" frontend/src/styles/tokens.css | sed 's/^\s*//' | sort
```

Diff that against the spec's documented values. A token defined as `#E8B87B` when the
design says `#E8B87A` propagates a wrong value everywhere, invisibly.

## 2. Responsive behaviour

Designs specify breakpoints; implementations forget the ones nobody looks at.

Extract what the design requires, then verify each:

```ts
// e2e/responsive.spec.ts
const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "tablet",  width: 900,  height: 1200 },  // at the breakpoint
  { name: "mobile",  width: 375,  height: 812 },
  { name: "narrow",  width: 320,  height: 640 },   // minimum supported
];

for (const vp of VIEWPORTS) {
  test(`workspace at ${vp.name}`, async ({ page }) => {
    await page.setViewportSize(vp);
    await page.goto("/c/demo/overview");

    // The page must never scroll horizontally. This catches most layout breaks.
    const overflow = await page.evaluate(() =>
      document.documentElement.scrollWidth > document.documentElement.clientWidth
    );
    expect(overflow, `horizontal scroll at ${vp.width}px`).toBe(false);

    // Behaviour that changes at the breakpoint, not just styling
    if (vp.width <= 900) {
      await expect(page.getByTestId("nav-rail")).toBeHidden();
      await expect(page.getByTestId("tab-bar")).toBeVisible();
    } else {
      await expect(page.getByTestId("nav-rail")).toBeVisible();
    }
  });
}
```

**Test *at* the breakpoint, not near it.** A rule written `max-width: 900px` behaves
differently at exactly 900 than at 901, and off-by-one boundary errors are common.

**Horizontal overflow is the highest-value single assertion.** It catches a large share of
responsive failures with one line and no design knowledge.

## 3. Interaction states

Designs specify states that implementations quietly skip because the happy path looks fine.

For each interactive component, verify:

| State | Commonly missed |
|-------|-----------------|
| Default | — |
| Hover | — |
| **Focus** | Very often — keyboard users get no visible indicator |
| Active | — |
| **Disabled** | Styled but still clickable |
| **Loading** | No feedback during an async action |
| **Empty** | The first thing a new user sees |
| **Error** | Failure renders as nothing at all |

**Empty states deserve particular attention.** They are what a new user encounters before
any data exists, and they are typically the last thing built — if they are built at all.
A design that omits them has a gap worth raising before implementation, not after.

```ts
test("quest list renders an empty state", async ({ page }) => {
  await page.route("**/api/v1/campaigns/*/quests", r => r.fulfill({ json: [] }));
  await page.goto("/c/demo/quests");
  await expect(page.getByTestId("empty-state")).toBeVisible();
});
```

## Visual comparison

Screenshot diffing is powerful and easy to misuse.

```ts
test("overview matches baseline", async ({ page }) => {
  await page.goto("/c/demo/overview");
  await page.waitForLoadState("networkidle");
  await expect(page).toHaveScreenshot("overview.png", { maxDiffPixelRatio: 0.01 });
});
```

Use it for **regression** — did this change alter something it should not have? — not for
initial fidelity. Comparing against a design mockup produces constant noise from font
rendering, antialiasing, and platform differences.

To keep it useful:

- Freeze anything non-deterministic: dates, random content, animations
  (`prefers-reduced-motion`, or a CSS override disabling transitions)
- Run in a container so rendering is consistent across machines and CI
- Set a small but non-zero `maxDiffPixelRatio` — exact matching is unattainable
- Review baseline updates deliberately. Auto-accepting new baselines makes the whole
  suite decorative

If the suite fails constantly, people stop reading it, and it is worse than nothing.

## Reporting

Structure findings so they are actionable:

```
TOKEN VIOLATIONS
  frontend/src/features/quests/QuestRow.module.css:24
    background: #1A1D25  →  var(--surface-elevated)

  frontend/src/ui/Badge.tsx:12
    inline style color "#7FD4A0"  →  var(--success)

RESPONSIVE
  Quest row overflows horizontally at 320px (title does not truncate).
    Spec requires support to 320px.

MISSING STATES
  QuestList — no empty state. Spec does not define one either;
    needs design input before it can be implemented.

  Button — focus ring not visible on keyboard navigation.
    Spec: focus moves the border to var(--accent).
```

Distinguish **implementation gaps** (built wrong) from **design gaps** (never specified).
They go to different people. Reporting a design gap as an implementation bug wastes a
developer's time and hides the real issue.

## Anti-patterns

**Reviewing fidelity by eye only.** Humans do not reliably spot `#1A1D25` where
`#1A1D24` was specified. Machines do.

**Screenshot-diffing against design mockups.** Constant false positives from rendering
differences train people to ignore failures.

**Testing only the default viewport.** Breakpoint bugs live specifically where nobody
looks.

**Treating token violations as trivial.** Individually trivial; collectively they are how a
design system dies.

**Adding a suite nobody maintains.** A visual suite with fifty stale baselines is worse
than none — it produces noise that masks real regressions.
