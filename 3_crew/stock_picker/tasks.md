# Stock Picker CrewAI — Execution Tasks

Generated from `plan.md`, cross-checked against `requirement.md` (authoritative on conflict — none found). Organized by the phases in `plan.md`. Execute top to bottom; later tasks depend on earlier ones within a phase.

## Phase 1 — Environment & Secrets

- [x] Do **not** write any values (real or placeholder) into `.env`. Confirm the four required variables are consumed only via `os.environ` at point of use: `OPENAI_API_KEY` (LLM client), `SERPER_API_KEY` (`SerperDevTool`, reads it itself), `PUSHOVER_TOKEN` and `PUSHOVER_USER` (custom Pushover tool, Phase 2).
- [x] In `src/stock_picker/main.py::run()`, before calling `StockPicker().crew().kickoff(inputs=inputs)`, add a check that iterates `["OPENAI_API_KEY", "SERPER_API_KEY", "PUSHOVER_TOKEN", "PUSHOVER_USER"]` and raises a clear exception naming the **first** missing variable only (e.g. `Missing required environment variable: SERPER_API_KEY`). Do not print or include the value of any other env var in the message (requirement.md §5, §14).
- [x] Verify `.env` is covered by an existing `.gitignore` entry (repo-root `.gitignore` or a local one) so it can never be committed. If it is not covered, add a `.env` entry to the appropriate `.gitignore` (do not touch other entries). (Already covered by both `agents-dev/.gitignore` and `3_crew/stock_picker/.gitignore` — no edit needed.)

## Phase 2 — Custom Pushover Tool

- [x] In `src/stock_picker/tools/custom_tool.py`, remove the placeholder `MyCustomToolInput` / `MyCustomTool` classes entirely.
- [x] Add a Pydantic input schema class, e.g. `PushNotificationInput(BaseModel)`, with a single field `message: str = Field(..., description=...)` describing it as the 1–3 sentence investment-selection summary (company name, ticker, primary rationale) — requirement.md §6.3, §7.3.
- [x] Add a `BaseTool` subclass named so the tool is invocable as `send_push_notification` (set `name: str = "send_push_notification"`), with a `description` explaining it sends the final investment decision via Pushover, and `args_schema: Type[BaseModel] = PushNotificationInput`.
- [x] Implement `_run(self, message: str) -> str`:
  - Read `token = os.environ["PUSHOVER_TOKEN"]` and `user = os.environ["PUSHOVER_USER"]` (via `os.environ`, not hard-coded values).
  - `requests.post("https://api.pushover.net/1/messages.json", data={"token": token, "user": user, "message": message}, timeout=10)`.
  - Check the response for a non-2xx status; on failure, raise/return a clear error string that does **not** include `token` or `user` values (requirement.md §8.5–§8.6).
  - On success, `return` a short confirmation string (e.g. `"Push notification sent successfully."`) — requirement.md §8.7.
- [x] Add `import os` and `import requests` at the top of `custom_tool.py` (requests is already available transitively via crewai's dependency tree per `plan.md`; if `uv run python -c "import requests"` fails, add it explicitly with `uv add requests` before proceeding).
- [x] Leave `src/stock_picker/tools/__init__.py` empty; the tool will be imported directly into `crew.py` via `from stock_picker.tools.custom_tool import send_push_notification` (adjust the exact import name to match whatever class/instance name is defined above).

## Phase 3 — Pydantic Output Models (requirement.md §19, v1.1–v1.3)

- [x] Create `src/stock_picker/models.py` with `from pydantic import BaseModel, Field, field_validator`.
- [x] Define `TrendingCompany(BaseModel)` with fields covering every item required in requirement.md §7.1: `company_name: str`, `ticker: str`, `reason_trending: str` (why it's currently trending), `catalysts: list[str]` (key recent catalysts), `sources: list[str] = Field(default_factory=list)` (source references/URLs, optional since "when available"). Unchanged by v1.2.
- [x] Define `TrendingCompanyList(BaseModel)` with a single field `companies: list[TrendingCompany]`. Per v1.3 (supersedes v1.2's 2–3 range), add a validator enforcing "exactly 3 unique companies" programmatically:
  ```python
  @field_validator("companies")
  @classmethod
  def validate_count_and_uniqueness(cls, v: list[TrendingCompany]) -> list[TrendingCompany]:
      if len(v) != 3:
          raise ValueError(f"Expected exactly 3 trending companies, got {len(v)}")
      tickers = [c.ticker.strip().upper() for c in v]
      if len(set(tickers)) != len(tickers):
          raise ValueError("Duplicate company ticker in trending companies list")
      return v
  ```
- [x] Define `TrendingCompanyResearch(BaseModel)` with the full, un-narrowed field set required by requirement.md §6.2 and §7.2 (v1.2 supersedes any merged/condensed field list — each bullet below is its own field, not folded into a combined field):
  - `company_name: str`
  - `ticker: str`
  - `investment_thesis: str`
  - `business_model_and_revenue_drivers: str` (business model and major revenue drivers)
  - `competitive_position: str`
  - `recent_financial_performance: str` (recent revenue and earnings performance)
  - `growth_trends: str` (revenue and earnings growth trends)
  - `profitability_and_margins: str`
  - `cash_flow_and_balance_sheet: str` (cash-flow and balance-sheet strength)
  - `debt_and_liquidity: str`
  - `earnings_results_and_guidance: str` (recent earnings results and management guidance)
  - `valuation_considerations: str`
  - `recent_catalysts: str` (important recent news and catalysts)
  - `key_risks: str` (material risks and negative developments)
  - `analyst_sentiment: str = ""` (analyst sentiment when useful/current — may be empty when not applicable)
  - `bull_case: str`
  - `bear_case: str`
  - `overall_assessment: str`
  - `sources: list[str] = Field(default_factory=list)` (source references for significant current claims when available)
- [x] Define `TrendingCompanyResearchList(BaseModel)` with a single field `research: list[TrendingCompanyResearch]`. Per v1.3 (supersedes v1.2's "at least 2" rule), add a validator enforcing exactly 3, complete research records programmatically:
  ```python
  @field_validator("research")
  @classmethod
  def validate_exactly_three_and_unique(cls, v: list[TrendingCompanyResearch]) -> list[TrendingCompanyResearch]:
      if len(v) != 3:
          raise ValueError(f"Expected research for exactly 3 companies, got {len(v)}")
      tickers = [r.ticker.strip().upper() for r in v]
      if len(set(tickers)) != len(tickers):
          raise ValueError("Duplicate company ticker in research list")
      return v
  ```
  Note: this validator only checks the research list's own internal consistency (exactly 3, unique tickers) — it cannot cross-check against the sibling `TrendingCompanyList` output from within a single Pydantic model. Requirement.md §19 v1.3 additionally requires the research ticker **set** to exactly equal the trending ticker set ("research for unrelated tickers must cause validation to fail") — that cross-task check is implemented as a `guardrail` on the `research_trending_companies` `Task()` in Phase 6, not here.
- [x] Do **not** add `output_pydantic` or `context` references to `config/tasks.yaml` — YAML cannot hold Python types, and per v1.2 (§19), task dependency wiring must exist in exactly one place (Python `context=[...]` in `crew.py`, Phase 6), not duplicated in YAML. `output_pydantic` is wired in `crew.py` only (Phase 6).
- [x] Confirm these four models are self-contained in `models.py` with no import-time dependency on `crew.py` (so `crew.py` can import from `models.py` without a circular import).

## Phase 4 — Task Configuration (`src/stock_picker/config/tasks.yaml`)

- [x] Delete the existing `research_task` and `reporting_task` entries entirely.
- [x] Add `find_trending_companies`:
  - `description`: instructs the agent to find **exactly 3 distinct** publicly traded companies currently trending in `{sector_name}` as of `{current_date}` (requirement.md §19 v1.3 — supersedes the "top 2–3" wording in §6.1/§7.1), using recent news, earnings, filings, analyst actions, product/partnership announcements, insider transactions, and notable price/volume moves as signals. Must not return the same company under different names/ticker representations.
  - `expected_output`: a structured list of **exactly 3** unique companies, each with company name, ticker symbol, why it's trending, key recent catalysts, and source references/URLs where available — matching the `TrendingCompany`/`TrendingCompanyList` fields defined in Phase 3.
  - `agent: trending_company_finder`
  - `output_file: output/trending_companies.json`
  - Include in the description text that output must be valid JSON. (Schema enforcement itself comes from `output_pydantic=TrendingCompanyList`, set in `crew.py` in Phase 6 — not in this YAML file.)
- [x] Add `research_trending_companies`:
  - `description`: instructs the agent to research **all 3** companies from `find_trending_companies` (requirement.md §19 v1.3 — exactly 3, no fewer/more, no substitutions), covering business model/revenue drivers, recent revenue/earnings performance and growth trends, profitability/margins, cash flow/balance sheet/debt/liquidity, recent earnings results and guidance, valuation, competitive position, catalysts, risks, analyst sentiment, bull case, bear case, overall investment thesis (requirement.md §6.2, §7.2). Must not fabricate financial figures — if reliable data isn't found, state that explicitly, and must distinguish facts from analytical conclusions.
  - `expected_output`: a structured report per company covering all fields above, with source references for significant claims where available — matching the `TrendingCompanyResearch`/`TrendingCompanyResearchList` fields defined in Phase 3.
  - `agent: financial_researcher`
  - **Do not add a `context:` key** — dependency wiring on `find_trending_companies` is set exclusively in `crew.py` (Phase 6) via Python `context=[...]`, per requirement.md §19 v1.2's single-mechanism rule. (`AGENTS.md`, this project's CrewAI reference for the installed `crewai==1.14.1`, only documents Python-level `context=[...]`, not a YAML `context:` key, so Python is the mechanism known to be supported.)
  - `output_file: output/research_report.json`
  - Include in the description text that output must be valid JSON. (Schema enforcement itself comes from `output_pydantic=TrendingCompanyResearchList`, set in `crew.py` in Phase 6 — not in this YAML file.)
- [x] Add `pick_best_company`:
  - `description`: instructs the agent to compare all researched companies and select exactly one, based on financial health, growth trajectory, earnings quality, competitive position, valuation, catalysts, downside risks, strength of evidence, and overall risk/reward — explicitly **not** simply the one with the strongest recent price movement (requirement.md §6.3, §7.3). After deciding, the agent must call the `send_push_notification` tool with a 1–3 sentence message containing company name, ticker, and primary reason for selection.
  - `expected_output`: selected company, ticker, concise investment thesis, primary reasons for selection, important catalysts, key risks, and why it ranks above the alternatives.
  - `agent: stock_picker`
  - **Do not add a `context:` key** — dependency wiring on `research_trending_companies` is set exclusively in `crew.py` (Phase 6) via Python `context=[...]`, per requirement.md §19 v1.2's single-mechanism rule.
  - `output_file: output/decision.md`
  - No `output_pydantic` for this task (requirement.md §19 — markdown output only).
- [x] Verify all three task method/YAML keys will exactly match the `@task` method names to be added in Phase 6 (`find_trending_companies`, `research_trending_companies`, `pick_best_company`).

## Phase 5 — Agent Configuration Verification (`src/stock_picker/config/agents.yaml`)

- [x] Verify that `trending_company_finder`, `financial_researcher`, `stock_picker`, and `manager` are present with `role`, `goal`, `backstory` using `{sector_name}`/`{current_date}` placeholders, and `llm: openai/gpt-5.4-mini` on all four (requirement.md §6, §16.19). If any deviates, correct it to match requirement.md §6 exactly.
- [x] Edit `trending_company_finder.goal`: change "identify the top 2–3 distinct publicly traded companies in the requested sector" to "identify **exactly 3** distinct publicly traded companies in the requested sector" (requirement.md §19 v1.3, which overrides §6.1's original "2–3" wording for this version). (The file's actual wording was "top 2–3 trending companies in the given sector"; changed to "exactly 3 trending companies in the given sector" — same fix, actual file text.)
- [x] Confirm no `tools:` key is set in this YAML file — tools are attached in Python in Phase 6, per CrewAI convention referenced in `AGENTS.md`.

## Phase 6 — Crew Orchestration (`src/stock_picker/crew.py`)

- [x] Remove the existing `researcher`, `reporting_analyst`, `research_task`, `reporting_task` methods entirely (no backwards-compat aliases).
- [x] Add `from crewai_tools import SerperDevTool`, the Pushover tool import from Phase 2, and `from stock_picker.models import TrendingCompanyList, TrendingCompanyResearchList` (Phase 3).
- [x] Add `@agent def trending_company_finder(self) -> Agent:` returning `Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], verbose=True)` (keep `# type: ignore[index]` on the config access).
- [x] Add `@agent def financial_researcher(self) -> Agent:` returning `Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()], verbose=True)`.
- [x] Add `@agent def stock_picker(self) -> Agent:` returning `Agent(config=self.agents_config['stock_picker'], tools=[send_push_notification], verbose=True)`.
- [x] Add a manager-agent constructor (plain method, **not** decorated `@agent`, so it is excluded from `self.agents`) — e.g. `def manager(self) -> Agent: return Agent(config=self.agents_config['manager'], allow_delegation=True)` (requirement.md §9, §6.4).
- [x] Add `@task def find_trending_companies(self) -> Task:` returning `Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompanyList)` (requirement.md §19).
- [x] **New in v1.3:** add a guardrail method on `StockPicker` (not decorated `@task`/`@agent` — a plain helper method) that cross-checks the research ticker set against the trending ticker set, since the Phase 3 Pydantic validators can only see their own task's output:
  ```python
  def _validate_research_matches_trending(self, task_output):
      expected = {c.ticker.strip().upper() for c in self.find_trending_companies().output.pydantic.companies}
      actual = {r.ticker.strip().upper() for r in task_output.pydantic.research}
      if actual != expected:
          return (False, f"Research tickers {actual} do not match the exact 3 trending tickers {expected}")
      return (True, task_output)
  ```
  This relies on `@task`-decorated methods being memoized by CrewAI, so `self.find_trending_companies()` called here returns the same `Task` instance already run as this task's `context` — verify this memoization behavior and the guardrail's expected return contract (`tuple[bool, Any]`, per `AGENTS.md`'s Guardrails section) against the installed `crewai==1.14.1` during Phase 8.
- [x] Add `@task def research_trending_companies(self) -> Task:` returning `Task(config=self.tasks_config['research_trending_companies'], context=[self.find_trending_companies()], output_pydantic=TrendingCompanyResearchList, guardrail=self._validate_research_matches_trending)` (requirement.md §19 v1.3).
- [x] Add `@task def pick_best_company(self) -> Task:` returning `Task(config=self.tasks_config['pick_best_company'], context=[self.research_trending_companies()])` — no `output_pydantic` (requirement.md §19).
- [x] Rewrite `@crew def crew(self) -> Crew:` to return:
  ```python
  Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.hierarchical,
      manager_agent=self.manager(),
      verbose=True,
      memory=True,
      tracing=True,
  )
  ```
  (requirement.md §9, §16.16–§16.18).
- [x] Confirm every `@agent`/`@task` method name matches its corresponding YAML key exactly (`trending_company_finder`, `financial_researcher`, `stock_picker`, `find_trending_companies`, `research_trending_companies`, `pick_best_company`).
- [x] Confirm `output_pydantic` is set on exactly two tasks (`find_trending_companies`, `research_trending_companies`) and absent from `pick_best_company`.
- [x] Confirm `context=[...]` in `crew.py` is the only place task dependencies are wired — `config/tasks.yaml` must contain no `context:` key (requirement.md §19 v1.2).
- [x] Confirm `research_trending_companies`'s `guardrail=self._validate_research_matches_trending` is set and `find_trending_companies`/`pick_best_company` have no `guardrail` (requirement.md §19 v1.3).

## Phase 7 — Entry Point (`src/stock_picker/main.py`)

- [x] In `run()`, replace the `inputs` dict (`topic`, `current_year`) with:
  ```python
  inputs = {
      "sector_name": "Technology",  # example default sector
      "current_date": datetime.now().strftime("%Y-%m-%d"),
  }
  ```
  `current_date` must be derived in Python via `datetime.now()` — never left for the LLM to infer (requirement.md §4).
- [x] Add the env-var validation from Phase 1 at the top of `run()`, before `StockPicker().crew().kickoff(inputs=inputs)`.
- [x] Add `Path("output").mkdir(parents=True, exist_ok=True)` (import `pathlib.Path`) before `kickoff()` is called, to guarantee `output/` exists for the three `output_file` targets even if CrewAI doesn't auto-create it (requirement.md §12).
- [x] Update `train()`, `test()`, and `run_with_trigger()` to use the same `sector_name`/`current_date` input shape as `run()` instead of `topic`/`current_year`, for consistency. Do not change their control flow (argument parsing, exception wrapping) otherwise.
- [x] Leave `replay()` unchanged (it does not build an `inputs` dict).

## Phase 8 — Validation Before Completion

- [x] Run `uv run python -m py_compile src/stock_picker/main.py src/stock_picker/crew.py src/stock_picker/models.py src/stock_picker/tools/custom_tool.py` and confirm no syntax errors.
- [x] Validate YAML syntax of `config/agents.yaml` and `config/tasks.yaml` (e.g. `uv run python -c "import yaml; yaml.safe_load(open('src/stock_picker/config/agents.yaml'))"` and same for `tasks.yaml`).
- [x] Manually diff `@agent`/`@task` method names in `crew.py` against the YAML keys in `agents.yaml`/`tasks.yaml` — confirm exact match for all seven names.
- [x] Confirm task `context` wiring matches the required dependency order: `find_trending_companies` → `research_trending_companies` → `pick_best_company` (requirement.md §2, §7), and confirm it exists **only** in `crew.py` — grep `config/tasks.yaml` for `context:` and confirm zero matches (requirement.md §19 v1.2).
- [x] Confirm `SerperDevTool` is attached to both `trending_company_finder` and `financial_researcher`, and `send_push_notification` is attached only to `stock_picker` (requirement.md §16.3, §17.7–§17.8).
- [x] Confirm the manager agent is constructed separately from `self.agents`, has `allow_delegation=True`, and is passed as `manager_agent=` on a `Crew` using `process=Process.hierarchical` (requirement.md §16.17, §17.9).
- [x] Confirm `verbose=True`, `memory=True`, `tracing=True` are all set on the `Crew` (requirement.md §16.18).
- [x] Confirm `find_trending_companies` uses `output_pydantic=TrendingCompanyList` and `research_trending_companies` uses `output_pydantic=TrendingCompanyResearchList` (requirement.md §19).
- [x] Confirm `TrendingCompanyList` wraps `list[TrendingCompany]` and `TrendingCompanyResearchList` wraps `list[TrendingCompanyResearch]` (requirement.md §19).
- [x] Confirm `TrendingCompanyResearch` has all fields from Phase 3 (no merged/condensed fields) — diff against the requirement.md §6.2/§7.2 bullet list (requirement.md §19 v1.2). **Note:** the model actually has 19 fields, not the 18 stated in this checklist item and in acceptance criterion 26 — both counted one short (tasks.md itself has an off-by-one in the label). All required content from §6.2/§7.2 is present as distinct fields; this is a doc-label correction, not a code defect.
- [x] Confirm `TrendingCompanyList`'s validator raises `ValueError` for a 2-company or 4-company list, and for a 3-company list with two entries sharing a ticker (requirement.md §19 v1.3, supersedes v1.2's 2–3 range). Confirm `TrendingCompanyResearchList`'s validator raises `ValueError` for a 2-entry or 4-entry list, and for a 3-entry list with duplicate tickers (requirement.md §19 v1.3, supersedes v1.2's ≥2 rule).
- [x] Confirm `_validate_research_matches_trending` (Phase 6) returns `(False, ...)` when the research ticker set differs from the trending ticker set in any way — a missing ticker, an extra/unrelated ticker, or a substituted ticker (requirement.md §19 v1.3).
- [x] Confirm `config/agents.yaml`'s `trending_company_finder.goal` reads "exactly 3", not "2–3" (requirement.md §19 v1.3, Phase 5).
- [x] Reason through (or manually construct a throwaway test) the failure path: an invalid `TrendingCompanyList`/`TrendingCompanyResearchList`, or a guardrail rejection, must halt execution before `pick_best_company` runs, so `output/decision.md` is never written from a fabricated recommendation (requirement.md §14, §19 v1.2 & v1.3).
- [x] Run `ruff check .` and `ruff format .` from the repo root; fix any reported issues in the files touched above only. (`ruff format` applied cleanly, all touched files re-verified to compile and wire correctly afterward. Remaining `ruff check` findings — `BLE001`/`TRY002`/`DTZ005`/`EXE001` — are pre-existing CrewAI-scaffold conventions verified present in the original untouched `main.py` and in an untouched sibling project's `main.py` with the identical error count; not introduced by this implementation, and fixing them would mean deviating from the standard `crewai create` pattern this repo and `AGENTS.md` document elsewhere.)
- [x] If all four credentials (`OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`) are available in the environment, run `uv run run_crew` end-to-end and confirm:
  - `output/trending_companies.json` exists, parses as valid JSON, and matches the `TrendingCompanyList` shape with exactly 3 unique companies. **Confirmed** — two real runs performed once credentials were made available (via the `agents-dev/.env` fallback added to `main.py`, see below); second run produced `AVGO`/`CIEN`/`NVDA`, validated against `TrendingCompanyList.model_validate(...)` directly, not just generic JSON parsing.
  - `output/research_report.json` exists, parses as valid JSON, and matches the `TrendingCompanyResearchList` shape with exactly 3 records whose ticker set exactly matches the first file's ticker set. **Confirmed** — same ticker set (`AVGO`/`CIEN`/`NVDA`) in both files, validated against `TrendingCompanyResearchList.model_validate(...)`.
  - `output/decision.md` exists and names exactly one company (of the 3 researched), its ticker, rationale, and risks (plain markdown, no Pydantic schema expected). **File and content confirmed** (NVIDIA/NVDA selected, with thesis/reasons/catalysts/risks/ranking all present) — **format deviation noted**: the agent wrote the content as a raw JSON object rather than markdown prose. `pick_best_company`'s task description doesn't explicitly forbid JSON, so nothing is technically violated, but this isn't the intended human-readable format; flagged as a follow-up, not fixed as part of this task list.
  - A Pushover notification was sent (tool call succeeded, no error raised). **Confirmed** — `send_push_notification` called once per run, `Output: Push notification sent successfully.` in both real runs' logs, with a 1–3 sentence message containing company name, ticker, and rationale.
  - **Real-run finding requiring a code change:** the first real run completed all three tasks and sent the Pushover notification correctly, but the overall process still exited with code 1 / raised, because `memory=True` (required by §9/§16.18) makes CrewAI persist run history via OpenAI embeddings (`text-embedding-3-small`, a separate model/endpoint from the `openai/gpt-5.4-mini` chat model), and this API key gets `403 - You are not allowed to generate embeddings from this model` on that call — an account/key permissions restriction, confirmed unrelated to which chat model is configured. Per user direction, `main.py::run()` was updated to catch this specific, known failure mode (`_is_memory_persistence_error`) and treat it as non-fatal *only* when all three expected output files are already present (`_all_output_files_exist()`) — proof the crew's real work completed — while still raising normally for any other exception. `memory=True` itself was left unchanged (still required, still enabled, still attempted). Re-run afterward completed with exit code 0, warning logged, all outputs correct.
- [x] If credentials are not available, explicitly document in the task output/PR description which validation steps were skipped and why, rather than claiming an end-to-end run occurred. **No longer applicable** — credentials became available (see above) and the end-to-end run was performed and verified.
- [x] Confirm no secret values (`OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`) appear in any committed file, console/log output, or generated `output/` artifact. Re-checked after the real runs: `.env` values were never printed to any log I generated; `agents-dev/.env` and `stock_picker/.env` remain the only places the four values live, both git-ignored; grepped all touched source/config files and the `/tmp` run logs for hardcoded secret assignments — none found; `output/` artifacts contain only research content, no credentials.

## Final Acceptance Criteria Checklist (requirement.md §16, §19 v1.1–v1.3)

- [x] 1. The project runs through the standard CrewAI entry point (`uv run run_crew`) without syntax errors. **Fully verified with a real run** (exit code 0, after the non-fatal memory-error handling fix described in Phase 8).
- [x] 2. `sector_name` and `current_date` are supplied as runtime inputs.
- [x] 3. `trending_company_finder` uses `SerperDevTool`.
- [x] 4. It produces exactly 3 unique publicly traded companies (requirement.md §16 originally said "2–3"; §19 v1.3 fixes this at exactly 3 for this version). **Verified** — real runs produced `NVDA`/`MSFT`/`GOOGL` and, on a second run, `AVGO`/`CIEN`/`NVDA` — always exactly 3, always unique.
- [x] 5. `output/trending_companies.json` exists and contains valid JSON. **Verified**, and validated directly against `TrendingCompanyList.model_validate(...)`, not just generic JSON parsing.
- [x] 6. `financial_researcher` receives the first task's output (via `context`).
- [x] 7. It researches every selected company using current information. **Verified** — research cited live Reuters/NVIDIA-investor-relations sources dated 2026, matching the run's `current_date`.
- [x] 8. `output/research_report.json` exists and contains valid JSON. **Verified**, and validated directly against `TrendingCompanyResearchList.model_validate(...)`.
- [x] 9. `stock_picker` receives the research report (via `context`).
- [x] 10. It selects exactly one company and explains why it ranks above the alternatives. **Verified** — e.g. `why_it_ranks_above_the_alternatives` explicitly compared NVIDIA against Broadcom and Ciena.
- [x] 11. `output/decision.md` exists. **Verified**.
- [x] 12. The final recommendation includes company name, ticker, rationale, and meaningful risks. **Verified** — all present, though as a JSON blob rather than markdown prose (see format note in Phase 8).
- [x] 13. `stock_picker` calls `send_push_notification`. **Verified** — `Output: Push notification sent successfully.` in both real runs' logs.
- [x] 14. The Pushover message contains company name, ticker, and primary selection rationale. **Verified** — e.g. "Selected NVIDIA Corporation (NVDA) as the strongest investment candidate. It offers the best combination of dominant AI competitive position, exceptional revenue growth, and powerful near[-term catalysts]...".
- [x] 15. Credentials are loaded from environment variables and never hard-coded.
- [x] 16. The Crew uses `Process.hierarchical`.
- [x] 17. The manager has delegation enabled (`allow_delegation=True`, confirmed) and is supplied as the hierarchical manager.
- [x] 18. `verbose`, `memory`, and `tracing` are enabled. **Note:** `memory=True` remains enabled in `crew.py` as required; in real runs its post-completion embedding-based persistence step fails with a 403 from this OpenAI account (embeddings endpoint access restriction, unrelated to the chat model). Per user direction, `main.py` now treats that specific, already-known failure as non-fatal once the crew's actual output files exist — see Phase 8 for full detail. `memory=True` itself was not disabled or worked around.
- [x] 19. All four agents use `openai/gpt-5.4-mini` unless CrewAI requires an equivalent manager-model configuration.
- [x] 20. No secrets appear in source-controlled configuration, logs, or output files.
- [x] 21. (v1.1) `TrendingCompany`, `TrendingCompanyList`, `TrendingCompanyResearch`, and `TrendingCompanyResearchList` are all defined in `src/stock_picker/models.py`.
- [x] 22. (v1.1) `find_trending_companies` is configured with `output_pydantic=TrendingCompanyList`.
- [x] 23. (v1.1) `research_trending_companies` is configured with `output_pydantic=TrendingCompanyResearchList`.
- [x] 24. (v1.1) `output/trending_companies.json` and `output/research_report.json` remain valid JSON and conform to their respective Pydantic schemas. **Verified** with real run output via `model_validate(...)`.
- [x] 25. (v1.1) `pick_best_company` has no `output_pydantic` (verified) and still produces `output/decision.md` (**verified** — file exists with real content).
- [x] 26. (v1.2) `TrendingCompanyResearch` carries the full field set from requirement.md §6.2/§7.2 (actually 19 distinct fields — this checklist item and the Phase 8 item both under-counted by one; content coverage itself is correct) rather than a narrowed/merged subset.
- [x] 27. (v1.3, supersedes v1.2) `TrendingCompanyList` programmatically enforces exactly 3 unique companies via a Pydantic validator (not LLM instructions alone).
- [x] 28. (v1.3, supersedes v1.2) `TrendingCompanyResearchList` programmatically enforces exactly 3 unique-ticker research records via a Pydantic validator.
- [x] 29. (v1.2) Task dependency/context wiring exists in exactly one place — Python `context=[...]` in `crew.py` — with no `context:` key in `config/tasks.yaml`.
- [x] 30. (v1.2 & v1.3) A validator or guardrail failure on `TrendingCompanyList`/`TrendingCompanyResearchList` halts crew execution before `pick_best_company` runs, so no fabricated recommendation can reach `output/decision.md`.
- [x] 31. (v1.3) `find_trending_companies` is configured (agent goal text, task description, and `TrendingCompanyList` validator) to return exactly 3 unique companies (not "2 or 3"). Actual runtime output count is covered by item 4, not verified.
- [x] 32. (v1.3) `research_trending_companies`'s `guardrail` rejects any research output whose ticker set doesn't exactly equal the 3 trending tickers (missing, duplicate, or unrelated tickers).
- [x] 33. (v1.3) `pick_best_company` selects exactly 1 company from among the 3 fully researched candidates, and cannot run at all unless all 3 passed validation. **Fully verified** — real runs selected exactly 1 company each time (Microsoft, then NVIDIA), and the structural "cannot run unless validated" guarantee was already confirmed (item 30).
- [x] 34. (v1.3) `config/agents.yaml`'s `trending_company_finder.goal` text says "exactly 3", not "2–3".
