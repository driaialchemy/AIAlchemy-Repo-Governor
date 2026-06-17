# CLAUDE.md — Agent Policy for Repo Governor

## Project Purpose

AIAlchemy Repo Governor is a local Python CLI tool that scans Git repositories, classifies risk, generates governance policy files (`CLAUDE.md` and `repo_policy.yaml`), and produces Markdown reports to prepare repos for safe AI-agent use.

This is **not** a cloud platform, web app, or Omnigent clone. Everything runs locally with no remote state.

## Architecture Overview

```
src/repo_governor/
    scanner.py      # Single-pass walk; detects 27+ file types + 13 API terms
    classifier.py   # 10 HIGH triggers, 11 MEDIUM signals, readiness score 0-100
    policy.py       # Generates CLAUDE.md (Markdown) + repo_policy.yaml (YAML)
    reporter.py     # Generates 3 Markdown report types
    cli.py          # argparse CLI: scan | classify | policy-init | report | agent-ready
```

External dependencies: `pyyaml>=6.0` (see `pyproject.toml`). Everything else is stdlib.

## Allowed Operations

- Read any source file, test file, or documentation file.
- Run `pytest` to execute the test suite.
- Edit source files under `src/repo_governor/` and `tests/`.
- Add new modules if clearly scoped to the MVP feature set.
- Write Markdown documentation under `docs/`.
- Run `pip install -e .` to install in editable mode.
- Run `repo-governor` CLI commands for testing (read-only against scanned repos).

## Forbidden Operations

- Do **not** delete any file without explicit user confirmation.
- Do **not** commit or push changes automatically.
- Do **not** read, print, or log the contents of `.env`, secrets, or credential files.
- Do **not** run destructive commands (`git reset --hard`, `rm -rf`, etc.).
- Do **not** install packages outside a virtual environment without asking.
- Do **not** add a database, web dashboard, or background scheduler — these are out of MVP scope.
- Do **not** write generated reports to git — they belong in `.gitignore`.

## Blocked Paths (never read contents of these)

- `.env`, `.env.*`, `.env.local`, `.env.production`
- `secrets.*`, `credentials.*`, `*.pem`, `*.key`
- Any file under `secrets/`, `private/`, `credentials/`

## Testing Command

```bash
pytest
# Expected: 145 tests passing
```

Always run tests before claiming a task is complete.

## Safe Development Workflow

```bash
# 1. Make a change
# 2. Run the test suite
pytest

# 3. Run a sample scan (read-only, does not modify scanned repos)
repo-governor scan "C:\Users\msell\OneDrive\AIAlchemy\repositories"

# 4. Summarize the diff
git diff

# 5. Commit only after review
git add src/ tests/ docs/ README.md pyproject.toml .gitignore AGENTS.md CLAUDE.md
git commit -m "feat: <short description>"
```

## Compact Instructions

If context becomes too large, run `/compact` with: "Focus on completed files, tests run, changed files, unresolved errors, and remaining tasks."

## Coding Standards

- `pathlib.Path` for all filesystem operations (no `os.path`).
- Dataclasses with defaults for all data models.
- Windows-compatible paths (`Path.as_posix()` for YAML/report output).
- No comments unless the WHY is non-obvious.
- Keep functions small and independently testable.
- No backwards-compatibility hacks — update callers when renaming fields.

## Build Phases (for reference)

1. Scanner — single-pass walk, 27+ detection targets, API term scan ✅
2. Classifier — HIGH/MEDIUM/LOW + readiness score + blocking_issues ✅
3. Policy generation — CLAUDE.md + repo_policy.yaml ✅
4. Reporter — 3 Markdown report types ✅
5. CLI — all 5 commands + --force + --output-dir ✅
6. Docs — README, AGENTS.md, CLAUDE.md, docs/ ✅
7. Git commit and push to GitHub

## Known Non-Goals

- No cloud sync, remote API, or web UI
- No database persistence
- No auto-remediation of scanned repositories
- No Omnigent clone functionality
- No background scheduler or daemon mode

## Scan Target (default)

`C:\Users\msell\OneDrive\AIAlchemy\repositories`
