# HIGH repos — walkthrough (one by one)

These six repos were classified **HIGH** in the 2026-08-22 scan. HIGH means: do not give an autonomous coding agent free roam until a human finishes the first safe step.

I did **not** read any `.env` or credential file contents. Findings below are from filenames, `.gitignore`, `git ls-files`, READMEs, and the scanner’s API-term list.

Work them in this order.

---

## 1. `driaialchemy/ai-agent-governance` — do this first

**What the scan said:** secret/credential file present at `backend/.env`; OpenAI and Postgres terms; missing `AGENTS.md`. `CLAUDE.md` already exists and is decent.

**What that actually means:** A file named `.env` is sitting in `backend/`. That filename is enough to call the repo HIGH. I did not open it.

**Worse than “file exists”:** `backend/.env` is **tracked in git**. `.gitignore` lists `.env`, which would hide a *new* untracked file, but git keeps tracking a file that was added before (or despite) that rule. Anyone with repo access can see the committed file.

### Safe first fix (human only)

1. Assume anything that was ever in that file is burned. In OpenAI / DB / any other dashboard, **rotate or revoke** those credentials. Do not paste old values into chat.
2. Stop tracking the file without printing it:
   ```bash
   cd ai-agent-governance
   git rm --cached backend/.env
   ```
   That un-tracks it. It does not display the contents.
3. Make ignore explicit:
   ```
   .env
   **/.env
   backend/.env
   ```
4. Commit that removal and the `.gitignore` change.
5. If this repo was ever public, or the file was pushed, treat those keys as leaked even after you delete them from the latest commit. History still had them until you rotate.
6. After that, you may add the draft `high/ai-agent-governance/AGENTS.md`. Do not overwrite the existing `CLAUDE.md` unless you want to merge rules.

**Do not** ask an agent to “clean up the env file.” That is how values get copied into chat logs.

---

## 2. `driaialchemy/ai-alchemy-prompt-evaluator`

**What the scan said:** multiple AI providers (Anthropic, OpenAI, Cloudflare) and `api_key` patterns; missing `CLAUDE.md` / `AGENTS.md`. No `.env` file was detected on disk.

**What that actually means:** This is a live Cloudflare Pages app. `main` auto-deploys. The HIGH flag is “this code talks to paid APIs,” not “we found a committed .env.” Keys should already live in Cloudflare secrets / local `.env` (gitignored).

### Safe first fix

1. In the Cloudflare dashboard (not in chat), confirm the function secrets exist and are not duplicated in `functions/` source.
2. Search the repo yourself for assignment names only (`API_KEY`, `sk-` string literals). If you find a real key in source, rotate it and remove the line. Do not paste the key here.
3. Add the drafts in `high/ai-alchemy-prompt-evaluator/` (`CLAUDE.md` + `AGENTS.md`).
4. Prefer a branch for agent work. A push to `main` can go public.

**Agent use after step 3:** small rubric/copy edits only. No deploys, no new providers.

---

## 3. `driaialchemy/AIAlchemy-Repo-Governor` (this repo)

**What the scan said:** many AI provider names, `api_key`, `database_url`, Postgres/Supabase terms.

**What that actually means:** This is mostly the **scanner’s own word list**. `scanner.py` and tests mention `openai`, `anthropic`, `gemini`, etc. so they can detect those terms in *other* repos. That trips the same detector here. There was **no** `.env` file on disk. `CLAUDE.md` and `AGENTS.md` already exist.

### Safe first fix

1. No secret rotation is required from this scan finding alone.
2. Keep using the existing policies. Do not let an agent loosen “never print secrets.”
3. Optional later improvement (in this repo, not urgent): stop counting the governor’s own detector vocabulary as a HIGH signal.

**Agent use:** already governed. Feature work in `src/repo_governor/` and `tests/` is the intended scope.

---

## 4. `driaialchemy/contractriskreviewpipeline` (Quorum)

**What the scan said:** Anthropic / Gemini / OpenAI + `api_key` patterns; missing README. `CLAUDE.md` and `AGENTS.md` already exist (they describe a LangGraph + Snowflake + multi-model ensemble).

**What that actually means:** HIGH is “many live model providers,” not a detected `.env`. A missing README makes agents guess; the policy files are already long and specific.

### Safe first fix

1. Confirm `.env` / Snowflake / provider keys are not committed (`git ls-files | findstr /i env` on Windows, or `git ls-files '*env*'`).
2. Add a short `README.md` that points at the existing `CLAUDE.md` and how to run `pytest` / Streamlit. Do not put connection strings in the README.
3. Do not add a fourth model provider to “improve” the ensemble unless you ask for that.

**Agent use after a README:** follow the existing CLAUDE/AGENTS files; tests required; no production Snowflake from an agent.

Drafts were **not** generated for this repo because the policies are already there.

---

## 5. `driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-`

**What the scan said:** missing `CLAUDE.md` / `AGENTS.md`; many `.xlsx` workbooks; Anthropic/Gemini/OpenAI; `api_key` and `database_url` patterns; Postgres.

**What that actually means:**

- `.env` is gitignored (`.env.example` is the template — that is correct).
- Several audit/demo spreadsheets **are tracked in git**. They are not `.env` files, but they can still hold operational or personal-looking device data.
- The app is built to talk to real model APIs and a database once you copy `.env.example` to `.env`.

### Safe first fix

1. Keep `.env` local only. Never commit it.
2. Open the tracked `.xlsx` files yourself. If any contain real customer/device data you would not want public, replace them with synthetic samples and commit the sanitized versions.
3. Then paste `high/Device-Lifecycle-Intelligence-Platform-DLIP-/CLAUDE.md` and `AGENTS.md`.

**Agent use after that:** Streamlit/agent-prompt edits only. No production `DATABASE_URL`. No new spreadsheet dumps of live data.

---

## 6. `driaialchemy/workeragentcowork`

**What the scan said:** Anthropic/OpenAI, `api_key`, Postgres/SQLite, missing policy files. `.env` was not detected as a present secret file. `.env.example` documents `OPENAI_API_KEY` and optional SMTP.

**What that actually means:** HIGH is “this worker can call models and send mail,” not “we found a leaked key file.” Docker and GitHub Actions increase the chance a secret gets logged if someone wires it wrong.

### Safe first fix

1. Confirm `.env` is not tracked (`git ls-files .env` should be empty).
2. In GitHub Actions settings, use repository secrets — do not put keys in workflow YAML.
3. Add `high/workeragentcowork/CLAUDE.md` and `AGENTS.md`.

**Agent use after that:** planner/worker/prompt edits. No unattended email sends. No workflow edits that print secrets.

---

## After you finish a HIGH repo

Re-scan that one folder:

```bash
repo-governor classify path/to/the/repo
```

`ai-agent-governance` will stay HIGH until `backend/.env` is gone from the working tree *or* you accept that filename-based HIGH is doing its job while the file still exists locally (even if gitignored). Local leftover `.env` files are OK if they are ignored and not committed; rotate first if they were ever pushed.

## What I will not do unless you ask

- Push these drafts into the other remotes
- Open PRs on those six repos
- Open or print `backend/.env`
- Auto-remediate secrets
