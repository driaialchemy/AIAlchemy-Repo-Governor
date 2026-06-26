"""Tests for clone-to-scan handoff in the multi-repo runner."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from repo_governor.evidence_report import generate_evidence_reports, summarize_multi_repo_results
from repo_governor.multi_repo_runner import (
    MultiRepoRunResult,
    clone_or_update_target_repo,
    run_multi_repo_governance_check,
    run_repo_governance_check,
)
from repo_governor.repo_discovery import RegistryRepo


def _registry_entry(
    name: str = "demo-repo",
    *,
    branch: str = "main",
    visibility: str = "public",
) -> RegistryRepo:
    return RegistryRepo(
        name=name,
        full_name=f"driaialchemy/{name}",
        url=f"https://github.com/driaialchemy/{name}.git",
        branch=branch,
        enabled=True,
        mode="scan_only",
        visibility=visibility,
    )


def _minimal_repo(tmp_path: Path) -> Path:
    repo = tmp_path
    repo.mkdir(parents=True, exist_ok=True)
    (repo / ".git").mkdir()
    (repo / ".gitignore").write_text("*\n", encoding="utf-8")
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text("# Policy\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (repo / "main.py").write_text("print('ok')\n", encoding="utf-8")
    return repo.resolve()


def _git_available() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def test_clone_creates_workspace_parent_directory(tmp_path):
    workspace = tmp_path / "workspace" / "repos"
    entry = _registry_entry("tiny-repo")

    def fake_git(args, *, cwd, token=None):
        dest = Path(args[-1])
        dest.mkdir(parents=True)
        (dest / ".git").mkdir()

    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        result = clone_or_update_target_repo(entry, workspace)

    assert workspace.exists()
    assert result == (workspace / "tiny-repo").resolve()
    assert result.is_dir()
    assert (result / ".git").exists()


def test_clone_uses_absolute_destination_not_nested_path(tmp_path, monkeypatch):
    """Regression: git clone cwd must not double-nest workspace/repos paths."""
    workspace = tmp_path / "workspace" / "repos"
    workspace.mkdir(parents=True)
    entry = _registry_entry("nested-check")
    captured: list[list[str]] = []

    def fake_git(args, *, cwd, token=None):
        captured.append(list(args))
        dest = Path(args[-1])
        assert dest.is_absolute()
        assert dest == (workspace / "nested-check").resolve()
        dest.mkdir(parents=True)
        (dest / ".git").mkdir()

    monkeypatch.chdir(tmp_path)
    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        result = clone_or_update_target_repo(entry, workspace)

    assert captured
    clone_args = captured[0]
    assert clone_args[0] == "clone"
    assert clone_args[-1] == str((workspace / "nested-check").resolve())
    assert result.is_dir()


def test_non_git_workspace_directory_is_removed_and_recloned(tmp_path):
    workspace = tmp_path / "workspace" / "repos"
    workspace.mkdir(parents=True)
    stale = workspace / "stale-repo"
    stale.mkdir()
    (stale / "not-git.txt").write_text("stale", encoding="utf-8")
    entry = _registry_entry("stale-repo")
    calls: list[str] = []

    def fake_git(args, *, cwd, token=None):
        calls.append(args[0])
        if args[0] == "clone":
            dest = Path(args[-1])
            dest.mkdir(parents=True, exist_ok=True)
            (dest / ".git").mkdir()

    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        result = clone_or_update_target_repo(entry, workspace)

    assert "clone" in calls
    assert not (stale / "not-git.txt").exists()
    assert (result / ".git").exists()


def test_valid_existing_git_repo_is_updated_not_recloned(tmp_path):
    workspace = tmp_path / "workspace" / "repos"
    repo = workspace / "existing-repo"
    repo.mkdir(parents=True)
    (repo / ".git").mkdir()
    entry = _registry_entry("existing-repo")
    calls: list[list[str]] = []

    def fake_git(args, *, cwd, token=None):
        calls.append(args)

    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        result = clone_or_update_target_repo(entry, workspace)

    assert result == repo.resolve()
    assert calls[0][0] == "fetch"
    assert not any(call[0] == "clone" for call in calls)


def test_scanner_receives_resolved_cloned_path(tmp_path):
    workspace = tmp_path / "workspace" / "repos"
    entry = _registry_entry("scan-target")
    received: list[Path] = []

    def fake_git(args, *, cwd, token=None):
        dest = Path(args[-1])
        dest.mkdir(parents=True, exist_ok=True)
        (dest / ".git").mkdir()
        (dest / "README.md").write_text("# Hi", encoding="utf-8")

    def capture_scan(repo_path, repo_entry, **kwargs):
        received.append(repo_path)
        return run_repo_governance_check(
            repo_path,
            repo_entry,
            mode=kwargs["mode"],
            audit_dir=kwargs["audit_dir"],
        )

    enabled = [entry]
    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        with patch("repo_governor.multi_repo_runner.load_effective_repo_registry") as mock_discover:
            mock_discover.return_value = (enabled, [], [])
            with patch(
                "repo_governor.multi_repo_runner.run_repo_governance_check",
                side_effect=capture_scan,
            ):
                result = run_multi_repo_governance_check(
                    owner="driaialchemy",
                    mode="scan_only",
                    discover=True,
                    workspace_dir=workspace,
                    audit_dir=tmp_path / "audit",
                )

    assert received
    assert received[0] == (workspace / "scan-target").resolve()
    assert received[0].is_dir()
    assert result.repo_results[0]["status"] == "scanned"


def test_clone_failure_reported_as_clone_failed(tmp_path):
    enabled = [_registry_entry("bad-clone")]

    def fail_clone(entry, workspace, token=None):
        raise RuntimeError("git clone failed: authentication required")

    with patch("repo_governor.multi_repo_runner.load_effective_repo_registry") as mock_discover:
        mock_discover.return_value = (enabled, [], [])
        with patch("repo_governor.multi_repo_runner.clone_or_update_target_repo", side_effect=fail_clone):
            result = run_multi_repo_governance_check(
                owner="driaialchemy",
                mode="scan_only",
                discover=True,
                workspace_dir=tmp_path / "ws",
                audit_dir=tmp_path / "audit",
            )

    assert result.repo_results[0]["status"] == "clone_failed"
    summary = summarize_multi_repo_results(result)
    assert summary["total_clone_failed"] == 1
    assert summary["total_scanned"] == 0


def test_scan_failure_increments_scan_failed_count(tmp_path):
    repo = _minimal_repo(tmp_path / "repo")
    audit_dir = tmp_path / "audit"

    with patch("repo_governor.multi_repo_runner.run_initial_scan", side_effect=RuntimeError("scan broke")):
        result = run_repo_governance_check(
            repo,
            _registry_entry(),
            mode="scan_only",
            audit_dir=audit_dir,
        )

    assert result["status"] == "scan_failed"
    run = MultiRepoRunResult(
        run_id="x",
        timestamp="t",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=1,
        repo_results=[result],
    )
    summary = summarize_multi_repo_results(run)
    assert summary["total_scan_failed"] == 1


def test_report_accounting_reflects_failures_not_zero_scanned_zero_skipped(tmp_path):
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-25T15:46:00+00:00",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=3,
        repo_results=[
            {
                "name": "bad",
                "full_name": "driaialchemy/bad",
                "status": "clone_failed",
                "errors": ["git clone failed"],
            }
        ],
        skipped_repos=[{"name": "archived", "skip_reason": "archived"}],
    )
    summary = summarize_multi_repo_results(run)
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    data = json.loads(paths.json_path.read_text(encoding="utf-8"))

    assert summary["total_discovered"] == 3
    assert summary["total_eligible"] == 1
    assert summary["total_clone_failed"] == 1
    assert summary["total_scanned"] == 0
    assert summary["total_skipped"] == 1
    assert "Clone failures: 1" in md
    assert data["total_clone_failed"] == 1


def test_clone_failure_user_facing_issue_not_not_a_directory(tmp_path):
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-25T15:46:00+00:00",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=1,
        repo_results=[
            {
                "name": "demo",
                "full_name": "driaialchemy/demo",
                "status": "clone_failed",
                "errors": ["Not a directory: /tmp/workspace/repos/demo"],
            }
        ],
    )
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    assert "could not be cloned into the workflow workspace" in md
    assert "Not a directory" not in md.split("Issue:")[1].split("Why it matters")[0]


def test_credential_urls_redacted_in_clone_failure_report(tmp_path):
    token = "github_pat_" + "A" * 20
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-25T15:46:00+00:00",
        report_date="2026-06-25",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=1,
        repo_results=[
            {
                "name": "demo",
                "full_name": "driaialchemy/demo",
                "status": "clone_failed",
                "errors": [
                    f"git clone https://x-access-token:{token}@github.com/driaialchemy/demo.git failed"
                ],
            }
        ],
    )
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    data = json.loads(paths.json_path.read_text(encoding="utf-8"))
    assert token not in md
    assert token not in json.dumps(data)


def test_multi_repo_continues_after_clone_failure(tmp_path):
    good_repo = _minimal_repo(tmp_path / "good")
    enabled = [_registry_entry("good"), _registry_entry("bad")]

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

    statuses = {r["name"]: r["status"] for r in result.repo_results}
    assert statuses["good"] == "scanned"
    assert statuses["bad"] == "clone_failed"
    assert len(result.repo_results) == 2


@pytest.mark.skipif(not _git_available(), reason="git not available")
def test_smoke_clone_public_repo(tmp_path):
    """Clone a small public repo into workspace/repos and verify scan handoff."""
    workspace = tmp_path / "workspace" / "repos"
    entry = RegistryRepo(
        name="Hello-World",
        full_name="octocat/Hello-World",
        url="https://github.com/octocat/Hello-World.git",
        branch="master",
        enabled=True,
        mode="scan_only",
        visibility="public",
    )
    repo_path = clone_or_update_target_repo(entry, workspace)
    assert repo_path == (workspace / "Hello-World").resolve()
    assert repo_path.is_dir()
    assert (repo_path / ".git").exists()

    audit_dir = tmp_path / "audit"
    result = run_repo_governance_check(
        repo_path,
        entry,
        mode="scan_only",
        audit_dir=audit_dir,
    )
    assert result["status"] == "scanned"
    assert Path(result["audit_path"]).exists()
