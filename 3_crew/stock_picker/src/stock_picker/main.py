#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load this project's own .env first (local values always win), then fall
# back to the repo-root .env for any variable not already set there.
# load_dotenv()'s default override=False means already-set variables are
# left untouched, so this only fills gaps.
load_dotenv()
load_dotenv(Path(__file__).resolve().parents[4] / ".env")

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "SERPER_API_KEY",
    "PUSHOVER_TOKEN",
    "PUSHOVER_USER",
]

EXPECTED_OUTPUT_FILES = [
    "output/trending_companies.json",
    "output/research_report.json",
    "output/decision.md",
]


def _validate_required_env_vars() -> None:
    for var_name in REQUIRED_ENV_VARS:
        if not os.environ.get(var_name):
            raise Exception(f"Missing required environment variable: {var_name}")


def _is_memory_persistence_error(exc: Exception) -> bool:
    """True if `exc` is CrewAI's post-run memory-save/embedding failure.

    memory=True is required (requirement.md §9), but its embedding calls can
    be rejected by API keys/accounts without embeddings access. That failure
    happens after the crew's actual tasks have already completed, so it must
    not be treated the same as a real pipeline failure.
    """
    return "not allowed to generate embeddings" in str(exc).lower()


def _all_output_files_exist() -> bool:
    return all(Path(f).is_file() for f in EXPECTED_OUTPUT_FILES)


def run():
    """
    Run the crew.
    """
    _validate_required_env_vars()

    inputs = {
        "sector_name": "Technology",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    Path("output").mkdir(parents=True, exist_ok=True)

    try:
        StockPicker().crew().kickoff(inputs=inputs)
    except Exception as e:
        if _is_memory_persistence_error(e) and _all_output_files_exist():
            print(
                "Warning: the crew produced all expected output files, but a "
                f"post-run memory-persistence step failed and was ignored: {e}"
            )
            return
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "sector_name": "Technology",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    try:
        StockPicker().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        StockPicker().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "sector_name": "Technology",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        StockPicker().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "sector_name": "",
        "current_date": "",
    }

    try:
        result = StockPicker().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
