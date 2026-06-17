# Usage Guide

## Installation

```bash
git clone https://github.com/driaialchemy/AIAlchemy-Repo-Governor.git
cd AIAlchemy-Repo-Governor
pip install -e .
```

After installation, the `repo-governor` command is available on your PATH.

---

## Commands

### `scan <root_path>`

Discovers all directories under `root_path` and inspects each for key files and metadata.

```bash
repo-governor scan "C:\Users\msell\OneDrive\AIAlchemy\repositories"
```

Output shows each repo's name, whether it has a `.git` directory, file count, and detected languages. This command never modifies scanned repositories.

---

### `classify <root_path>`

Runs `scan` and applies risk classification (LOW / MEDIUM / HIGH) to each repo.

```bash
repo-governor classify "C:\Users\msell\OneDrive\AIAlchemy\repositories"
```

HIGH-risk repos and their specific risk factors are printed at the end. Each repo also gets a readiness score (0-100).

---

### `policy-init <repo_path>`

Generates two policy files in the specified repository:

| File | Format | Purpose |
|------|--------|---------|
| `CLAUDE.md` | Markdown | Human-readable agent policy |
| `repo_policy.yaml` | YAML | Machine-readable policy for automated tooling |

```bash
repo-governor policy-init "C:\Users\msell\OneDrive\AIAlchemy\repositories\my-project"
```

The command prints the risk level, readiness score, and any blocking issues. Neither file is committed automatically — review before adding to version control.

Flags:

| Flag | Description |
|------|-------------|
| `--overwrite` / `--force` | Replace existing policy files |

Example `repo_policy.yaml` structure:

```yaml
repo_name: my-project
generated_at: '2026-06-16T12:00:00+00:00'
risk_level: LOW
readiness_score: 95
allowed_edit_paths:
  - src/
  - tests/
blocked_paths:
  - .env
  - .env.*
  - .venv/
  - '*.db'
  - '*.log'
  - secrets/
required_checks:
  - run_tests
  - lint_check
agent_permissions:
  read: allowed
  edit: allowed
  shell: restricted
  network: denied_by_default
commit_requires_tests: false
push_requires_human_approval: true
secret_handling:
  scan_before_commit: true
  blocked_patterns:
    - .env
    - '*.pem'
    - id_rsa
  alert_on_detection: true
report_paths:
  - repo_governor_report_*.md
notes:
  - No significant risks detected.
```

---

### `report <root_path>`

Generates three Markdown report files covering all repos under `root_path`.

```bash
# Write to ./reports/ (default)
repo-governor report "C:\Users\msell\OneDrive\AIAlchemy\repositories"

# Write to a custom directory
repo-governor report "C:\...\repositories" --output-dir "C:\reports\scan-2026-06"

# Single combined file (legacy mode)
repo-governor report "C:\...\repositories" --output report.md
```

| Report file | Contents |
|-------------|----------|
| `AI_REPO_GOVERNANCE_REPORT.md` | Full per-repo findings, readiness scores, blocking issues |
| `agent_readiness_report.md` | Ready / needs cleanup / blocked summary |
| `cleanup_recommendations.md` | Repo-by-repo cleanup steps with sample commands |

Reports are excluded from git by default (`reports/` is in `.gitignore`). Review before sharing — they may contain local file paths and security findings.

---

### `agent-ready <root_path>`

Shows which repos pass all agent-readiness checks, and lists the blocking issues for those that don't.

```bash
repo-governor agent-ready "C:\Users\msell\OneDrive\AIAlchemy\repositories"
```

A repo is agent-ready when:
1. It is a git repository.
2. It has a `.gitignore`.
3. No `.env` or credential files are present.
4. It has a `CLAUDE.md` policy file.
5. Risk level is LOW.

---

## Typical Workflow

```bash
# 1. Scan everything to get an overview
repo-governor scan "C:\path\to\repos"

# 2. Classify to see risk levels at a glance
repo-governor classify "C:\path\to\repos"

# 3. Generate governance reports
repo-governor report "C:\path\to\repos"

# 4. Generate CLAUDE.md + repo_policy.yaml for a specific repo
repo-governor policy-init "C:\path\to\repos\my-project"

# 5. Confirm agent-readiness
repo-governor agent-ready "C:\path\to\repos"
```
