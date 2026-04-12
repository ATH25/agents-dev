# Scaffold Plan: `agents-dev`

**Source:** `/Users/ajuthomas/DEV/projects/AI_Agents/agents`
**Target:** `/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev`
**Based on:** `assessment.md` in this directory
**Status:** Planning only — no files created yet

---

## Goal & Scope

Scaffold `agents-dev` as a clean project with the same tooling, AI-assistant configuration, dependency management, and Git hygiene as `agents`, but with no Python source files or Jupyter notebooks copied. Code starts fresh; only configuration and infrastructure are ported.

### In scope
- AI assistant instruction files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`)
- Claude Code settings and hooks (`.claude/`)
- Dependency management (`pyproject.toml`, `uv.lock`, `requirements.txt`)
- Git configuration (`.gitignore`, `.gitattributes`)
- Python version pin (`.python-version`)
- Project identity (`LICENSE`, `README.md`)
- Environment template (`.env.example`)

### Out of scope
- All `.py` files
- All `.ipynb` files
- `guides/`, `setup/`, `assets/` directories
- Curriculum week directories (`1_foundations/` through `6_mcp/`)
- `3_crew/` CrewAI sub-projects
- `.git/` (new repo initialized separately)
- `.env` (provisioned manually by user, never created by this plan)

---

## Files to Copy As-Is

These files have no absolute paths or project-specific identifiers. Copy byte-for-byte from source.

| Source Path | Target Path | Notes |
|-------------|-------------|-------|
| `agents/.python-version` | `agents-dev/.python-version` | Contains only `3.12` |
| `agents/.gitattributes` | `agents-dev/.gitattributes` | Contains only `*.ipynb filter=nbstripout` |
| `agents/LICENSE` | `agents-dev/LICENSE` | MIT, no paths |
| `agents/uv.lock` | `agents-dev/uv.lock` | 705 KB; copy for reproducible resolution |
| `agents/requirements.txt` | `agents-dev/requirements.txt` | Auto-generated; copy or regenerate via `uv pip compile` |

---

## Files to Copy With Modifications

Each entry below specifies the exact changes required. No other edits should be made.

---

### 1. `pyproject.toml`

**Source:** `agents/pyproject.toml`
**Target:** `agents-dev/pyproject.toml`

**Changes — lines 2–3 only:**

```toml
# BEFORE:
name = "agents"
description = "Add your description here"

# AFTER:
name = "agents-dev"
description = "Development project based on the AI Agents curriculum"
```

All dependency entries (`dependencies = [...]`, `[dependency-groups]`) are copied unchanged.

---

### 2. `.gitignore`

**Source:** `agents/.gitignore`
**Target:** `agents-dev/.gitignore`

**Change — remove line 197 only:**

```gitignore
# REMOVE this line (abandoned branch artifact from agents repo):
/.claude/worktrees/musing-swanson/
```

All other 197 lines are kept as-is. The curriculum-specific ignore entries below are harmless
(gitignore silently skips patterns with no matching files) and are retained for consistency:

```gitignore
# Keep — inert but forward-compatible if similar dirs are created:
3_crew/engineering_team/output/
memory.db-shm
memory.db-wal
memory.db
6_mcp/accounts.db
6_mcp/memory/*.db
```

---

### 3. `.claude/settings.local.json`

**Source:** `agents/.claude/settings.local.json`
**Target:** `agents-dev/.claude/settings.local.json`

**Changes — 4 path substitutions (replace `agents/` and `agents/` with `agents-dev/` and `agents-dev/`):**

```json
// BEFORE (full file):
{
  "permissions": {
    "deny": [
      "Read(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents/**|.claude/**))",
      "Edit(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents/**|.claude/**))",
      "Write(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents/**|.claude/**))"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/ajuthomas/DEV/projects/AI_Agents/agents/.claude/hooks/check_bash_paths.sh"
          }
        ]
      }
    ]
  }
}

// AFTER (full file):
{
  "permissions": {
    "deny": [
      "Read(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents-dev/**|.claude/**))",
      "Edit(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents-dev/**|.claude/**))",
      "Write(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents-dev/**|.claude/**))"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/.claude/hooks/check_bash_paths.sh"
          }
        ]
      }
    ]
  }
}
```

**Risk:** If these paths are wrong, Claude's permission boundary will either be broken (blocking all operations) or absent (no protection). This must be verified before any other work.

---

### 4. `.claude/hooks/check_bash_paths.sh`

**Source:** `agents/.claude/hooks/check_bash_paths.sh`
**Target:** `agents-dev/.claude/hooks/check_bash_paths.sh`

**Changes — 2 substitutions:**

```bash
# BEFORE — comment on line 3:
# Allowed: /Users/ajuthomas/DEV/projects/AI_Agents/agents  and  ~/.claude

# AFTER — comment on line 3:
# Allowed: /Users/ajuthomas/DEV/projects/AI_Agents/agents-dev  and  ~/.claude
```

```python
# BEFORE — Python allowed tuple on lines 26–29:
allowed = (
    '/Users/ajuthomas/DEV/projects/AI_Agents/agents/',
    '/Users/ajuthomas/.claude/',
)

# AFTER — Python allowed tuple on lines 26–29:
allowed = (
    '/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/',
    '/Users/ajuthomas/.claude/',
)
```

**Critical:** The trailing slash in `agents-dev/` must be present. The script uses `startswith()` for
path matching; missing the slash would allow paths like `agents-dev-other/` to pass the guard.

**Post-copy action:** The file must be made executable:
```bash
chmod +x agents-dev/.claude/hooks/check_bash_paths.sh
```

---

### 5. `CLAUDE.md`

**Source:** `agents/CLAUDE.md`
**Target:** `agents-dev/CLAUDE.md`

**Change 1 — Permissions section (line 9), path update:**

```markdown
# BEFORE:
Always ask the user for explicit permission before editing or writing any file outside of
`/Users/ajuthomas/DEV/projects/AI_Agents/agents/`.

# AFTER:
Always ask the user for explicit permission before editing or writing any file outside of
`/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/`.
```

**Change 2 — Remove the "Running Code" section entirely:**

The following section references curriculum directories that do not exist in `agents-dev`:

```markdown
# REMOVE this entire section:
## Running Code

**Jupyter Notebooks** — the primary format for labs: ...
**Gradio Apps** (found in `1_foundations/`, `4_langgraph/`, `6_mcp/`): ...
**CrewAI Projects** (run from inside each project directory): ...
**MCP Servers** (run as separate processes): ...
**Environment diagnostics:** ...
```

**Change 3 — Remove "Notebook Output Management" section entirely:**

```markdown
# REMOVE this entire section:
## Notebook Output Management
`nbstripout` is configured to strip outputs before commits. ...
```

**Change 4 — Replace the "Architecture Overview" section:**

```markdown
# REMOVE this entire section (lines 66–109):
## Architecture Overview
This is a **6-week AI agents curriculum** ...
[all table and subsection content]
### Environment Variables
The `.env` file at the repo root ...

# REPLACE WITH:
## Project Description

`agents-dev` is a development project based on the AI Agents curriculum.
It shares tooling and configuration with the `agents` project but has an
independent codebase. Use `.env.example` as the template for required API keys.
```

**Change 5 — Remove the "Package Management" CrewAI note (line 21):**

```markdown
# REMOVE this line:
CrewAI projects in `3_crew/*/` each have their own `pyproject.toml` and must be
managed independently with `uv` from within each project directory.
```

**Sections to keep unchanged:**
- `## Permissions` (after path fix above)
- `## Package Management` (minus the CrewAI line)
- `## Linting`
- `## Workflow (from AGENTS.md)`
- `## MCP Server Preference`

---

### 6. `AGENTS.md`

**Source:** `agents/AGENTS.md`
**Target:** `agents-dev/AGENTS.md`

**Changes — remove 2 lines that reference curriculum-specific directories:**

The file is largely generic, but these two lines reference curriculum-specific context:

```markdown
# REMOVE the HTML comment line (line 5 in source, if present):
<!-- SSH push from Claude Code verified working on 2026-03-16 -->
```

> Note: This comment is in `CLAUDE.md`, not `AGENTS.md`. `AGENTS.md` contains no
> curriculum-specific paths. It can be copied as-is.

**No other changes required.** All guidance in `AGENTS.md` (workflow, MCP preference) applies
equally to `agents-dev`.

---

### 7. `GEMINI.md`

**Source:** `agents/GEMINI.md`
**Target:** `agents-dev/GEMINI.md`

The source file is a full 6-week Gemini curriculum overview. None of that curriculum content
applies to `agents-dev`. Replace the body entirely while keeping the file.

**New content for `agents-dev/GEMINI.md`:**

```markdown
# agents-dev

## Project Overview

`agents-dev` is a development project based on the AI Agents curriculum.
It is a sibling project to `agents`, sharing tooling and configuration
but maintaining an independent codebase.

## Building and Running

### Dependency Management
This project uses **`uv`** for dependency management.
- **Install all dependencies:** `uv sync`
- **Add a new dependency:** `uv add <package>`
- **Regenerate requirements.txt:** `uv pip compile pyproject.toml -o requirements.txt`

## Development Conventions

### Linting
- `ruff check .` — lint
- `ruff format .` — format

### Environment Configuration
- Copy `.env.example` to `.env` and fill in the required API keys.
- Never commit `.env`.


### MCP Server Preference
- Use the JetBrains MCP server that matches the currently active IDE configuration.
- If multiple servers are available, use the one that is connected and providing tools.
```

---

## Files to Create New

These files do not exist in the source project and must be written from scratch.

---

### 1. `README.md`

A fresh project README. Minimum viable content:

```markdown
# agents-dev

Development project based on the [AI Agents curriculum](../agents).

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and fill in your API keys
   ```

3. Lint:
   ```bash
   ruff check .
   ruff format .
   ```

## Relationship to `agents`

`agents-dev` shares tooling and configuration with `agents` but has an
independent codebase. Curriculum files (notebooks, guides, assets) are
not present here.
```

---

### 2. `.env.example`

Documents all required environment variables. Never contains real values.

```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Notifications (Pushover)
PUSHOVER_USER=...
PUSHOVER_TOKEN=...

# Email (SendGrid)
SENDGRID_API_KEY=SG....

# Observability (LangSmith)
LANGSMITH_API_KEY=...

# Market Data (Polygon)
POLYGON_API_KEY=...

# Logging
LOG_LEVEL=INFO
ROOT_LOG_LEVEL=WARNING
```

This file is committed to git. The actual `.env` is provisioned manually by the user
and is excluded by `.gitignore` (already present in the inherited `.gitignore`).

---

## Files to Exclude

The following are explicitly not created in `agents-dev`:

| Path | Reason |
|------|--------|
| `.env` | Security — provision manually after scaffold |
| `.git/` | New repo; `git init` run separately by user |
| `.claude/worktrees/` | Abandoned branch from `agents` history |
| `.junie/` | Session memory specific to `agents` |
| `.idea/` | PyCharm settings tied to absolute paths |
| `1_foundations/` through `6_mcp/` | No `.py` or `.ipynb` files in scope |
| `guides/`, `setup/`, `assets/` | Curriculum content, not applicable |
| `3_crew/` | Independent uv workspaces, not applicable |
| `NOTES.md` | `agents`-specific course notes |
| `readme-old.md` | Legacy artifact |
| `delete` | Empty marker file |
| `.ruff_cache/`, `.venv/`, `__pycache__/` | Auto-generated; never copied |
| `*.db`, `*.db-shm`, `*.db-wal` | Runtime state; never copied |
| `~/.claude/settings.json` | User-level config; must not be modified |

---

## Proposed Creation Order

Order matters: Claude settings must exist before any Claude-assisted work begins.

```
Step 1 — Directory skeleton
  mkdir -p agents-dev/.claude/hooks

Step 2 — Git hygiene (copy as-is)
  .gitattributes
  .gitignore            ← copy then remove musing-swanson line

Step 3 — Python environment (copy as-is)
  .python-version
  pyproject.toml        ← copy then update name/description
  uv.lock               ← copy as-is
  requirements.txt      ← copy as-is

Step 4 — Claude security boundary (highest-risk modifications)
  .claude/hooks/check_bash_paths.sh    ← copy then update ALLOWED_PATH + comment
  chmod +x .claude/hooks/check_bash_paths.sh
  .claude/settings.local.json          ← copy then update all 4 paths

Step 5 — AI assistant instruction files
  CLAUDE.md             ← copy then apply 5 changes
  AGENTS.md             ← copy as-is
  GEMINI.md             ← write new content

Step 6 — New files (no source)
  .env.example          ← write from scratch
  README.md             ← write from scratch

Step 7 — Project identity
  LICENSE               ← copy as-is

Step 8 — Validation (see checklist below)
```

---

## Assumptions

1. **`agents-dev` purpose is not yet defined.** `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and
   `README.md` use placeholder descriptions. These should be updated once the project's specific
   goal is known.

2. **`uv.lock` is copied for reproducibility.** If a clean dependency resolution is preferred
   (e.g., to pick up newer patch versions), the user can delete `uv.lock` after the scaffold and
   run `uv sync` to regenerate it.

3. **`requirements.txt` may become stale.** It is auto-generated from `pyproject.toml`. If
   `pyproject.toml` is modified post-scaffold, regenerate with:
   ```bash
   uv pip compile pyproject.toml -o requirements.txt
   ```

4. **No `git init` is included in this plan.** The user will initialize the new repo separately.
   If `uv.lock` or `.gitattributes` are committed before `nbstripout --install` is run, notebook
   output stripping will not be active.

5. **The `.claude/` config is local, not committed.** `settings.local.json` is typically listed
   in `.gitignore` for shared repos. Verify whether `agents-dev` should commit it or not,
   depending on whether it is a personal or shared project.

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Wrong path in `settings.local.json` | High | Verify all 4 substitutions before first Claude session |
| Wrong `ALLOWED_PATH` in hook script | High | Verify trailing slash; test with a benign command |
| Hook script not executable | Medium | `chmod +x` is explicitly in the creation order |
| `.env` accidentally created with secrets | High | Plan explicitly excludes it; only `.env.example` is created |
| `uv.lock` conflict if `name` changes | Low | `uv lock` or `uv sync` will update the name reference automatically |
| Stale `CLAUDE.md` content confuses Claude | Medium | Remove all curriculum section references before first session |

---

## Validation Checklist

Run these checks after the scaffold is complete and before starting any work in `agents-dev`:

- [ ] `agents-dev/.claude/settings.local.json` — confirm all 3 deny rules reference `agents-dev`
- [ ] `agents-dev/.claude/settings.local.json` — confirm hook command path references `agents-dev`
- [ ] `agents-dev/.claude/hooks/check_bash_paths.sh` — confirm `allowed` tuple path is `agents-dev/` (with trailing slash)
- [ ] `agents-dev/.claude/hooks/check_bash_paths.sh` — confirm file is executable (`ls -l`)
- [ ] `agents-dev/pyproject.toml` — confirm `name = "agents-dev"`
- [ ] `agents-dev/.gitignore` — confirm `musing-swanson` line is absent
- [ ] `agents-dev/.gitignore` — confirm `.env` is present in the ignore list
- [ ] `agents-dev/CLAUDE.md` — confirm path references `agents-dev/` in Permissions section
- [ ] `agents-dev/CLAUDE.md` — confirm curriculum sections (Architecture Overview, Running Code, Notebook Output Management) are removed
- [ ] `agents-dev/.env.example` — confirm all expected keys are present
- [ ] `agents-dev/.env` — confirm it does NOT exist (user provisions separately)
- [ ] `agents-dev/.git/` — confirm it does NOT exist (no copy of source git history)
- [ ] Run `uv sync` from `agents-dev/` — confirm environment resolves cleanly
- [ ] Run `ruff check .` from `agents-dev/` — confirm linter runs without errors (no `.py` files = clean pass)
