# Gemini CLI Reference

Essential flags and options for Gemini CLI usage.

## Basic Syntax

```bash
gemini -m [model] "prompt"
gemini -m [model] -e [extension] "prompt"
```

## Models

| Model | Use Case |
|-------|----------|
| `gemini-3-pro` | **DEFAULT** - Best reasoning, preferred for all tasks |
| `gemini-3-flash` | Fast alternative when speed > quality |
| `gemini-2.5-pro` | Legacy - good reasoning |
| `gemini-2.5-flash` | Legacy - fast, cost-effective |
| `gemini-2.0-flash` | Older model, basic tasks |

## Common Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-m` | Select model | `-m gemini-2.5-flash` |
| `-e` | Enable extension | `-e web_search` |
| `-y` | Auto-approve actions | `-y` |
| `-r` | Resume session | `-r latest "continue..."` |
| `--output-format` | Output type | `--output-format json` |

## Extensions

| Extension | Use Case |
|-----------|----------|
| `web_search` | Web browsing, fact-checking |
| `playwright` | Browser automation (via MCP) |

## Browser & Playwright Actions

Gemini can control browsers via Playwright MCP. Common tasks:

```bash
# Navigate and screenshot
gemini -m gemini-3-pro "Navigate to https://example.com and take a screenshot"

# Fill forms and interact
gemini -m gemini-3-pro "Go to login page, fill username 'user' and password 'pass', then click submit"

# Extract page content
gemini -m gemini-3-pro "Navigate to https://docs.example.com and extract the main content"

# Multi-step browser workflow
gemini -m gemini-3-pro "Open https://app.example.com, login with provided credentials, navigate to settings, and screenshot the page"
```

### Available Browser Tools (via Playwright MCP)

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_take_screenshot` | Capture page/element |
| `browser_click` | Click elements |
| `browser_type` | Type text into fields |
| `browser_fill_form` | Fill multiple form fields |
| `browser_snapshot` | Get accessibility tree |
| `browser_evaluate` | Execute JavaScript |
| `browser_wait_for` | Wait for conditions |
| `browser_tabs` | Manage tabs |

### Check MCP Status

```bash
# List connected MCP servers
gemini mcp list

# Inside interactive session
/mcp list
```

## Input Methods

```bash
# Text prompt
gemini -m gemini-3-pro "Your prompt"

# File input (screenshots, images)
gemini -m gemini-3-pro "Analyze this" < image.png

# Pipe input
cat file.txt | gemini -m gemini-3-pro "Summarize this"
```

## Session Management

```bash
# List sessions
gemini --list-sessions

# Resume session
gemini -r latest "Continue previous task"

# Delete session
gemini --delete-session 0
```

## Error Handling

```bash
# Check if installed
command -v gemini

# Fallback chain
gemini -m gemini-3-pro "prompt" || echo "Gemini failed"
```

## Environment

```bash
# API key
export GEMINI_API_KEY="your-key"

# Config location
~/.gemini/settings.json
```
