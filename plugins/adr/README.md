# adr

Architectural Decision Records for Claude Code.

```bash
/plugin install adr@llm-utils
```

## The skill

**`adr-from-codebase`** — the decision is already in the code, and nobody wrote down why.
The risk is inventing a confident rationale nobody actually had. The skill's job is honest
reconstruction, with observed, documented, and inferred claims kept distinct in the record.

For a decision made in conversation, write the ADR straight from the plan or discussion
using the same template (`skills/adr-from-codebase/references/adr-template.md`). The
former `adr-from-brainstorm` skill and its Stop hook are in `archived/adr/`.

## Record format

`docs/adr/adr-NNNN-[title-slug].md`, with YAML frontmatter and coded bullets:

| Prefix | Section |
|--------|---------|
| `CON-` | Context — constraints and forces |
| `POS-` / `NEG-` | Consequences, positive and negative |
| `ALT-` | Alternatives considered |
| `IMP-` | Implementation notes |
| `REF-` | References |

Stable identifiers let a later record cite one point precisely ("supersedes ADR-0005
NEG-001") and make a directory greppable:

```bash
grep -rn "NEG-" docs/adr/    # every recorded cost across all decisions
```

## Conventions the skill enforces

- **Negative consequences are mandatory.** An ADR with only positives is marketing.
- **Rejection reasons must be specific.** "Too complex" is not a reason a future reader
  can evaluate.
- **Deferrals need triggers.** "Not yet" without an observable condition that would change
  the answer is indistinguishable from "never", and gets re-litigated forever.
- **Accepted records are immutable.** A changed decision is a new ADR that supersedes the
  old one.
- **Never invent alternatives.** A fabricated alternatives section manufactures false
  confidence that options were weighed.
