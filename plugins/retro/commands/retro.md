---
description: Retrospective on a coding session - suggest improvements to the agent's environment (navigation, checks, review rules, steering files).
argument-hint: "[session id | log path | description]  (default: current session)"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: true
---

# /retro

Run a **retrospective**. You suggest improvements to the coding agent's **environment** so
future runs go better. You do not change the code the session produced, and you do not
edit anything until the user picks a candidate.

Session: `$ARGUMENTS` (empty means the current session).

## Steps

1. If the `claude-docs:writing-claude-md` skill is available, load it for the style guide
   on agent-facing writing. Otherwise write every proposed line as short, imperative, and
   specific.

2. Read the primary sources for the session. Do not work from memory of the conversation
   alone. For a past session, search the logs on this machine:
   `~/.claude/projects/<project-slug>/*.jsonl`. Read the repo's steering files too:
   `CLAUDE.md`/`AGENTS.md` (repo and `~/.claude/`), the review-rules file if one exists,
   and the repo's own check command (`package.json` / build-tool `lint` and `check`
   scripts, the CI workflow, pre-commit config).

3. Look for candidates in these categories. Each has a *use when*; skip categories that
   do not apply.

   - **Navigation** - how easy was it to find the right files? Hidden dependencies between
     files? Would a **navigation pointer** help? *Use when* the session spent a long time
     finding one piece of information.
   - **Automated checks** - could linting, typing, tests, or a filesystem linter have
     caught an error the agent made? Read the repo's existing checks first, so a check
     that exists but is unwired or silently broken is the finding, not a reinvention. A
     repo with no **guardrail** (no pre-commit hook and no CI job running lint, typecheck
     or tests) is itself a finding. *Use when* the agent made a mistake a check could have
     caught, or the repo has no guardrail.
   - **Coding standards** - should the reviewer be given a new rule, or an existing rule
     removed or clarified? Classify the violation first. A **mechanical** one (fixed
     syntactic pattern, banned API, import shape, file-location rule) gets a deterministic
     check: a custom linter rule, pre-commit hook, or CI job, whichever is cheapest here.
     Default to building the check over writing the rule. Reserve the review-rules file
     for **judgement calls** (cross-file consistency, "matches the surrounding style").
     *Use when* review failed to catch a mistake.
   - **Steering files** - is anything in `CLAUDE.md`/`AGENTS.md` better placed in the
     review rules or an automated check? *Use when* the file is large, in the repo or in
     the user's global scope.
   - **Tool economy** - expensive tool calls that could be streamlined; token-heavy custom
     CLIs or MCP servers. *Use when* the agent made an expensive call.
   - **No-ops** - instructions in steering files that do not change agent behaviour.
     *Use when* steering files are large and unwieldy.
   - **Information access** - a crucial fact the agent could not reach: dev-server logs,
     read-only access to a third-party service. *Use when* the agent lacked information.

4. Present the candidates **in order of severity**. For each: the category, the evidence
   (log line, command, or file:line), the proposed change, and where it goes. Say plainly
   when the session surfaced nothing worth changing. Then ask which to apply.

## Reference

### Implementation vs review

All work goes through two stages. The **implementation** agent has the most context
pressure: it explores, writes code, and debugs. The **review** agent has the least: it
receives a diff and needs no exploration. So the review agent, not the implementation
agent, should impose coding standards.

### Where things go

- `CLAUDE.md` / `AGENTS.md` - pushed into every agent's context. Use incredibly sparingly,
  usually only for **navigation pointers** to other files.
- Review-rules file (e.g. `CODING_STANDARDS.md`) - read during review, not implementation.
  Add navigation pointers to docs folders once it passes 1,000 lines.
- Docs - reference material, pointed to by other files. Look for an existing doc before
  writing a new one.
- Skills - for docs whose description belongs in the agent's context, or for
  user-invoked commands.
