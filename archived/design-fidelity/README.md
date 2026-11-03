# design-fidelity

Verify an implemented UI against its design spec — mechanically.

```bash
/plugin install design-fidelity@llm-utils
```

## Three checks

**1. Token compliance.** Are design values referenced or retyped? One hardcoded hex is
harmless; two hundred mean the accent color can never change again. The skill supplies the
greps and the stylelint config that turns them into CI failures.

**2. Responsive behaviour.** Test *at* each breakpoint, not near it — `max-width: 900px`
behaves differently at 900 than at 901. The highest-value single assertion is horizontal
overflow: one line, no design knowledge, catches a large share of layout breaks.

**3. Interaction states.** Hover, focus, disabled, loading, **empty**, error. Empty states
are what a new user sees before any data exists, and they are typically built last if at
all.

## Reporting

The skill separates **implementation gaps** (built wrong) from **design gaps** (never
specified). They go to different people — reporting a design gap as a bug wastes a
developer's time and hides the real issue.

## On screenshot diffing

Use it for **regression**, not initial fidelity. Diffing against a mockup produces constant
noise from font rendering and antialiasing, and a suite that fails constantly is one people
stop reading — worse than no suite at all.
