Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

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
- Always plan in top-down manner. High level design first, then break it down into smaller parts.

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

## 5. Prefer my personal skills over defaults

When a task matches one of my skills in `~/.claude/skills/`, use it instead of a generic approach, a plugin skill, or a built-in agent covering the same ground. My skills encode preferences I've already tuned — defaults don't. Check for a matching personal skill *before* reaching for `superpowers:*`, built-in agents, or ad-hoc process.

Rough mapping (not exhaustive — always scan the skill list):

| Task | Prefer | Over |
|---|---|---|
| Reviewing diffs / PRs / recent changes | `python-code-review` | `pr-review-toolkit:*`, `superpowers:receiving-code-review`, generic review |
| Eliciting underspecified requirements | `interview-me` | ad-hoc clarifying questions |
| Writing pytest tests | `write-tests` | generic test writing, `superpowers:test-driven-development` defaults |
| Python architecture / implementation | `python-dev` | generic Python coding |
| Implementing a plan yourself, agent guiding | `guided-implementation` | `goal-workflow` (that's agent-driven) |
| Debugging a bug / failing test | `systematic-debugging` | `superpowers:systematic-debugging`, ad-hoc debugging |
| Navigating / mapping an unfamiliar codebase | `codebase-research` | ad-hoc grepping, general-purpose research agents |
| Explaining code / walkthroughs | `explain-code` | plain prose explanation |
| LLM / RAG / agent / fine-tuning work | `llm-dev` | generic ML advice |
| Browser automation / web UI testing | `playwright-cli` | ad-hoc playwright scripts |
| Handing off work to another session | `task-handover` | freeform summary |
| Quick code cleanup after a change | `simplify` | ad-hoc refactoring |
| Bootstrapping `.hac/` in any project | `hac-init` | manually creating files or copying from `python-project-scaffold` |
| Writing a PR description | `pr-description` | ad-hoc `gh pr create` prompts, manual template filling |

Plugin skills (`superpowers:*`, `pr-review-toolkit:*`, etc.) are still fine when no personal skill covers the task, or when the user explicitly names one.

## 6. Miscellaneous
- Prefer CLI tools over their MCP equivalents when both are available (e.g., `git`/`gh` over GitHub MCP, `kubectl` over Kubernetes MCP, `aws`/`gcloud` over their MCP counterparts). CLIs use far fewer tokens per operation, are more reliable in practice, and let you pipe with `jq`/`grep`/`awk` so intermediate output stays out of context. Reach for an MCP only when no CLI covers the capability (e.g., Context7 for docs, Notion, Linear).
- Always use Context7 MCP for library/API docs without being asked
- Before saying something doesn't exist or isn't known, web search first — especially for recent versions, releases, or compatibility info
- Plans always go in the project's `.claude/plans/` directory — never in `docs/` or anywhere else in the repo. This applies to plans created manually and those generated by superpowers skills (e.g. `superpowers:writing-plans`). The project `.claude/` directory is already gitignored, keeping plans out of version control.

## 7. Delegation & Output Shape

### Delegation
Delegate to a subagent only for large tracks of work that are genuinely independent and parallelizable — a wide multi-file investigation, for example. Don't delegate what you can finish in a handful of tool calls, and don't use subagents to verify or double-check your own work. If one subagent can do the job, use one rather than several.

### Written deliverables
Match the length of written documents (plans, `.hac/` files, handovers, reports) to what the task needs. Cover the substance without padding: no filler sections, redundant summaries, or boilerplate.

## 8. Coding Conventions

### Tooling & QA
- Always use `.venv` when available.
- Detect and use whatever the project already has configured (check `pyproject.toml`/deps) rather than assuming specific tools — e.g. for docstring coverage or doc-site generation.
- Don't chase pyright stub warnings for external dependencies — ignore them, not worth the noise.

### Docstrings
- Google-style docstrings on all public methods, enforced by lint rules + coverage tooling if configured.
- One-liners are fine for trivial methods; use `Args/Returns/Raises` only when the signature isn't self-explanatory.
- Class-level docstrings go on the class, not `__init__`.
- Keep module/class docstrings generic — describe purpose and role, not concrete class/function names or implementation details. Names and signatures change; a docstring that has to be touched on every refactor is fragile. Say what the module *does* structurally (e.g. "defines the ports the runner depends on"), not which specific classes do it.
- `Created by @author on <date>` header line is fine to keep (creation date only, not last-touched — that's git blame's job).

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

Projects may have a `.hac/` directory — a shared context layer between the human and the agent. It solves the "where were we?" problem across sessions. This section defines the **protocol** for reading and maintaining `.hac/` during sessions. For file templates and bootstrapping, use the `hac-init` skill.

**Skip all of this for:** trivial bug fixes, formatting changes, single-file edits, or anything completable in one short session. Use judgment — if you wouldn't bother writing a plan on paper, don't bother with `.hac/`.

---

### Bootstrapping

If the user asks to "set up hac", "add .hac", "set up working memory", or you begin multi-session work on a project without a `.hac/` directory:

1. Use the `hac-init` skill. It owns the templates and the bootstrapping process.
2. If prior plan files exist elsewhere (e.g., `.claude/*.md`, `TODO.md`), offer to migrate them into `.hac/tasks/`.

### Session Start (multi-session tasks only)

- Read `.hac/status.md` overview table to understand what's active, blocked, and parked.
- Open the relevant task file linked from the table and read the session log.

### During Execution

- **New non-trivial work:** *Before starting* multi-session or multi-step work, create `.hac/tasks/<task-name>.md` using the task template from the `hac-init` skill. Add a row to the `status.md` overview table (ordered by priority: P0 → P1 → P2; within same priority: Active before Blocked before Parked) and the `README.md` master index (newest-first by completion date).

  Task files are forward-looking working memory. Never create one for work that is already complete — a finished task with no task file gets a `status.md` → `README.md` row and nothing else. If you reach wrap-up and no task file exists, that is the correct state, not a gap to fill.
- **Progress:** Update task file checklists as steps complete.
- **Session log:** Append to the session log at the end of a work block.
- **Discoveries:** Record in the Notes/Findings section of the task file.
- **Parked ideas:** When a useful idea surfaces but is out of scope for the current task, add it to the "Parked Ideas" table in `status.md` with a one-line description and the originating context. Insert newest-first by date. Don't create a task file for parked ideas.

### Design Decisions

- When making a strategic or architectural choice, append to `.hac/decisions.md`.
- Use the format: Context, Choice, Why, Rejected (what alternatives were ruled out and why).
- Add a row to the quick reference table at the top of `decisions.md` and the decisions table in `README.md`.
- Decisions are append-only. Never edit or remove past entries.

### Status Transitions

| From | To | Trigger |
|------|----|---------|
| 🟢 Active | ⚪ Done | Agent or user judges the work complete (e.g. before opening a PR) |
| 🟢 Active | 🔴 Blocked | External dependency, unresolved question, or pending review blocks progress |
| 🔴 Blocked | 🟢 Active | Blocker resolved |
| 🔵 Parked | 🟢 Active | Idea promoted — create a task file, remove from Parked Ideas table |
| Any | ⚪ Done | Move the row from `status.md` overview to `README.md` master index |

Done is a local judgment, not an external approval. `.hac/` does not mirror PR/review state — the PR is its own review surface. If a task needs human sign-off before it can be considered complete, keep it 🔴 Blocked ("blocked on review of X") rather than reintroducing a review state.

### Wrap-Up

- Update the task row in `status.md` overview table (status → ⚪, add date).
- Move the completed row to the `README.md` master index. If the work never had a task file, use `—` in the `File` column.
- **If a task file exists:** set its metadata table status to `⚪ Done (YYYY-MM-DD)` and append a final session log entry.
- **If no task file exists:** stop here. Do not create one.
