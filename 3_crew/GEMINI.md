# Debate Crew Simulation

## Project Overview
This project is a specialized module within the `agents-dev` workspace focused on building a multi-agent debate simulation using the **CrewAI** framework. The system facilitates a structured debate on a given motion, automating the generation of opposing arguments followed by a reasoned judgment.

The workflow is designed to be agent-driven, progressing from high-level requirements to a detailed task list, ensuring rigorous implementation and verification.

## Building and Running

### Dependency Management
This project uses **`uv`** and **`crewai`** CLI for management.
- **Install dependencies:** `crewai install` (run within the `debate/` directory)
- **Run the simulation:** 
  - `crewai run`
  - `uv run run_crew`

### Environment Configuration
- Ensure `.env` exists in the root of `agents-dev` or within `debate/`.
- Required API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
- Never commit the `.env` file.

## Development Workflow & Conventions

This module follows a strict **Requirement -> Plan -> Task** progression:
1. **Requirement Analysis (`requirement.md`)**: The source of truth capturing technical expectations, file names, and business rules.
2. **Implementation Planning (`plan.md`)**: A step-by-step technical strategy derived from the requirements.
3. **Task Execution (`tasks.md`)**: Actionable, execution-ready tasks in checklist format (`[ ]` / `[X]`).

### Key Files
- **`requirement.md`**: Structured specification for the current task.
- **`prompt-1.md`**: Foundational instructions for agents to manage the workflow artifacts.
- **`debate/src/debate/crew.py`**: Implementation of the CrewAI logic, agents, and tasks.
- **`debate/src/debate/config/`**: YAML configurations for `agents.yaml` and `tasks.yaml`.

## Technical Requirements
- **Python Version**: `>=3.10` and `<3.13`.
- **Framework**: `crewAI >= 0.108.0`.
- **LLM Configuration**:
  - **Debater Agent**: `openai/gpt-4o-mini` (optimized for speed/conciseness).
  - **Judge Agent**: `anthropic/claude-3-7-sonnet-latest` (optimized for complex reasoning).

## Workspace Guidelines
- **Contextual Precedence**: Instructions in this `GEMINI.md` take precedence over general defaults.
- **Surgical Updates**: Always perform targeted changes based on the active `tasks.md`.
- **Tooling**: Prefer using the JetBrains MCP server and `ruff` for linting/formatting.
