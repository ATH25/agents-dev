#!/usr/bin/env python3

"""
Codex Command Safety Hook

Purpose:
- Allow normal Codex development operations.
- Block a small set of explicitly destructive commands.
- Rely on Codex's native sandbox and approval policies
  for primary filesystem and execution protection.

This is a lightweight safety check, not a security sandbox.
"""

import json
import os
import shlex
import sys
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_FILE = Path("/tmp/codex_command_safety.log")


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

def log(message: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(message + "\n")
    except OSError:
        pass


# ---------------------------------------------------------
# Hook decisions
# ---------------------------------------------------------

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


def allow(command: str, cwd: Path) -> None:
    log(f"ALLOWED: cwd={cwd} command={command}")
    sys.exit(0)


# ---------------------------------------------------------
# Read Codex hook payload
# ---------------------------------------------------------

try:
    payload = json.load(sys.stdin)
except (ValueError, OSError) as exc:
    deny(f"Invalid hook input: {exc}")


# Only inspect Bash tool calls.
if (
    payload.get("hook_event_name") != "PreToolUse"
    or payload.get("tool_name") != "Bash"
):
    sys.exit(0)


tool_input = payload.get("tool_input") or {}

command = tool_input.get("command", "")

if not isinstance(command, str) or not command.strip():
    deny("Missing or malformed Bash command.")


cwd = Path(
    payload.get("cwd") or os.getcwd()
).resolve(strict=False)


# ---------------------------------------------------------
# Working directory validation
# ---------------------------------------------------------

# Require commands to start from within the repository.
# This does not prevent commands from accessing other paths;
# Codex's sandbox is responsible for filesystem restrictions.

try:
    cwd.relative_to(PROJECT_ROOT)
except ValueError:
    deny(f"Working directory outside agents-dev: {cwd}")


# ---------------------------------------------------------
# Command parsing
# ---------------------------------------------------------

# Do not reject commands merely because they contain:
#
#   &&
#   ||
#   |
#   ;
#   >
#   <
#   multiline shell syntax
#
# These are normal shell constructs used by coding agents.
#
# The Codex sandbox and approval policy remain responsible
# for enforcing execution and filesystem permissions.

try:
    tokens = shlex.split(command, posix=True)
except ValueError:
    # Avoid blocking ordinary development workflows because
    # the lightweight parser cannot understand the command.
    log(f"DEFERRED TO SANDBOX: {command}")
    sys.exit(0)


if not tokens:
    sys.exit(0)


# ---------------------------------------------------------
# Basic destructive command protections
# ---------------------------------------------------------

# Block direct privilege escalation.
if tokens[0] in {"sudo", "su"}:
    deny("Privilege escalation command blocked.")


# Block direct recursive deletion.
if tokens[0] == "rm":

    recursive = any(
        argument == "--recursive"
        or (
            argument.startswith("-")
            and not argument.startswith("--")
            and "r" in argument.lower()
        )
        for argument in tokens[1:]
    )

    if recursive:
        deny("Recursive deletion is blocked.")


# Block direct force pushes.
if tokens[:2] == ["git", "push"]:

    force_push = any(
        argument in {
            "-f",
            "--force",
            "--force-with-lease"
        }
        for argument in tokens[2:]
    )

    if force_push:
        deny("Force-pushing Git history is blocked.")


# Block direct hard resets.
if tokens[:2] == ["git", "reset"]:

    if "--hard" in tokens[2:]:
        deny("git reset --hard is blocked.")


# Block direct forced Git cleaning.
if tokens[:2] == ["git", "clean"]:

    force_clean = any(
        argument == "--force"
        or (
            argument.startswith("-")
            and not argument.startswith("--")
            and "f" in argument
        )
        for argument in tokens[2:]
    )

    if force_clean:
        deny("git clean with force is blocked.")


# ---------------------------------------------------------
# Allow command
# ---------------------------------------------------------

allow(command, cwd)