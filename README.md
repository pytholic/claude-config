# Claude Configuration

Personal Claude Code configuration — behavioral guidelines, custom skills, and agent definitions.

## Structure

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global behavioral guidelines (think-first, simplicity, surgical changes, goal-driven execution) |
| `settings.json` | Permissions, enabled plugins, and effort level |
| `skills/` | Reusable skill definitions (git submodule → [pytholic/claude-skills](https://github.com/pytholic/claude-skills)) |
| `agents/` | Custom agent configurations for delegated tasks |
| `scripts/` | Wrapper scripts for MCP servers (committed; no secrets) |

## Skills

Skills live in a separate repo and are linked here as a submodule. See [pytholic/claude-skills](https://github.com/pytholic/claude-skills) for the full list and install instructions.

To clone this repo with skills included:

```bash
git clone --recurse-submodules https://github.com/pytholic/claude-config.git ~/.claude
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init
```

## MCP Servers

MCP (Model Context Protocol) servers extend Claude Code with external tool access. Server configs are registered per-machine in `~/.claude.json` (not committed). Wrapper scripts live in `scripts/` (committed) and contain no secrets — they fetch credentials from macOS Keychain at runtime.

This avoids hardcoding tokens in config files and works regardless of home directory path on a new machine.

### mcp-atlassian

Gives Claude Code read/write access to Confluence and Jira at `lunit.atlassian.net` via [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian).

**One-time setup on a new machine:**

1. **Store the Atlassian API token in Keychain** — generate one at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens), then:

   ```bash
   security add-generic-password -a "$USER" -s "confluence-lunit" -w "YOUR_API_TOKEN"
   ```

2. **Make the wrapper executable:**

   ```bash
   chmod +x ~/.claude/scripts/mcp-atlassian
   ```

3. **Register with Claude Code:**

   ```bash
   claude mcp add --scope user mcp-atlassian "$HOME/.claude/scripts/mcp-atlassian"
   ```

The wrapper script (`scripts/mcp-atlassian`) reads the token from Keychain and passes it to the MCP server as environment variables. No unlock step needed — macOS handles auth transparently via the login session.

## Agents

- **code-reviewer** — Automated code quality review
- **issue-analyzer-fixer** — Bug diagnosis and remediation
- **test-runner** — Test execution and failure reporting
