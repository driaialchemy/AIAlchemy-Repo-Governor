# AIAlchemy Repo Governor

A local Python CLI that scans repositories, classifies risk, generates governance policies, produces Markdown reports, and prepares repos for safe AI-agent use (Claude Code, Codex, Copilot, etc.).

**This is a local governance tool, not a cloud platform.** It runs entirely on your machine, stores nothing remotely, and has no dashboard or background service. It is not a clone of Omnigent or any SaaS product.

---

## The Problem It Solves

When you point an AI coding agent at a repository it can't see:

- which files contain secrets or credentials
- whether `.gitignore` and `CLAUDE.md` exist
- whether the repo is even a git repository

Without governance, agents happily read `.env` files, commit generated artifacts, or edit sensitive paths. Repo Governor gives you a structured, auditable view of every repository in your workspace and generates per-repo policy files that constrain what agents are allowed to do.

---

## MVP Features

- **Scan** — Discovers repos, detects languages, counts files, finds sensitive filenames, scans source code for API terms
- **Classify** — Assigns HIGH / MEDIUM / LOW risk with 10 HIGH triggers, 11 MEDIUM signals, and a 0-100 readiness score
- **Policy generation** — Writes `CLAUDE.md` (human-readable) and `repo_policy.yaml` (machine-readable) per repo
- **Reports** — Generates 3 Markdown reports: governance overview, agent readiness, cleanup recommendations
- **Agent-ready check** — Prints which repos pass all safety gates for immediate agent use

---

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/driaialchemy/AIAlchemy-Repo-Governor.git
cd AIAlchemy-Repo-Governor
pip install -e .
```

---

## Quick Start (Windows paths)

```powershell
# Scan all repos
repo-governor scan "C:\Users\msell\OneDrive\AIAlchemy\repositories"

# Classify risk levels
repo-governor classify "C:\Users\msell\OneDrive\AIAlchemy\repositories"

# Generate policies for one repo (creates CLAUDE.md + repo_policy.yaml)
repo-governor policy-init "C:\Users\msell\OneDrive\AIAlchemy\repositories\my-project"

# Generate all 3 Markdown reports into ./reports/
repo-governor report "C:\Users\msell\OneDrive\AIAlchemy\repositories"

# Show agent-readiness status
repo-governor agent-ready "C:\Users\msell\OneDrive\AIAlchemy\repositories"
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `scan <root_path>` | Discover and inspect all repos under a root directory |
| `classify <root_path>` | Apply risk classification (LOW / MEDIUM / HIGH) |
| `policy-init <repo_path> [--overwrite\|--force]` | Write `CLAUDE.md` + `repo_policy.yaml` to a repo |
| `report <root_path> [--output-dir DIR]` | Generate 3 Markdown reports (governance, readiness, cleanup) |
| `agent-ready <root_path>` | Show repos that are safe for agent use |

### `policy-init` flags

| Flag | Description |
|------|-------------|
| `--overwrite` / `--force` | Replace existing policy files |

### `report` flags

| Flag | Description |
|------|-------------|
| `--output-dir DIR` | Write reports to DIR (default: `./reports/`) |
| `--output FILE` | Write a single combined report to FILE |

---

## Risk Levels

| Level | Description |
|-------|-------------|
| 🔴 HIGH | Secrets/`.env` present, no git init, or no `.gitignore` + data artifacts |
| 🟡 MEDIUM | 2+ moderate signals: missing docs, has CI/CD, many files, external HTTP |
| 🟢 LOW | Well-configured repo, no sensitive files detected |

A repo is **Agent-Ready** when it is LOW risk, has `CLAUDE.md`, has `.gitignore`, and has no exposed secrets.

---

## Files Generated

| File | Written to | Should commit? |
|------|-----------|----------------|
| `CLAUDE.md` | Target repo root | Yes, after review |
| `repo_policy.yaml` | Target repo root | Yes, after review |
| `reports/AI_REPO_GOVERNANCE_REPORT.md` | Working directory | No (in `.gitignore`) |
| `reports/agent_readiness_report.md` | Working directory | No (in `.gitignore`) |
| `reports/cleanup_recommendations.md` | Working directory | No (in `.gitignore`) |

---

## Safety Rules

- Reports are excluded from git by default (`reports/` and `repo_governor_report_*.md` are in `.gitignore`).
- `policy-init` never overwrites existing files unless `--overwrite` / `--force` is passed.
- No destructive filesystem operations are performed on scanned repositories.
- No secrets, environment variable values, or credential file contents are printed or logged.
- Binary files and files larger than 1 MB are never read.

---

## Running Tests

```bash
pytest
```

145 tests across scanner, classifier, policy generator, and reporter.

---

## Project Structure

```
src/repo_governor/
    cli.py          # argparse CLI entry point
    scanner.py      # Repo discovery and file inspection
    classifier.py   # Risk classification (HIGH/MEDIUM/LOW + readiness score)
    policy.py       # CLAUDE.md + repo_policy.yaml generator
    reporter.py     # Markdown report generator (3 report types)
tests/              # pytest test suite (145 tests)
docs/               # Extended documentation
```

---

## Roadmap (post-MVP)

- Batch `policy-init` across all repos in a root directory
- `--watch` mode to re-scan on file changes
- Integration with pre-commit hooks
- GitHub Actions workflow to block PRs from HIGH-risk repos
- Config file (`.repo-governor.yaml`) for custom scan targets and blocked paths

---

## License

MIT
