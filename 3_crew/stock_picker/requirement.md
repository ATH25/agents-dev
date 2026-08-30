# Stock Picker CrewAI — Implementation Requirements

## 1. Objective

Build a complete, runnable CrewAI project named `stock_picker` that researches currently trending publicly traded companies within a user-supplied market sector, performs detailed financial and market research on those companies, selects the strongest investment candidate, writes intermediate and final results to files, and sends the final recommendation through a Pushover push notification.

The project scaffold has already been generated using:

```bash
crewai create crew stock_picker
```

Work within the generated CrewAI project structure. Do not replace CrewAI with a custom orchestration framework.

The implementation must use a hierarchical CrewAI process managed by a dedicated manager agent.

## 2. Functional Flow

The completed application must:

1. Accept a stock-market sector through `sector_name`.
2. Accept or derive the current date as `current_date`.
3. Research current market information and identify 2–3 trending publicly traded companies in that sector.
4. Perform detailed financial and investment research on each selected company.
5. Compare the researched companies and select exactly one as the best current investment candidate.
6. Write intermediate research artifacts and the final decision to the `output/` directory.
7. Send a concise Pushover notification containing the selected company, ticker symbol, and primary investment rationale.
8. Return the final CrewAI task result through the normal CrewAI execution flow.

The workflow must use three worker agents plus one manager:

- `trending_company_finder`
- `financial_researcher`
- `stock_picker`
- `manager`

The workflow must use three tasks:

- `find_trending_companies`
- `research_trending_companies`
- `pick_best_company`

Task dependencies must flow in that order.

## 3. Technology and Implementation Constraints

Required technologies and capabilities:

- CrewAI for agents, tasks, and orchestration.
- `Process.hierarchical` for crew execution.
- `SerperDevTool` for current web/search research.
- Pushover REST API for the final push notification.
- Environment variables loaded from `.env` for secrets.
- OpenAI model `openai/gpt-5.4-mini` for all four agents unless CrewAI requires the manager model to be configured separately.

Do not hard-code secret values in Python or YAML files.

## 4. Runtime Inputs

### `sector_name`

A string identifying the stock-market sector or industry to research.

Examples include `Technology`, `Healthcare`, `Financial Services`, `Energy`, and `Semiconductors`.

### `current_date`

The date against which market research should be considered current. Use `YYYY-MM-DD`.

If possible, derive the current date automatically in the application entry point before calling:

```python
crew().kickoff(inputs=inputs)
```

Do not rely on the LLM's internal knowledge of the current date.

## 5. Environment Configuration

The project must expect:

```dotenv
OPENAI_API_KEY=<your-openai-api-key>
SERPER_API_KEY=<your-serper-api-key>
PUSHOVER_TOKEN=<your-pushover-application-token>
PUSHOVER_USER=<your-pushover-user-key>
```

Pushover endpoint:

```text
https://api.pushover.net/1/messages.json
```

Never embed credential values in prompts, YAML configuration, logs, output files, or committed source code.

If a required credential is missing, fail with a clear error identifying the missing environment variable without exposing other secrets.

## 6. Agent Requirements

### 6.1 `trending_company_finder`

**Role:** Market trends researcher responsible for identifying currently trending publicly traded companies in `{sector_name}`.

**Goal:** Research current information as of `{current_date}` and identify the top 2–3 distinct publicly traded companies in the requested sector that merit deeper investment research.

The agent must use `SerperDevTool` rather than relying solely on model knowledge.

Consider relevant signals such as:

- Recent company news.
- Earnings announcements and guidance.
- Press releases.
- SEC filings or material filing-related news.
- Analyst upgrades, downgrades, or estimate changes.
- Product, customer, partnership, or strategic announcements.
- Insider transactions when relevant and verifiable.
- Significant stock-price or volume movement and its cause.
- Sector-specific developments.

Select 2–3 unique companies. Do not return the same company under different names or ticker representations.

**Backstory:** You are an experienced market researcher skilled at identifying meaningful trends and separating substantive investment developments from short-lived market noise.

**LLM:** `openai/gpt-5.4-mini`

**Tools:** `SerperDevTool`

### 6.2 `financial_researcher`

**Role:** Senior financial researcher with a strong background in company analysis and investment research.

**Goal:** Perform detailed research on every company supplied by `find_trending_companies` and produce a structured, evidence-based comparison for the final stock-selection stage.

For each company, investigate where reliable information is available:

- Company name and ticker.
- Business model and major revenue drivers.
- Recent revenue and earnings performance.
- Revenue and earnings growth trends.
- Profitability and margins.
- Cash flow and balance-sheet strength.
- Debt and liquidity.
- Recent earnings results and management guidance.
- Valuation considerations.
- Competitive position.
- Important recent news and catalysts.
- Material risks and negative developments.
- Analyst sentiment when useful and current.
- Bull case.
- Bear case.
- Overall investment thesis.

Do not fabricate financial figures. If reliable data cannot be found, explicitly state that instead of guessing.

Distinguish factual findings from analytical conclusions.

**Backstory:** You are a thorough senior market and financial researcher who evaluates positive and negative evidence and verifies important claims using current information.

**LLM:** `openai/gpt-5.4-mini`

**Tools:** `SerperDevTool`

### 6.3 `stock_picker`

**Role:** Senior investment analyst responsible for selecting the strongest investment candidate.

**Goal:** Review the complete research output, compare all researched companies, select exactly one company, explain the decision, write the final decision to disk, and send a concise Pushover notification.

The decision must be based on the preceding research rather than simply choosing the company with the strongest recent price movement.

Consider:

- Financial health.
- Growth trajectory.
- Earnings quality.
- Competitive position.
- Valuation.
- Near- and medium-term catalysts.
- Downside risks.
- Strength of available evidence.
- Overall risk/reward relative to the other candidates.

After reaching the decision, use `send_push_notification`.

The notification must be 1–3 sentences and include the company name, ticker symbol, and primary reason for selection.

**Backstory:** You are a meticulous market analyst who synthesizes complex research into disciplined investment decisions and explicitly considers downside risk.

**LLM:** `openai/gpt-5.4-mini`

**Tools:** `send_push_notification`

### 6.4 `manager`

**Role:** Investment research project manager.

**Goal:** Coordinate the hierarchical workflow and delegate work to the appropriate specialized agents.

Ensure:

- Trending-company research occurs first.
- Detailed research covers every selected company.
- Final selection is based on completed research.
- Agents remain focused on their responsibilities.
- The workflow reaches a clear result without unnecessary repeated delegation.

**Backstory:** You are an experienced project manager who understands investment-research workflows and delegates specialized work effectively.

**LLM:** `openai/gpt-5.4-mini`

**Delegation:** `allow_delegation=True`

## 7. Task Requirements

### 7.1 `find_trending_companies`

**Assigned agent:** `trending_company_finder`

Find the top 2–3 distinct publicly traded companies currently trending within `{sector_name}` as of `{current_date}`.

For every company provide:

- Company name.
- Ticker symbol.
- Why it is currently trending.
- Key recent catalysts.
- Important source references or URLs when available.

**Expected output:** A structured list containing exactly 2 or 3 unique companies with enough supporting information for deeper research.

**Output file:** `output/trending_companies.json`

The output must be valid JSON.

### 7.2 `research_trending_companies`

**Assigned agent:** `financial_researcher`

**Context:** `find_trending_companies`

Research every company identified by the first task.

The report should include:

- Company and ticker.
- Investment thesis.
- Business and competitive position.
- Recent financial performance.
- Growth indicators.
- Profitability, cash-flow, and balance-sheet observations.
- Valuation observations.
- Recent catalysts.
- Key risks.
- Bull case.
- Bear case.
- Overall assessment.
- Source references for significant current claims when available.

**Output file:** `output/research_report.json`

The output must be valid JSON.

### 7.3 `pick_best_company`

**Assigned agent:** `stock_picker`

**Context:** `research_trending_companies`

Compare all candidate companies and select exactly one as the strongest investment candidate.

Include:

- Selected company.
- Ticker.
- Concise investment thesis.
- Primary reasons for selection.
- Important catalysts.
- Key risks.
- Why the company ranks above the alternatives.

After determining the winner, call `send_push_notification`.

**Output file:** `output/decision.md`

## 8. Custom Pushover Tool

Implement a CrewAI-compatible custom tool named `send_push_notification`.

It must:

1. Read `PUSHOVER_TOKEN` from the environment.
2. Read `PUSHOVER_USER` from the environment.
3. POST to `https://api.pushover.net/1/messages.json`.
4. Supply `token`, `user`, and `message`.
5. Detect unsuccessful HTTP responses and surface a meaningful error.
6. Never log or expose credentials.
7. Return a short success result after Pushover accepts the message.
8. Use a reasonable HTTP timeout.

Only the final `stock_picker` stage should send the investment-selection notification.

## 9. Crew Configuration

The Crew must use hierarchical processing.

Conceptually:

```python
manager = Agent(
    config=self.agents_config["manager"],
    allow_delegation=True,
)

return Crew(
    agents=self.agents,
    tasks=self.tasks,
    verbose=True,
    memory=True,
    tracing=True,
    process=Process.hierarchical,
    manager_agent=manager,
)
```

Use syntax compatible with the installed CrewAI version.

Required:

- `Process.hierarchical`
- Dedicated `manager_agent`
- `verbose=True`
- `memory=True`
- `tracing=True`

Do not include the manager in the normal worker-agent list if CrewAI expects it to be supplied separately through `manager_agent`.

## 10. CrewAI Configuration Files

Follow the structure generated by `crewai create crew stock_picker`.

### `config/agents.yaml`

Define:

- `trending_company_finder`
- `financial_researcher`
- `stock_picker`
- `manager`

Use `{sector_name}` and `{current_date}` placeholders where appropriate.

### `config/tasks.yaml`

Define:

- `find_trending_companies`
- `research_trending_companies`
- `pick_best_company`

Configure task dependencies/context using the mechanism supported by the installed CrewAI version.

Keep agent and task behavioral configuration in the standard CrewAI configuration files where practical rather than duplicating large prompts in Python.

## 11. Expected Python Components

The completed project must contain or configure:

- `StockPicker` decorated with `@CrewBase`.
- `@agent` method for `trending_company_finder`.
- `@agent` method for `financial_researcher`.
- `@agent` method for `stock_picker`.
- Dedicated manager-agent creation.
- `@task` method for `find_trending_companies`.
- `@task` method for `research_trending_companies`.
- `@task` method for `pick_best_company`.
- `@crew` method returning the configured `Crew`.
- `SerperDevTool` attached to both research agents.
- `send_push_notification` attached to `stock_picker`.
- Runnable entry point supplying `sector_name` and `current_date`.

Use type annotations where practical.

## 12. Output Artifacts

The application must produce:

```text
output/
├── trending_companies.json
├── research_report.json
└── decision.md
```

Ensure the directory exists if CrewAI does not create it automatically.

Do not store secrets in output artifacts.

## 13. Research Quality Rules

All agents must:

1. Treat `{current_date}` as the current research cutoff.
2. Use current search results for time-sensitive claims.
3. Never invent financial metrics, analyst ratings, news, SEC filings, stock prices, or dates.
4. Distinguish facts from analytical judgments.
5. Consider negative as well as positive evidence.
6. Prefer recent and authoritative sources.
7. Corroborate important claims where practical.
8. Treat ambiguous search snippets cautiously.
9. State uncertainty when information cannot be verified.
10. Never present investment performance as guaranteed.

## 14. Error Handling

Handle at minimum:

- Missing `OPENAI_API_KEY`.
- Missing `SERPER_API_KEY`.
- Missing `PUSHOVER_TOKEN`.
- Missing `PUSHOVER_USER`.
- Pushover HTTP errors.
- Empty or malformed research output.
- Fewer than two valid companies.

Do not fabricate a recommendation merely to complete the workflow.

Never expose secrets in error messages.

## 15. Logging and Observability

CrewAI verbose output, memory, and tracing are intentionally enabled.

Logs should make it possible to determine:

- Which task is executing.
- Which agent is responsible.
- Whether external research occurred.
- Whether output artifacts were produced.
- Whether the Pushover notification succeeded.

Never log credentials.

## 16. Acceptance Criteria

Implementation is complete when:

1. The project runs through the standard CrewAI entry point without syntax errors.
2. `sector_name` and `current_date` are supplied as runtime inputs.
3. `trending_company_finder` uses `SerperDevTool`.
4. It produces 2–3 unique publicly traded companies.
5. `output/trending_companies.json` exists and contains valid JSON.
6. `financial_researcher` receives the first task's output.
7. It researches every selected company using current information.
8. `output/research_report.json` exists and contains valid JSON.
9. `stock_picker` receives the research report.
10. It selects exactly one company and explains why it ranks above the alternatives.
11. `output/decision.md` exists.
12. The final recommendation includes company name, ticker, rationale, and meaningful risks.
13. `stock_picker` calls `send_push_notification`.
14. The Pushover message contains company name, ticker, and primary selection rationale.
15. Credentials are loaded from environment variables and never hard-coded.
16. The Crew uses `Process.hierarchical`.
17. The manager has delegation enabled and is supplied as the hierarchical manager.
18. `verbose`, `memory`, and `tracing` are enabled.
19. All four agents use `openai/gpt-5.4-mini` unless CrewAI requires an equivalent manager-model configuration.
20. No secrets appear in source-controlled configuration, logs, or output files.

## 17. Validation Before Completion

Before declaring the implementation complete:

1. Inspect and preserve the generated CrewAI project structure.
2. Validate Python syntax.
3. Validate YAML syntax.
4. Verify Python agent names exactly match YAML agent names.
5. Verify Python task names exactly match YAML task names.
6. Verify task dependencies/context are correctly wired.
7. Verify `SerperDevTool` is available to both research agents.
8. Verify `send_push_notification` is available to `stock_picker`.
9. Verify the manager is configured for hierarchical processing.
10. Verify all output paths.
11. Verify generated JSON files parse successfully.
12. Verify missing credentials fail safely.
13. Run available tests and linting.
14. If credentials are available, perform an end-to-end run and confirm all three output artifacts are generated.

## 18. Scope Boundaries

This is an educational/research stock-selection workflow.

Out of scope unless explicitly requested:

- Automated brokerage integration.
- Executing stock trades.
- Portfolio rebalancing.
- Options or derivatives trading.
- Persistent user portfolios.
- UI/authentication development.
- Real-time streaming market feeds.
- Autonomous recurring scheduling.

The system recommends a researched candidate; it must never place a trade.
