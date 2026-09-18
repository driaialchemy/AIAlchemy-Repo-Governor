# AIAlchemy Repo Governor — Weekly Evidence Report

**Report date:** 2026-09-18T00:48:33+00:00
**GitHub owner:** driaialchemy
**Run mode:** scan_only

## Executive Summary

Repo Governor discovered 20 repositories under driaialchemy. 20 were eligible for scanning. 19 were scanned successfully. 0 were skipped because they were archived, forks, excluded by configuration, or otherwise disabled.
1 could not be cloned and 0 failed during scanning.
Of the scanned repositories, 4 passed agent-readiness checks and 15 need additional governance work before an autonomous coding agent should be allowed to make changes.

The evidence report was emailed successfully.

## Counts

- Repositories discovered: 20
- Repositories eligible: 20
- Repositories scanned successfully: 19
- Clone failures: 1
- Scan failures: 0
- Repositories skipped: 0
- Agent-ready (passed): 4
- Need governance work: 15

## Repository Details

### driaialchemy/Agent-Workflow-Review

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_Agent-Workflow-Review_20260918T004834Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/agentstack

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_agentstack_20260918T004835Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - Test suite present — actively developed project.
  - Large file count (619 files) — broad agent scope increases risk of unintended changes.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/ai-agent-governance

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json`
- **Remaining issues:**
  - External AI API usage: openai — API key management required.
  - Credential pattern indicators in code: api_key
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: requirements.txt, package.json
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/ai-agent-research-emailer

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_ai-agent-research-emailer_20260918T004838Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/ai-alchemy-prompt-evaluator

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_ai-alchemy-prompt-evaluator_20260918T004838Z.json`
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: requirements.txt
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/AIAlchemy-Repo-Governor

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json`
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key, database_url
  - External database terms detected (postgres, supabase) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: pyproject.toml
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/contract-risk-review-pipeline

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_contract-risk-review-pipeline_20260918T004839Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/contractriskreviewpipeline

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json`
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, gemini, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: pyproject.toml
  - HTTP networking libraries in use: requests
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 75/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json`
- **Remaining issues:**
  - Spreadsheet/data export files found: audit_trail.xlsx, audit_trail_with_tools_populated_demo_v2.xlsx, audit_trail_with_tools_populated_demo_v3.xlsx
  - Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key, database_url
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/expenseverificationpipeline

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 85/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json`
- **Missing controls:** AGENTS.md
- **Remaining issues:**
  - Spreadsheet/data export files found: sample_expenses.xlsx
  - External AI API usage: anthropic — API key management required.
  - Credential pattern indicators in code: api_key
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: pyproject.toml
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/fishhatchery

- **Risk level:** LOW
- **Agent-ready:** PASS
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_fishhatchery_20260918T004902Z.json`
- **Recommended next action:** No action required — repository is agent-ready.

### driaialchemy/governance-logger

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_governance-logger_20260918T004903Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: package.json
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/jobseeker

- **Risk level:** LOW
- **Agent-ready:** PASS
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_jobseeker_20260918T004904Z.json`
- **Recommended next action:** No action required — repository is agent-ready.

### driaialchemy/mavenfuzzyfactory

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: pyproject.toml
  - CI/CD workflow configuration present (.github/workflows).
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/mslw111

- **Risk level:** LOW
- **Agent-ready:** PASS
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_mslw111_20260918T004905Z.json`
- **Recommended next action:** No action required — repository is agent-ready.

### driaialchemy/realestateprospectingapp

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 75/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Spreadsheet/data export files found: synthetic_hidden_equity_data_az (1).xlsx
  - Cloud deployment configuration present: wrangler.toml
  - Risk level is HIGH, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: package.json
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/skillsartifactsbuild

- **Risk level:** LOW
- **Agent-ready:** PASS
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_skillsartifactsbuild_20260918T004906Z.json`
- **Recommended next action:** No action required — repository is agent-ready.

### driaialchemy/testingsoftwareengineering

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_testingsoftwareengineering_20260918T004906Z.json`
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - Test suite present — actively developed project.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/workeragentcowork

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json`
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
  - Dependency manifests present: requirements.txt
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

## Failed Repositories

### driaialchemy/deterministic-intake-agent

- **Status:** clone failed
- **Error:** git clone --branch main --single-branch https://github.com/driaialchemy/deterministic-intake-agent.git /home/runner/work/AIAlchemy-Repo-Governor/AIAlchemy-Repo-Governor/workspace/repos/deterministic-intake-agent failed: Cloning into '/home/runner/work/AIAlchemy-Repo-Governor/AIAlchemy-Repo-Governor/workspace/repos/deterministic-intake-agent'...
fatal: Remote branch main not found in upstream origin

## Corrective and Verifiable Actions

### 1. driaialchemy/Agent-Workflow-Review

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Agent-Workflow-Review_20260918T004834Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 2. driaialchemy/Agent-Workflow-Review

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Agent-Workflow-Review_20260918T004834Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 3. driaialchemy/Agent-Workflow-Review

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Agent-Workflow-Review_20260918T004834Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 4. driaialchemy/agentstack

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_agentstack_20260918T004835Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 5. driaialchemy/agentstack

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_agentstack_20260918T004835Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 6. driaialchemy/agentstack

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_agentstack_20260918T004835Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 7. driaialchemy/agentstack

- **Issue:** Large file count (619 files) — broad agent scope increases risk of unintended changes.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_agentstack_20260918T004835Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 8. driaialchemy/ai-agent-governance

- **Issue:** External AI API usage: openai — API key management required.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 9. driaialchemy/ai-agent-governance

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 10. driaialchemy/ai-agent-governance

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 11. driaialchemy/ai-agent-governance

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 12. driaialchemy/ai-agent-governance

- **Issue:** Dependency manifests present: requirements.txt, package.json
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 13. driaialchemy/ai-agent-governance

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-governance_20260918T004837Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 14. driaialchemy/ai-agent-research-emailer

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-research-emailer_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 15. driaialchemy/ai-agent-research-emailer

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-research-emailer_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 16. driaialchemy/ai-agent-research-emailer

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-research-emailer_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 17. driaialchemy/ai-agent-research-emailer

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-agent-research-emailer_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 18. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-alchemy-prompt-evaluator_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 19. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-alchemy-prompt-evaluator_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 20. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-alchemy-prompt-evaluator_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 21. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_ai-alchemy-prompt-evaluator_20260918T004838Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 22. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 23. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Credential pattern indicators in code: api_key, database_url
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 24. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** External database terms detected (postgres, supabase) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 25. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 26. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 27. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 28. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** HTTP networking libraries in use: aiohttp, httpx, requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 29. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_AIAlchemy-Repo-Governor_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 30. driaialchemy/contract-risk-review-pipeline

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contract-risk-review-pipeline_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 31. driaialchemy/contract-risk-review-pipeline

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contract-risk-review-pipeline_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 32. driaialchemy/contract-risk-review-pipeline

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contract-risk-review-pipeline_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 33. driaialchemy/contract-risk-review-pipeline

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contract-risk-review-pipeline_20260918T004839Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 34. driaialchemy/contractriskreviewpipeline

- **Issue:** Multiple AI provider integrations (anthropic, gemini, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 35. driaialchemy/contractriskreviewpipeline

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 36. driaialchemy/contractriskreviewpipeline

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 37. driaialchemy/contractriskreviewpipeline

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 38. driaialchemy/contractriskreviewpipeline

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 39. driaialchemy/contractriskreviewpipeline

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_contractriskreviewpipeline_20260918T004840Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 40. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Spreadsheet/data export files found: audit_trail.xlsx, audit_trail_with_tools_populated_demo_v2.xlsx, audit_trail_with_tools_populated_demo_v3.xlsx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 41. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 42. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Credential pattern indicators in code: api_key, database_url
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 43. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 44. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 45. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 46. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Container configuration present (Dockerfile / docker-compose).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 47. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** HTTP networking libraries in use: httpx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 48. driaialchemy/expenseverificationpipeline

- **Issue:** Spreadsheet/data export files found: sample_expenses.xlsx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 49. driaialchemy/expenseverificationpipeline

- **Issue:** External AI API usage: anthropic — API key management required.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 50. driaialchemy/expenseverificationpipeline

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 51. driaialchemy/expenseverificationpipeline

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 52. driaialchemy/expenseverificationpipeline

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 53. driaialchemy/expenseverificationpipeline

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 54. driaialchemy/expenseverificationpipeline

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_expenseverificationpipeline_20260918T004902Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 55. driaialchemy/governance-logger

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_governance-logger_20260918T004903Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 56. driaialchemy/governance-logger

- **Issue:** Dependency manifests present: package.json
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_governance-logger_20260918T004903Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 57. driaialchemy/governance-logger

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_governance-logger_20260918T004903Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 58. driaialchemy/governance-logger

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_governance-logger_20260918T004903Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 59. driaialchemy/mavenfuzzyfactory

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 60. driaialchemy/mavenfuzzyfactory

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 61. driaialchemy/mavenfuzzyfactory

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 62. driaialchemy/mavenfuzzyfactory

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 63. driaialchemy/mavenfuzzyfactory

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_mavenfuzzyfactory_20260918T004904Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 64. driaialchemy/realestateprospectingapp

- **Issue:** Spreadsheet/data export files found: synthetic_hidden_equity_data_az (1).xlsx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 65. driaialchemy/realestateprospectingapp

- **Issue:** Cloud deployment configuration present: wrangler.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 66. driaialchemy/realestateprospectingapp

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 67. driaialchemy/realestateprospectingapp

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 68. driaialchemy/realestateprospectingapp

- **Issue:** Dependency manifests present: package.json
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 69. driaialchemy/realestateprospectingapp

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 70. driaialchemy/realestateprospectingapp

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_realestateprospectingapp_20260918T004905Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 71. driaialchemy/testingsoftwareengineering

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_testingsoftwareengineering_20260918T004906Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 72. driaialchemy/testingsoftwareengineering

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_testingsoftwareengineering_20260918T004906Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 73. driaialchemy/testingsoftwareengineering

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_testingsoftwareengineering_20260918T004906Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 74. driaialchemy/workeragentcowork

- **Issue:** Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 75. driaialchemy/workeragentcowork

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 76. driaialchemy/workeragentcowork

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 77. driaialchemy/workeragentcowork

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 78. driaialchemy/workeragentcowork

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 79. driaialchemy/workeragentcowork

- **Issue:** Container configuration present (Dockerfile / docker-compose).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 80. driaialchemy/workeragentcowork

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 81. driaialchemy/workeragentcowork

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-09-18/repo_workeragentcowork_20260918T004907Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 82. driaialchemy/deterministic-intake-agent

- **Issue:** The repository could not be cloned into the workflow workspace.
- **Why it matters:** The repository could not be assessed, leaving a governance gap.
- **Corrective action:** Verify clone URL, branch name, token access, and GitHub Actions permissions; then rerun the workflow.
- **Verification action:** Confirm the next evidence report shows the repo status as scanned.
- **Expected evidence:** Per-repo audit JSON exists and contains scan results.
- **Recommended mode:** scan_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.
- **Technical detail:** git clone --branch main --single-branch https://github.com/driaialchemy/deterministic-intake-agent.git /home/runner/work/AIAlchemy-Repo-Governor/AIAlchemy-Repo-Governor/workspace/repos/deterministic-intake-agent failed: Cloning into '/home/runner/work/AIAlchemy-Repo-Governor/AIAlchemy-Repo-Governor/workspace/repos/deterministic-intake-agent'...
fatal: Remote branch main not found in upstream origin
