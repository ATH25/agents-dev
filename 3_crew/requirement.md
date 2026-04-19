# Requirements for Debate Crew

## Project Overview
This project is a `crewAI` based simulation that facilitates a debate on a given motion. It automates the process of generating arguments both for and against the motion, followed by a final judgment to determine the more convincing side.

## System Intent
The intent of the code is to demonstrate a multi-agent workflow where different AI models take on specific roles (Proponent, Opponent, and Judge) to explore a topic from multiple perspectives and arrive at a reasoned conclusion.

## Functional Requirements
- **Input**: The system requires a `motion` string as input (e.g., "There needs to be strict laws to regulate LLMs").
- **Multi-Agent Simulation**:
    - **Debater Agent**: Responsible for generating both the "Propose" and "Oppose" arguments.
    - **Judge Agent**: Responsible for evaluating the arguments and deciding on a winner.
- **Workflow Steps**:
    1. **Propose**: Generate a compelling argument in favor of the motion.
    2. **Oppose**: Generate a compelling argument against the motion.
    3. **Decide**: Evaluate both arguments and provide a final decision with reasoning.
- **Output**: The results of each step must be saved as Markdown files in the `output/` directory:
    - `output/propose.md`
    - `output/oppose.md`
    - `output/decide.md`

## Technical Requirements
- **Python Version**: `>=3.10` and `<3.13`.
- **Framework**: `crewAI` (specifically version `>=0.108.0`).
- **LLM Requirements**:
    - **Debater**: `openai/gpt-4o-mini` (optimized for fast, concise arguments).
    - **Judge**: `anthropic/claude-3-7-sonnet-latest` (optimized for reasoning and fair evaluation).
- **Project Structure**:
    - `src/debate/main.py`: Entry point for running the crew.
    - `src/debate/crew.py`: Definition of agents, tasks, and the crew's logic.
    - `src/debate/config/agents.yaml`: Configuration for agent roles, goals, and backstories.
    - `src/debate/config/tasks.yaml`: Configuration for task descriptions and expected outputs.

## Usage
To run the debate crew, use the following command from the project root:
```bash
crewai run
```
Alternatively, using `uv`:
```bash
uv run run_crew
```
