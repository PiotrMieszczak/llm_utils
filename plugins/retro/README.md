# retro

Retrospective on a coding session. Suggests changes to the agent's **environment**, not to the code the session produced.

```bash
/plugin install retro@llm-utils
```

## Usage

```
/retro                 # current session
/retro <session id>    # a past session, found in ~/.claude/projects/<slug>/*.jsonl
```

The command reads the session and the repo's steering files and checks, then reports candidates in order of severity across seven categories: navigation, automated checks, coding standards, steering files, tool economy, no-ops, information access. It edits nothing until you pick.

Mechanical violations get a deterministic check (linter rule, hook, CI job) rather than a written rule. The review-rules file is for judgement calls only.

Optional: loads `claude-docs:writing-claude-md` for style when installed.
