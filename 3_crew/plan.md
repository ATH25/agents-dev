<file name=0 path=plan.md># Implementation Plan - Debate Crew Simulation

This plan outlines the steps to implement the Debate Crew simulation based on the requirements in `requirement.md`.

## 1. Environment Configuration
- Ensure `.env` contains `OPENAI_API_KEY`.
- The `openai/gpt-4o-mini` and `openai/gpt-4o` models will be used.

## 2. Agent Configuration (`debate/src/debate/config/agents.yaml`)
- Define `debater` agent:
    - Role: Proponent/Opponent Debater.
    - Goal: Generate compelling arguments for or against a motion.
    - Backstory: A skilled debater capable of seeing multiple sides of an issue and constructing persuasive arguments.
- Define `judge` agent:
    - Role: Debate Judge.
    - Goal: Evaluate arguments and decide on a winner.
    - Backstory: An impartial judge with deep reasoning capabilities, focused on logic, evidence, and rhetorical strength.

## 3. Task Configuration (`debate/src/debate/config/tasks.yaml`)
- Define `propose_task`:
    - Description: Generate a compelling argument in favor of the `{motion}`.
    - Expected Output: A persuasive markdown document supporting the motion.
    - Agent: `debater`
    - Output File: `output/propose.md`
- Define `oppose_task`:
    - Description: Generate a compelling argument against the `{motion}`.
    - Expected Output: A persuasive markdown document opposing the motion.
    - Agent: `debater`
    - Output File: `output/oppose.md`
- Define `decide_task`:
    - Description: Evaluate the arguments from the proponent and opponent for the `{motion}` and declare a winner.
    - Expected Output: A reasoned judgment in markdown format including the winner and justification.
    - Agent: `judge`
    - Output File: `output/decide.md`

## 4. Crew Logic Implementation (`debate/src/debate/crew.py`)
- Update the `Debate` class to include:
    - `@agent debater` method returning an Agent with `llm="gpt-4o-mini"`.
    - `@agent judge` method returning an Agent with `llm="gpt-4o"`.
    - `@task propose_task` method.
    - `@task oppose_task` method.
    - `@task decide_task` method.
- Ensure the `output/` directory is created if it doesn't exist (can be handled in `main.py` or via a `@before_kickoff` decorator).

## 5. Main Entry Point (`debate/src/debate/main.py`)
- Update the `run()` function to:
    - Accept or define the `motion` input.
    - Pass `motion` to the `kickoff()` method.
- Ensure proper error handling and directory setup.

## 6. Verification
- Run `crewai run` and verify:
    - Arguments are generated in `output/propose.md` and `output/oppose.md`.
    - Final judgment is generated in `output/decide.md`.
    - Models used match the requirements.
