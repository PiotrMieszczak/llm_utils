---
name: writing-explanation
description: Write the overview.md for a documentation topic - the file that explains why a system works the way it does. Use when creating or revising a topic overview, when someone asks "why is it built like this", when onboarding material is needed, or when a document meant to explain has drifted into listing parameters.
model-hint: opus
---

# Writing Explanation

`overview.md` answers **"why is it like this?"**

It is the file someone reads once to understand a topic, then rarely returns to. That
makes it the hardest of the three roles to write, because there is no obvious completeness
test — a reference is done when every field is listed, a how-to is done when the steps
work, but an explanation is done when someone *gets it*.

## What it is for

The reader has a working system in front of them and a question the code cannot answer:
why this shape and not another?

Explanation supplies:

- **The problem** the design responds to
- **How the parts relate** — the mental model
- **Trade-offs** that were accepted, and what was given up
- **Boundaries** — what this deliberately does not do

It is read at a desk, not mid-task. That is the practical distinction: a reader consulting
an explanation is trying to *understand*, not to *finish something*. Nobody has a terminal
open.

## Structure

Roughly 40–120 lines. Longer usually means reference material crept in.

```markdown
# Retrieval

One paragraph: what this is and what it is for.

## The problem

What made this necessary. Constraints, forces, what the naive approach costs.

## How it works

The mental model — components and how they relate. A diagram earns its place here.

## Why this way

The trade-offs. What was chosen, what was given up, under what assumptions.
Link the ADRs that decided contentious parts.

## What this does not do

Boundaries. Prevents the most common misunderstanding.
```

The last section is undervalued. Stating what a system deliberately omits prevents more
confusion than any amount of describing what it does — and it is where most "I assumed
it would handle X" failures come from.

## Techniques

**Start from the problem, not the solution.** "Retrieval uses FTS5" tells a reader what;
"a GM asks a rules question mid-session and cannot wait ninety seconds" tells them why the
design has the shape it has. The second makes the first inevitable.

**Name the alternative you did not take.** Explanation is comparative by nature. "We index
with FTS5 rather than embeddings, because queries are largely terminological" explains far
more than a description of FTS5 alone.

**Use a diagram for relationships, prose for reasoning.** Diagrams are excellent at
structure and useless at trade-offs. Do not caption a diagram and call it explanation.

**Write in the present tense about the system, past tense about decisions.** "Retrieval
runs over chunk text" and "we chose FTS5 because…".

**Link to ADRs rather than restating them.** An overview cites decisions; it does not
relitigate them. If a paragraph is turning into a rationale with alternatives and
consequences, it is an ADR trying to be born.

## What does not belong

| Content | Belongs in |
|---------|-----------|
| Field names, parameters, exact values | `reference.md` |
| Step-by-step procedures | `how-to.md` |
| Full decision rationale with alternatives | an ADR |
| Installation and setup | `README.md` |
| Long code listings | the codebase |

Short code fragments are fine when they *illustrate a concept*. A twenty-line example is
reference material wearing a disguise.

## The failure mode

**Explanation drifting into reference** is the single most common documentation problem,
and it happens gradually: someone adds "the config keys are…", someone else adds a table
of defaults, and within a year the overview is a parameter list with a paragraph on top.

Symptoms:

- Tables of field names or values
- Exhaustive lists of anything
- Sentences a reader would search for rather than read
- The file growing steadily without the system changing

The fix is mechanical: move the lists to `reference.md` and leave the reasoning. If
nothing remains after moving the lists out, the file was never an explanation.

## Testing it

There is no automated check, but there are two useful questions.

**Could a competent developer, after reading this, predict roughly where a new feature
would go?** If not, the mental model is missing.

**Does it answer a question the code cannot?** If every sentence could be derived by
reading the source in five minutes, the file is describing rather than explaining, and it
will go stale for no benefit.

## Anti-patterns

**The feature tour.** Walking through each component describing what it does. That is
reference organised badly.

**Assuming the reader knows why the problem is hard.** They usually do not — that is why
they are reading.

**Explaining the obvious and skipping the surprising.** The unusual choice is exactly the
one needing explanation; it is also the one the author has stopped noticing.

**Hedging.** "You might want to consider possibly using…" Say what the system does and
why. Explanation is not advice.
