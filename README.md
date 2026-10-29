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

`CLAUDE.md` §2 imports the minimality ladder from `skills/shared/minimality-ladder.md`, and the skills point to it rather than carrying copies. This makes the submodule required: without it, the import is missing. Edit the ladder only in that file; nothing needs syncing.

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

## Editor rules (Zed, Cursor)

Zed (`~/.config/zed/AGENTS.md`) and Cursor (`~/.cursor/rules/personal.mdc`) don't resolve Claude's `@` imports, so their global rules are generated from `CLAUDE.md` with imports inlined. The generated files are not committed.

Run after cloning, and again after editing `CLAUDE.md` or the ladder in `skills/shared/minimality-ladder.md`:

```bash
~/.claude/scripts/sync_editor_rules.py
```

It needs the `skills` submodule (`git submodule update --init`) and exits with an error if an imported file is missing.

## New machine checklist

1. Clone with submodules (see [Skills](#skills)).
2. Install the CLI tools that `CLAUDE.md` tells the agent to prefer over MCP servers: `git`, `gh` (run `gh auth login`), `jq`, and `ntn` (`npm i -g ntn`, then `ntn login`).
3. Register the per-machine MCP servers: Context7 and mcp-atlassian (see [MCP Servers](#mcp-servers)). Server configs live in `~/.claude.json`, which is not committed.
4. Run `~/.claude/scripts/sync_editor_rules.py` to generate the Zed and Cursor rule files (see [Editor rules](#editor-rules-zed-cursor)).
5. Open Claude Code and check that `/permissions` shows the rules from `settings.json`.

## Agents

- **test-runner** — Runs tests and reports only the failures, keeping verbose output out of the main conversation. Uses per-project memory (`.claude/agent-memory/test-runner/`).
