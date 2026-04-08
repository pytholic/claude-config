# .claude

Personal Claude Code configuration — behavioral guidelines, custom skills, and agent definitions.

## Structure

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global behavioral guidelines (think-first, simplicity, surgical changes, goal-driven execution) |
| `settings.json` | Permissions, enabled plugins, and effort level |
| `skills/` | Reusable skill definitions for specialized workflows |
| `agents/` | Custom agent configurations for delegated tasks |

## Skills

- **code-review** — Structured code review with checklist
- **codebase-research** — Navigate, search, and map codebases to answer structural and locational questions
- **explain-code** — Visual diagrams and analogies for code explanation
- **llm-dev** — LLM architecture, fine-tuning, RAG, and agentic workflows
- **playwright-cli** — Automate browser interactions and work with Playwright tests
- **python-dev** — SOLID/OOP-driven Python development workflow
- **systematic-debugging** — Four-phase debugging with root cause analysis
- **task-handover** — Create structured handover documents for session continuity
- **write-tests** — Focused pytest coverage for critical paths and edge cases

## Agents

- **code-reviewer** — Automated code quality review
- **issue-analyzer-fixer** — Bug diagnosis and remediation
- **test-runner** — Test execution and failure reporting
