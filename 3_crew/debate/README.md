# Debate Crew

Welcome to the Debate Crew project, powered by [crewAI](https://crewai.com). This multi-agent AI system simulates a structured debate on a given motion, featuring automated generation of opposing arguments followed by a reasoned judgment.

## Project Structure

```text
3_crew/debate/
├── knowledge/
│   └── user_preference.txt   # Stores preferences for the debate simulation.
├── output/                    # Generated markdown files for each debate stage.
│   ├── propose.md            # Argument in favor of the motion.
│   ├── oppose.md             # Argument against the motion.
│   └── decide.md             # Final judgment and winner declaration.
├── src/debate/
│   ├── config/
│   │   ├── agents.yaml      # Definitions for Debater and Judge agents.
│   │   └── tasks.yaml       # Definitions for Propose, Oppose, and Decide tasks.
│   ├── tools/
│   │   └── custom_tool.py    # Placeholder for specialized debate tools.
│   ├── crew.py              # Main crew logic linking agents and tasks.
│   └── main.py              # Entry point for executing the simulation.
├── pyproject.toml             # Project metadata and dependencies (CrewAI, UV).
└── README.md                  # Project documentation.
```

## Progress & Accomplishments

We have successfully built a functional debate simulation with the following milestones:
- **Environment Setup:** Configured a CrewAI-ready environment using `uv` for dependency management.
- **Agent Configuration:** Defined two specialized agents:
  - `debater`: Optimized for generating compelling arguments (uses `gpt-4o-mini`).
  - `judge`: Optimized for complex reasoning and evaluation (uses `gpt-4o`).
- **Task Implementation:** Created a sequential workflow where:
  1. A motion is proposed.
  2. The same motion is opposed.
  3. A judge evaluates both arguments to declare a winner.
- **Output Management:** Integrated file-saving logic to automatically store debate results in the `output/` directory as markdown documents.
- **Execution:** Verified the system with a sample motion: *"There needs to be strict laws to regulate LLMs"*.

## Installation

Ensure you have Python >=3.10 <3.13 installed.

### 1. Install uv
```bash
pip install uv
```

### 2. Install Project Dependencies
```bash
crewai install
```

### Run
crewai create crew debate

## Running the Project

To start the debate simulation, run:

```bash
crewai run
```
or
```bash
uv run run_crew
```

The simulation will execute the debate based on the motion defined in `src/debate/main.py` and save the results to the `output/` folder.

## Customizing

- **Motion:** Modify the `inputs` dictionary in `src/debate/main.py` to change the debate topic.
- **Agents:** Adjust roles or models in `src/debate/config/agents.yaml`.
- **Tasks:** Refine task descriptions or expected outputs in `src/debate/config/tasks.yaml`.
- **Logic:** Update `src/debate/crew.py` to add new agents, tasks, or custom tools.

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
