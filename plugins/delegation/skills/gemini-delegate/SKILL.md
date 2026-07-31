---
name: gemini-delegate
description: Delegate tasks to Gemini CLI for large context ingestion (2M+ tokens), screenshot/video processing, web browsing, browser automation, and bulk refactoring. Track token savings.
---

# Gemini Delegation Skill

Delegate specific tasks to Gemini CLI where it has clear advantages. Track token savings after each delegation.

## Before Delegating: Check Available Tools

Always check what MCP tools are available:
```bash
# List configured MCP servers
gemini mcp list

# Inside interactive session, run:
/mcp list
```

## When to Use Gemini CLI

**Delegate these use cases:**

### 1. Large Context Ingestion (2M+ tokens)
Entire repositories, full codebases, multi-file analysis.
```bash
gemini -m gemini-3-pro "Analyze the entire codebase for coupling issues"
```

### 2. Screenshot & Video Processing
UI screenshots, screen recordings, visual analysis.
```bash
gemini -m gemini-3-pro "Analyze this screenshot and describe the layout" < screenshot.png
```

### 3. Web Browsing & Fact-checking
Current docs, latest versions, real-time research.
```bash
gemini -m gemini-3-pro -e web_search "What are the latest React 19 features?"
```

### 4. Browser Automation (via Playwright MCP)
Navigate websites, take screenshots, fill forms, interact with pages.
```bash
gemini -m gemini-3-pro "Navigate to https://example.com and take a screenshot"
gemini -m gemini-3-pro "Go to login page, fill username and password, then submit"
```

### 5. Bulk Refactoring (High-volume, Low-complexity)
Large-scale find-replace, consistency updates, formatting.
```bash
gemini -m gemini-3-pro "Convert all let to const where appropriate across all .ts files"
```

## When to Use Claude Code Instead

Claude handles these better:

- **Complex reasoning & autonomous planning** - multi-step problem solving
- **Big documentation writing** - comprehensive docs, architecture docs, guides
- **Deep codebase understanding** - context-aware modifications
- **File operations** - Read, Edit, Write tools are faster
- **Security-sensitive tasks** - safer within Claude's guardrails

## Default Model

**`gemini-3-pro`** - Default for all delegations (best reasoning capability)

Use `gemini-3-flash` for faster responses when speed is more important than quality.

## Workflow

### Step 1: Validate
Is this one of the approved use cases? If NO → handle in Claude directly.

### Step 2: Check Tools (if needed)
```bash
gemini mcp list
```

### Step 3: Execute
```bash
gemini -m gemini-3-pro "your prompt"
```

### Step 4: Report Token Savings
After EVERY Gemini delegation, show this summary:

```
---
**Token Savings Report**
Task: [brief description]
Type: [large-context | screenshot | web-research | bulk-refactor]
Gemini tokens used: ~X,XXX
Estimated Claude tokens saved: ~X,XXX
---
```

**Estimation guide:**
- Large context ingestion: 10,000-50,000 tokens saved
- Screenshot processing: 2,000-5,000 tokens saved
- Web research: 3,000-8,000 tokens saved
- Browser automation: 2,000-10,000 tokens saved
- Bulk refactoring: 5,000-20,000 tokens saved (depends on file count)

## Quick Reference

```bash
# Large context
gemini -m gemini-3-pro "Analyze entire src/ directory..."

# Screenshot
gemini -m gemini-3-pro "Describe this UI" < image.png

# Web research
gemini -m gemini-3-pro -e web_search "Research topic..."

# Browser automation
gemini -m gemini-3-pro "Navigate to URL and take screenshot"

# Bulk refactor
gemini -m gemini-3-pro "Refactor all files to..."

# Check available tools
gemini mcp list
```

## Error Handling

If Gemini CLI fails:
1. Check availability: `command -v gemini`
2. Inform user of the error
3. Fall back to Claude if appropriate

## References

- `references/cli-reference.md` - Gemini CLI flags and options
- `references/mcp-tools-reference.md` - MCP servers, Playwright tools, extensions
