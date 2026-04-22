# Claude Configuration

Personal Claude Code configuration — behavioral guidelines, custom skills, and agent definitions.

## Structure

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global behavioral guidelines (think-first, simplicity, surgical changes, goal-driven execution) |
| `settings.json` | Permissions, enabled plugins, and effort level |
| `skills/` | Reusable skill definitions (git submodule → [pytholic/claude-skills](https://github.com/pytholic/claude-skills)) |
| `agents/` | Custom agent configurations for delegated tasks |

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

## Agents

- **code-reviewer** — Automated code quality review
- **issue-analyzer-fixer** — Bug diagnosis and remediation
- **test-runner** — Test execution and failure reporting
