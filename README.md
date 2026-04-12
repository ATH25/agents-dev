# agents-dev

Development project based on the [AI Agents curriculum](../agents).

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and fill in your API keys
   ```

3. Lint:
   ```bash
   ruff check .
   ruff format .
   ```

## Relationship to `agents`

`agents-dev` shares tooling and configuration with `agents` but has an
independent codebase. Curriculum files (notebooks, guides, assets) are
not present here.
