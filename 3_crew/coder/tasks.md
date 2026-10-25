# Coder Crew Implementation Tasks

Source documents: `requirement.md` (FR-01, FR-02 with FR-02.1 to FR-02.5, FR-05, FR-07, FR-08) and `plan.md` (phases P-01 to P-06).

- `[x]` = completed and verified. `[ ]` = not completed. Items marked *Implemented — verification pending* have code in place but stay unchecked until verified.
- Task IDs are stable. Do not renumber them.
- New tasks follow `REQUIREMENTS_DRIVEN_DEVELOPMENT_WORKFLOW.md` (`T-FR-XX-NN`, `T-FR-XX-NN.N`). Flat `T-0NN` IDs created before RDDW are kept; where migrated, the old ID stays as a superseded entry pointing to its new ID. Active tasks reference the new IDs directly. Migrating the remaining flat IDs (FR-01, FR-05, FR-07, FR-08 tasks) needs owner approval.

## Phase P-01 — Baseline and Decision Gates

- [x] **T-001: Confirm the generated CrewAI project scaffold is present.**
  - Requirement: FR-01 · AC: AC-01
  - Verified: Repository inspection found `pyproject.toml` (`[tool.crewai] type = "crew"`, `crewai[tools]==1.14.1`), `src/coder/crew.py` (`@CrewBase class Coder`), `src/coder/main.py`, `src/coder/config/agents.yaml`, `src/coder/config/tasks.yaml`, and `src/coder/tools/`.

- [x] **T-002: Verify the project runtime and CrewAI version.**
  - Requirement: FR-01 · AC: AC-01
  - Depends on: T-001
  - Done when: In the project's `uv` environment, `uv run python -c "import crewai; print(crewai.__version__)"` prints the version, `crewai_tools` imports successfully, and the latest PyPI version and relevant changelog entries are recorded (per `AGENTS.md`).
  - Verified (2026-10-18):
    - Ran `uv sync` (uv 0.9.26), which created the project-local `.venv` (Python 3.12.7) and `uv.lock`, matching the sibling `stock_picker` and `financial_researcher` projects.
    - `crewai` 1.14.1 and `crewai-tools` 1.14.1 both import from `.venv`.
    - `Coder().crew()` builds the scaffold agents and tasks without an LLM call, using `OPENAI_API_KEY`.
    - Latest PyPI release: `crewai` 1.15.28.
    - Changelog entries relevant to this project:
      - 1.14.0: `CodeInterpreterTool` removed; code-execution parameters (`allow_code_execution`) deprecated. This affects O-1 in `plan.md` §4.4.
      - 1.14.3: E2B and Daytona sandbox tools added (candidates for O-3, but they need an upgrade).
      - 1.14.5: `CrewAgentExecutor` deprecated; crew agents default to `AgentExecutor`.
      - 1.14.7: pluggable default memory backends.
      - 1.15.0: JSON crew definitions.
      - No YAML `llm` or `output_file` changes are documented.
  - Finding: the project `.env` contains only `MODEL` and no `OPENAI_API_KEY`. The key is set in the repository root `.env`. Before `crewai run` can work, add the key to the project `.env` or pass `--env-file ../../.env`.

- [ ] **T-003: Record the approved CrewAI target version.**
  - Requirement: FR-01 · AC: AC-01
  - Depends on: T-002
  - Done when: The owner confirms keeping `crewai[tools]==1.14.1` or approves an upgrade. This task does not change dependency files.

- [ ] **T-004: Get approval for the sandbox design.**
  - Requirement: FR-05 · AC: AC-05 · Open questions: Q-01, Q-02, Q-04, Q-06
  - Done when: The chosen option (O-1, O-2, or O-3 in `plan.md` §4.4), sandbox directory, filename rule, timeout, network and filesystem limits, file retention, and failure behavior are recorded and approved.

- [ ] **T-005: Get approval for the assignment input interface and retained entry points.**
  - Requirement: FR-07 · AC: AC-07 · Open questions: Q-03, Q-09
  - Done when: The source of `assignment` for `run` is defined, and the owner decides whether `train`, `test`, and `run_with_trigger` stay supported (and how a trigger payload maps to `assignment`).

- [ ] **T-006: Get approval for memory scope and tracing destination.**
  - Requirement: FR-08 · AC: AC-08 · Open questions: Q-07, Q-08
  - Done when: Memory defaults/persistence and the tracing destination and authentication are recorded.

- [ ] **T-029: Get a decision on the output file format.**
  - Requirement: FR-02 (FR-02.4; was FR-06) · AC: AC-FR-02-04 · Open question: Q-05
  - Done when: The owner either accepts "code plus summary" with no fixed structure, or approves a structure (for example, R-02). If a structure is approved, update `requirement.md` and T-FR-02-02.2.

## Phase P-02 — YAML Configuration

### FR-02: Define the Coder Crew

#### T-FR-02-01: Configure `agents.yaml`

- [ ] T-FR-02-01.1: Replace the scaffold agents with the single `coder` agent and define its role (draft wording). *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-01.2: Define the `coder` goal with `{assignment}`, sandbox tools, and write-then-run instructions (draft wording). *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-01.3: Define the `coder` backstory (draft wording). *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-01.4: Configure `llm: openai/gpt-5.4-mini`. *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-01.5: Validate the agent configuration (`plan.md` §4.2, steps 1–3).

Functional Requirement:
- FR-02 (FR-02.1, FR-02.2, FR-02.5)

Technical Requirements:
- TR-FR-02-01, TR-FR-02-02

Acceptance Criteria:
- AC-FR-02-01, AC-FR-02-02, AC-FR-02-05, AC-FR-02-06

Dependencies:
- T-001

Completion Conditions:
- `agents.yaml` has exactly one key, `coder`, with non-empty `role`, `goal`, and `backstory` matching `requirement.md` §3.1, and `llm: openai/gpt-5.4-mini`.
- `researcher` and `reporting_analyst` are gone; `{assignment}` is the only placeholder.

Verification Evidence:
- Pending. Validation deferred by the owner until a module is complete.

#### T-FR-02-02: Configure `tasks.yaml`

- [ ] T-FR-02-02.1: Replace the scaffold tasks with the single `coding_task`, with the draft description (including `{assignment}` and sandbox tools) and `agent: coder`. *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-02.2: Define `expected_output` as the code plus a summary of what was done (draft wording; no stricter format until T-029). *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-02.3: Configure `output_file: output/code-task-output.md`. *Implemented 2026-10-19 — verification pending.*
- [ ] T-FR-02-02.4: Validate the task configuration (`plan.md` §4.2, steps 1–3).

Functional Requirement:
- FR-02 (FR-02.3, FR-02.4, FR-02.5)

Technical Requirements:
- TR-FR-02-01

Acceptance Criteria:
- AC-FR-02-03, AC-FR-02-04, AC-FR-02-05, AC-FR-02-06

Dependencies:
- T-001, T-FR-02-01 (the task references the `coder` agent); T-029 for the final output format.

Completion Conditions:
- `tasks.yaml` has exactly one key, `coding_task`, with `description` containing `{assignment}` and sandbox tools, `expected_output` asking for code plus summary, `agent: coder`, and `output_file: output/code-task-output.md`.
- `research_task` and `reporting_task` are gone; `{assignment}` is the only placeholder.

Verification Evidence:
- Pending. Validation deferred by the owner until a module is complete.

#### T-FR-02-03: Add YAML configuration tests

- [ ] T-FR-02-03.1: Add tests under `tests/` that parse both YAML files and check keys, field content, `llm`, `{assignment}`, `agent: coder`, `expected_output`, and `output_file`.
- [ ] T-FR-02-03.2: Confirm the tests pass against the new YAML without calling the model.

Functional Requirement:
- FR-02

Technical Requirements:
- TR-FR-02-01, TR-FR-02-02

Acceptance Criteria:
- AC-FR-02-01 to AC-FR-02-06 (configuration parts)

Dependencies:
- T-FR-02-01, T-FR-02-02

Completion Conditions:
- Tests exist and pass in the project environment with no live model calls.

Verification Evidence:
- Pending.

#### Superseded P-02 tasks (kept for traceability)

- **T-007** → T-FR-02-01.1 to T-FR-02-01.3 (superseded 2026-10-19).
- **T-008** → T-FR-02-01.4 (superseded 2026-10-19).
- **T-009** → T-FR-02-02.1 (superseded 2026-10-19).
- **T-010** → T-FR-02-02.2, T-FR-02-02.3 (superseded 2026-10-19).
- **T-011** → T-FR-02-03 (superseded 2026-10-19).

Later tasks were updated on 2026-10-19 to reference the T-FR-02 IDs directly. These entries remain for historical lookup only.

## Phase P-03 — Sandbox Capability

- [ ] **T-012: Implement the approved sandbox capability.**
  - Requirement: FR-05 · AC: AC-05
  - Depends on: T-003, T-004
  - Done when: The approved option can write a `.py` file only in the approved sandbox directory, run it, and return stdout, stderr, and exit status. For O-2, the tool lives in `src/coder/tools/`, runs Python with list arguments (no shell string), and replaces the `MyCustomTool` placeholder.

- [ ] **T-013: Enforce the approved sandbox limits.**
  - Requirement: FR-05 · AC: AC-05
  - Depends on: T-012
  - Done when: Path confinement (no traversal outside the sandbox directory), timeout, and any approved network or resource limits from T-004 are applied, and requests outside them are rejected with a clear message to the agent.

- [ ] **T-014: Attach the sandbox capability to the `coder` agent.**
  - Requirements: FR-02, FR-05 · AC: AC-05
  - Depends on: T-FR-02-01, T-012, T-013
  - Done when: The `coder` agent factory has only the approved sandbox capability (tool or approved execution flags). `code_execution_mode="unsafe"` is not used unless explicitly approved in T-004.

- [ ] **T-015: Add sandbox tests.**
  - Requirement: FR-05 · AC: AC-05
  - Depends on: T-012, T-013
  - Done when: Tests cover a successful run with known output, a non-zero exit, a timeout, and a rejected path traversal, using only harmless test code. (For O-1, tests that need Docker are marked and skipped when Docker is unavailable.)

## Phase P-04 — Crew and Entry-Point Wiring

- [ ] **T-016: Replace the scaffold factories in `crew.py` with `coder` and `coding_task`.**
  - Requirement: FR-02 (FR-02.1, FR-02.3) · AC: AC-FR-02-01, AC-FR-02-03, AC-FR-02-05 · TR: TR-FR-02-01, TR-FR-02-02
  - Depends on: T-FR-02-01, T-FR-02-02, T-014
  - Done when: `crew.py` has `@agent def coder` reading `self.agents_config["coder"]` and `@task def coding_task` reading `self.tasks_config["coding_task"]`, both with `# type: ignore[index]`. The `researcher`, `reporting_analyst`, `research_task`, and `reporting_task` factories and the `output_file='report.md'` argument are removed. `crew.py` sets no `llm` override.

- [ ] **T-017: Configure the crew flags.**
  - Requirement: FR-08 · AC: AC-08
  - Depends on: T-006, T-016
  - Done when: The `@crew` method returns `Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True, memory=True, tracing=True)` with no commented-out code left in the edited section.

- [ ] **T-018: Implement assignment input and validation in `main.py` for `run`.**
  - Requirement: FR-07 · AC: AC-07
  - Depends on: T-005
  - Done when: `run` gets `assignment` through the approved interface, rejects empty or whitespace-only values before kickoff, and calls `kickoff(inputs={"assignment": assignment})`. `topic`, `current_year`, and the unused `datetime` import are removed.

- [ ] **T-019: Update the other retained entry points for `assignment`.**
  - Requirement: FR-07 · AC: AC-07
  - Depends on: T-005, T-018
  - Done when: Every entry point kept by T-005 (`train`, `test`, `run_with_trigger`) passes `assignment` instead of `topic`/`current_year`. Entry points not kept are removed from both `main.py` and `[project.scripts]` in `pyproject.toml`. `replay` stays unchanged.

- [ ] **T-020: Remove remaining scaffold leftovers.**
  - Requirements: FR-02 (FR-02.4), FR-08 · AC: AC-FR-02-04, AC-FR-02-05, AC-08
  - Depends on: T-014, T-016, T-017
  - Done when: Unused imports and the unused placeholder tool are removed (if not replaced in T-012), and there is no unrelated refactoring or formatting-only churn. `knowledge/user_preference.txt` is left unchanged.

- [ ] **T-021: Add wiring and input tests.**
  - Requirements: FR-02, FR-07, FR-08 · AC: AC-FR-02-01, AC-FR-02-03, AC-FR-02-05, AC-FR-02-06, AC-07, AC-08 · TR: TR-FR-02-01, TR-FR-02-02
  - Depends on: T-014, T-016, T-017, T-018, T-019
  - Done when: Tests (with no live model calls) confirm the crew has one agent with role from `coder` and one task, the exact crew flags, `assignment` reaching kickoff with placeholders resolved, and empty input being rejected.

## Phase P-05 — Documentation Alignment

- [ ] **T-022: Rewrite the README for the Coder Crew.**
  - Requirements: FR-01, FR-02, FR-05, FR-07, FR-08 · AC: AC-01, AC-FR-02-01 to AC-FR-02-06, AC-05, AC-07, AC-08
  - Depends on: T-017, T-019, T-020
  - Done when: The README explains setup with `uv`, `OPENAI_API_KEY`, how to provide `assignment`, sandbox prerequisites (for example, Docker for O-1), memory/tracing prerequisites, where the `.py` file and `output/code-task-output.md` are written, and how to reset memory. The research-crew and `report.md` text is gone.

- [ ] **T-023: Document sandbox safety and failure behavior.**
  - Requirement: FR-05 · AC: AC-05
  - Depends on: T-004, T-013
  - Done when: The README (or a linked section) describes the approved limits and what an operator sees on success, failure, and timeout.

## Phase P-06 — Validation

- [ ] **T-024: Run lint and automated tests.**
  - Requirements: FR-01, FR-02, FR-05, FR-07, FR-08 · AC: AC-01, AC-FR-02-01 to AC-FR-02-06, AC-05, AC-07, AC-08
  - Depends on: T-FR-02-03, T-015, T-021, T-022, T-023
  - Done when: `ruff check .` passes, all tests pass in the project environment, `coder.crew` imports, and the installed CrewAI version matches T-003.

- [ ] **T-025: Validate access to `openai/gpt-5.4-mini`.**
  - Requirement: FR-02 (FR-02.2) · AC: AC-FR-02-02
  - Depends on: T-003, T-FR-02-01
  - Done when: One controlled call through CrewAI confirms the model works with the configured key. No secret is printed or committed.

- [ ] **T-026: Run one harmless end-to-end assignment.**
  - Requirements: FR-02 (FR-02.3, FR-02.4, FR-02.5), FR-05, FR-07, FR-08 · AC: AC-FR-02-03, AC-FR-02-04, AC-FR-02-06, AC-05, AC-07, AC-08
  - Depends on: T-024, T-025
  - Done when: With a deterministic assignment (for example, "print the first 10 Fibonacci numbers"), the run log shows `{assignment}` resolved, a `.py` file written in the sandbox directory, the file executed, and the execution result returned to the agent.

- [ ] **T-027: Verify the output file.**
  - Requirement: FR-02 (FR-02.4) · AC: AC-FR-02-04
  - Depends on: T-026
  - Done when: `output/code-task-output.md` exists and contains the Python code and a non-empty summary that match the assignment.

- [ ] **T-028: Verify memory and tracing, and record acceptance evidence.**
  - Requirement: FR-08 · AC: AC-08
  - Depends on: T-006, T-026
  - Done when: The run shows memory and tracing enabled with no configuration errors, trace evidence is available at the approved destination, and results for AC-01, AC-FR-02-01 to AC-FR-02-06, AC-05, AC-07, and AC-08 are recorded.

## Traceability Matrix

| FR | Acceptance criteria | Technical requirements | Phases | Tasks |
|----|---------------------|------------------------|--------|-------|
| FR-01 | AC-01 | — | P-01, P-05, P-06 | T-001 ✅, T-002 ✅, T-003, T-022, T-024 |
| FR-02 | AC-FR-02-01 to AC-FR-02-06 | TR-FR-02-01, TR-FR-02-02 | P-01, P-02, P-03, P-04, P-05, P-06 | T-029, T-FR-02-01, T-FR-02-02, T-FR-02-03, T-014, T-016, T-020, T-021, T-022, T-024, T-025, T-026, T-027, T-028 |
| FR-03 | AC-03 (superseded) | — | — | Superseded by FR-02.2 |
| FR-04 | AC-04 (superseded) | — | — | Superseded by FR-02.3 |
| FR-05 | AC-05 | — | P-01, P-03, P-05, P-06 | T-004, T-012, T-013, T-014, T-015, T-023, T-024, T-026 |
| FR-06 | AC-06 (superseded) | — | — | Superseded by FR-02.4 |
| FR-07 | AC-07 | — | P-01, P-04, P-05, P-06 | T-005, T-018, T-019, T-021, T-022, T-024, T-026 |
| FR-08 | AC-08 | — | P-01, P-04, P-05, P-06 | T-006, T-017, T-020, T-021, T-022, T-024, T-026, T-028 |

### Identifier migration (2026-10-19)

| Old ID | New ID |
|--------|--------|
| T-007 | T-FR-02-01.1 to T-FR-02-01.3 |
| T-008 | T-FR-02-01.4 |
| T-009 | T-FR-02-02.1 |
| T-010 | T-FR-02-02.2, T-FR-02-02.3 |
| T-011 | T-FR-02-03 |
| FR-03 / AC-03 | FR-02.2 / AC-FR-02-02 |
| FR-04 / AC-04 | FR-02.3 / AC-FR-02-03 |
| FR-06 / AC-06 | FR-02.4 / AC-FR-02-04 |
| AC-02 | AC-FR-02-01 |
| AC-09 | AC-FR-02-03, AC-FR-02-05 |
