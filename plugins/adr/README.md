# adr

Architectural Decision Records for Claude Code.

```bash
/plugin install adr@llm-utils
```

## Why two skills

Decisions arrive in two ways, and recovering them takes opposite techniques.

**`adr-from-brainstorm`** — the decision was just made in conversation. You have the
alternatives, the constraints, and the reasoning; the risk is that it evaporates when the
session ends. The skill's job is capture.

**`adr-from-codebase`** — the decision is already in the code, and nobody wrote down why.
The risk is the opposite: inventing a confident rationale nobody actually had. The skill's
job is honest reconstruction, with observed, documented, and inferred claims kept
distinct in the record.

Using the brainstorm skill on legacy code produces fiction. Using the codebase skill on a
live conversation wastes the context you already have.

## The hook

After a design or planning session, the plugin blocks the turn **once** and requires a
review of existing ADRs.

It is not a reminder to write ADRs. It targets one specific failure: a session decides
something that contradicts an already-accepted record, and both end up in the directory
marked `Accepted`, with nothing indicating which is current. That is worse than having no
ADRs, because both get cited.

### How it works

Two hooks, split so the common path stays cheap:

| Hook | Event | Behaviour |
|------|-------|-----------|
| `mark_design_session.py` | `PostToolUse` on `Skill` | Writes a marker when a design-producing skill runs (brainstorming, writing-plans, speckit specify/plan) |
| `check_adrs.py` | `Stop` | If a marker exists, consumes it and blocks once with the existing ADR list and three specific checks |

On turns where no design skill ran, the Stop hook does one file-existence check and exits
silently.

### Design properties

- **Fires at most once per session.** The marker is consumed before blocking.
- **Cannot loop.** It honours `stop_hook_active` and deletes the marker before returning
  exit 2.
- **Never breaks a turn.** Malformed input, unwritable state directories, and missing
  paths all exit 0 silently. A hook that blocks real work is worse than a missed reminder.
- **Adapts to the project.** Different guidance when no ADR directory exists yet.
- **Does not demand an ADR.** "Nothing architectural was decided" is an accepted answer,
  and the prompt says so explicitly — otherwise it would manufacture records to satisfy
  itself.

### Disabling it

Uninstall the plugin, or remove the `Stop` entry from `hooks/hooks.json` if you want the
skills without the enforcement.

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

## Conventions both skills enforce

- **Negative consequences are mandatory.** An ADR with only positives is marketing.
- **Rejection reasons must be specific.** "Too complex" is not a reason a future reader
  can evaluate.
- **Deferrals need triggers.** "Not yet" without an observable condition that would change
  the answer is indistinguishable from "never", and gets re-litigated forever.
- **Accepted records are immutable.** A changed decision is a new ADR that supersedes the
  old one.
- **Never invent alternatives.** A fabricated alternatives section manufactures false
  confidence that options were weighed.
