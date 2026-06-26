# AIAlchemy Repo Governor — Weekly Evidence Report

**Report date:** 2026-06-26T23:04:27+00:00
**GitHub owner:** driaialchemy
**Run mode:** scan_only

## Executive Summary

Repo Governor discovered 16 repositories under driaialchemy. 16 were eligible for scanning. 16 were scanned successfully. 0 were skipped because they were archived, forks, excluded by configuration, or otherwise disabled.
Of the scanned repositories, 0 passed agent-readiness checks and 16 need additional governance work before an autonomous coding agent should be allowed to make changes.

Discovery notes:
- No REPO_GOVERNOR_PAT or GITHUB_TOKEN set — only public repositories will be discovered. Private repos require a token.

The evidence report was emailed successfully.

## Counts

- Repositories discovered: 16
- Repositories eligible: 16
- Repositories scanned successfully: 16
- Clone failures: 0
- Scan failures: 0
- Repositories skipped: 0
- Agent-ready (passed): 0
- Need governance work: 16

## Repository Details

### driaialchemy/Agent-Workflow-Review

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: requirements.txt
  - Test suite present — actively developed project.
  - Missing CLAUDE.md — no agent policy defined.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/ai-agent-governance

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 60/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json`
- **Missing controls:** AGENTS.md, secret/credential file handling
- **Remaining issues:**
  - Credential/secret files present: backend/.env
  - External AI API usage: openai — API key management required.
  - Credential pattern indicators in code: api_key
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/ai-agent-research-emailer

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: requirements.txt
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/ai-alchemy-prompt-evaluator

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key
  - Risk level is HIGH, expected LOW.
  - Missing CLAUDE.md.
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
- **Audit file:** `audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json`
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
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json`
- **Missing controls:** README, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Dependency manifests present: requirements.txt
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
  - Missing README — project context unavailable to agent.
- **Recommended next action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.

### driaialchemy/contractriskreviewpipeline

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** present
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json`
- **Missing controls:** README
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
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Spreadsheet/data export files found: audit_trail.xlsx, audit_trail_with_tools_populated_demo_v2.xlsx, audit_trail_with_tools_populated_demo_v3.xlsx
  - Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key, database_url
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

### driaialchemy/fishhatchery

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 60/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json`
- **Missing controls:** CLAUDE.md, .gitignore, README, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Missing .gitignore.
  - HTTP networking libraries in use: requests
  - Missing README — project context unavailable to agent.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/governance-logger

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: package.json
  - HTTP networking libraries in use: requests
  - Test suite present — actively developed project.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/jobseeker

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json`
- **Missing controls:** CLAUDE.md, .gitignore, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Missing .gitignore.
  - Missing CLAUDE.md — no agent policy defined.
  - Missing AGENTS.md — no machine-readable safety policy.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/mavenfuzzyfactory

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json`
- **Missing controls:** CLAUDE.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: pyproject.toml
  - CI/CD workflow configuration present (.github/workflows).
  - HTTP networking libraries in use: requests
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/mslw111

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 80/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json`
- **Missing controls:** CLAUDE.md, .gitignore, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Missing .gitignore.
  - Missing CLAUDE.md — no agent policy defined.
  - Missing AGENTS.md — no machine-readable safety policy.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/skillsartifactsbuild

- **Risk level:** LOW
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_skillsartifactsbuild_20260626T230456Z.json`
- **Missing controls:** CLAUDE.md
- **Remaining issues:**
  - Missing CLAUDE.md.
  - Missing CLAUDE.md — no agent policy defined.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/testingsoftwareengineering

- **Risk level:** MEDIUM
- **Agent-ready:** FAIL
- **Readiness score:** 100/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Risk level is MEDIUM, expected LOW.
  - Missing CLAUDE.md.
  - Dependency manifests present: requirements.txt
  - Test suite present — actively developed project.
  - Missing CLAUDE.md — no agent policy defined.
- **Recommended next action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.

### driaialchemy/workeragentcowork

- **Risk level:** HIGH
- **Agent-ready:** FAIL
- **Readiness score:** 90/100
- **Mode:** scan_only
- **CLAUDE.md:** missing
- **Policy artifacts:** recommendations_only
- **Remediation status:** not_requested
- **Verification status:** scan_only_no_verification_loop
- **Audit file:** `audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json`
- **Missing controls:** CLAUDE.md, AGENTS.md
- **Remaining issues:**
  - Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
  - Credential pattern indicators in code: api_key
  - External database terms detected (postgres) — potential data compliance risk.
  - Risk level is HIGH, expected LOW.
  - Missing CLAUDE.md.
- **Recommended next action:** Resolve HIGH-risk blocking issues before allowing any agent access.

## Corrective and Verifiable Actions

### 1. driaialchemy/Agent-Workflow-Review

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 2. driaialchemy/Agent-Workflow-Review

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 3. driaialchemy/Agent-Workflow-Review

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 4. driaialchemy/Agent-Workflow-Review

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 5. driaialchemy/Agent-Workflow-Review

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 6. driaialchemy/Agent-Workflow-Review

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Agent-Workflow-Review_20260626T230428Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 7. driaialchemy/ai-agent-governance

- **Issue:** Credential/secret files present: backend/.env
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 8. driaialchemy/ai-agent-governance

- **Issue:** External AI API usage: openai — API key management required.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 9. driaialchemy/ai-agent-governance

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 10. driaialchemy/ai-agent-governance

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 11. driaialchemy/ai-agent-governance

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 12. driaialchemy/ai-agent-governance

- **Issue:** Exposed secret or credential files detected.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 13. driaialchemy/ai-agent-governance

- **Issue:** Dependency manifests present: requirements.txt, package.json
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 14. driaialchemy/ai-agent-governance

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 15. driaialchemy/ai-agent-governance

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-governance_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 16. driaialchemy/ai-agent-research-emailer

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 17. driaialchemy/ai-agent-research-emailer

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 18. driaialchemy/ai-agent-research-emailer

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 19. driaialchemy/ai-agent-research-emailer

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 20. driaialchemy/ai-agent-research-emailer

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 21. driaialchemy/ai-agent-research-emailer

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 22. driaialchemy/ai-agent-research-emailer

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-agent-research-emailer_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 23. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 24. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 25. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 26. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 27. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 28. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 29. driaialchemy/ai-alchemy-prompt-evaluator

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_ai-alchemy-prompt-evaluator_20260626T230430Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 30. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 31. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Credential pattern indicators in code: api_key, database_url
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 32. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** External database terms detected (postgres, supabase) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 33. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 34. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 35. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 36. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** HTTP networking libraries in use: aiohttp, httpx, requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 37. driaialchemy/AIAlchemy-Repo-Governor

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_AIAlchemy-Repo-Governor_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 38. driaialchemy/contract-risk-review-pipeline

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 39. driaialchemy/contract-risk-review-pipeline

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 40. driaialchemy/contract-risk-review-pipeline

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 41. driaialchemy/contract-risk-review-pipeline

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 42. driaialchemy/contract-risk-review-pipeline

- **Issue:** Missing README — project context unavailable to agent.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 43. driaialchemy/contract-risk-review-pipeline

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Review audit evidence and run prompt_only or goal_loop when ready to remediate.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contract-risk-review-pipeline_20260626T230431Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 44. driaialchemy/contractriskreviewpipeline

- **Issue:** Multiple AI provider integrations (anthropic, gemini, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 45. driaialchemy/contractriskreviewpipeline

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 46. driaialchemy/contractriskreviewpipeline

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 47. driaialchemy/contractriskreviewpipeline

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 48. driaialchemy/contractriskreviewpipeline

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 49. driaialchemy/contractriskreviewpipeline

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 50. driaialchemy/contractriskreviewpipeline

- **Issue:** Missing README — project context unavailable to agent.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_contractriskreviewpipeline_20260626T230432Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 51. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Spreadsheet/data export files found: audit_trail.xlsx, audit_trail_with_tools_populated_demo_v2.xlsx, audit_trail_with_tools_populated_demo_v3.xlsx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 52. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Multiple AI provider integrations (anthropic, gemini, google.generativeai, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 53. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Credential pattern indicators in code: api_key, database_url
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 54. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 55. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 56. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 57. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 58. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Container configuration present (Dockerfile / docker-compose).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 59. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** HTTP networking libraries in use: httpx
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 60. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 61. driaialchemy/Device-Lifecycle-Intelligence-Platform-DLIP-

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_Device-Lifecycle-Intelligence-Platform-DLIP-_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 62. driaialchemy/fishhatchery

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 63. driaialchemy/fishhatchery

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 64. driaialchemy/fishhatchery

- **Issue:** Missing .gitignore.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 65. driaialchemy/fishhatchery

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 66. driaialchemy/fishhatchery

- **Issue:** Missing README — project context unavailable to agent.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 67. driaialchemy/fishhatchery

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 68. driaialchemy/fishhatchery

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 69. driaialchemy/fishhatchery

- **Issue:** Missing .gitignore — unintended files may be tracked.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_fishhatchery_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 70. driaialchemy/governance-logger

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 71. driaialchemy/governance-logger

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 72. driaialchemy/governance-logger

- **Issue:** Dependency manifests present: package.json
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 73. driaialchemy/governance-logger

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 74. driaialchemy/governance-logger

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 75. driaialchemy/governance-logger

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 76. driaialchemy/governance-logger

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_governance-logger_20260626T230454Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 77. driaialchemy/jobseeker

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 78. driaialchemy/jobseeker

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 79. driaialchemy/jobseeker

- **Issue:** Missing .gitignore.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 80. driaialchemy/jobseeker

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 81. driaialchemy/jobseeker

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 82. driaialchemy/jobseeker

- **Issue:** Missing .gitignore — unintended files may be tracked.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_jobseeker_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 83. driaialchemy/mavenfuzzyfactory

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 84. driaialchemy/mavenfuzzyfactory

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 85. driaialchemy/mavenfuzzyfactory

- **Issue:** Dependency manifests present: pyproject.toml
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 86. driaialchemy/mavenfuzzyfactory

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 87. driaialchemy/mavenfuzzyfactory

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 88. driaialchemy/mavenfuzzyfactory

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 89. driaialchemy/mavenfuzzyfactory

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mavenfuzzyfactory_20260626T230455Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 90. driaialchemy/mslw111

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 91. driaialchemy/mslw111

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 92. driaialchemy/mslw111

- **Issue:** Missing .gitignore.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 93. driaialchemy/mslw111

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 94. driaialchemy/mslw111

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 95. driaialchemy/mslw111

- **Issue:** Missing .gitignore — unintended files may be tracked.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_mslw111_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 96. driaialchemy/skillsartifactsbuild

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_skillsartifactsbuild_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 97. driaialchemy/skillsartifactsbuild

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_skillsartifactsbuild_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 98. driaialchemy/testingsoftwareengineering

- **Issue:** Risk level is MEDIUM, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 99. driaialchemy/testingsoftwareengineering

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 100. driaialchemy/testingsoftwareengineering

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 101. driaialchemy/testingsoftwareengineering

- **Issue:** Test suite present — actively developed project.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 102. driaialchemy/testingsoftwareengineering

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 103. driaialchemy/testingsoftwareengineering

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Add CLAUDE.md using `repo-governor policy-init` and review before committing.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_testingsoftwareengineering_20260626T230456Z.json
- **Recommended mode:** prompt_only
- **Human review required:** No
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 104. driaialchemy/workeragentcowork

- **Issue:** Multiple AI provider integrations (anthropic, openai) — elevated orchestration complexity.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 105. driaialchemy/workeragentcowork

- **Issue:** Credential pattern indicators in code: api_key
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 106. driaialchemy/workeragentcowork

- **Issue:** External database terms detected (postgres) — potential data compliance risk.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 107. driaialchemy/workeragentcowork

- **Issue:** Risk level is HIGH, expected LOW.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 108. driaialchemy/workeragentcowork

- **Issue:** Missing CLAUDE.md.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 109. driaialchemy/workeragentcowork

- **Issue:** Dependency manifests present: requirements.txt
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 110. driaialchemy/workeragentcowork

- **Issue:** Container configuration present (Dockerfile / docker-compose).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 111. driaialchemy/workeragentcowork

- **Issue:** CI/CD workflow configuration present (.github/workflows).
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 112. driaialchemy/workeragentcowork

- **Issue:** HTTP networking libraries in use: requests
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 113. driaialchemy/workeragentcowork

- **Issue:** Missing CLAUDE.md — no agent policy defined.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.

### 114. driaialchemy/workeragentcowork

- **Issue:** Missing AGENTS.md — no machine-readable safety policy.
- **Why it matters:** Autonomous coding agents can make unsafe changes when governance controls are missing or risk is elevated.
- **Corrective action:** Resolve HIGH-risk blocking issues before allowing any agent access.
- **Verification action:** Re-run `repo-governor weekly-evidence --mode scan_only` and confirm agent-ready PASS for this repository.
- **Expected evidence:** Updated audit file with PASS status: audit/multi_repo/2026-06-26/repo_workeragentcowork_20260626T230457Z.json
- **Recommended mode:** prompt_only
- **Human review required:** Yes
- **Note:** Weekly scan_only mode reports findings only — target repos are not modified automatically.
