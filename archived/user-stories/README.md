# user-stories

The smallest spec a developer can build from without asking questions.

```bash
/plugin install user-stories@llm-utils
```

## Four parts

**Need** — one sentence: situation, capability, why. The `why` is the only part that cannot
be read off the codebase, and it is what decides whether something cheaper would do.

**Scope** — in and out. The out-of-scope list is the half that prevents the argument in
review.

**Criteria** — Gherkin. One `When` per scenario, `Then` stated as something observable, and
the unhappy path written down.

**Notes** — links to the ADR, spec, or design that constrains it. Cite ids; do not
paraphrase, or the spec drifts from the decision.

## Opinions worth knowing

**No story-card ritual.** "As a user, I want…" carries no information when the product has
one kind of user. Lead with the situation instead.

**The unhappy path is not optional.** Empty, error, denied. A happy-path-only spec is
half-written and the missing half is where the work is.

**Never split by layer.** "Backend for X" plus "frontend for X" is one feature cut in half
— neither ships anything visible, and finishing one proves nothing.

**Technical work skips the need statement.** A migration or a CI fix has no user-visible
outcome. Scope and criteria are enough.

**Decisions do not live here.** Boundaries, data shapes, protocols — those go in an ADR the
spec links to. See the `adr` plugin.

## Relationship to the other plugins here

`workflow-gates` owns when work advances between stages. This owns the shape of the
artefact a developer picks up.
