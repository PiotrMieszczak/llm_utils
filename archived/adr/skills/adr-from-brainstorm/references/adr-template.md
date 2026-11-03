# ADR Template

Copy this structure exactly. Replace bracketed text; delete guidance lines starting with
`<!--`.

```md
---
title: "ADR-NNNN: [Decision Title]"
status: "Proposed"
date: "YYYY-MM-DD"
authors: "[Names or roles]"
tags: ["architecture", "decision"]
supersedes: ""
superseded_by: ""
---

# ADR-NNNN: [Decision Title]

## Status

Proposed | **Accepted** | Rejected | Superseded | Deprecated
<!-- Bold the one that applies. -->

## Context

<!-- The forces that made a decision necessary. Constraints, requirements, and
     pressures - not the decision itself. A reader should finish this section
     understanding why something had to be decided, without yet knowing the answer. -->

- **CON-001**: [Constraint or requirement driving this decision]
- **CON-002**: [Another force in play]
- **CON-003**: [Existing commitment or limitation that narrows the options]

## Decision

<!-- What was chosen, stated plainly. Active voice, past tense. One paragraph is
     usually enough; if it takes five, the ADR is probably covering several
     decisions that should be separate records. -->

[The chosen approach and the reasoning that selected it.]

## Consequences

### Positive

- **POS-001**: [What this makes easier or better]
- **POS-002**: [Capability gained or cost avoided]

### Negative

<!-- MANDATORY. Every real decision costs something. An ADR with no negative
     consequences has not been thought through. -->

- **NEG-001**: [What this makes harder]
- **NEG-002**: [Complexity, debt, or risk introduced]

## Alternatives Considered

<!-- Only options genuinely considered. Never invent alternatives to pad the
     section. Rejection reasons must be specific enough that a future reader can
     evaluate whether they still hold. -->

### [Alternative Name]

- **ALT-001**: **Description**: [What this option was]
- **ALT-002**: **Rejection Reason**: [Specifically why it lost - which constraint
  it violated, what it cost]

### [Another Alternative]

- **ALT-003**: **Description**: [What this option was]
- **ALT-004**: **Rejection Reason**: [Specifically why it lost]

## Implementation Notes

<!-- How the decision is carried out and, where relevant, how it is enforced.
     A decision that relies purely on discipline tends to erode; note the
     mechanism that keeps it true. -->

- **IMP-001**: [Key implementation consideration]
- **IMP-002**: [Enforcement mechanism - a test, lint rule, or CI check]
- **IMP-003**: [Revisit trigger, if this is a deferral: the observable condition
  that would change the answer]

## References

- **REF-001**: [Related ADRs]
- **REF-002**: [Documentation, spec, or design source]
- **REF-003**: [External standard or article that informed the choice]
```

## Notes on the coded bullets

The prefixes are stable identifiers, not decoration. They let a later record cite one
specific point precisely — "this supersedes ADR-0005 NEG-001" — and they make a directory
of ADRs greppable:

```bash
grep -rn "NEG-" docs/adr/    # every recorded cost across all decisions
```

Number within each section, starting at 001. Do not renumber existing bullets when editing
a Proposed record; stability is the point.
