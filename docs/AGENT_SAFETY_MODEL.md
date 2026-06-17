# Agent Safety Model

This document describes the threat model and safety principles behind AIAlchemy Repo Governor's risk classification.

## Why Repos Need Governance Before Agent Use

AI coding agents (Claude Code, Codex, Copilot Workspace) operate with broad filesystem and shell access. Without guardrails, they can:

- Read and exfiltrate secrets stored in `.env` files.
- Commit sensitive files to git history.
- Run destructive commands without checkpoints.
- Modify infrastructure files outside their intended scope.

Repo Governor addresses these risks by scanning repos before agent sessions begin, classifying the risk profile, and generating scoped `CLAUDE.md` / `AGENTS.md` policies.

## Risk Level Definitions

### HIGH

The repo has at least one of:

- **Exposed secrets** — `.env`, `credentials.json`, private keys, or similar files are present at the filesystem level and may not be in `.gitignore`.
- **No version control** — The directory is not a git repository. There is no rollback mechanism if the agent makes destructive changes.

**Action required:** Do not use an agent in this repo until HIGH-risk issues are resolved.

### MEDIUM

Two or more of:

- Missing `.gitignore` — unintended files may be committed.
- Missing `README.md` — the agent has no natural-language description of the project's purpose.
- Missing `CLAUDE.md` — the agent has no explicit permission/prohibition policy.
- Missing `AGENTS.md` — no machine-readable agent safety declaration.
- More than 500 files — broad filesystem context increases the chance of accidental modification.

**Action required:** Resolve at least the missing `CLAUDE.md` before starting an agent session.

### LOW

Fewer than two MEDIUM-level issues and no HIGH-level issues.

## Agent-Ready Criteria

A repo is **agent-ready** when all of the following are true:

1. Risk level is LOW.
2. `CLAUDE.md` is present.
3. `.gitignore` is present.
4. No sensitive files (`.env`, etc.) are present.

## Sensitive File Detection

Repo Governor checks for filenames in a known-bad list including:

- `.env`, `.env.local`, `.env.production`, `.env.development`, `.env.staging`
- `secrets.json`, `credentials.json`
- `private_key.pem`, `id_rsa`, `id_ed25519`, `id_dsa`
- `.netrc`, `token.json`

Detection is filename-based only. Content scanning (e.g., regex for API keys in source code) is out of MVP scope.

## Non-Destructive Principle

Repo Governor never modifies, moves, or deletes files it finds. All operations are:

- **Read-only** during `scan`, `classify`, `report`, and `agent-ready`.
- **Additive only** during `policy-init` (writes a new `CLAUDE.md`; refuses to overwrite without `--overwrite`).
