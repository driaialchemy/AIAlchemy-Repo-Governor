"""Tests for repo_governor.reporter."""
from datetime import datetime
from pathlib import Path

from repo_governor.classifier import ClassifiedRepo, RiskLevel
from repo_governor.reporter import generate_report, write_report
from repo_governor.scanner import RepoInfo


def _classified(
    name: str = "myrepo",
    risk: RiskLevel = RiskLevel.LOW,
    agent_ready: bool = True,
    risk_factors: list[str] | None = None,
    recommendations: list[str] | None = None,
) -> ClassifiedRepo:
    repo = RepoInfo(
        name=name,
        path=Path(f"C:/tmp/{name}"),
        is_git_repo=True,
        has_gitignore=True,
        has_readme=True,
        has_claude_md=True,
        has_agents_md=True,
        has_pyproject=False,
        has_requirements_txt=False,
        has_env_files=False,
        env_file_paths=[],
        file_count=5,
        languages=["Python"],
        last_modified=datetime.now(),
    )
    return ClassifiedRepo(
        repo=repo,
        risk_level=risk,
        risk_reasons=risk_factors or [],
        recommended_actions=recommendations or [],
        agent_ready=agent_ready,
    )


def test_generate_report_contains_repo_name():
    report = generate_report([_classified("myrepo")], Path("C:/tmp"))
    assert "myrepo" in report


def test_generate_report_starts_with_header():
    report = generate_report([_classified()], Path("C:/tmp"))
    assert report.startswith("# AIAlchemy Repo Governor")


def test_generate_report_has_summary_table():
    report = generate_report([_classified()], Path("C:/tmp"))
    assert "Summary" in report
    assert "LOW" in report or "HIGH" in report


def test_generate_report_counts_are_correct():
    classified = [
        _classified("a", RiskLevel.HIGH, agent_ready=False),
        _classified("b", RiskLevel.MEDIUM, agent_ready=False),
        _classified("c", RiskLevel.LOW, agent_ready=True),
    ]
    report = generate_report(classified, Path("C:/tmp"))
    assert "| 🔴 HIGH | 1 |" in report
    assert "| 🟡 MEDIUM | 1 |" in report
    assert "| 🟢 LOW | 1 |" in report


def test_generate_report_includes_risk_factors():
    cr = _classified(risk_factors=["Missing .gitignore"])
    report = generate_report([cr], Path("C:/tmp"))
    assert "Missing .gitignore" in report


def test_generate_report_includes_recommendations():
    cr = _classified(recommendations=["Add a .gitignore file."])
    report = generate_report([cr], Path("C:/tmp"))
    assert "Add a .gitignore file." in report


def test_write_report_creates_file(tmp_path):
    output = tmp_path / "report.md"
    path = write_report([_classified()], Path("C:/tmp"), output_path=output)
    assert path.exists()
    assert path.read_text(encoding="utf-8").startswith("# AIAlchemy")


def test_write_report_default_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = write_report([_classified()], Path("C:/tmp"))
    assert path.name.startswith("repo_governor_report_")
    assert path.suffix == ".md"


def test_generate_report_multiple_repos():
    classified = [_classified(f"repo_{i}") for i in range(5)]
    report = generate_report(classified, Path("C:/tmp"))
    for i in range(5):
        assert f"repo_{i}" in report
