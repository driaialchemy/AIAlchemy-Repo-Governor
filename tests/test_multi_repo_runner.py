"""Tests for evidence report generation and multi-repo runner."""
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from repo_governor.evidence_report import generate_evidence_reports, summarize_multi_repo_results
from repo_governor.multi_repo_runner import (
    MultiRepoRunResult,
    run_multi_repo_governance_check,
    run_repo_governance_check,
)
from repo_governor.repo_discovery import RegistryRepo


def _registry_entry(name: str = "demo-repo") -> RegistryRepo:
    return RegistryRepo(
        name=name,
        full_name=f"driaialchemy/{name}",
        url=f"https://github.com/driaialchemy/{name}.git",
        branch="main",
        enabled=True,
        mode="scan_only",
        visibility="public",
    )


def _minimal_repo(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("*\n")
    (tmp_path / "README.md").write_text("# Demo\n")
    (tmp_path / "CLAUDE.md").write_text("# Policy\n")
    (tmp_path / "AGENTS.md").write_text("# Agents\n")
    (tmp_path / "main.py").write_text("print('ok')\n")
    return tmp_path


def test_scan_only_does_not_modify_target_repo(tmp_path):
    repo = _minimal_repo(tmp_path / "repo")
    original_claude = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    audit_dir = tmp_path / "audit"

    result = run_repo_governance_check(
        repo,
        _registry_entry(),
        mode="scan_only",
        audit_dir=audit_dir,
    )

    assert result["status"] == "scanned"
    assert (repo / "CLAUDE.md").read_text(encoding="utf-8") == original_claude
    assert result["policy_artifact_status"] == "recommendations_only"
    assert Path(result["audit_path"]).exists()


def test_prompt_only_generates_prompt_without_repo_changes(tmp_path):
    repo = _minimal_repo(tmp_path / "repo")
    (repo / "CLAUDE.md").unlink()
    audit_dir = tmp_path / "audit"

    result = run_repo_governance_check(
        repo,
        RegistryRepo(
            name="repo",
            full_name="driaialchemy/repo",
            url="https://github.com/driaialchemy/repo.git",
            branch="main",
            mode="prompt_only",
        ),
        mode="prompt_only",
        audit_dir=audit_dir,
    )

    assert not (repo / "CLAUDE.md").exists()
    assert result["remediation_status"] == "manual_agent_prompt_generated"
    assert result["policy_artifact_status"] == "prompt_generated_not_written_to_repo"


def test_invalid_mode_rejected():
    with pytest.raises(ValueError, match="Invalid mode"):
        run_repo_governance_check(
            Path("."),
            _registry_entry(),
            mode="bad_mode",
            audit_dir=Path("audit"),
        )


def test_multi_repo_continues_after_one_repo_fails(tmp_path):
    good_repo = _minimal_repo(tmp_path / "good")
    enabled = [
        _registry_entry("good"),
        RegistryRepo(
            name="bad",
            full_name="driaialchemy/bad",
            url="https://github.com/driaialchemy/bad.git",
            branch="main",
            mode="scan_only",
        ),
    ]

    def fake_clone(entry, workspace, token=None):
        if entry.name == "good":
            return good_repo
        raise RuntimeError("clone failed")

    with patch("repo_governor.multi_repo_runner.load_effective_repo_registry") as mock_discover:
        mock_discover.return_value = (enabled, [], [])
        with patch("repo_governor.multi_repo_runner.clone_or_update_target_repo", side_effect=fake_clone):
            result = run_multi_repo_governance_check(
                owner="driaialchemy",
                mode="scan_only",
                discover=True,
                workspace_dir=tmp_path / "ws",
                audit_dir=tmp_path / "audit",
            )

    statuses = {r["name"]: r.get("status") for r in result.repo_results}
    assert statuses.get("good") == "scanned"
    assert statuses.get("bad") == "failed"
    assert len(result.repo_results) == 2


def test_evidence_report_files_created(tmp_path):
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-25T15:46:00+00:00",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=2,
        repo_results=[
            {
                "name": "demo",
                "full_name": "driaialchemy/demo",
                "status": "scanned",
                "passed": True,
                "risk_level": "LOW",
                "readiness_score": 95,
                "has_claude_md": True,
                "mode": "scan_only",
                "initial_scan": {"has_claude_md": True, "has_gitignore": True, "has_readme": True, "has_agents_md": True, "has_env_files": False, "is_git_repo": True},
                "remediation_status": "not_requested",
                "verification_status": "scan_only_no_verification_loop",
                "audit_path": "/audit/demo.json",
                "remaining_issues": [],
                "missing_controls": [],
                "recommended_action": "No action required.",
                "policy_artifact_status": "recommendations_only",
            }
        ],
        skipped_repos=[
            {"name": "archived-one", "skip_reason": "archived"},
        ],
    )

    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    assert paths.markdown_path.exists()
    assert paths.text_path.exists()
    assert paths.json_path.exists()

    md = paths.markdown_path.read_text(encoding="utf-8")
    txt = paths.text_path.read_text(encoding="utf-8")
    data = json.loads(paths.json_path.read_text(encoding="utf-8"))

    assert "driaialchemy" in md
    assert "driaialchemy" in txt
    assert data["total_discovered"] == 2
    assert data["total_scanned"] == 1


def test_summarize_multi_repo_results():
    run = MultiRepoRunResult(
        run_id="x",
        timestamp="t",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=3,
        repo_results=[{"status": "scanned", "passed": True}, {"status": "scanned", "passed": False}],
        skipped_repos=[{"name": "skip"}],
    )
    summary = summarize_multi_repo_results(run)
    assert summary["total_scanned"] == 2
    assert summary["total_passed"] == 1
    assert summary["total_needs_work"] == 1
