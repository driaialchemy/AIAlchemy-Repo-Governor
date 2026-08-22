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
    url: str | None = None,
) -> RegistryRepo:
    return RegistryRepo(
        name=name,
        full_name=f"driaialchemy/{name}",
        url=url or f"https://github.com/driaialchemy/{name}.git",
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


def _init_local_git_repo(source: Path) -> Path:
    source.mkdir(parents=True, exist_ok=True)
    (source / "README.md").write_text("# Source\n", encoding="utf-8")
    (source / ".gitignore").write_text("*\n", encoding="utf-8")
    subprocess.run(["git", "init", "-b", "main"], cwd=source, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=source, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=source, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=source, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=source, check=True, capture_output=True)
    return source


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


def test_relative_workspace_dir_does_not_nest_clone(tmp_path, monkeypatch):
    """Regression for weekly CI: relative workspace/repos must not nest under cwd."""
    monkeypatch.chdir(tmp_path)
    relative_ws = Path("workspace") / "repos"
    entry = _registry_entry("rel-repo")
    captured: list[list[str]] = []

    def fake_git(args, *, cwd, token=None):
        captured.append(list(args))
        dest = Path(args[-1])
        assert dest.is_absolute(), f"clone dest must be absolute, got {dest}"
        assert dest == (tmp_path / "workspace" / "repos" / "rel-repo").resolve()
        dest.mkdir(parents=True)
        (dest / ".git").mkdir()

    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        result = clone_or_update_target_repo(entry, relative_ws)

    expected = (tmp_path / "workspace" / "repos" / "rel-repo").resolve()
    assert result == expected
    assert result.is_dir()
    nested = tmp_path / "workspace" / "repos" / "workspace" / "repos" / "rel-repo"
    assert not nested.exists()
    assert captured
    assert captured[0][-1] == str(expected)


def test_clone_uses_absolute_destination_not_nested_path(tmp_path, monkeypatch):
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
    issue_block = md.split("**Issue:**", 1)[1].split("**Why it matters**", 1)[0]
    assert "could not be cloned into the workflow workspace" in issue_block
    assert "Not a directory" not in issue_block


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


def test_verify_cloned_repo_rejects_missing_directory(tmp_path):
    workspace = tmp_path / "workspace" / "repos"
    entry = _registry_entry("missing-dir")

    def fake_git(args, *, cwd, token=None):
        return None

    with patch("repo_governor.multi_repo_runner._git", side_effect=fake_git):
        with pytest.raises(RuntimeError, match="not a directory"):
            clone_or_update_target_repo(entry, workspace)


@pytest.mark.skipif(not _git_available(), reason="git not available")
def test_real_clone_from_local_repo_with_relative_workspace(tmp_path, monkeypatch):
    source = _init_local_git_repo(tmp_path / "source-repo")
    work = tmp_path / "run"
    work.mkdir()
    monkeypatch.chdir(work)

    entry = _registry_entry("source-repo", url=str(source))
    result = clone_or_update_target_repo(entry, Path("workspace") / "repos")

    expected = (work / "workspace" / "repos" / "source-repo").resolve()
    assert result == expected
    assert result.is_dir()
    assert (result / "README.md").exists()
    assert (result / ".git").exists()
    nested = work / "workspace" / "repos" / "workspace" / "repos" / "source-repo"
    assert not nested.exists()

    audit_dir = tmp_path / "audit"
    scan_result = run_repo_governance_check(
        result,
        entry,
        mode="scan_only",
        audit_dir=audit_dir,
    )
    assert scan_result["status"] == "scanned"
