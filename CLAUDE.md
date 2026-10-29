Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Priorities:** correctness and caution first, then simplicity: modern best practices and simple, Pythonic code (the Zen of Python). Speed is a plus, never at the cost of those. For trivial tasks, use judgment.

## 0. Context
- Python-focused ML/AI engineer on macOS (South Korea)
- Default stack: .venv, pytest, ruff + pyright, pyproject.toml, Python 3.13+ type syntax
- Planning-first: requirements → architecture → components → code

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly.
- Make routine judgment calls yourself. Check in only when different readings of the request would lead to materially different work.
- If a simpler approach exists, say so in a sentence and continue with the task as asked — don't quietly narrow, widen, or transform it.
- For medium and large tasks, plan top-down: high-level design first, then components, then code. Trivial tasks don't need a plan.

## 2. Simplicity First — the minimality ladder

**Minimum code that solves the problem. Nothing speculative.**

@~/.claude/skills/shared/minimality-ladder.md

The ladder is the single test for "is this warranted?" — during implementation, during design, and during review. In a review, name the rung that should have caught each unnecessary abstraction.

(Ladder adapted from ponytail, MIT. Canonical copy: `~/.claude/skills/shared/minimality-ladder.md` — do not inline it here.)

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### File editing
- Modify existing source files with the Edit tool, one logical change per call, so I can review each diff. Use Write for new files.
- Don't rewrite source files in place via Bash (`python3 - <<EOF`, `sed -i`, `perl -i`). If Edit fails, re-read the file and retry with a corrected match.
- Bash is fine for reading, searching, and running commands (tests, linters, git, builds).

**Exceptions:**
- Mechanical bulk changes (renames, import rewrites, codemods): a script is fine. Say what it does and which files it touches first, then show `git diff --stat` afterward.
- When I've explicitly said to work autonomously (e.g. "auto mode", "just do it").

## 4. Goal-Driven Execution

**Define success criteria up front.**

Transform tasks into testable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step]
2. [Step]
3. [Step]
```

Strong success criteria let you work independently. Weak criteria ("make it work") require constant clarification.

The tests, type checker, and linter are the acceptance check. Don't layer a separate verification pass on top of them, and don't re-read files or re-run checks to confirm work you've already confirmed.

## 5. Personal skills

My skills in `~/.claude/skills/` encode preferences I've already tuned. When one of them and a plugin skill or built-in command cover the same task, use mine — for example `python-code-review` over the built-in `/code-review`. Plugin skills and built-ins are fine when no personal skill covers the task, or when I name one.

## 6. Miscellaneous
- Prefer CLI tools over their MCP equivalents when both are available (e.g., `git`/`gh` over GitHub MCP, `kubectl` over Kubernetes MCP, `aws`/`gcloud` over their MCP counterparts). CLIs use far fewer tokens per operation, are more reliable in practice, and let you pipe with `jq`/`grep`/`awk` so intermediate output stays out of context. Reach for an MCP only when no CLI covers the capability (e.g., Context7 for docs, Linear). For Notion, see the bullet below.
- Use Context7 to check library and API docs whenever the answer depends on a library's current API, version-specific behavior, or anything that may have changed since your training. Don't wait to be asked.
- Before saying something doesn't exist or isn't known, web search first — especially for recent versions, releases, or compatibility info
- Plans go in the project's `.claude/plans/` directory, never in `docs/` or anywhere else in the repo. The project `.claude/` directory is gitignored, so plans stay out of version control.
- Confluence edits: for a change confined to one heading, use `confluence_update_page_section` with `content_format="storage"` (it replaces only that section and leaves macros, panels and inline comments elsewhere intact), not a full-body `confluence_update_page`. Use the full-body update only for edits spanning several sections. Either way, re-fetch the page version right before saving. The section tool is a deferred MCP tool, so load its schema with ToolSearch first.
- Notion: use the `ntn` CLI for page work and the Notion MCP for database-heavy work. Follow the `notion-cli` skill for the commands, the CLI-or-MCP choice, and the quirks.
- Never add attribution to commit messages or PR descriptions: no `Co-Authored-By` trailer and no "Generated with Claude Code" line. The `attribution` setting enforces this; this line is the backup.

## 7. Delegation & Output Shape

### Delegation
Delegate to a subagent only for large tracks of work that are genuinely independent and parallelizable — a wide multi-file investigation, for example. Don't delegate what you can finish in a handful of tool calls, and don't use subagents to verify or double-check your own work. If one subagent can do the job, use one rather than several.

### Written deliverables
Match the length of written documents (plans, `.hac/` files, handovers, reports) to what the task needs. Cover the substance without padding: no filler sections, redundant summaries, or boilerplate.

### Explanations & output format
- When explaining, reviewing, or planning for me, write about 80% toward ASD-STE100: short sentences (about 20 words for steps, 25 for descriptions), active voice, one idea per sentence, one term per concept. Keep exact technical terms, identifiers, and numbers unchanged.
- Do not apply this to code, comments, docstrings, commit messages, config, or any output that a tool or another agent will read.
- Default format is Markdown. Use HTML only when I ask for it.

## 8. Coding Conventions

### Tooling & QA
- Always use `.venv` when available.
- Detect and use whatever the project already has configured (check `pyproject.toml`/deps) rather than assuming specific tools — e.g. for docstring coverage or doc-site generation.
- Don't chase pyright stub warnings for external dependencies — ignore them, not worth the noise.

### Comments & Docstrings
- Docstrings: Google-style on all public methods, enforced by lint rules + coverage tooling if configured. One-liners are fine for trivial methods; use `Args/Returns/Raises` only when the signature isn't self-explanatory.
- State purpose only — what it does / what it returns. Don't explain rationale, don't narrate how two callers "must agree," and don't cross-reference other functions or pipeline stages as justification. That's design-doc material (`.hac/decisions.md`), not docstring material.
- If a non-obvious invariant truly must be flagged, one short clause is enough — not a paragraph.
- Class-level docstrings go on the class, not `__init__`.
- Keep module/class docstrings generic — describe purpose and role, not concrete class/function names or implementation details. Names and signatures change; a docstring that has to be touched on every refactor is fragile. Say what the module *does* structurally (e.g. "defines the ports the runner depends on"), not which specific classes do it.
- Inline comments follow the same rule: explain a non-obvious *what*, not the reasoning behind a design choice or which other file depends on this behaving a certain way. If two things must stay in sync, enforce that with a test or the code structure — not a comment.
- `Created by @author on <date>` header line is fine to keep (creation date only, not last-touched — that's git blame's job).

**Example:**
```python
# Too verbose — explains rationale + cross-references other pipeline stages
"""True when every BreastView has exactly one output.

Single source of truth for the four-view rule, which both gates CPC blending
(cross_case_task) and sets each prediction's inference_mode (format_output)...
"""

# Correct — states purpose, stops
"""True when every BreastView has exactly one output."""
```

### Code Style
- No blanket `print()` ban — prefer the project logger or `rich.console` for application code. `print()`/`pprint` is fine for quick smoke tests or examples.
- Prefer composition over inheritance, unless deliberately extending a protocol/entity hierarchy.
- Add helper functions after the main function that calls them.

### Testing
- Add tests when behavior changes; doc-only changes don't need new tests unless fixtures/examples change.
- For private method tests, add double underscore i.e. for `_example_func` use `test__example_func`

### Naming Conventions
- **Object-creation prefixes:** *(none)* = fixed fixture value, `make_*` = pure in-memory factory, `create_*` = factory with side effects (DB/API/disk I/O), `build_*` = step-by-step builder pattern.
- **File roles:** `types.py` (pure typing constructs), `models.py` (ML models or domain/ORM models), `entities.py` (pipeline domain objects), `inputs.py` (grouped pipeline-stage inputs).
- Scripts use `verb_noun.py` (executed directly); modules use `noun.py` (imported) — the function name carries the verb, not the filename.
- Prefer plural filenames for collections (`protocols.py`, not `protocol.py`); singular only when the file owns exactly one concept.
- Don't stutter with the parent folder name (`utils/io.py` not `utils/io_utils.py`).

## 9. HAC — Human-Agent Context (.hac/ directory)

Projects may have a `.hac/` directory: a committed, shared context layer that answers "where were we?" across sessions. This is the protocol for using it. Templates and bootstrapping live in the `hac-init` skill. Skip HAC for trivial fixes, formatting, single-file edits, or anything finished in one short session.

- **Bootstrapping:** when I ask to set up HAC, or multi-session work starts in a project without `.hac/`, use `hac-init`. Offer to migrate existing plan files (`.claude/*.md`, `TODO.md`) into `.hac/tasks/`.
- **Session start (multi-session tasks):** read the `.hac/status.md` overview table, then the relevant task file and its session log.
- **New non-trivial work:** before starting, create `.hac/tasks/<task-name>.md` from the `hac-init` template. Add a row to `status.md` (P0 → P1 → P2; within a priority, Active before Blocked before Parked) and to the `README.md` master index (newest-first by completion date).
- **Task files are forward-looking.** Never create one for work that is already complete. A finished task with no task file gets a `status.md` → `README.md` row and nothing else; that is the correct state, not a gap to fill.
- **During work:** update task checklists as steps complete, record discoveries in Notes/Findings, and append to the session log at the end of a work block.
- **Parked ideas:** add out-of-scope ideas to the Parked Ideas table in `status.md`, newest-first, with one line of context. No task file.
- **Decisions:** append strategic or architectural choices to `.hac/decisions.md` as Context / Choice / Why / Rejected, and add a row to its quick-reference table and to `README.md`'s decisions table. Decisions are append-only.
- **Status:** 🟢 Active, 🔴 Blocked, 🔵 Parked, ⚪ Done. Transition rules and priority levels are defined once, in each project's `status.md`.
- **Wrap-up:** set the status to ⚪ with the date and move the row to `README.md`'s master index (`—` in `File` if no task file exists). If a task file exists, set its status field and append a final session-log entry.
