---
name: writing-how-to
description: Write the how-to.md for a documentation topic - tested recipes for tasks people repeat. Use when documenting a recurring procedure, when the same question keeps being asked, when onboarding steps live only in someone's head, or when deciding whether a topic needs a how-to file at all.
model-hint: sonnet
---

# Writing How-To

`how-to.md` answers **"how do I do X?"**

The reader has a goal and a terminal open. They are mid-task, mildly blocked, and want to
be unblocked — not educated.

## First: does this topic need one?

**Most topics do not.** `how-to.md` is optional in this pattern, and that is deliberate.

Write one only when a topic has procedures people **actually repeat**:

- "Add a new chunker"
- "Add an endpoint with campaign scoping"
- "Debug why retrieval returns nothing"

Do **not** create one for:

- One-off setup — that is `README.md`
- Anything done once and never again
- Procedures with a single obvious step
- Filling out the template

A thin or empty `how-to.md` is worse than none. It permanently signals "documentation
incomplete" and teaches people to skip the whole directory. If you cannot name two real
recipes, do not create the file.

The honest test: **has someone asked this twice?** A procedure asked once is a
conversation; asked twice, it is a recipe.

## Structure

One file per topic, several recipes inside. Each recipe is independent — a reader jumps
straight to the one they need.

```markdown
# Retrieval How-To

## Add a new chunker

Goal: split documents by a strategy the current chunkers do not cover.

1. Implement `Chunker` in `backend/app/ingestion/chunkers/`:

   ```python
   class HeadingChunker(Chunker):
       def split(self, text: str, meta: DocMeta) -> list[Chunk]: ...
   ```

2. Register it in `chunkers/__init__.py`.
3. Add a fixture document to `tests/fixtures/` covering the case it handles.
4. Add an expectation to the retrieval eval set.

Verify:

```bash
pytest tests/ingestion/test_chunkers.py -k heading
python3 scripts/eval_retrieval.py    # recall must not drop
```

## Debug empty retrieval results

...
```

## What makes a recipe work

**A goal line.** State what the reader ends up with. They are scanning headings to find
their situation; "Add a new chunker" is findable, "Chunker configuration" is not.

**Numbered, ordered steps.** How-to is the one role where sequence matters. Use numbers,
not bullets — bullets imply the order is optional.

**Concrete commands and paths.** `backend/app/ingestion/chunkers/`, not "the chunkers
directory". The reader is going to type it.

**A verification step.** The most-skipped and most valuable part: how does the reader know
it worked? Without it, they finish the steps and still do not know if they are done.

**One goal per recipe.** If a recipe branches ("if you are using X, instead do Y"), it is
two recipes.

## What does not belong

| Content | Belongs in |
|---------|-----------|
| Why the system works this way | `overview.md` |
| Exhaustive parameter lists | `reference.md` |
| Teaching the domain from scratch | nowhere in this pattern |
| One-off installation | `README.md` |

A how-to may *link* to explanation and reference — often should. It should not contain
them. "See `reference.md` for every chunker option" keeps the recipe short and the
reference authoritative.

## Keeping recipes true

How-to decays fast, silently, and painfully: the reader follows step 3, it fails, and now
they distrust the whole document.

**Prefer commands that are already tested.** A recipe that says `make seed` stays true as
long as the target works. A recipe that inlines six shell commands breaks when any one
changes. Point at the project's own tooling wherever possible.

**Verification steps double as tests.** If every recipe ends with a command that either
passes or fails, an audit can run them:

```bash
grep -A5 "^Verify:" docs/*/how-to.md | grep -E "^\s*(npm|pytest|make|python3)" 
```

**Date or version anything environment-specific.** A recipe depending on a tool version
should say which, so a reader hitting a mismatch knows why.

## Anti-patterns

**Explaining mid-recipe.** "Because the gateway abstracts providers, you will need to…" —
the reader is mid-task. Link to the overview instead.

**Assuming state.** "Now run the migration" — from where, with what running? Say what the
recipe assumes at the top, or make step 1 establish it.

**No verification.** The reader finishes and does not know whether it worked.

**Stale command names.** The most common failure, and the reason to point at project
tooling rather than inlining commands.

**Writing recipes nobody requested.** Speculative how-tos are template debris. Wait for
the second time someone asks.
