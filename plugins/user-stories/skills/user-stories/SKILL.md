---
name: user-stories
description: Turn a feature request into a minimal spec a developer can build from — one need, the scope boundary, and Gherkin acceptance criteria including the unhappy path. Use when writing a user story, adding acceptance criteria to a ticket, splitting work that is too big, or when a request arrives as a solution ("add a dropdown") instead of a need.
model-hint: sonnet
---

# Minimal spec

Not a story card ritual. The smallest document a developer can build from without asking
you questions.

Four parts. Nothing else.

```
Need        one sentence: who, what, why
Scope       in / out — the boundary, not a wishlist
Criteria    Given / When / Then, happy path and the states that break it
Notes       links to the spec, ADR, or design that constrains it
```

## Need

One sentence. The `why` is the part that matters — it is the only thing a developer cannot
read off the codebase, and it decides whether something cheaper would do.

```
When I upload a rulebook mid-session, I want to see how far indexing has got,
so I can tell whether to wait or keep going without it.
```

Lead with the situation, not a persona. "As a user" carries no information when there is
one kind of user.

**If the request names a solution, ask why once.** "I want a dropdown of systems" is a
solution; *pick the system my campaign uses* is the need. The dropdown may still be the
answer — but now it is the developer's call, which is where it belongs.

## Scope

Two lists. Out-of-scope is the half that prevents the argument in review.

```
In:  progress percentage on the document row, live while processing
Out: the upload interaction itself, retry on failure (separate ticket)
```

## Criteria

Gherkin, because it is unambiguous and a tester can run it without you.

```gherkin
Scenario: progress reflects real work
  Given a 400-page PDF is indexing
  When I open the documents view
  Then the row shows "Processing" and a percentage that increases

Scenario: an unparseable PDF says so
  Given a PDF with no text layer
  Then the row shows "Failed" with the reason
```

Four rules:

- **One `When` per scenario.** Two actions is two scenarios, or a missing `Given`
- **`Then` is observable.** "the list updates" is not; "the list shows 3 rows" is
- **`Given` is state, not navigation.** "Given I am on the page" is noise; "Given the
  campaign has no documents" is a real precondition
- **Write the unhappy path.** Empty, error, denied. A happy-path-only spec is half-written,
  and the missing half is where the work actually is

Three to five scenarios. More means the ticket is too big — split it.

## Notes

Links only. What constrains the implementation:

```
Design: docs/design/overview.md §4
Decided: ADR-0002 bars a model from this path
Criterion: AC-008 — processing never blocks the UI
```

Cite existing ids rather than restating the rule. A spec that paraphrases an ADR will
drift from it.

## Splitting

When criteria pass five checkboxes, split along a seam that still delivers something
usable: one workflow step, one business rule, one entity type, or happy path first with
error handling after.

**Never split by layer.** "Backend for X" and "frontend for X" are one feature cut in
half — neither ships anything a user can see, and finishing one proves nothing.

## Where this bends

**Technical work needs no need statement.** A migration, a dependency bump, a CI fix. Write
the scope and the criteria; skip the rest. Forcing "as a developer, I want…" onto
infrastructure is theatre.

**If it cannot be estimated, it is research, not a feature.** The output is a decision, not
a shipped capability. Write the question to answer and let the spec follow.

**Do not put decisions here.** Anything that constrains future work — a boundary, a data
shape, a protocol — belongs in an ADR the spec links to. A spec is thin on purpose.
