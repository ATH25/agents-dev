#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from debate.crew import Debate

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    motion = "There needs to be strict laws to regulate LLMs"
    if len(sys.argv) > 1:
        motion = sys.argv[1]

    inputs = {
        'motion': motion,
        'current_year': str(datetime.now().year)
    }

    try:
         Debate().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "motion": "There needs to be strict laws to regulate LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Debate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Debate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "motion": "There needs to be strict laws to regulate LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        Debate().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "motion": "",
        "current_year": ""
    }

    try:
        result = Debate().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


# CLI entry-point dispatch
if __name__ == "__main__":
    if len(sys.argv) < 2:
        run()
    elif sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "train":
        if len(sys.argv) < 4:
            raise Exception("Usage: python -m debate.main train <iterations> <filename>")
        # shift arguments for train()
        sys.argv = [sys.argv[0], sys.argv[2], sys.argv[3]]
        train()
    elif sys.argv[1] == "replay":
        replay()
    elif sys.argv[1] == "test":
        test()
    else:
        run()
