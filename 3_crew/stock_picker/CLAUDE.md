# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

CrewAI project (`crewai[tools]==1.14.1`, Python >=3.10,<3.14) scaffolded via `crewai create crew stock_picker`. See `AGENTS.md` in this directory for the full CrewAI API reference (agent/task/crew/flow patterns, YAML config rules, tool authoring) — consult it before writing or modifying any CrewAI code, since the API surface changes frequently and training data is likely stale.

## Commands

```bash
uv sync                              # install dependencies
uv run run_crew                      # run the crew (same as `crewai run`)
uv run train <n_iterations> <file>   # train the crew
uv run replay <task_id>              # replay from a specific task
uv run test <n_iterations> <eval_llm># test the crew
```

Entry points are defined in `pyproject.toml` under `[project.scripts]` and implemented in `src/stock_picker/main.py` (`run`, `train`, `replay`, `test`, `run_with_trigger`).

No test suite exists yet (`tests/` is empty). Linting uses `ruff check .` / `ruff format .` per the repo-root `CLAUDE.md`.

## Current state: spec vs. implementation (read before editing)

This project is mid-build. `requirement.md` describes the *target* architecture, but the code has only been partially migrated toward it — don't assume the two match without checking:

- **`config/agents.yaml`** has been updated to the target agents: `trending_company_finder`, `financial_researcher`, `stock_picker`, `manager`.
- **`config/tasks.yaml`, `src/stock_picker/crew.py`, `src/stock_picker/main.py`, and `src/stock_picker/tools/custom_tool.py` still contain the original `crewai create` scaffold** — generic `researcher`/`reporting_analyst` agents, `research_task`/`reporting_task` tasks driven by `{topic}`/`{current_year}`, `Process.sequential`, and a placeholder `MyCustomTool`. None of the target tasks (`find_trending_companies`, `research_trending_companies`, `pick_best_company`), the hierarchical process, the manager wiring, `SerperDevTool`, or the `send_push_notification` Pushover tool exist in code yet.
- The `output/` directory (which should hold `trending_companies.json`, `research_report.json`, `decision.md`) has not been created — nothing has produced it yet.

When asked to build or continue this project, treat `requirement.md` as the source of truth for what to build, and treat `crew.py`/`tasks.yaml`/`main.py`/`tools/` as not yet caught up to it.

## Spec-driven workflow files

This directory uses a draft → spec → plan → tasks pipeline, described in `prompt.md`:

1. `requirement-draft.md` — freeform draft requirements (source of truth if present).
2. `requirement.md` — structured spec generated from the draft; detailed enough to implement without guessing (this is the current state).
3. `plan.md` — step-by-step implementation plan generated from `requirement.md` (not yet created).
4. `tasks.md` — checklist-format, execution-ready tasks generated from `plan.md`, using `- [ ]` / `- [X]` (not yet created). This is the *only* file that uses checklist items.

Rules from `prompt.md`:
- Only read/update these files from the current working folder (`3_crew/stock_picker/`), never from a `completed-tasks/` archive folder — that's reference-only and the user moves files there manually.
- Information must flow forward (draft → requirement → plan → tasks) without being dropped or oversimplified; each downstream file must preserve implementation-relevant details (env var names, function/file names, API usage, defaults) from the file that generated it.

## Architecture (CrewAI `@CrewBase` pattern)

- `src/stock_picker/crew.py` — the `StockPicker` class, decorated `@CrewBase`. `@agent` methods build `Agent` objects from `agents_config[...]`; `@task` methods build `Task` objects from `tasks_config[...]`; the `@crew` method assembles `Crew(agents=self.agents, tasks=self.tasks, process=..., ...)`. Agent/task method names must exactly match the keys in the YAML files below.
- `src/stock_picker/config/agents.yaml` / `config/tasks.yaml` — declarative agent (role/goal/backstory/llm) and task (description/expected_output/agent/context/output_file) definitions. `{sector_name}` / `{current_date}` (target) or `{topic}` / `{current_year}` (current scaffold) placeholders are interpolated from the `inputs` dict passed to `crew().kickoff(inputs=...)`.
- `src/stock_picker/main.py` — CLI entry points only; per the file's own comment, avoid adding business logic here beyond building the `inputs` dict and calling `kickoff`.
- `src/stock_picker/tools/custom_tool.py` — custom `BaseTool` implementations shared across agents (target: a Pushover `send_push_notification` tool posting to `https://api.pushover.net/1/messages.json` using `PUSHOVER_TOKEN`/`PUSHOVER_USER` from `.env`, with credentials never logged or exposed in errors).
- `knowledge/` — knowledge-source files (e.g. `user_preference.txt`) loadable via `knowledge_sources` on an `Agent` or `Crew`.
- Per `requirement.md`, the target `Crew` uses `Process.hierarchical` with a dedicated `manager_agent` (not the default `Process.sequential` currently in `crew.py`), plus `memory=True` and `tracing=True`.

## Secrets

`.env` holds `OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER` (per `requirement.md`; currently only `MODEL` is set). Never hard-code these in Python/YAML, never log them, and fail with a clear error naming the missing variable (without exposing others) when one is absent.
