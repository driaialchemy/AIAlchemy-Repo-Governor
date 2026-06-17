"""Tests for repo_governor.classifier."""
from datetime import datetime
from pathlib import Path

import pytest

from repo_governor.classifier import ClassifiedRepo, RiskLevel, classify_all, classify_repo
from repo_governor.scanner import RepoInfo


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def _repo(
    name: str = "test",
    is_git_repo: bool = True,
    has_gitignore: bool = True,
    has_readme: bool = True,
    has_claude_md: bool = True,
    has_agents_md: bool = True,
    has_pyproject: bool = False,
    has_requirements_txt: bool = False,
    has_env_files: bool = False,
    env_file_paths: list[str] | None = None,
    file_count: int = 10,
    artifact_paths: list[str] | None = None,
    api_terms_found: list[str] | None = None,
    has_tests_dir: bool = False,
    has_package_json: bool = False,
    has_dockerfile: bool = False,
    has_docker_compose: bool = False,
    has_github_workflows: bool = False,
    has_wrangler_toml: bool = False,
    has_vercel_json: bool = False,
    has_netlify_toml: bool = False,
    has_render_yaml: bool = False,
    has_node_modules: bool = False,
    has_env_example: bool = False,
) -> RepoInfo:
    return RepoInfo(
        name=name,
        path=Path(f"C:/tmp/{name}"),
        is_git_repo=is_git_repo,
        has_gitignore=has_gitignore,
        has_readme=has_readme,
        has_claude_md=has_claude_md,
        has_agents_md=has_agents_md,
        has_pyproject=has_pyproject,
        has_requirements_txt=has_requirements_txt,
        has_env_files=has_env_files,
        env_file_paths=env_file_paths or [],
        file_count=file_count,
        languages=["Python"],
        last_modified=datetime.now(),
        artifact_paths=artifact_paths or [],
        api_terms_found=api_terms_found or [],
        has_tests_dir=has_tests_dir,
        has_package_json=has_package_json,
        has_dockerfile=has_dockerfile,
        has_docker_compose=has_docker_compose,
        has_github_workflows=has_github_workflows,
        has_wrangler_toml=has_wrangler_toml,
        has_vercel_json=has_vercel_json,
        has_netlify_toml=has_netlify_toml,
        has_render_yaml=has_render_yaml,
        has_node_modules=has_node_modules,
        has_env_example=has_env_example,
    )


# ---------------------------------------------------------------------------
# Original tests — must remain green
# ---------------------------------------------------------------------------

def test_fully_configured_repo_is_low_and_agent_ready():
    result = classify_repo(_repo())
    assert result.risk_level == RiskLevel.LOW
    assert result.agent_ready is True


def test_env_files_trigger_high_risk():
    result = classify_repo(_repo(has_env_files=True, env_file_paths=[".env"]))
    assert result.risk_level == RiskLevel.HIGH
    assert result.agent_ready is False


def test_no_git_triggers_high_risk():
    result = classify_repo(_repo(is_git_repo=False))
    assert result.risk_level == RiskLevel.HIGH


def test_missing_gitignore_and_readme_is_medium():
    result = classify_repo(_repo(has_gitignore=False, has_readme=False))
    assert result.risk_level == RiskLevel.MEDIUM


def test_single_missing_field_stays_low():
    result = classify_repo(_repo(has_readme=False))
    assert result.risk_level == RiskLevel.LOW


def test_missing_claude_md_not_agent_ready():
    result = classify_repo(_repo(has_claude_md=False))
    assert result.agent_ready is False


def test_large_repo_adds_medium_risk_factor():
    result = classify_repo(_repo(file_count=501))
    assert any("Large" in f for f in result.risk_factors)


def test_missing_claude_md_recommends_policy_init():
    result = classify_repo(_repo(has_claude_md=False))
    assert any("policy-init" in r for r in result.recommendations)


def test_classify_all_returns_same_count():
    repos = [_repo(name=f"repo_{i}") for i in range(5)]
    assert len(classify_all(repos)) == 5


def test_classify_all_preserves_order():
    repos = [_repo(name=f"repo_{i}") for i in range(3)]
    results = classify_all(repos)
    for i, cr in enumerate(results):
        assert cr.repo.name == f"repo_{i}"


# ---------------------------------------------------------------------------
# HIGH risk — each trigger independently
# ---------------------------------------------------------------------------

def test_high_risk_database_artifact():
    result = classify_repo(_repo(artifact_paths=["local.db"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("Database" in r for r in result.risk_reasons)


def test_high_risk_sqlite_artifact():
    result = classify_repo(_repo(artifact_paths=["app.sqlite"]))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_spreadsheet_artifact():
    result = classify_repo(_repo(artifact_paths=["export.xlsx"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("Spreadsheet" in r or "data export" in r.lower() for r in result.risk_reasons)


def test_high_risk_csv_artifact():
    result = classify_repo(_repo(artifact_paths=["data.csv"]))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_log_artifact():
    result = classify_repo(_repo(artifact_paths=["app.log"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("Log" in r or "log" in r for r in result.risk_reasons)


def test_high_risk_single_ai_api():
    result = classify_repo(_repo(api_terms_found=["openai"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("openai" in r.lower() for r in result.risk_reasons)


def test_high_risk_multiple_ai_providers():
    result = classify_repo(_repo(api_terms_found=["openai", "anthropic"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("Multiple" in r for r in result.risk_reasons)


def test_high_risk_credential_indicator():
    result = classify_repo(_repo(api_terms_found=["api_key"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("api_key" in r for r in result.risk_reasons)


def test_high_risk_database_url_indicator():
    result = classify_repo(_repo(api_terms_found=["database_url"]))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_external_db_postgres():
    result = classify_repo(_repo(api_terms_found=["postgres"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any("compliance" in r.lower() for r in result.risk_reasons)


def test_high_risk_external_db_supabase():
    result = classify_repo(_repo(api_terms_found=["supabase"]))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_vercel_deployment():
    result = classify_repo(_repo(has_vercel_json=True))
    assert result.risk_level == RiskLevel.HIGH
    assert any("vercel.json" in r for r in result.risk_reasons)


def test_high_risk_wrangler_deployment():
    result = classify_repo(_repo(has_wrangler_toml=True))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_netlify_deployment():
    result = classify_repo(_repo(has_netlify_toml=True))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_render_deployment():
    result = classify_repo(_repo(has_render_yaml=True))
    assert result.risk_level == RiskLevel.HIGH


def test_high_risk_missing_gitignore_with_artifacts():
    result = classify_repo(_repo(has_gitignore=False, artifact_paths=["data.csv"]))
    assert result.risk_level == RiskLevel.HIGH
    assert any(".gitignore" in r for r in result.risk_reasons)


# ---------------------------------------------------------------------------
# MEDIUM risk
# ---------------------------------------------------------------------------

def test_medium_risk_package_files_and_tests():
    result = classify_repo(_repo(has_pyproject=True, has_tests_dir=True))
    assert result.risk_level == RiskLevel.MEDIUM


def test_medium_risk_dockerfile_and_ci():
    result = classify_repo(_repo(has_dockerfile=True, has_github_workflows=True))
    assert result.risk_level == RiskLevel.MEDIUM


def test_medium_risk_missing_two_docs():
    result = classify_repo(_repo(has_gitignore=False, has_readme=False))
    assert result.risk_level == RiskLevel.MEDIUM


def test_medium_risk_http_client_and_no_readme():
    result = classify_repo(_repo(api_terms_found=["requests"], has_readme=False))
    assert result.risk_level == RiskLevel.MEDIUM


def test_medium_risk_single_trigger_stays_low():
    """One MEDIUM trigger alone is not enough to escalate to MEDIUM."""
    result = classify_repo(_repo(has_pyproject=True))
    assert result.risk_level == RiskLevel.LOW


# ---------------------------------------------------------------------------
# LOW risk
# ---------------------------------------------------------------------------

def test_low_risk_clean_skeleton():
    result = classify_repo(_repo())
    assert result.risk_level == RiskLevel.LOW
    assert result.agent_ready is True


def test_low_risk_agent_ready_requires_claude_md():
    result = classify_repo(_repo(has_claude_md=False))
    assert result.risk_level == RiskLevel.LOW
    assert result.agent_ready is False


def test_low_risk_agent_ready_requires_gitignore():
    result = classify_repo(_repo(has_gitignore=False))
    assert result.risk_level == RiskLevel.LOW
    assert result.agent_ready is False


# ---------------------------------------------------------------------------
# Readiness score
# ---------------------------------------------------------------------------

def test_readiness_score_perfect_except_no_tests():
    # _repo() defaults: no tests dir → -10
    result = classify_repo(_repo())
    assert result.readiness_score == 90


def test_readiness_score_with_tests_dir():
    result = classify_repo(_repo(has_tests_dir=True))
    assert result.readiness_score == 100


def test_readiness_score_env_file_deducts_20():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    with_env = classify_repo(_repo(has_tests_dir=True, has_env_files=True)).readiness_score
    assert base - with_env == 20


def test_readiness_score_db_artifact_deducts_20():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    with_db = classify_repo(_repo(has_tests_dir=True, artifact_paths=["a.db"])).readiness_score
    assert base - with_db == 20


def test_readiness_score_spreadsheet_deducts_15():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    with_sheet = classify_repo(_repo(has_tests_dir=True, artifact_paths=["x.xlsx"])).readiness_score
    assert base - with_sheet == 15


def test_readiness_score_log_deducts_15():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    with_log = classify_repo(_repo(has_tests_dir=True, artifact_paths=["app.log"])).readiness_score
    assert base - with_log == 15


def test_readiness_score_missing_readme_deducts_10():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    without_readme = classify_repo(_repo(has_tests_dir=True, has_readme=False)).readiness_score
    assert base - without_readme == 10


def test_readiness_score_missing_tests_deducts_10():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    without_tests = classify_repo(_repo(has_tests_dir=False)).readiness_score
    assert base - without_tests == 10


def test_readiness_score_missing_gitignore_deducts_10():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    without_gi = classify_repo(_repo(has_tests_dir=True, has_gitignore=False)).readiness_score
    assert base - without_gi == 10


def test_readiness_score_api_without_env_example_deducts_10():
    base = classify_repo(_repo(has_tests_dir=True)).readiness_score
    with_api_no_example = classify_repo(
        _repo(has_tests_dir=True, api_terms_found=["openai"])
    ).readiness_score
    # openai → HIGH, but score still computed independently
    with_api_with_example = classify_repo(
        _repo(has_tests_dir=True, api_terms_found=["openai"], has_env_example=True)
    ).readiness_score
    assert with_api_no_example < with_api_with_example


def test_readiness_score_floor_is_zero():
    # Deliberately terrible repo: stacks every deduction
    result = classify_repo(
        _repo(
            has_env_files=True,                                  # -20
            artifact_paths=["a.db", "b.xlsx", "c.log"],         # -20, -15, -15
            has_readme=False,                                    # -10
            has_gitignore=False,                                 # -10
            # has_tests_dir=False is default                     # -10
        )
    )
    assert result.readiness_score == 0


def test_readiness_score_never_negative():
    result = classify_repo(
        _repo(
            has_env_files=True,
            artifact_paths=["a.db", "b.xlsx", "c.csv", "d.log"],
            has_readme=False,
            has_gitignore=False,
            api_terms_found=["openai"],
        )
    )
    assert result.readiness_score >= 0


# ---------------------------------------------------------------------------
# Blocking issues and recommended actions
# ---------------------------------------------------------------------------

def test_blocking_issues_present_for_high_risk():
    result = classify_repo(_repo(has_env_files=True, env_file_paths=[".env"]))
    assert bool(result.blocking_issues)


def test_blocking_issues_empty_for_low_risk():
    result = classify_repo(_repo())
    assert result.blocking_issues == []


def test_blocking_issues_describe_the_problem():
    result = classify_repo(_repo(artifact_paths=["secrets.db"]))
    assert any("Database" in issue for issue in result.blocking_issues)


def test_recommended_actions_generated_for_high_risk():
    result = classify_repo(_repo(has_env_files=True))
    assert bool(result.recommended_actions)


def test_recommended_actions_generated_for_medium_risk():
    result = classify_repo(_repo(has_pyproject=True, has_tests_dir=True))
    assert bool(result.recommended_actions)


def test_recommended_actions_no_duplicates():
    # Two HIGH triggers that share an action should not duplicate it
    result = classify_repo(_repo(api_terms_found=["openai", "anthropic"]))
    assert len(result.recommended_actions) == len(set(result.recommended_actions))


# ---------------------------------------------------------------------------
# New interface fields
# ---------------------------------------------------------------------------

def test_repo_name_property():
    result = classify_repo(_repo(name="my-project"))
    assert result.repo_name == "my-project"


def test_risk_factors_alias_returns_same_list():
    result = classify_repo(_repo(file_count=501))
    assert result.risk_factors is result.risk_reasons


def test_recommendations_alias_returns_same_list():
    result = classify_repo(_repo(has_claude_md=False))
    assert result.recommendations is result.recommended_actions
