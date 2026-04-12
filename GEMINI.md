# agents-dev

## Project Overview

`agents-dev` is a development project based on the AI Agents curriculum.
It is a sibling project to `agents`, sharing tooling and configuration
but maintaining an independent codebase.

## Building and Running

### Dependency Management
This project uses **`uv`** for dependency management.
- **Install all dependencies:** `uv sync`
- **Add a new dependency:** `uv add <package>`
- **Regenerate requirements.txt:** `uv pip compile pyproject.toml -o requirements.txt`

## Development Conventions

### Linting
- `ruff check .` — lint
- `ruff format .` — format

### Environment Configuration
- Copy `.env.example` to `.env` and fill in the required API keys.
- Never commit `.env`.

### MCP Server Preference
- Use the JetBrains MCP server that matches the currently active IDE configuration.
- If multiple servers are available, use the one that is connected and providing tools.
