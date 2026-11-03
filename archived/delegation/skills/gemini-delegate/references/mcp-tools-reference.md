# Gemini CLI MCP & Tools Reference

## Discovering Available Tools

Before delegating tasks, discover what tools Gemini has access to.

### List MCP Servers
```bash
gemini mcp list
```

Shows configured MCP servers and their connection status.

### Interactive Tool Discovery
Inside an interactive Gemini session, use:
```
/mcp list
```

This lists all available MCP tools that Claude can leverage through Gemini.

## MCP Management Commands

```bash
# List configured servers
gemini mcp list

# Add new MCP server
gemini mcp add <name> <commandOrUrl> [args...]

# Remove MCP server
gemini mcp remove <name>
```

## Common MCP Servers

| Server | Purpose | Tools Provided |
|--------|---------|----------------|
| `playwright` | Browser automation | Screenshot, navigate, click, fill forms, etc. |
| Custom servers | Project-specific | Varies by configuration |

## Playwright MCP Tools

When playwright MCP is connected, Gemini has access to:

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_take_screenshot` | Capture page screenshot |
| `browser_snapshot` | Accessibility snapshot |
| `browser_click` | Click elements |
| `browser_fill_form` | Fill form fields |
| `browser_type` | Type text |
| `browser_evaluate` | Run JavaScript |
| `browser_tabs` | Manage browser tabs |
| `browser_wait_for` | Wait for conditions |
| `browser_network_requests` | Monitor network |
| `browser_console_messages` | Read console logs |

## Built-in Extensions

List installed extensions:
```bash
gemini -l
# or
gemini extensions list
```

### Common Extensions

| Extension | Flag | Purpose |
|-----------|------|---------|
| `web_search` | `-e web_search` | Web browsing, fact-checking |
| `playwright` | Auto-enabled via MCP | Browser automation |

## Extension Management

```bash
# Install extension
gemini extensions install <git-url-or-path>

# Uninstall
gemini extensions uninstall <name>

# Update all
gemini extensions update --all

# Enable/disable
gemini extensions enable <name>
gemini extensions disable <name>
```

## Workflow: Check Tools Before Delegation

1. **Check MCP servers**: `gemini mcp list`
2. **Check extensions**: `gemini -l`
3. **Interactive discovery**: Start session and run `/mcp list`
4. **Delegate with appropriate tools**

## Example: Screenshot Task with Playwright

```bash
# Verify playwright MCP is connected
gemini mcp list

# Navigate and screenshot
gemini -m gemini-3-pro "Navigate to https://example.com and take a screenshot"
```
