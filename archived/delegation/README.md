# delegation

Delegate work to Gemini CLI where it has a clear advantage, and report what it saved.

```bash
/plugin install delegation@llm-utils
```

## Requirements

The `gemini` CLI must be on `PATH`:

```bash
gemini --version
```

## `gemini-delegate`

Hands specific task types to Gemini CLI rather than doing them in-context.

**Worth delegating:**

| Task | Why Gemini |
|------|-----------|
| Large context ingestion | 2M+ token windows — entire repositories in one pass |
| Screenshot and video analysis | Native multimodal handling |
| Web browsing and fact-checking | Live search for current docs and versions |
| Browser automation | Playwright MCP integration |
| Bulk refactoring | High-volume, low-complexity edits |

**Not worth delegating:** complex reasoning, autonomous planning, deep codebase
understanding, and ordinary file operations — Claude Code's own tools are faster and the
round trip costs more than it saves.

The skill reports token savings after each delegation, so the trade is visible rather
than assumed.

## When this is actually worth it

Delegation has real overhead: a subprocess, a context handoff, and a result you must
still read and verify. It pays off when the input is genuinely large or genuinely
multimodal — reading a 500-file repository, analysing a screen recording — and loses when
the task is small enough that the handoff dominates.

If you find yourself delegating a two-file refactor, do it directly instead.
