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
- **Goal-based loop** — Runs scan → classify → policy → remediation prompt → verify with a JSON audit trail

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

# Run a full goal-based governance loop on one repo
repo-governor goal-loop "C:\Users\msell\OneDrive\AIAlchemy\repositories\my-project"
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
| `goal-loop <repo_path>` | Run scan → classify → policy → remediate → verify loop |
| `weekly-evidence` | Discover all owner repos, scan, and generate evidence report |

### `goal-loop` flags

| Flag | Description |
|------|-------------|
| `--goal TEXT` | Remediation goal (default: `make repo agent-ready`) |
| `--audit-dir DIR` | Where to write audit JSON logs (default: `./audit/`) |
| `--overwrite` / `--force` | Replace existing `CLAUDE.md` and `repo_policy.yaml` |

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
| `audit/goal_loop_*.json` | Working directory | No (in `.gitignore`) |
| `audit/<loop_id>/remediation_agent_prompt.md` | Working directory | No (in `.gitignore`) |
| `audit/<loop_id>/remediation_plan.md` | Working directory | No (in `.gitignore`) |

---

## Goal-Based Loop

The goal-based loop automates the governance workflow for a **single repository**:

1. **Scan** — inspect files, languages, secrets indicators, and structure
2. **Classify** — assign risk level and agent-readiness score
3. **Policy** — write `CLAUDE.md` and `repo_policy.yaml` into the target repo
4. **Remediate** — generate a bounded agent prompt and remediation plan (see safety limits below)
5. **Verify** — re-scan and compare before/after agent-readiness

### How to run

```powershell
repo-governor goal-loop "C:\path\to\your-repo"
```

Optional flags:

```powershell
repo-governor goal-loop "C:\path\to\your-repo" --audit-dir .\audit --overwrite
```

Exit code `0` means the verification scan reports the repo as agent-ready. Exit code `1` means issues remain.

### What files it creates

| Location | Purpose |
|----------|---------|
| `<repo>/CLAUDE.md` | Agent policy (in the target repo) |
| `<repo>/repo_policy.yaml` | Machine-readable policy (in the target repo) |
| `./audit/goal_loop_<timestamp>_<id>.json` | Full audit trail for the loop run |
| `./audit/<loop_id>/remediation_agent_prompt.md` | Bounded prompt for a human or external agent |
| `./audit/<loop_id>/remediation_plan.md` | Step-by-step remediation checklist |

### Audit trail contents

Each JSON audit file records:

- `loop_id`, `timestamp`, `target_repo`, and `goal`
- `initial_scan` — snapshot of the first scan
- `risk_classification` — risk level, blocking issues, readiness score
- `generated_artifacts` — paths to policy files written
- `remediation_status` — `manual_agent_prompt_generated`, `executed`, or `failed`
- `verification_scan` — post-loop scan and classification
- `passed` — whether the repo is agent-ready after verification
- `remaining_issues` and `errors`

### Safety limits of autonomous remediation

Repo Governor does **not** silently fix repositories on its own. By default:

- The loop **generates** a remediation prompt and plan but does **not** execute an AI agent.
- The audit log honestly records `remediation_status: manual_agent_prompt_generated`.
- Verification re-scans the repo as-is; if no external agent applied fixes, `passed` will be `false` unless the repo was already agent-ready.
- To hook up an external runner in the future, set `REPO_GOVERNOR_AGENT_RUNNER` — automatic execution is not yet implemented.

The generated prompt instructs any agent to make **minimal safe changes** and forbids touching secrets, credentials, production config, or destructive operations.

---

## Safety Rules

- Reports are excluded from git by default (`reports/` and `repo_governor_report_*.md` are in `.gitignore`).
- `policy-init` never overwrites existing files unless `--overwrite` / `--force` is passed.
- No destructive filesystem operations are performed on scanned repositories.
- No secrets, environment variable values, or credential file contents are printed or logged.
- Binary files and files larger than 1 MB are never read.

The generated prompt instructs any agent to make **minimal safe changes** and forbids touching secrets, credentials, production config, or destructive operations.

---

## Weekly All-Repo Evidence Reports

Repo Governor can automatically discover **all eligible repositories** under the GitHub account `driaialchemy`, scan each one, and produce a single combined evidence report. This reuses the existing goal-based loop engine for `goal_loop` mode, but defaults to the safer `scan_only` mode.

### What the weekly check does

1. Discovers all repositories owned by `driaialchemy` from the GitHub API
2. Applies inclusion/exclusion rules from `config/repo-discovery.yml`
3. Clones or updates each eligible repo into a temporary workspace
4. Scans and classifies each repository
5. Writes per-repo audit JSON files and one combined evidence report
6. Optionally emails the report to `draialchemy@gmail.com`

### Configuration files

| File | Purpose |
|------|---------|
| `config/repo-discovery.yml` | Controls which repos are included or excluded |
| `config/repos.generated.yml` | Auto-generated registry from GitHub discovery |
| `config/repos.yml` | Optional manual overrides for specific repos |

You do **not** need to manually list every repository. Discovery is dynamic.

### Excluding repositories

Edit `config/repo-discovery.yml`:

- `exclude_repos` — exact repo names to skip
- `exclude_patterns` — glob patterns (e.g. `tmp-*`, `*-archive`)
- `include_archived: false` — skip archived repos (default)
- `include_forks: false` — skip forks (default)
- `include_templates: false` — skip template repos (default)
- `repo_overrides` — per-repo mode and enabled flag

### Run modes

| Mode | What it does |
|------|-------------|
| `scan_only` | Scan + classify + audit evidence. **Does not modify** target repos. **Default.** |
| `prompt_only` | Scan + classify + generate remediation prompt in audit folder. No repo changes. |
| `goal_loop` | Uses the full goal-based loop. If no agent runner is configured, records `goal_loop_requested_but_agent_execution_not_configured`. |

`scan_only` is the default because it is the safest option for unattended weekly runs.

### How to run locally

```powershell
# Discover all driaialchemy repos and generate today's evidence report
repo-governor weekly-evidence --discover --mode scan_only

# Same via module entry point (used by GitHub Actions)
python -m repo_governor.multi_repo_runner --owner driaialchemy --discover --mode scan_only

# Include email delivery (requires SMTP env vars)
repo-governor weekly-evidence --discover --mode scan_only --send-email
```

### Where files are saved

| Location | Contents |
|----------|----------|
| `audit/multi_repo/YYYY-MM-DD/` | Per-repo audit JSON + run summary |
| `reports/YYYY-MM-DD/evidence-summary.md` | Human-readable combined report |
| `reports/YYYY-MM-DD/evidence-summary.txt` | Plain-text report (used as email body) |
| `reports/YYYY-MM-DD/evidence-summary.json` | Machine-readable combined report |
| `config/repos.generated.yml` | Generated registry of discovered repos |
| `workspace/repos/` | Temporary clones (never committed) |

### Email delivery

Set these environment variables (or GitHub Actions secrets):

| Variable / Secret | Required | Purpose |
|-------------------|----------|---------|
| `REPORT_EMAIL_FROM` | Yes | Sender email address |
| `SMTP_HOST` | Yes | SMTP server hostname |
| `SMTP_PORT` | Yes | SMTP port (e.g. `587`) |
| `SMTP_USERNAME` | Yes | SMTP login |
| `SMTP_PASSWORD` | Yes | SMTP password |
| `SMTP_USE_TLS` | Yes | `true` or `false` |
| `REPORT_EMAIL_TO` | No | Defaults to `draialchemy@gmail.com` (also set as GitHub secret) |
| `REPO_GOVERNOR_PAT` | Optional | Needed to discover and scan **private** repos |

If credentials are missing, the report is still saved locally and the audit records `email_delivery_status: skipped_missing_credentials`.

### Corrective and Verifiable Actions

When a repository fails agent-readiness checks or cannot be scanned, the evidence report includes a **Corrective and Verifiable Actions** section. Each finding lists:

- **Issue** — what was found
- **Why it matters** — risk to autonomous agent use
- **Corrective action** — what to fix
- **Verification action** — how to confirm the fix
- **Expected evidence** — audit file or PASS status to look for
- **Recommended mode** — usually `prompt_only` for safe remediation planning
- **Human review required** — Yes for HIGH-risk or scan failures

Weekly `scan_only` runs report these actions but **do not modify target repositories**.

### GitHub Actions

A workflow at `.github/workflows/weekly-repo-governor-evidence.yml` runs automatically and can be triggered manually.

**Manual trigger:** GitHub → Actions → "Weekly Repo Governor Evidence" → Run workflow → choose mode (defaults to `scan_only`).

**Schedule:** The default schedule is every Thursday at 3:46 PM America/Phoenix.

The workflow commits evidence reports and audit files back to this repository (not the scanned target repos).

### Private repo discovery

Public repos can be discovered without a token. To include **private** repositories, set `REPO_GOVERNOR_PAT` (or `GITHUB_TOKEN`) with `repo` scope. Without a token, only public repos are discovered and a warning is recorded in the audit trail.

---

## Running Tests

```bash
pytest
```

182 tests across scanner, classifier, policy generator, reporter, goal-based loop, and weekly evidence reporting.

---

## Project Structure

```
src/repo_governor/
    cli.py          # argparse CLI entry point
    scanner.py      # Repo discovery and file inspection
    classifier.py   # Risk classification (HIGH/MEDIUM/LOW + readiness score)
    policy.py       # CLAUDE.md + repo_policy.yaml generator
    reporter.py     # Markdown report generator (3 report types)
    goal_based_loop.py  # Goal-based scan → classify → policy → verify loop
    repo_discovery.py   # GitHub API repo discovery and registry
    multi_repo_runner.py  # Multi-repo governance runner
    evidence_report.py  # Combined evidence report generator
    email_delivery.py   # SMTP evidence report delivery
tests/              # pytest test suite
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
