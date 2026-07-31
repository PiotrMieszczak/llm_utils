---
description: Create, audit, or extend project documentation on the Diataxis model without tutorials - explanation, reference, and optional how-to.
argument-hint: "[init|audit|add-topic <name>|write <topic>]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
disable-model-invocation: true
---

# /docs

Project documentation, one topic per folder, up to three roles per topic.

Mode: `$ARGUMENTS` — `audit` (default), `init`, `add-topic <name>`, or `write <topic>`.

## The pattern

```
docs/
├── README.md            the index
├── adr/                 decisions — immutable, cross-cutting
├── retrieval/
│   ├── overview.md      why it works this way        (decays slowly)
│   ├── reference.md     schemas, params, fields      (decays fast)
│   └── how-to.md        recipes — optional
└── design/
    ├── overview.md
    └── reference.md
```

Three roles because they have different readers and **different decay rates**. Mixed into
one file, you cannot tell which half is supposed to match the code — so either everything
gets checked, or nothing does.

`how-to.md` exists only when a topic has recurring procedures. Files exist because a topic
needs them, never to complete a template.

[Diátaxis](https://diataxis.fr/) — also published as Divio's
[Documentation System](https://docs.divio.com/documentation-system/) — minus tutorials.

---

## `init`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/docs_tool.py" init
```

Creates `docs/` with an index. If documentation already exists elsewhere
(`agents_docs/`, scattered `.md` files), **read it first** and propose a migration rather
than starting fresh alongside it.

---

## `add-topic <name>`

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/docs_tool.py" add-topic retrieval
```

Creates `overview.md` and `reference.md`, and updates the index. **Does not create
`how-to.md`** — that is optional, and a stub permanently signals "incomplete".

Name topics after **the question someone arrives with**: `retrieval`, `design`,
`deployment`. Not `utils` or `misc` — nobody asks "how does utils work?"

Then fill them. The templates are intentionally near-empty; use the writing skills:

| File | Skill |
|------|-------|
| `overview.md` | `writing-explanation` |
| `reference.md` | `writing-reference` |
| `how-to.md` | `writing-how-to` |

---

## `audit`

Structural pass first:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/docs_tool.py" audit
```

Catches flat files outside topics, reference-without-overview, tables in explanations,
stub how-tos, and broken index links.

Then the judgement pass, which a script cannot do — follow the `auditing-docs` skill:

**Staleness**, checked per role:

```bash
# reference against its source
git log -1 --format="%ar" -- docs/retrieval/reference.md
git log -1 --format="%ar" -- backend/app/retrieval/

# how-to verification steps still run?
grep -A6 "^Verify:" docs/*/how-to.md | grep -E "^\s*(npm|pytest|make|python3)"
```

**Gaps** — subsystems with no topic, and topics with reference but no overview.

**Orphans** — files nothing links to:

```bash
for f in docs/*/*.md; do
  grep -rq "$(basename "$f")" docs/README.md CLAUDE.md docs/*/*.md 2>/dev/null \
    || echo "ORPHAN: $f"
done
```

Report **stale before structural**. A wrong value causes wrong work today; a misfiled
explanation causes slow work eventually.

---

## `write <topic>`

Fill or revise one topic. Read the code the topic describes before writing about it — a
document written from assumptions is stale on arrival.

For each role, the test:

- **`overview.md`** — could a reader predict roughly where a new feature would go?
- **`reference.md`** — is it complete, and does every name match the code exactly?
- **`how-to.md`** — does each recipe end with a way to know it worked?

---

## Do not enforce the template

A topic with only `overview.md` is complete if that is all it needs. Flagging every missing
file produces stubs, which is exactly what the optional rule exists to prevent.

Moving detail between roles is restructuring; deleting it is data loss. Say which you are
proposing.
