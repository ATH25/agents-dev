#!/usr/bin/env bash
# PreToolUse hook: gate Bash commands that reference paths outside allowed directories.
# Allowed: /Users/ajuthomas/DEV/projects/AI_Agents/agents-dev  and  ~/.claude

input=$(cat)

# Only intercept the Bash tool
tool_name=$(printf '%s' "$input" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

if [[ "$tool_name" != "Bash" ]]; then
  exit 0
fi

command=$(printf '%s' "$input" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Find /Users/ajuthomas/… paths that are NOT under the two allowed roots
# Write the Python checker to a temp file to avoid heredoc-inside-$() quote-balancing bug
_pyfile=$(mktemp /tmp/check_paths_XXXXXX.py)
cat > "$_pyfile" <<'PYEOF'
import re, sys

command = sys.argv[1]
allowed = (
    '/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/',
    '/Users/ajuthomas/.claude/',
)

# Match any token that looks like an absolute path under /Users/ajuthomas
paths = re.findall(r'/Users/ajuthomas/[^\s\'";&|><`(){}\\[\\]]+', command)
seen = set()
for p in paths:
    if not any(p.startswith(a) for a in allowed) and p not in seen:
        seen.add(p)
        print(p)
PYEOF
suspicious=$(python3 "$_pyfile" "$command")
rm -f "$_pyfile"

if [[ -z "$suspicious" ]]; then
  exit 0
fi

TTY=/dev/tty
{
  printf '\n\033[1;33m⚠  PERMISSION REQUIRED\033[0m\n'
  printf 'Claude wants to run a Bash command referencing paths outside the allowed directories.\n\n'
  printf 'Command:\n  %s\n\n' "$command"
  printf 'Paths outside allowed dirs:\n'
  while IFS= read -r p; do
    printf '  %s\n' "$p"
  done <<< "$suspicious"
  printf '\nAllow this command? [y/N] '
} > "$TTY"

read -r response < "$TTY"

if [[ "$response" =~ ^[Yy]$ ]]; then
  exit 0
else
  printf 'Blocked by user: command references paths outside allowed directories.\n'
  exit 2
fi
