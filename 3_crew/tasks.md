# Tasks for Debate Crew Simulation

- [X] **Task 1: Environment Configuration**
    - Ensure the shared `.env` file at `/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/.env` contains `OPENAI_API_KEY`, since the API keys are stored at the `agents-dev` project root rather than inside `3_crew/debate`.
    - Verify that the environment supports `crewAI >= 0.108.0` and Python `>=3.10, <3.13`.

- [X] **Task 2: Configure Agents (`debate/src/debate/config/agents.yaml`)**
    - Update `agents.yaml` to define the following agents:
        - `debater`:
            - Role: Proponent/Opponent Debater
            - Goal: Generate compelling arguments for or against a motion.
            - Backstory: A skilled debater capable of seeing multiple sides of an issue and constructing persuasive arguments.
        - `judge`:
            - Role: Debate Judge
            - Goal: Evaluate arguments and decide on a winner.
            - Backstory: An impartial judge with deep reasoning capabilities, focused on logic, evidence, and rhetorical strength.

- [X] **Task 3: Configure Tasks (`debate/src/debate/config/tasks.yaml`)**
    - Update `tasks.yaml` to define the following tasks:
        - `propose_task`:
            - Description: Generate a compelling argument in favor of the `{motion}`.
            - Expected Output: A persuasive markdown document supporting the motion.
            - Agent: `debater`
        - `oppose_task`:
            - Description: Generate a compelling argument against the `{motion}`.
            - Expected Output: A persuasive markdown document opposing the motion.
            - Agent: `debater`
        - `decide_task`:
            - Description: Evaluate the arguments from the proponent and opponent for the `{motion}` and declare a winner.
            - Expected Output: A reasoned judgment in markdown format including the winner and justification.
            - Agent: `judge`

- [X] **Task 4: Implement Crew Logic (`debate/src/debate/crew.py`)**
    - Modify the `Debate` class:
        - Define `@agent debater` using `llm="gpt-4o-mini"`.
        - Define `@agent judge` using `llm="gpt-4o"`.
        - Define `@task propose_task` with `output_file="output/propose.md"`.
        - Define `@task oppose_task` with `output_file="output/oppose.md"`.
        - Define `@task decide_task` with `output_file="output/decide.md"`.
    - Add a `@before_kickoff` decorator or logic in `main.py` to ensure the `output/` directory exists.

- [X] **Task 5: Update Entry Point (`debate/src/debate/main.py`)**
    - Update the `run()` function:
        - Set a default `motion` (e.g., "There needs to be strict laws to regulate LLMs") or allow it to be passed via CLI.
        - Update the `inputs` dictionary to include `'motion': motion`.
        - Pass `inputs` to `Debate().crew().kickoff(inputs=inputs)`.

- [X] **Task 6: Verification and Execution**
    - Run the simulation using `crewai run` or `uv run run_crew`.
    - Verify that `output/propose.md`, `output/oppose.md`, and `output/decide.md` are created with valid content.
    - Confirm that the agents utilized the correct models as specified.
