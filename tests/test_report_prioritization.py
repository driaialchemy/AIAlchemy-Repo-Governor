"""Tests for prioritized, de-noised weekly evidence reporting."""
from __future__ import annotations

import json
from pathlib import Path

from repo_governor.evidence_report import generate_evidence_reports, summarize_multi_repo_results
from repo_governor.multi_repo_runner import MultiRepoRunResult, run_repo_governance_check
from repo_governor.repo_discovery import RegistryRepo
from repo_governor.report_analysis import (
    _build_risk_signals,
    _build_structured_findings,
    build_remediation_order,
    build_repo_action_plan,
)


def _scan_result(
    name: str = "demo",
    *,
    risk_level: str = "MEDIUM",
    passed: bool = False,
    remaining_issues: list[str] | None = None,
    initial_scan: dict | None = None,
) -> dict:
    scan = {
        "has_claude_md": False,
        "has_agents_md": False,
        "has_readme": True,
        "has_gitignore": True,
        "has_env_files": False,
        "has_tests_dir": True,
        "has_requirements_txt": True,
        "has_pyproject": False,
        "has_package_json": False,
        "has_dockerfile": False,
        "has_docker_compose": False,
        "has_github_workflows": False,
        "api_terms_found": ["requests"],
        "is_git_repo": True,
        "artifact_paths": [],
        "env_file_paths": [],
        "file_count": 42,
    }
    if initial_scan:
        scan.update(initial_scan)
    return {
        "name": name,
        "full_name": f"driaialchemy/{name}",
        "status": "scanned",
        "passed": passed,
        "risk_level": risk_level,
        "remaining_issues": remaining_issues or [],
        "initial_scan": scan,
        "has_claude_md": scan.get("has_claude_md", False),
        "audit_path": f"/audit/{name}.json",
        "mode": "scan_only",
    }


def test_dependency_manifests_are_risk_signals_not_findings():
    item = _scan_result(
        remaining_issues=[
            "Missing CLAUDE.md — no agent policy defined.",
            "Dependency manifests present: requirements.txt",
        ],
    )
    findings = _build_structured_findings(item)
    signals = _build_risk_signals(item)
    titles = {f["title"] for f in findings}
    signal_labels = " ".join(s["label"] for s in signals)
    assert not any("dependency manifest" in t.lower() for t in titles)
    assert "requirements.txt" in signal_labels.lower() or "dependency manifest" in signal_labels.lower()


def test_test_suite_present_is_positive_signal_not_corrective_action():
    item = _scan_result(
        remaining_issues=["Test suite present — actively developed project."],
    )
    findings = _build_structured_findings(item)
    signals = _build_risk_signals(item)
    assert not any("test suite present" in f["title"].lower() for f in findings)
    assert any("test suite" in s["label"].lower() for s in signals)


def test_http_libraries_are_risk_signals_not_standalone_corrective_actions():
    item = _scan_result(
        remaining_issues=["HTTP networking libraries in use: requests"],
    )
    plan = build_repo_action_plan(item)
    action_text = json.dumps(plan["top_corrective_actions"]).lower()
    assert "requests" not in action_text or "http networking" in json.dumps(plan["risk_signals"]).lower()
    assert not any("http networking libraries in use" in a["title"].lower() for a in plan["top_corrective_actions"])


def test_duplicate_claude_md_findings_are_merged():
    item = _scan_result(
        remaining_issues=[
            "Missing CLAUDE.md.",
            "Missing CLAUDE.md — no agent policy defined.",
        ],
    )
    findings = _build_structured_findings(item)
    claude = [f for f in findings if f["id"] == "missing_claude_md"]
    assert len(claude) == 1
    assert "agent operating instructions" in claude[0]["title"].lower()


def test_duplicate_agents_md_findings_are_merged():
    item = _scan_result(
        initial_scan={"has_agents_md": False},
        remaining_issues=[
            "Missing AGENTS.md — no machine-readable safety policy.",
        ],
    )
    findings = _build_structured_findings(item)
    agents = [f for f in findings if f["id"] == "missing_agents_md"]
    assert len(agents) == 1


def test_high_risk_wording_does_not_expect_low():
    item = _scan_result(
        risk_level="HIGH",
        remaining_issues=["Risk level is HIGH, expected LOW."],
        initial_scan={"has_env_files": True, "env_file_paths": [".env"]},
    )
    findings = _build_structured_findings(item)
    high = [f for f in findings if f["id"] == "high_risk_controls"]
    assert high
    assert "expected LOW" not in high[0]["title"]
    assert "additional controls" in high[0]["title"].lower()


def test_medium_risk_wording():
    item = _scan_result(
        risk_level="MEDIUM",
        remaining_issues=["Risk level is MEDIUM, expected LOW."],
        initial_scan={"has_claude_md": True, "has_agents_md": True},
    )
    findings = _build_structured_findings(item)
    medium = [f for f in findings if f["id"] == "medium_risk_controls"]
    assert medium
    assert "expected LOW" not in medium[0]["title"]


def test_high_risk_recommends_human_review_first():
    item = _scan_result(risk_level="HIGH", initial_scan={"has_env_files": True, "env_file_paths": [".env"]})
    plan = build_repo_action_plan(item)
    assert plan["recommended_mode"] == "human_review_first"
    assert plan["human_review_required"] is True


def test_low_risk_missing_policy_recommends_prompt_only():
    item = _scan_result(risk_level="LOW", initial_scan={"has_claude_md": False, "has_agents_md": False})
    plan = build_repo_action_plan(item)
    assert plan["recommended_mode"] == "prompt_only"


def test_executive_summary_includes_risk_counts(tmp_path):
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-26T15:46:00+00:00",
        report_date="2026-06-26",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=3,
        repo_results=[
            _scan_result("low", risk_level="LOW"),
            _scan_result("med", risk_level="MEDIUM"),
            _scan_result("high", risk_level="HIGH", initial_scan={"has_env_files": True, "env_file_paths": [".env"]}),
        ],
    )
    summary = summarize_multi_repo_results(run)
    assert summary["total_high_risk"] == 1
    assert summary["total_medium_risk"] == 1
    assert summary["total_low_risk"] == 1
    assert summary["executive_narrative"]
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    assert "High-risk repositories: 1" in md


def test_remediation_order_is_generated_dynamically():
    scanned = [
        _scan_result("skillsartifactsbuild", risk_level="LOW"),
        _scan_result("ai-agent-governance", risk_level="HIGH", initial_scan={"has_env_files": True, "env_file_paths": [".env"]}),
        _scan_result("jobseeker", risk_level="MEDIUM"),
    ]
    order = build_remediation_order(scanned)
    assert "skillsartifactsbuild" in order["start_here"]
    assert "jobseeker" in order["next"]
    assert "ai-agent-governance" in order["human_review_first"]


def test_report_limits_top_corrective_actions_per_repo():
    item = _scan_result(
        risk_level="HIGH",
        initial_scan={
            "has_claude_md": False,
            "has_agents_md": False,
            "has_readme": False,
            "has_gitignore": False,
            "has_env_files": True,
            "env_file_paths": [".env"],
        },
    )
    plan = build_repo_action_plan(item, max_actions=5)
    assert len(plan["top_corrective_actions"]) <= 5


def test_raw_audit_json_preserves_detailed_remaining_issues(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    (repo / "requirements.txt").write_text("requests\n", encoding="utf-8")
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
    (repo / "main.py").write_text("import requests\napi_key='x'\n", encoding="utf-8")

    result = run_repo_governance_check(
        repo,
        RegistryRepo(
            name="repo",
            full_name="driaialchemy/repo",
            url="https://github.com/driaialchemy/repo.git",
            branch="main",
            mode="scan_only",
        ),
        mode="scan_only",
        audit_dir=tmp_path / "audit",
    )
    audit = json.loads(Path(result["audit_path"]).read_text(encoding="utf-8"))
    assert audit["remaining_issues"]
    assert len(audit["remaining_issues"]) >= 2


def test_report_is_concise_without_hundreds_of_actions(tmp_path):
    noisy_issues = [
        "Missing CLAUDE.md.",
        "Missing CLAUDE.md — no agent policy defined.",
        "Dependency manifests present: requirements.txt",
        "Test suite present — actively developed project.",
        "HTTP networking libraries in use: requests",
        "Risk level is MEDIUM, expected LOW.",
    ]
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-26T15:46:00+00:00",
        report_date="2026-06-26",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=2,
        repo_results=[
            _scan_result("demo-a", remaining_issues=noisy_issues),
            _scan_result("demo-b", remaining_issues=noisy_issues, risk_level="HIGH", initial_scan={"has_env_files": True, "env_file_paths": [".env"]}),
        ],
    )
    summary = summarize_multi_repo_results(run)
    assert len(summary["corrective_actions"]) < 20
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    assert "Per-Repo Action Plans" in md
    assert "Dependency manifests present: requirements.txt" not in md.split("Top corrective actions")[0]
    assert md.count("Add CLAUDE.md using") == 0


def test_missing_claude_md_gets_specific_corrective_action():
    item = _scan_result(
        risk_level="LOW",
        initial_scan={
            "has_claude_md": False,
            "has_agents_md": True,
            "has_readme": True,
            "has_gitignore": True,
            "has_requirements_txt": False,
            "api_terms_found": [],
        },
    )
    plan = build_repo_action_plan(item)
    claude_actions = [
        a for a in plan["top_corrective_actions"]
        if "claude" in a["title"].lower() or "claude" in a["corrective_action"].lower()
    ]
    assert claude_actions
    assert "allowed agent actions" in claude_actions[0]["corrective_action"].lower()


def test_no_secrets_in_prioritized_report(tmp_path):
    token = "github_pat_" + "A" * 24
    run = MultiRepoRunResult(
        run_id="run-1",
        timestamp="2026-06-26T15:46:00+00:00",
        report_date="2026-06-26",
        github_owner="driaialchemy",
        mode="scan_only",
        total_discovered=1,
        repo_results=[
            {
                "name": "demo",
                "full_name": "driaialchemy/demo",
                "status": "clone_failed",
                "errors": [f"git clone https://x-access-token:{token}@github.com/org/repo.git failed"],
            }
        ],
    )
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    data = json.loads(paths.json_path.read_text(encoding="utf-8"))
    assert token not in md
    assert token not in json.dumps(data)
