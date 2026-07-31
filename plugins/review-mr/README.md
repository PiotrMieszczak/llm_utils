# review-mr

The `/mr` command: audit → fix → commit → pull request.

```bash
/plugin install review-mr@llm-utils
```

## Usage

```bash
/mr                    # audit against main, fix, commit, open PR
/mr develop            # target a different base branch
/mr --no-fix           # audit and report only
/mr --draft            # open as a draft PR
/mr --wip              # commit and push, skip the PR
```

## What it does differently

**It reviews against your repository's own decisions**, not generic best practice. Before
looking at the diff it reads your `CLAUDE.md`, your docs, and the ADRs relevant to the
changed files — so findings cite a standard you already agreed to:

> `parse.py:88` calls the gateway from the ingestion path. Violates ADR-0002 —
> extraction must be deterministic.

That is arguable on the merits. "Consider adding error handling" is not.

**Two-axis reporting.** Findings split into **Standards** (does it follow our decisions?)
and **Spec** (does it build what was asked?), reported separately and never reranked
against each other. A change can follow every convention while implementing the wrong
thing; merging the axes lets a clean Standards report mask that.

**No AI attribution, anywhere.** Commit messages, PR titles, and PR bodies are written as
a human engineer on the project would write them. No `Co-Authored-By`, no generation
footer, no robot emoji. The command verifies this before pushing and again after opening
the PR.

## Phases

| Phase | What happens |
|-------|--------------|
| 1 Audit | Read `CLAUDE.md`, docs, and relevant ADRs; review the diff on both axes; report before touching anything |
| 2 Fix | Correct BLOCKING and SHOULD FIX findings; ask before acting on judgement calls; update docs when they drifted |
| 3 Commit | Group logically, write a plain factual message, verify no attribution, push |
| 4 PR | Fill `.github/pull_request_template.md` honestly; open with `gh`; sweep the result for attribution |

## Requirements

- `gh` authenticated (`gh auth status`)
- A feature branch — the command refuses to run on the base branch

## Skills

- **`doc-aware-review`** — the audit logic, usable on its own for a review without the
  commit and PR steps.
