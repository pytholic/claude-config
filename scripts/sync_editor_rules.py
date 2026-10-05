#!/usr/bin/env python3
"""Generates Zed and Cursor global rule files from ~/.claude/CLAUDE.md."""

import re
import sys
from pathlib import Path

HEADER = "<!-- Generated from ~/.claude/CLAUDE.md by scripts/sync_editor_rules.py. Do not edit. -->\n\n"
CURSOR_FRONTMATTER = (
    "---\n"
    "description: Personal coding preferences (from ~/.claude/CLAUDE.md)\n"
    "alwaysApply: true\n"
    "---\n\n"
)
IMPORT_LINE = re.compile(r"^@(\S+)\s*$", re.MULTILINE)


def main() -> None:
    home = Path.home()
    body = inline_imports((home / ".claude" / "CLAUDE.md").read_text(), home)

    write(home / ".config" / "zed" / "AGENTS.md", HEADER + body)
    write(
        home / ".cursor" / "rules" / "personal.mdc", CURSOR_FRONTMATTER + HEADER + body
    )


def inline_imports(text: str, home: Path) -> str:
    """Replaces each `@path` line with the file's contents."""

    def replace(match: re.Match[str]) -> str:
        path = Path(match.group(1).replace("~", str(home), 1))
        if not path.is_file():
            sys.exit(
                f"Missing import {match.group(1)} (did you clone with --recurse-submodules?)"
            )
        return path.read_text().strip()

    text = IMPORT_LINE.sub(replace, text)
    return text.replace(" — do not inline it here.)", ".)")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
