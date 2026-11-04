# ADR Index Template

Create `docs/adr/README.md` when the directory is first used, and add a row for every new
record. An unindexed ADR is one nobody finds.

```md
# Architectural Decision Records

Decisions that constrain implementation live here, not scattered through prose. If a
choice would surprise a new contributor, or if someone might reasonably undo it without
knowing why, it belongs in an ADR.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](adr-0001-example-slug.md) | Example decision title | Accepted |

## Format

- YAML frontmatter: `title`, `status`, `date`, `authors`, `tags`, `supersedes`,
  `superseded_by`
- Sections: Status, Context, Decision, Consequences, Alternatives Considered,
  Implementation Notes, References
- Coded bullets (`CON-001`, `POS-001`, `NEG-001`, `ALT-001`, `IMP-001`, `REF-001`) so
  later records can cite a specific point

Filename convention: `adr-NNNN-[title-slug].md`, sequential four-digit numbering.

## Status values

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion; not yet binding |
| **Accepted** | In force; implementation should follow it |
| **Rejected** | Considered and declined; kept so it is not re-litigated |
| **Superseded** | Replaced by a later ADR, named in `superseded_by` |
| **Deprecated** | No longer applies, with no direct replacement |

Records are immutable once accepted. A changed decision means a **new ADR** that
supersedes the old one — the history of why is as valuable as the current state.
```

## Keeping the index honest

When a record's status changes, update the index row in the same commit. An index showing
`Accepted` for a superseded decision is worse than no index, because it is trusted.
