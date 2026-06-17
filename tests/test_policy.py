"""Tests for repo_governor.policy."""
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from repo_governor.classifier import ClassifiedRepo, RiskLevel, classify_repo
from repo_governor.policy import (
    DEFAULT_BLOCKED_PATHS,
    generate_policy,
    generate_repo_policy,
    write_policy,
    write_repo_policy,
)
from repo_governor.scanner import RepoInfo, scan_repo


# ---------------------------------------------------------------------------
# Original tests (10) — must remain green
# ---------------------------------------------------------------------------

def test_generate_policy_contains_repo_name(tmp_path):
    content = generate_policy(tmp_path, risk_level="LOW")
    assert tmp_path.name in content


def test_generate_policy_contains_risk_level(tmp_path):
    content = generate_policy(tmp_path, risk_level="HIGH")
    assert "HIGH" in content


def test_generate_policy_forbidden_section_present(tmp_path):
    content = generate_policy(tmp_path)
    assert "Forbidden" in content


def test_write_policy_creates_claude_md(tmp_path):
    path = write_policy(tmp_path, risk_level="LOW")
    assert path.exists()
    assert path.name == "CLAUDE.md"


def test_write_policy_content_is_valid_markdown(tmp_path):
    write_policy(tmp_path, risk_level="MEDIUM")
    text = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert text.startswith("# CLAUDE.md")


def test_write_policy_refuses_overwrite_by_default(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("existing content")
    with pytest.raises(FileExistsError):
        write_policy(tmp_path, risk_level="LOW")


def test_write_policy_overwrite_flag_replaces_file(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("existing content")
    write_policy(tmp_path, risk_level="LOW", overwrite=True)
    text = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "existing content" not in text
    assert "CLAUDE.md" in text


def test_generate_policy_warns_about_env_files(tmp_path):
    (tmp_path / ".env").write_text("SECRET=x")
    content = generate_policy(tmp_path, risk_level="HIGH")
    assert "WARNING" in content


def test_generate_policy_detects_python_build_tool(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'")
    content = generate_policy(tmp_path)
    assert "pyproject.toml" in content


def test_generate_policy_detects_requirements_txt(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests")
    content = generate_policy(tmp_path)
    assert "requirements.txt" in content


# ---------------------------------------------------------------------------
# Helpers for YAML policy tests
# ---------------------------------------------------------------------------

def _make_classified(tmp_path: Path) -> ClassifiedRepo:
    """Scan + classify tmp_path with the real pipeline."""
    return classify_repo(scan_repo(tmp_path))


def _git_init(path: Path) -> None:
    """Create a minimal git repo structure so is_git_repo=True."""
    (path / ".git").mkdir(exist_ok=True)
    (path / ".gitignore").write_text("*.pyc\n__pycache__/\n")


def _make_high(tmp_path: Path) -> ClassifiedRepo:
    _git_init(tmp_path)
    (tmp_path / ".env").write_text("SECRET=x")
    return _make_classified(tmp_path)


def _make_medium(tmp_path: Path) -> ClassifiedRepo:
    _git_init(tmp_path)
    (tmp_path / "README.md").write_text("# Test\n")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    (tmp_path / "tests").mkdir(exist_ok=True)
    return _make_classified(tmp_path)


def _make_low(tmp_path: Path) -> ClassifiedRepo:
    _git_init(tmp_path)
    (tmp_path / "README.md").write_text("# Test\n")
    (tmp_path / "CLAUDE.md").write_text("# Policy\n")
    (tmp_path / "AGENTS.md").write_text("# Agents\n")
    return _make_classified(tmp_path)


def _make_low_with_tests(tmp_path: Path) -> ClassifiedRepo:
    _git_init(tmp_path)
    (tmp_path / "README.md").write_text("# Test\n")
    (tmp_path / "CLAUDE.md").write_text("# Policy\n")
    (tmp_path / "AGENTS.md").write_text("# Agents\n")
    (tmp_path / "tests").mkdir(exist_ok=True)
    return _make_classified(tmp_path)


# ---------------------------------------------------------------------------
# generate_repo_policy — schema and field tests
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {
    "repo_name",
    "generated_at",
    "risk_level",
    "readiness_score",
    "allowed_edit_paths",
    "blocked_paths",
    "required_checks",
    "agent_permissions",
    "commit_requires_tests",
    "push_requires_human_approval",
    "secret_handling",
    "report_paths",
    "notes",
}


def test_generate_repo_policy_returns_dict(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert isinstance(result, dict)


def test_generate_repo_policy_has_all_required_fields(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert _REQUIRED_FIELDS.issubset(result.keys())


def test_generate_repo_policy_repo_name_matches(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert result["repo_name"] == tmp_path.name


def test_generate_repo_policy_risk_level_is_string(tmp_path):
    cr = _make_high(tmp_path)
    result = generate_repo_policy(cr)
    assert result["risk_level"] == "HIGH"
    assert isinstance(result["risk_level"], str)


def test_generate_repo_policy_readiness_score_is_int(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert isinstance(result["readiness_score"], int)
    assert 0 <= result["readiness_score"] <= 100


def test_generate_repo_policy_generated_at_is_iso8601(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    ts = result["generated_at"]
    # Must be parseable as an ISO 8601 string
    datetime.fromisoformat(ts)


def test_generate_repo_policy_blocked_paths_contains_defaults(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    for path in DEFAULT_BLOCKED_PATHS:
        assert path in result["blocked_paths"]


def test_generate_repo_policy_push_always_requires_human_approval(tmp_path):
    for i, make_fn in enumerate((_make_low, _make_medium, _make_high)):
        sub = tmp_path / str(i)
        sub.mkdir()
        cr = make_fn(sub)
        assert generate_repo_policy(cr)["push_requires_human_approval"] is True


def test_generate_repo_policy_secret_handling_fields(tmp_path):
    cr = _make_low(tmp_path)
    sh = generate_repo_policy(cr)["secret_handling"]
    assert sh["scan_before_commit"] is True
    assert sh["alert_on_detection"] is True
    assert isinstance(sh["blocked_patterns"], list)
    assert len(sh["blocked_patterns"]) > 0


def test_generate_repo_policy_report_paths_present(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert result["report_paths"] == ["repo_governor_report_*.md"]


def test_generate_repo_policy_notes_is_list(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert isinstance(result["notes"], list)
    assert len(result["notes"]) > 0


# ---------------------------------------------------------------------------
# HIGH risk behaviour
# ---------------------------------------------------------------------------

def test_generate_repo_policy_high_edit_is_restricted(tmp_path):
    cr = _make_high(tmp_path)
    perms = generate_repo_policy(cr)["agent_permissions"]
    assert perms["edit"] == "restricted"
    assert perms["read"] == "allowed"
    assert perms["network"] == "denied_by_default"


def test_generate_repo_policy_high_requires_human_review(tmp_path):
    cr = _make_high(tmp_path)
    checks = generate_repo_policy(cr)["required_checks"]
    assert "human_review" in checks
    assert "security_scan" in checks


def test_generate_repo_policy_high_commit_requires_tests(tmp_path):
    cr = _make_high(tmp_path)
    assert generate_repo_policy(cr)["commit_requires_tests"] is True


# ---------------------------------------------------------------------------
# MEDIUM risk behaviour
# ---------------------------------------------------------------------------

def test_generate_repo_policy_medium_edit_is_src_and_tests(tmp_path):
    cr = _make_medium(tmp_path)
    perms = generate_repo_policy(cr)["agent_permissions"]
    assert perms["edit"] == "allowed_in_src_and_tests"
    assert perms["network"] == "denied_by_default"


def test_generate_repo_policy_medium_commit_requires_tests(tmp_path):
    cr = _make_medium(tmp_path)
    assert generate_repo_policy(cr)["commit_requires_tests"] is True


def test_generate_repo_policy_medium_no_human_review_in_checks(tmp_path):
    cr = _make_medium(tmp_path)
    checks = generate_repo_policy(cr)["required_checks"]
    assert "human_review" not in checks


# ---------------------------------------------------------------------------
# LOW risk behaviour
# ---------------------------------------------------------------------------

def test_generate_repo_policy_low_edit_is_allowed(tmp_path):
    cr = _make_low(tmp_path)
    perms = generate_repo_policy(cr)["agent_permissions"]
    assert perms["edit"] == "allowed"


def test_generate_repo_policy_low_no_tests_commit_not_required(tmp_path):
    cr = _make_low(tmp_path)  # no tests dir
    assert generate_repo_policy(cr)["commit_requires_tests"] is False


def test_generate_repo_policy_low_with_tests_commit_required(tmp_path):
    cr = _make_low_with_tests(tmp_path)
    assert generate_repo_policy(cr)["commit_requires_tests"] is True


def test_generate_repo_policy_low_checks_without_tests(tmp_path):
    cr = _make_low(tmp_path)
    checks = generate_repo_policy(cr)["required_checks"]
    assert "human_review" not in checks
    assert "security_scan" not in checks


# ---------------------------------------------------------------------------
# allowed_edit_paths
# ---------------------------------------------------------------------------

def test_generate_repo_policy_allowed_paths_is_list(tmp_path):
    cr = _make_low(tmp_path)
    result = generate_repo_policy(cr)
    assert isinstance(result["allowed_edit_paths"], list)


def test_generate_repo_policy_high_allowed_paths_excludes_everything(tmp_path):
    # HIGH with no recognised src dirs → falls back to ["src/"]
    cr = _make_high(tmp_path)
    paths = generate_repo_policy(cr)["allowed_edit_paths"]
    assert isinstance(paths, list)
    assert len(paths) > 0


def test_generate_repo_policy_recognised_src_dir_appears_in_high(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / ".env").write_text("S=x")
    cr = classify_repo(scan_repo(tmp_path))
    paths = generate_repo_policy(cr)["allowed_edit_paths"]
    assert "src/" in paths


# ---------------------------------------------------------------------------
# write_repo_policy — file I/O
# ---------------------------------------------------------------------------

def test_write_repo_policy_creates_yaml_file(tmp_path):
    cr = _make_low(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    assert path.exists()
    assert path.name == "repo_policy.yaml"
    assert path.suffix == ".yaml"


def test_write_repo_policy_output_is_valid_yaml(tmp_path):
    cr = _make_low(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    content = path.read_text(encoding="utf-8")
    parsed = yaml.safe_load(content)
    assert isinstance(parsed, dict)


def test_write_repo_policy_parsed_yaml_has_all_fields(tmp_path):
    cr = _make_medium(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert _REQUIRED_FIELDS.issubset(parsed.keys())


def test_write_repo_policy_repo_name_in_file(tmp_path):
    cr = _make_low(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    content = path.read_text(encoding="utf-8")
    assert tmp_path.name in content


def test_write_repo_policy_has_header_comment(tmp_path):
    cr = _make_low(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    content = path.read_text(encoding="utf-8")
    assert content.startswith("#")
    assert "Repo Governor" in content


def test_write_repo_policy_refuses_overwrite_by_default(tmp_path):
    cr = _make_low(tmp_path)
    write_repo_policy(tmp_path, cr)
    with pytest.raises(FileExistsError):
        write_repo_policy(tmp_path, cr)


def test_write_repo_policy_overwrite_flag_replaces_file(tmp_path):
    cr = _make_low(tmp_path)
    write_repo_policy(tmp_path, cr)
    # Modify the file, then overwrite
    policy_path = tmp_path / "repo_policy.yaml"
    policy_path.write_text("old: content\n", encoding="utf-8")
    write_repo_policy(tmp_path, cr, overwrite=True)
    parsed = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    assert "repo_name" in parsed


def test_write_repo_policy_returns_path_object(tmp_path):
    cr = _make_low(tmp_path)
    result = write_repo_policy(tmp_path, cr)
    assert isinstance(result, Path)


def test_write_repo_policy_high_risk_yaml_shows_restricted(tmp_path):
    cr = _make_high(tmp_path)
    path = write_repo_policy(tmp_path, cr)
    parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert parsed["agent_permissions"]["edit"] == "restricted"
    assert parsed["risk_level"] == "HIGH"
