# agents-dev

`agents-dev` is a development workspace for building and experimenting with AI agents. It provides a clean setup with established tooling and configuration for independent development and testing.

## Project Overview

This repository provides a standalone environment for developing, testing, and experimenting with AI agents using a consistent set of tools and configurations.

### Key Features
- **Dependency Management:** Powered by `uv`.
- **Linting & Formatting:** Uses `ruff` for consistent code style.
- **AI-Ready:** Pre-configured with instructions for Claude, Gemini, and other AI assistants.
- **Experimental Agents:** Includes implementations like the SendGrid-powered Email Agent.

## Project Structure

- `2_openai/deep_research/`: Contains OpenAI-based agents and research tasks.
  - `email_agent.py`: An agent that converts reports into HTML emails using SendGrid.
- `AGENTS.md`: Shared AI assistant workflow guidance.
- `CLAUDE.md` / `GEMINI.md`: IDE-specific assistant configurations.
- `pyproject.toml`: Project metadata and dependencies.

## Setup

1. **Install Dependencies:**
   Ensure you have `uv` installed, then run:
   ```bash
   uv sync
   ```

2. **Configure Environment:**
   Copy the example environment file and fill in your API keys (OpenAI, Anthropic, SendGrid, etc.):
   ```bash
   cp .env.example .env
   ```
   *Note: Never commit your `.env` file.*

3. **Verify Installation:**
   Run the linter to ensure everything is set up correctly:
   ```bash
   ruff check .
   ```

## Running Agents

### Email Agent
The Email Agent can be found in `2_openai/deep_research/email_agent.py`. It requires a `SENDGRID_API_KEY` in your `.env`.

To run the test script:
```bash
python 2_openai/deep_research/email_agent.py
```

## Development Workflow

### Linting & Formatting
Always run the following before committing:
```bash
ruff check .   # Lint
ruff format .  # Format
```

## Project Scope

This repository is focused on building and experimenting with AI agents. 