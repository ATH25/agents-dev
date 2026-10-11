# Stock Picker Crew

A [CrewAI](https://crewai.com) project that researches currently trending publicly traded companies in a given market sector, performs detailed financial research on them, selects the strongest investment candidate, and sends the final recommendation as a push notification.

This is an educational/research workflow. It recommends a researched candidate; it never places a trade.

## How it works

The crew runs a hierarchical process — a dedicated `manager` agent coordinates three worker agents through three tasks, in order:

| Task | Agent | Output |
|---|---|---|
| `find_trending_companies` | `trending_company_finder` | `output/trending_companies.json` |
| `research_trending_companies` | `financial_researcher` | `output/research_report.json` |
| `pick_best_company` | `stock_picker` | `output/decision.md` |

The flow is a fixed **3 → 3 → 1**:

1. `trending_company_finder` uses `SerperDevTool` to find **exactly 3** unique, currently trending publicly traded companies in the requested sector.
2. `financial_researcher` uses `SerperDevTool` to research all 3 companies (business model, financials, growth, valuation, risks, bull/bear case, etc.).
3. `stock_picker` compares the completed research and selects exactly one company, then sends a Pushover push notification with the company name, ticker, and primary reason for selection.

The first two tasks return structured Pydantic output (`TrendingCompanyList`, `TrendingCompanyResearchList` — see `src/stock_picker/models.py`), which is validated programmatically:

- Both lists are rejected unless they contain exactly 3 unique companies/records (by ticker).
- A guardrail on `research_trending_companies` additionally rejects any research whose ticker set doesn't exactly match the trending companies' ticker set.

If either check fails, execution halts before `pick_best_company` runs — a fabricated final recommendation is never produced.

## Prerequisites

- Python >=3.10, <3.14
- [uv](https://docs.astral.sh/uv/) for dependency management

## Creating a CrewAI project from scratch

This project was originally scaffolded with the CrewAI CLI. For reference, that's the general recipe for starting any new CrewAI crew project:

```bash
uv tool install crewai        # install the CrewAI CLI (one-time)
crewai create crew <name>     # scaffold a new crew project named <name>
cd <name>
crewai install                # (optional) lock and install dependencies
```

`crewai create crew <name>` generates the same layout this project uses: `src/<name>/crew.py`, `src/<name>/main.py`, `src/<name>/config/agents.yaml`, `src/<name>/config/tasks.yaml`, `src/<name>/tools/`, and a `pyproject.toml` with `[tool.crewai] type = "crew"`. From there you customize `agents.yaml`/`tasks.yaml` for your agents and tasks, add any custom tools, and wire it all together in `crew.py` — which is what was done here to build the Stock Picker crew described below.

## Installation

To install *this* project's dependencies:

```bash
uv sync
```

## Environment variables

Create a `.env` file in this directory (`3_crew/stock_picker/.env`) with:

```
OPENAI_API_KEY=
SERPER_API_KEY=
PUSHOVER_TOKEN=
PUSHOVER_USER=
```

- `OPENAI_API_KEY` — used by all four agents' LLM (`openai/gpt-5.4-mini`).
- `SERPER_API_KEY` — used by `SerperDevTool` for web research.
- `PUSHOVER_TOKEN` / `PUSHOVER_USER` — used by the custom `send_push_notification` tool to deliver the final decision via [Pushover](https://pushover.net).

If a required variable is missing, the app fails fast with a clear error naming the missing variable — it never logs or exposes secret values.

`main.py` also falls back to the repository-root `.env` (`agents-dev/.env`) for any of these variables not already set locally, without overriding whatever is already loaded from the local `.env`.

## Running the project

Run from within this directory (`3_crew/stock_picker/`) using either command — they do the same thing:

```bash
crewai run
# or
uv run run_crew
```

`sector_name` (defaults to `"Technology"` in `main.py`) and `current_date` (derived automatically from the system clock, `YYYY-MM-DD`) are passed as inputs to the crew. The date is always derived in code — agents never rely on their own internal notion of "today."

Other entry points (see `pyproject.toml` → `[project.scripts]`):

```bash
uv run train <n_iterations> <filename>   # train the crew
uv run replay <task_id>                  # replay from a specific task
uv run test <n_iterations> <eval_llm>    # test the crew
```

## Output

Each run produces (and overwrites) three files in `output/`:

```
output/
├── trending_companies.json   # the 3 trending companies (structured)
├── research_report.json      # research on all 3 companies (structured)
└── decision.md                # the single selected company + rationale
```

## Project structure

```
src/stock_picker/
├── crew.py               # StockPicker @CrewBase — agents, tasks, hierarchical Crew
├── main.py                # CLI entry points; builds inputs, validates env vars
├── models.py              # Pydantic models + validators for structured task output
├── config/
│   ├── agents.yaml        # role/goal/backstory/llm for the 4 agents
│   └── tasks.yaml          # description/expected_output for the 3 tasks
├── tools/
│   └── custom_tool.py      # send_push_notification (Pushover) tool
└── knowledge/
    └── user_preference.txt
```

Agent and task Python method names match their YAML keys exactly, per CrewAI's `@CrewBase` convention. Task dependencies are wired only in `crew.py` (via `context=[...]`), not duplicated in `tasks.yaml`.

## Notes

- The crew runs with `memory=True`, `tracing=True`, and `verbose=True`. If the configured OpenAI account/key doesn't have access to the embeddings endpoint CrewAI's memory system uses, a post-completion memory-persistence step may fail — `main.py` treats that specific, already-identified failure as non-fatal once the three output files have been produced, so a working run still exits successfully.
- Not in scope: automated trading, brokerage integration, portfolio rebalancing, or any other execution of a trade — this project only recommends.
