# Stock Picker CrewAI — Implementation Plan

Generated from `requirement.md`. This plan organizes the requirement into an ordered set of implementation phases. Section references (`§N`) point back to the corresponding section in `requirement.md` so no detail is dropped. `tasks.md` (generated next) will break each phase below into checklist-tracked, execution-ready tasks.

## Current State (baseline this plan builds from)

- `config/agents.yaml` already defines `trending_company_finder`, `financial_researcher`, `stock_picker`, `manager` with `{sector_name}`/`{current_date}` placeholders — matches target roughly but has no `tools:` wiring (tools are attached in Python, not YAML, per CrewAI convention) and no per-agent `llm` override validation needed since `openai/gpt-5.4-mini` is already set on all four. Its `trending_company_finder.goal` text currently reads "top 2–3 distinct publicly traded companies" (copied from requirement.md §6.1) — per §19 v1.3 this must be edited to say "exactly 3" so the agent's own instructions match the enforced count.
- `config/tasks.yaml`, `crew.py`, `main.py`, `tools/custom_tool.py` still contain the original `crewai create` scaffold (`researcher`/`reporting_analyst`, `research_task`/`reporting_task`, `Process.sequential`, placeholder `MyCustomTool`) and must be replaced.
- `output/` directory does not exist.
- `.env` only defines `MODEL`; `OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER` are not yet present.
- `pyproject.toml` already declares `crewai[tools]==1.14.1`, so `crewai_tools.SerperDevTool` is available without adding a dependency; `requests` is available transitively via crewai's dependency tree and can be used directly for the Pushover POST (§8).
- No Pydantic models module exists yet; v1.1 (§19) requires one before task/crew wiring can use `output_pydantic`.
- v1.2 (§19) tightens two things beyond v1.1: (a) the Pydantic models must not narrow the research content already specified in §6.2/§7.2 — several fields need to be split out more granularly than the v1.1 model draft had them; (b) task dependency/context wiring and the "no fabricated recommendation" rule must be enforced programmatically (Pydantic validators), not left to YAML/LLM instructions alone.
- v1.3 (§19) fixes the flow at exactly 3 → 3 → 1: `find_trending_companies` must return **exactly 3** unique companies (not "2 or 3" — v1.3 explicitly overrides every "2–3" reference elsewhere in this document, including §6.1's and §16's literal wording, for this version), `research_trending_companies` must research **exactly those same 3** companies (no more, no fewer, no substitutions), and `pick_best_company` must not run unless all 3 are validated. The "exactly 3, same tickers" check between the two lists cannot be expressed inside a single Pydantic model (a model can't see its sibling task's output), so it requires a CrewAI task `guardrail` in `crew.py` in addition to the Phase 3 field validators.

## Phase 1 — Environment & Secrets (§5, §14)

1. No placeholders are written to `.env` — the user populates real values for `OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER` themselves. Code reads all four via `os.environ` at the point of use (SerperDevTool picks up `SERPER_API_KEY` itself; the Pushover tool reads `PUSHOVER_TOKEN`/`PUSHOVER_USER` directly; `OPENAI_API_KEY` is read by the LLM client).
2. Decide where env-var presence is validated: at crew construction (`crew.py`) or at the entry point (`main.py`). Plan: validate in `main.py` `run()` before calling `kickoff()`, so a missing var fails fast with a message naming only the missing variable (§5, §14) — never dump all env state or other secret values in the error.
3. Confirm `.env` stays out of version control (already covered by root `.gitignore`; no action needed unless verification reveals otherwise).

## Phase 2 — Custom Pushover Tool (§8, §6.3)

Implement `send_push_notification` in `src/stock_picker/tools/custom_tool.py`, replacing the placeholder `MyCustomTool`:

1. `BaseTool` subclass (or `@tool` decorator function — pick one consistent with the rest of the file) named to match `send_push_notification`.
2. Pydantic input schema with a single `message: str` field (the 1–3 sentence summary containing company name, ticker, and rationale).
3. `_run` implementation:
   - Read `PUSHOVER_TOKEN` and `PUSHOVER_USER` from environment (`os.environ`), not hard-coded.
   - `POST https://api.pushover.net/1/messages.json` with `token`, `user`, `message`.
   - Use a reasonable timeout (e.g. 10s) via `requests.post(..., timeout=10)`.
   - Raise/return a clear error on non-2xx response without including token/user values in the error text or logs.
   - Return a short success string on success.
4. Export the tool from `tools/__init__.py` if other tools follow that convention (currently empty — fine to leave empty and import directly from `custom_tool` in `crew.py`).

## Phase 3 — Pydantic Output Models (§19, v1.1–v1.3)

Add a new module `src/stock_picker/models.py` defining the four Pydantic models required by v1.1, with the schema completeness requirements added by v1.2 and the exact-3-companies rule added by v1.3:

1. `TrendingCompany` — one field per data point required in §7.1's per-company output: company name, ticker symbol, why it's currently trending, key recent catalysts, source references/URLs where available. (Unchanged by v1.2/v1.3 — §7.1's five data points already map one-to-one to this model.)
2. `TrendingCompanyList` — wraps a `list[TrendingCompany]`. Per v1.3 (superseding v1.2's "2 or 3" range), this must **enforce, not just describe**, "exactly 3 unique companies": add a field validator that raises if the list length isn't exactly 3, or if any two entries share a ticker (normalized case/whitespace) — matching §6.1's "do not return the same company under different names or ticker representations."
3. `TrendingCompanyResearch` — per v1.2, must carry the full, **un-narrowed** set of data points from §6.2/§7.2 as distinct fields rather than merged ones (v1.3 does not change this — only the company *count* changes, not the per-company field content). The v1.1 draft merged several §6.2/§7.2 items into combined fields (e.g. one "business and competitive position" field, no explicit analyst-sentiment or debt/liquidity field); v1.2 requires each of the following to be its own field: company name, ticker, investment thesis, business model and major revenue drivers, competitive position, recent revenue/earnings performance, revenue/earnings growth trends, profitability and margins, cash-flow and balance-sheet strength, debt and liquidity, recent earnings results and management guidance, valuation considerations, recent news/catalysts, material risks, analyst sentiment (when useful/current — may be empty), bull case, bear case, overall assessment, source references where available.
4. `TrendingCompanyResearchList` — wraps a `list[TrendingCompanyResearch]`. Per v1.3 (superseding v1.2's "at least 2" rule), must contain **exactly 3** unique research records; add a field validator that raises if the list length isn't exactly 3 or contains duplicate tickers. This is still only a self-consistency check — a model-level validator cannot see the sibling `TrendingCompanyList` output to confirm the ticker **sets** match exactly, which v1.3 explicitly requires ("whose ticker set matches the ticker set produced by `TrendingCompanyList`", "research for unrelated tickers must cause validation to fail"). That cross-task check is not expressible inside a single Pydantic model and is added as a CrewAI task `guardrail` in Phase 5 instead.

These models are consumed by `crew.py` (Phase 5), where `TrendingCompanyList` and `TrendingCompanyResearchList` are attached via `output_pydantic=` on the corresponding `Task()` calls. They are **not** referenced from `tasks.yaml` — CrewAI's YAML config cannot hold Python types, so `output_pydantic` must be set in the `@task` method itself, while `description`/`expected_output`/`agent`/`output_file` stay YAML-driven (Phase 4).

CrewAI still serializes `output_pydantic` results to the task's `output_file` as JSON, so `output/trending_companies.json` and `output/research_report.json` remain valid JSON (§12) and are now additionally schema- and rule-validated. A validator raising `ValueError` fails that task's structured-output parse, which halts crew execution before `pick_best_company` can run — this is the programmatic enforcement v1.2 requires and v1.3 tightens to "not exactly 3 valid unique companies, research not covering exactly those 3 companies (missing, duplicate, or unrelated tickers)" (§19 v1.2 & v1.3, §14), superseding reliance on task-description behavioral instructions alone. `pick_best_company` is otherwise unaffected — no Pydantic model is required for it, and it keeps producing `output/decision.md` as free-form markdown.

## Phase 4 — Task Configuration (`config/tasks.yaml`) (§7)

Replace `research_task`/`reporting_task` with three tasks, each interpolating `{sector_name}` / `{current_date}`:

1. **`find_trending_companies`** — agent: `trending_company_finder`. Description covers company name, ticker, why trending, key catalysts, source references. `expected_output`: structured list of **exactly 3** unique companies (§19 v1.3 — supersedes the earlier "2–3" wording). `output_file: output/trending_companies.json`. Structured output is enforced by `output_pydantic=TrendingCompanyList` set in `crew.py` (Phase 3, Phase 5), not in this YAML file.
2. **`research_trending_companies`** — agent: `financial_researcher`. Description covers business model, financials, growth, profitability, cash flow/balance sheet, valuation, competitive position, catalysts, risks, bull/bear case, overall assessment, sources. `output_file: output/research_report.json`. Structured output is enforced by `output_pydantic=TrendingCompanyResearchList` set in `crew.py` (Phase 3, Phase 5), not in this YAML file.
3. **`pick_best_company`** — agent: `stock_picker`. Description covers selection, ticker, thesis, reasons, catalysts, risks, ranking justification, and instructs the agent to call `send_push_notification` after deciding. `output_file: output/decision.md`. No `output_pydantic`.

**Task dependency/context wiring (§19 v1.2):** the requirement now explicitly forbids wiring the same task dependency in both YAML and Python. This YAML file therefore carries **no `context:` key** for any task — dependency wiring lives exclusively in `crew.py`'s Python `context=[...]` arguments (Phase 5). Rationale for choosing Python over a YAML `context:` key: `AGENTS.md` (this project's own CrewAI reference for the installed `crewai==1.14.1`) documents task dependencies only via the Python `context=[self.other_task()]` pattern in its Crew Class Pattern example, and never shows `context:` as a `tasks.yaml` key — so Python-level wiring is the mechanism known to be supported by the installed version, per §19 v1.2's "prefer YAML when supported by the installed version" fallback clause.

Both JSON-output tasks must produce valid JSON (verified in Phase 8), now additionally validated against their Pydantic schemas.

## Phase 5 — Crew Orchestration (`crew.py`) (§6, §9, §11, §19, v1.1–v1.3)

Rewrite `StockPicker` (`@CrewBase`):

1. `@agent trending_company_finder()` → `Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], verbose=True)`.
2. `@agent financial_researcher()` → `Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()], verbose=True)`.
3. `@agent stock_picker()` → `Agent(config=self.agents_config['stock_picker'], tools=[send_push_notification], verbose=True)`.
4. Manager agent: build a plain `Agent(config=self.agents_config['manager'], allow_delegation=True)` — **not** decorated `@agent`, so it isn't added to `self.agents` and isn't treated as a worker (§9: "Do not include the manager in the normal worker-agent list"). Construct it either as a method called from `crew()` or as a `@crew`-time local, whichever keeps `self.agents` limited to the three workers.
5. Import `TrendingCompanyList` and `TrendingCompanyResearchList` from the new `models.py` (Phase 3). `@task find_trending_companies()` → `Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompanyList)`. `@task research_trending_companies()` → `Task(config=self.tasks_config['research_trending_companies'], context=[self.find_trending_companies()], output_pydantic=TrendingCompanyResearchList, guardrail=<cross-check function, see step 5a>)`. `@task pick_best_company()` → `Task(config=self.tasks_config['pick_best_company'], context=[self.research_trending_companies()])` (no `output_pydantic`). Method names must exactly match the YAML keys from Phase 4. These `context=[...]` arguments are the **only** place dependency wiring is set (§19 v1.2) — `tasks.yaml` must not also declare `context:`.
5a. **New in v1.3:** add a `guardrail` callable on the `research_trending_companies` `Task()` that cross-checks the two lists' ticker sets, since Pydantic validators (Phase 3) can't see a sibling task's output. Because `@task`-decorated methods are memoized by CrewAI, `self.find_trending_companies()` called from inside the guardrail returns the *same* `Task` instance already executed as this task's `context`, so its `.output` is populated by the time the guardrail runs. Sketch:
   ```python
   def _validate_research_matches_trending(self, task_output):
       expected = {c.ticker.strip().upper() for c in self.find_trending_companies().output.pydantic.companies}
       actual = {r.ticker.strip().upper() for r in task_output.pydantic.research}
       if actual != expected:
           return (False, f"Research tickers {actual} do not match the exact 3 trending tickers {expected}")
       return (True, task_output)
   ```
   Confirm the exact `TaskOutput` import path and guardrail return-type contract (`tuple[bool, Any]` per `AGENTS.md`) against the installed `crewai==1.14.1` during implementation (Phase 8).
6. `@crew crew()` → `Crew(agents=self.agents, tasks=self.tasks, process=Process.hierarchical, manager_agent=<manager instance>, verbose=True, memory=True, tracing=True)`.
7. Remove the old `researcher`/`reporting_analyst`/`research_task`/`reporting_task` methods entirely (no backwards-compat shims).
8. Keep `# type: ignore[index]` on every `self.agents_config[...]` / `self.tasks_config[...]` access per CrewAI convention (see `AGENTS.md`).

## Phase 6 — Entry Point (`main.py`) (§4, §14)

1. In `run()`, replace the `topic`/`current_year` inputs with:
   - `sector_name` (from a hard-coded default or `sys.argv`, matching how the existing scaffold takes inputs — plan default: a literal example sector like `"Technology"`, overridable later).
   - `current_date` derived via `datetime.now().strftime('%Y-%m-%d')` in Python, never left for the LLM to infer (§4 explicitly forbids relying on model knowledge for the date).
2. Before calling `StockPicker().crew().kickoff(inputs=inputs)`, validate required env vars (`OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`) are present; raise a clear exception naming the first missing one if not.
3. Leave `train()`, `replay()`, `test()`, `run_with_trigger()` structurally intact, updating their `inputs` dicts to the new `sector_name`/`current_date` shape for consistency.
4. Ensure `output/` is created if CrewAI doesn't auto-create it for `output_file` targets (§12) — add a `Path("output").mkdir(exist_ok=True)` guard in `run()` if testing in Phase 8 shows it's needed.

## Phase 7 — Error Handling (§14, §19 v1.2 & v1.3)

Confirm each of the following surfaces a clear, secret-free error rather than a silent failure or fabricated result:
- Missing `OPENAI_API_KEY` / `SERPER_API_KEY` / `PUSHOVER_TOKEN` / `PUSHOVER_USER` (Phase 6, step 2).
- Pushover HTTP errors (Phase 2, step 3).
- Not exactly 3 valid unique companies from `find_trending_companies`, or `research_trending_companies` producing research that is empty, malformed, for fewer/more than 3 companies, for duplicate tickers, or for tickers not in the trending list: per §19 v1.2 & v1.3, this must be **handled programmatically, not only via LLM behavioral instructions**. Enforcement is (a) the `TrendingCompanyList`/`TrendingCompanyResearchList` field validators from Phase 3 (self-consistency: exactly 3, unique tickers) and (b) the `research_trending_companies` task `guardrail` from Phase 5 (cross-consistency: research ticker set exactly equals the trending ticker set). A validator raising `ValueError` or a guardrail returning `(False, ...)` fails that task and halts the crew before `pick_best_company` can run, so no fabricated recommendation is ever produced. The existing task-description behavioral instructions (Phase 4) remain as a first line of defense for the LLM, but the validators/guardrail are the actual enforcement mechanism.

## Phase 8 — Validation Before Completion (§17, §16, §19)

Run in order once Phases 1–7 are implemented:

1. Python syntax check (e.g. `uv run python -m py_compile src/stock_picker/*.py src/stock_picker/**/*.py`).
2. YAML syntax check for `config/agents.yaml` and `config/tasks.yaml`.
3. Confirm every `@agent`/`@task` method name matches its YAML key exactly (manual diff).
4. Confirm task `context` wiring matches §7 dependency order: `find_trending_companies` → `research_trending_companies` → `pick_best_company`, and that it is set **only** in `crew.py` — confirm `config/tasks.yaml` has no `context:` key anywhere (§19 v1.2).
5. Confirm `SerperDevTool` is attached to both `trending_company_finder` and `financial_researcher`; confirm `send_push_notification` is attached to `stock_picker` only.
6. Confirm `manager_agent` is a dedicated `Agent` with `allow_delegation=True`, and `process=Process.hierarchical`.
7. Confirm `verbose=True`, `memory=True`, `tracing=True` are set on the `Crew`.
8. Confirm `find_trending_companies` has `output_pydantic=TrendingCompanyList` and `research_trending_companies` has `output_pydantic=TrendingCompanyResearchList`, and that `pick_best_company` has neither.
9. Confirm `TrendingCompanyResearch` carries the full, un-narrowed field set from §6.2/§7.2 (Phase 3, item 3) rather than the merged v1.1 draft fields (§19 v1.2).
10. Confirm `TrendingCompanyList`'s field validator rejects any list that isn't exactly 3 unique companies, and `TrendingCompanyResearchList`'s field validator rejects any list that isn't exactly 3 unique-ticker entries — both by raising `ValueError` (§19 v1.3, superseding v1.2's 2–3/≥2 ranges).
11. Confirm the `research_trending_companies` task `guardrail` (Phase 5, step 5a) rejects a research list whose ticker set doesn't exactly equal the trending list's ticker set — test conceptually with a substituted, missing, or extra ticker (§19 v1.3).
12. Confirm `config/agents.yaml`'s `trending_company_finder.goal` text says "exactly 3", not "2–3" (§19 v1.3).
13. `ruff check .` / `ruff format .`.
14. If credentials are available, run `uv run run_crew` end-to-end and confirm `output/trending_companies.json`, `output/research_report.json`, and `output/decision.md` all exist, the two JSON files parse, and their contents match the shape of `TrendingCompanyList`/`TrendingCompanyResearchList` with exactly 3 companies each, sharing the same ticker set.
15. Confirm no secrets appear in any committed file, log output, or the generated `output/` artifacts.

## Acceptance Criteria Mapping (§16)

Each of the 20 acceptance criteria in `requirement.md` §16 is satisfied by a specific phase above:
- Criteria 1–2 (runs via standard entry point, accepts `sector_name`/`current_date`) → Phase 6.
- Criteria 3–5 (trending finder uses SerperDevTool, produces 2–3 companies — read as exactly 3 per §19 v1.3, valid JSON output) → Phases 3–5, verified in Phase 8.
- Criteria 6–8 (financial researcher receives prior task output, researches all companies, valid JSON output) → Phases 3–5, verified in Phase 8.
- Criteria 9–12 (stock picker receives report, selects one company with justification, `decision.md` exists, includes name/ticker/rationale/risks) → Phase 4.
- Criteria 13–14 (Pushover call made, message contains name/ticker/rationale) → Phase 2.
- Criterion 15 (credentials from env, never hard-coded) → Phases 1–2.
- Criteria 16–18 (hierarchical process, manager delegation enabled, verbose/memory/tracing) → Phase 5.
- Criterion 19 (all four agents on `openai/gpt-5.4-mini`) → already satisfied in `config/agents.yaml`; re-verify in Phase 8.
- Criterion 20 (no secrets committed) → Phases 1, 7, 8.
- v1.1 structured Pydantic outputs (§19: four models, `output_pydantic` wiring, JSON validity preserved, `decision.md` unaffected) → Phases 3, 4, 5, verified in Phase 8.
- v1.2 schema completeness and programmatic wiring/validation (§19: un-narrowed `TrendingCompanyResearch` fields, single-mechanism task-context wiring, programmatic enforcement of the fewer-than-two-companies/empty-research/no-fabrication rule) → Phases 3, 4, 5, 7, verified in Phase 8.
- v1.3 fixed 3 → 3 → 1 flow (§19: `find_trending_companies` returns exactly 3, `research_trending_companies` researches exactly those 3 via model validator + cross-list guardrail, `pick_best_company` cannot run without all 3 validated, `agents.yaml` wording updated) → Phases 3, 4, 5, 7, verified in Phase 8.
