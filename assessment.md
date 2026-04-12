# Project Assessment: `agents` → `agents-dev`

---

## 1. COPY AS-IS

Files that can be reused without modification:

### Root-Level Files
| File | Reason |
|------|--------|
| `.python-version` | Python 3.12 pin, no path references |
| `.gitattributes` | `*.ipynb filter=nbstripout` — generic |
| `LICENSE` | MIT, no paths |
| `pyproject.toml` | Dependency list is reusable (see note below) |
| `uv.lock` | Reproducible dependency versions |
| `requirements.txt` | Auto-generated, no paths |

> **Note on `pyproject.toml`:** The dependency list is copy-worthy, but `name` and `description` need updating — see category 2.

---

## 2. COPY WITH MODIFICATIONS

### `pyproject.toml`
**Change:** `name = "agents"` → `name = "agents-dev"` and update `description`.
**Why:** Avoids package name collision if both environments are ever active.

---

### `CLAUDE.md`
**Change:** Update the absolute path in the permissions section:
```
# Before:
/Users/ajuthomas/DEV/projects/AI_Agents/agents/

# After:
/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/
```
Also remove the Week 1–6 architecture detail (it describes Python/notebook code you won't be copying). Replace with a brief description of what `agents-dev` is for.
**Why:** Claude reads this to understand project boundaries and context.

---

### `AGENTS.md`
**Change:** Same path reference update as `CLAUDE.md`. Strip out curriculum-specific workflow instructions that don't apply.
**Why:** Keeps the guidance accurate for the new project's scope.

---

### `GEMINI.md`
**Change:** Update or replace the curriculum-specific content with whatever is relevant to `agents-dev`. If `agents-dev` isn't a Gemini-specific project, consider omitting it entirely.
**Why:** Currently this file describes the 6-week Gemini curriculum, which won't exist in `agents-dev`.

---

### `.gitignore`
**Change:** Remove this entry (abandoned branch artifact):
```
.claude/worktrees/musing-swanson/
```
Keep all other entries — SQLite patterns, `.venv/`, `__pycache__/`, etc. remain valid.
**Why:** That entry is history from the `agents` repo, not applicable to a new project.

---

### `.claude/settings.local.json`
**Change:** Update all 4 path references:
```json
// Before:
"Read(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents/**|.claude/**))"
"command": "bash /Users/ajuthomas/DEV/projects/AI_Agents/agents/.claude/hooks/check_bash_paths.sh"

// After:
"Read(/Users/ajuthomas/!(DEV/projects/AI_Agents/agents-dev/**|.claude/**))"
"command": "bash /Users/ajuthomas/DEV/projects/AI_Agents/agents-dev/.claude/hooks/check_bash_paths.sh"
```
**Why:** Permission boundaries and hook invocation will be broken if the path is wrong.

---

### `.claude/hooks/check_bash_paths.sh`
**Change:** Update the `ALLOWED_PATH` constant inside the script:
```bash
# Before:
ALLOWED_PATH="/Users/ajuthomas/DEV/projects/AI_Agents/agents"

# After:
ALLOWED_PATH="/Users/ajuthomas/DEV/projects/AI_Agents/agents-dev"
```
**Why:** This is the guard that prevents commands from escaping the project boundary.

---

## 3. DO NOT COPY

| Path | Why |
|------|-----|
| `.env` | Live API secrets — always provision fresh |
| `.git/` | Repo history is specific to `agents` |
| `.claude/worktrees/` | Abandoned branch artifacts |
| `.junie/` | Session-specific memory cache |
| `.idea/` | PyCharm project settings use absolute paths |
| `README.md` | Describes the `agents` course — write a new one |
| `NOTES.md` | Course-specific notes, not relevant to a fresh project |
| `readme-old.md` | Legacy archived file |
| `delete` | Empty marker file, no purpose |
| `1_foundations/`, `2_openai/`, etc. | All Python/notebook content |
| `guides/`, `setup/`, `assets/` | Curriculum content — not applicable |
| `3_crew/` | Independent CrewAI workspaces with their own configs |
| `.ruff_cache/`, `.venv/`, `__pycache__/` | Caches and environments — always regenerated |

---

## 4. SECURITY-SENSITIVE

| File | Action |
|------|--------|
| `.env` | **Never copy.** Create a fresh `.env` in `agents-dev` and provision keys manually. |

**Best practice:** Create `.env.example` in `agents-dev` (see category 5) to document what keys are needed.

---

## 5. RECOMMENDED NEW FILES

### `.env.example` *(create this)*
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
SENDGRID_API_KEY=SG....
LANGSMITH_API_KEY=...
POLYGON_API_KEY=...
LOG_LEVEL=INFO
ROOT_LOG_LEVEL=WARNING
```

### `README.md` *(write fresh)*
Describe what `agents-dev` is, how it relates to `agents`, and how to set it up.

---

## 6. FINAL FILE LIST FOR `agents-dev`

```
agents-dev/
│
├── .claude/
│   ├── settings.local.json     ← MODIFIED (path update)
│   └── hooks/
│       └── check_bash_paths.sh ← MODIFIED (ALLOWED_PATH update)
│
├── .env                        ← NEW (provision manually, never commit)
├── .env.example                ← NEW (commit this)
├── .gitignore                  ← MODIFIED (remove musing-swanson entry)
├── .gitattributes              ← COPY AS-IS
├── .python-version             ← COPY AS-IS
│
├── CLAUDE.md                   ← MODIFIED (path + content update)
├── AGENTS.md                   ← MODIFIED (path update, trim curriculum content)
├── GEMINI.md                   ← OPTIONAL / MODIFIED or omit
├── README.md                   ← NEW (fresh write)
├── LICENSE                     ← COPY AS-IS
│
├── pyproject.toml              ← MODIFIED (name, description)
├── uv.lock                     ← COPY AS-IS (optional but recommended)
└── requirements.txt            ← COPY AS-IS (or regenerate via uv)
```

**Total files to manage: ~12.** Everything else starts fresh.

---

The 4 files that require the most care are the **2 path-sensitive Claude files** (`.claude/settings.local.json`, `.claude/hooks/check_bash_paths.sh`) and **2 AI instruction files** (`CLAUDE.md`, `AGENTS.md`) — get those right first before doing anything else in the new project.
