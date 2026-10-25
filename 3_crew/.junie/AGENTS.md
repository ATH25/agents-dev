# 3_crew Agent Guidelines

This file defines the specific workflow and rules for the `3_crew` sub-project. These rules supplement the repository-wide `AGENTS.md`.

## Workflow Overview

This structured artifact-driven workflow is active **ONLY** when the relevant files are present and specific instructions have been given to use it. If prompted for unrelated tasks, do not look for or use these files.

`requirement-draft.md` → `requirement.md` → `plan.md` → `tasks.md`

### 1. Preparation & Generation (from `prompt-1.md`)
- **Source of Truth**: 
    - Use `requirement-draft.md` as the primary source of truth if present.
    - If `requirement-draft.md` is missing but `requirement.md` exists, use `requirement.md` as the source of truth and proceed to generate the plan and tasks.
- **Artifact Creation**:
    - Generate `requirement.md`: A detailed specification including technical details, environment variables, and business rules.
    - Generate `plan.md`: A step-by-step implementation plan derived from `requirement.md`.
    - Generate `tasks.md`: Actionable tasks in checklist format (`- [ ]`).
- **Data Integrity**: Ensure details (file names, APIs, constraints) are carried forward without being dropped or oversimplified.
- **Archival**: Treat the `completed-tasks` folder as read-only archive/history. Never modify files there.

### 2. Task Execution (from `execution-prompt.md`)
- **Context**: Before executing, read `requirement.md`, `plan.md`, and `tasks.md` to understand full context.
- **Execution Order**: Process tasks in `tasks.md` one at a time, in order.
- **Tracking**: Update `tasks.md` immediately after completing a task by marking it as completed (`- [X]`).
- **Rules**:
    - Do not skip tasks or modify already completed tasks.
    - Keep changes minimal and aligned with the task description.
    - Focus only on `tasks.md` during execution; do not regenerate requirements/plans unless explicitly asked.
    - If a task is unclear, make a reasonable assumption and proceed.

## General Rules
- Use only `tasks.md` for checkboxes (`- [ ]`, `- [X]`).
- All relative paths in prompts refer to the `3_crew` folder.
- Refer to the root `AGENTS.md` for repository-wide MCP preferences and general workflow.
