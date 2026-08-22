# Policy drafts and HIGH-repo walkthrough

These files were generated after the 2026-08-22 weekly scan (17/17 public repos scanned). They are **drafts in this repo** so you can review them. Nothing has been pushed to the other GitHub repositories.

## How to use the MEDIUM / LOW drafts

Each folder under `medium-low/<repo>/` has:

- `APPLY.md` — short instructions for you or an agent
- `CLAUDE.md` and/or `AGENTS.md` — paste at the **root** of that GitHub repo
- extra files only when the scan said they were missing (`.gitignore`, a stub `README.md`)

Suggested order (easiest first):

1. `skillsartifactsbuild` — LOW; only needs `CLAUDE.md` (`AGENTS.md` already exists)
2. `mavenfuzzyfactory` — only needs `CLAUDE.md` (strong `AGENTS.md` already exists)
3. `Agent-Workflow-Review` and `testingsoftwareengineering` — small Streamlit apps
4. `governance-logger` and `ai-agent-research-emailer`
5. `contract-risk-review-pipeline` — add `AGENTS.md` only; `CLAUDE.md` already exists
6. `agentstack` — large tree; add policies, do not refactor
7. `fishhatchery`, `jobseeker`, `mslw111` — nearly empty; policies plus `.gitignore` (and a stub README for fishhatchery)

Do not commit until you have read the file. Do not let an agent push for you unless you ask.

## HIGH repos

Read **[HIGH-REPOS.md](HIGH-REPOS.md)** first. Drafts under `high/` are optional and must wait until the human steps in that walkthrough are done.

`AIAlchemy-Repo-Governor` and `contractriskreviewpipeline` already have `CLAUDE.md` and `AGENTS.md`. They need a walkthrough, not new policy files.

## What this does *not* do

- It does not change the other remotes.
- It does not rotate credentials.
- It does not mark any repo agent-ready by itself. After you paste files into a target repo, re-scan that repo.
