"""Tests for repo_governor.goal_based_loop."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from repo_governor.goal_based_loop import (
    generate_starter_agent_prompt,
    run_goal_based_loop,
    run_initial_scan,
    run_remediation_agent,
    run_verification_scan,
    write_goal_loop_audit_log,
)
from repo_governor.policy import generate_repo_policy


def _minimal_repo(tmp_path: Path) -> Path:
    """Create a small repo with a blocking HIGH-risk issue (no git)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    (tmp_path / "README.md").write_text("# Sample\n")
    (tmp_path / "main.py").write_text("print('hello')\n")
    return tmp_path


def _agent_ready_repo(tmp_path: Path) -> Path:
    """Create a repo that should pass agent-ready checks."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    (tmp_path / "README.md").write_text("# Sample\n")
    (tmp_path / "CLAUDE.md").write_text("# Agent Policy\n")
    (tmp_path / "AGENTS.md").write_text("# Agents\n")
    (tmp_path / "main.py").write_text("print('hello')\n")
    return tmp_path


def test_run_initial_scan_missing_path(tmp_path):
    missing = tmp_path / "does-not-exist"
    with pytest.raises(ValueError, match="Not a directory"):
        run_initial_scan(missing)


def test_run_initial_scan_returns_repo_info(tmp_path):
    repo = _minimal_repo(tmp_path)
    info = run_initial_scan(repo)
    assert info.name == tmp_path.name
    assert info.has_gitignore is True
    assert info.is_git_repo is False


def test_generate_starter_agent_prompt_includes_constraints(tmp_path):
    repo = _minimal_repo(tmp_path)
    info = run_initial_scan(repo)
    from repo_governor.classifier import classify_repo

    classified = classify_repo(info)
    policy = generate_repo_policy(classified)
    prompt = generate_starter_agent_prompt(repo, info, classified, policy)
    assert str(repo.resolve().as_posix()) in prompt
    assert "Prohibited Actions" in prompt
    assert "secrets" in prompt.lower()
    assert classified.risk_level.value in prompt


def test_run_remediation_agent_writes_prompt_and_plan(tmp_path):
    prompt_path_parent = tmp_path / "loop-out"
    status, summary, prompt_file, plan_file = run_remediation_agent(
        tmp_path,
        "# Prompt\n",
        "# Plan\n",
        prompt_path_parent,
    )
    assert status == "manual_agent_prompt_generated"
    assert prompt_file.exists()
    assert plan_file.exists()
    assert "not executed" in summary.lower()


def test_write_goal_loop_audit_log_creates_json(tmp_path):
    audit_dir = tmp_path / "audit"
    path = write_goal_loop_audit_log(
        audit_dir,
        "test-loop-id",
        target_repo="/tmp/repo",
        goal="make repo agent-ready",
        initial_scan={"name": "repo"},
        risk_classification={"risk_level": "LOW"},
        generated_artifacts=["/tmp/repo/CLAUDE.md"],
        agent_prompt_path="/tmp/audit/prompt.md",
        remediation_status="manual_agent_prompt_generated",
        remediation_summary="Prompt generated.",
        verification_scan={"agent_ready": False},
        passed=False,
        remaining_issues=["Missing CLAUDE.md."],
        errors=[],
    )
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["loop_id"] == "test-loop-id"
    assert data["remediation_status"] == "manual_agent_prompt_generated"
    assert data["passed"] is False


def test_run_goal_based_loop_produces_audit_and_verification(tmp_path):
    repo = _minimal_repo(tmp_path / "sample-repo")
    audit_dir = tmp_path / "audit"

    result = run_goal_based_loop(repo, audit_dir=audit_dir, overwrite_policy=True)

    assert result.audit_log_path is not None
    assert Path(result.audit_log_path).exists()
    assert result.agent_prompt_path is not None
    assert Path(result.agent_prompt_path).exists()
    assert result.remediation_status == "manual_agent_prompt_generated"
    assert result.verification_risk_level == "HIGH"
    assert result.passed is False
    assert len(result.remaining_issues) > 0


def test_run_goal_based_loop_passes_for_agent_ready_repo(tmp_path):
    repo = _agent_ready_repo(tmp_path / "ready-repo")
    audit_dir = tmp_path / "audit"

    result = run_goal_based_loop(repo, audit_dir=audit_dir, overwrite_policy=True)

    assert result.initial_agent_ready is True
    assert result.verification_agent_ready is True
    assert result.passed is True
    assert result.remaining_issues == []


def test_run_verification_scan_reclassifies(tmp_path):
    repo = _minimal_repo(tmp_path)
    info, classified = run_verification_scan(repo)
    assert info.is_git_repo is False
    assert classified.agent_ready is False
    assert classified.risk_level.value == "HIGH"


def test_goal_loop_cli_smoke(tmp_path):
    repo = _minimal_repo(tmp_path / "cli-repo")
    audit_dir = tmp_path / "audit"
    src_dir = Path(__file__).resolve().parents[1] / "src"
    env = {**os.environ, "PYTHONPATH": str(src_dir)}
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "repo_governor.cli",
            "goal-loop",
            str(repo),
            "--audit-dir",
            str(audit_dir),
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    assert "Loop ID:" in proc.stdout
    assert proc.returncode == 1
    audit_files = list(audit_dir.glob("goal_loop_*.json"))
    assert len(audit_files) >= 1
