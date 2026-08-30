The purpose of `requirement-draft.md` is to capture high-level requirements for the project. If missing, use `requirement.md` as the source of truth and build files forward.

All workflow files referenced in this prompt (`requirement-draft.md`, `requirement.md`, `plan.md`, `tasks.md`, and `execution-prompt.md`) must be read and updated only from the current working folder. Do not read from, reuse, or modify files inside the `completed-tasks` folder. Treat `completed-tasks` as archive/reference history only, and ignore it unless the user explicitly asks you to inspect it.

Use this file (or `requirement.md` if the draft is missing) to create or update a detailed and structured specification in `requirement.md`. This document must capture all implementation-relevant details from the draft, including technical expectations, required inputs, environment variables, file names, function names, API usage, configuration values, default values, and any explicit business rules. It should be clear enough for an AI agent (Claude, Gemini, Codex, or Junie) to interpret and act on without guessing missing details.

Only `tasks.md` should use checklist items to track execution:
- [ ] for incomplete tasks
- [X] for completed tasks

From `requirement.md`, the agent should generate a step-by-step implementation plan in `plan.md`. The plan must preserve and organize all important details from `requirement.md` so nothing critical is lost between files.

From `plan.md`, the agent should then create `tasks.md`, which contains a list of actionable, execution-ready tasks, all in checklist format. Each task must include all details needed to implement it correctly, such as required file names, function names, environment variable names, external APIs or libraries, expected inputs and outputs, default values, email addresses, configuration values, and any constraints or rules. `tasks.md` should be detailed enough that an agent can execute the work directly without needing to infer missing information.

Information and implementation details must progressively flow from one file to the next without being dropped or oversimplified. Only `tasks.md` uses checklist-style entries for execution tracking.

---

Agent Execution Instructions

Purpose:
Agents should read and follow the instructions in this file directly. The agent must process the latest `requirement-draft.md` (or `requirement.md` if the draft is missing) and generate all downstream artifacts (`requirement.md`, `plan.md`, and `tasks.md`). The user will continuously update `requirement-draft.md`, and the agent should always work from the latest version. The agent must ensure that implementation details are carried forward from the source of truth into `requirement.md`, then into `plan.md`, and finally into `tasks.md` so the final task list is complete and execution-ready. The agent should not move or archive files; the user will manually move completed work to a `completed-tasks` folder. When following these instructions, always use the active workflow files in the current folder and ignore archived files under `completed-tasks` unless explicitly instructed otherwise.

---------
**Important note**: `requirement-draft.md` mentioned in this file is the `requirement-draft.md` file in the current working folder. If missing, use `requirement.md` and build files forward. Create `requirement.md`, `plan.md`, and `tasks.md` in the current working folder. 









