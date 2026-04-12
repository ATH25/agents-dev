# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Permissions

Always ask the user for explicit permission before editing or writing any file outside of `/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/`.

## Package Management

This project uses `uv` (not pip) for dependency management:

```bash
uv sync                          # Install all dependencies
uv add <package>                 # Add a new dependency
uv pip compile pyproject.toml -o requirements.txt  # Regenerate requirements.txt
```

## Linting

```bash
ruff check .         # Lint
ruff format .        # Format
```

## Project Description

`agents-dev` is a development project based on the AI Agents curriculum.
It shares tooling and configuration with the `agents` project but has an
independent codebase. Use `.env.example` as the template for required API keys.

## Workflow (from AGENTS.md)

- Work from the repository root; keep changes scoped to the requested task.
- For non-trivial tasks: search for relevant files → open key files → propose changes → apply edits.
- Keep edits minimal; avoid formatting-only churn.

## MCP Server Preference

- Support both **PyCharm 2025.3.3** (`pycharm_2025`) and **PyCharm 2026.1** (`pycharm_2026`).
- Use the MCP server that matches the active IDE version.
- If multiple servers are available, default to the one that currently provides tools.
