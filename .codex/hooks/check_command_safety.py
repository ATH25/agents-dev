#!/usr/bin/env python3

import json
import os
import re
import shlex
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_FILE = Path("/tmp/codex_command_safety.log")


def log(message: str) -> None:
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(message + "\n")


def deny(reason: str) -> None:
    log(f"BLOCKED: {reason}")

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }))

    sys.exit(0)


def is_within_project(path: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(PROJECT_ROOT)
        return True
    except (ValueError, OSError):
        return False


# Read the PreToolUse payload from Codex.
try:
    payload = json.load(sys.stdin)
except Exception as exc:
    deny(f"Safety hook could not parse its input: {exc}")


# This hook protects Bash tool calls.
if (
    payload.get("hook_event_name") != "PreToolUse"
    or payload.get("tool_name") != "Bash"
):
    sys.exit(0)


command = payload.get("tool_input", {}).get("command", "")

if not isinstance(command, str) or not command.strip():
    deny("Bash command was missing or malformed.")


cwd = Path(
    payload.get("cwd") or os.getcwd()
).resolve(strict=False)

if not is_within_project(cwd):
    deny(
        f"Command working directory is outside agents-dev: {cwd}"
    )


# Block compound shell expressions because they can hide additional
# commands from this simple safety validator.
if (
    re.search(r"[;&|`]", command)
    or "$(" in command
    or "\n" in command
):
    deny(
        "Compound commands, pipes, command substitution, "
        "and multiline shell commands are blocked."
    )


try:
    tokens = shlex.split(command, posix=True)
except ValueError as exc:
    deny(f"Unable to safely parse command: {exc}")


if not tokens:
    sys.exit(0)


# Block privilege escalation.
if tokens[0] in {"sudo", "su"}:
    deny(f"Privileged command is blocked: {tokens[0]}")


# Block recursive deletion.
if (
    tokens[0] == "rm"
    and any(
        flag in {"-r", "-R", "-rf", "-fr", "--recursive"}
        for flag in tokens[1:]
    )
):
    deny("Recursive deletion is blocked.")


# Block dangerous Git operations.
if (
    tokens[:2] == ["git", "push"]
    and any(
        flag in {"-f", "--force", "--force-with-lease"}
        for flag in tokens[2:]
    )
):
    deny("Force-pushing Git history is blocked.")


if (
    tokens[:2] == ["git", "reset"]
    and "--hard" in tokens[2:]
):
    deny("git reset --hard is blocked.")


if (
    tokens[:2] == ["git", "clean"]
    and any(
        "f" in flag.lstrip("-")
        for flag in tokens[2:]
        if flag.startswith("-")
    )
):
    deny("git clean with force is blocked.")


# Block explicit paths resolving outside agents-dev.
for token in tokens[1:]:

    if token.startswith("-"):
        continue

    candidate = None

    if token.startswith("~"):
        candidate = Path(os.path.expanduser(token))

    elif token.startswith("/"):
        candidate = Path(token)

    elif (
        token in {"..", "."}
        or token.startswith("../")
        or token.startswith("./")
        or "/" in token
    ):
        candidate = cwd / token

    if (
        candidate is not None
        and not is_within_project(candidate)
    ):
        deny(f"Path outside agents-dev is blocked: {token}")


log(f"ALLOWED: cwd={cwd} command={command}")

sys.exit(0)
