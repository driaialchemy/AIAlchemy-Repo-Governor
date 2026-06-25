"""Tests for repo_governor.repo_discovery."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from repo_governor.repo_discovery import (
    DiscoveredRepo,
    build_effective_repo_registry,
    discover_github_repos,
    filter_discovered_repos,
    load_generated_repo_registry,
    load_repo_discovery_config,
    write_generated_repo_registry,
)


def _sample_api_page() -> list[dict]:
    return [
        {
            "name": "AIAlchemy-Repo-Governor",
            "full_name": "driaialchemy/AIAlchemy-Repo-Governor",
            "clone_url": "https://github.com/driaialchemy/AIAlchemy-Repo-Governor.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": False,
            "fork": False,
            "disabled": False,
            "is_template": False,
            "pushed_at": "2026-06-01T12:00:00Z",
        },
        {
            "name": "archived-example",
            "full_name": "driaialchemy/archived-example",
            "clone_url": "https://github.com/driaialchemy/archived-example.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": True,
            "fork": False,
            "disabled": False,
            "is_template": False,
            "pushed_at": "2025-01-01T00:00:00Z",
        },
        {
            "name": "forked-tool",
            "full_name": "driaialchemy/forked-tool",
            "clone_url": "https://github.com/driaialchemy/forked-tool.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": False,
            "fork": True,
            "disabled": False,
            "is_template": False,
            "pushed_at": "2025-06-01T00:00:00Z",
        },
        {
            "name": "tmp-scratch",
            "full_name": "driaialchemy/tmp-scratch",
            "clone_url": "https://github.com/driaialchemy/tmp-scratch.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": False,
            "fork": False,
            "disabled": False,
            "is_template": False,
            "pushed_at": "2025-06-01T00:00:00Z",
        },
        {
            "name": "template-starter",
            "full_name": "driaialchemy/template-starter",
            "clone_url": "https://github.com/driaialchemy/template-starter.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": False,
            "fork": False,
            "disabled": False,
            "is_template": True,
            "pushed_at": "2025-06-01T00:00:00Z",
        },
    ]


def _discovered_from_api() -> list[DiscoveredRepo]:
    return [
        DiscoveredRepo(
            name=item["name"],
            full_name=item["full_name"],
            clone_url=item["clone_url"],
            default_branch=item["default_branch"],
            visibility=item["visibility"],
            archived=item["archived"],
            fork=item["fork"],
            disabled=item["disabled"],
            is_template=item["is_template"],
            last_pushed=item["pushed_at"],
        )
        for item in _sample_api_page()
    ]


def test_discover_github_repos_pagination():
    base = _sample_api_page()[0]
    page1 = [base] + [
        {
            "name": f"pad-{i}",
            "full_name": f"driaialchemy/pad-{i}",
            "clone_url": f"https://github.com/driaialchemy/pad-{i}.git",
            "default_branch": "main",
            "visibility": "public",
            "private": False,
            "archived": False,
            "fork": False,
            "disabled": False,
            "is_template": False,
            "pushed_at": "2026-06-01T00:00:00Z",
        }
        for i in range(99)
    ]
    page2 = [_sample_api_page()[0] | {"name": "extra-repo", "full_name": "driaialchemy/extra-repo"}]

    call_count = {"n": 0}

    def fake_request_json(url, token=None):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return page1
        return page2

    with patch("repo_governor.repo_discovery._request_json", side_effect=fake_request_json):
        repos, _ = discover_github_repos("driaialchemy", token="test-token")

    assert call_count["n"] == 2
    assert any(r.name == "extra-repo" for r in repos)


def test_discover_github_repos_warns_without_token():
    with patch("repo_governor.repo_discovery._request_json", return_value=[]):
        with patch("repo_governor.repo_discovery.resolve_github_token", return_value=(None, None)):
            _, warnings = discover_github_repos("driaialchemy", token=None)
    assert any("token" in w.lower() for w in warnings)


def _discovery_config() -> dict:
    return {
        "include_archived": False,
        "include_forks": False,
        "include_templates": False,
        "include_private": True,
        "default_mode": "scan_only",
        "exclude_repos": ["test-temp-repo"],
        "exclude_patterns": ["tmp-*", "*-archive"],
        "include_repos": [],
        "repo_overrides": {
            "AIAlchemy-Repo-Governor": {"mode": "scan_only", "enabled": True},
        },
    }


def test_filter_archived_repos():
    config = _discovery_config()
    included, skipped = filter_discovered_repos(_discovered_from_api(), config)
    skipped_names = {s.name for s in skipped}
    assert "archived-example" in skipped_names
    assert any(s.skip_reason == "archived" for s in skipped if s.name == "archived-example")


def test_filter_forks():
    config = _discovery_config()
    _, skipped = filter_discovered_repos(_discovered_from_api(), config)
    assert any(s.name == "forked-tool" and s.skip_reason == "fork" for s in skipped)


def test_filter_templates():
    config = _discovery_config()
    _, skipped = filter_discovered_repos(_discovered_from_api(), config)
    assert any(s.name == "template-starter" for s in skipped)


def test_exclude_repos():
    config = _discovery_config()
    config["exclude_repos"] = ["AIAlchemy-Repo-Governor"]
    included, skipped = filter_discovered_repos(_discovered_from_api(), config)
    assert not any(r.name == "AIAlchemy-Repo-Governor" for r in included)
    assert any(s.name == "AIAlchemy-Repo-Governor" for s in skipped)


def test_exclude_patterns():
    config = _discovery_config()
    _, skipped = filter_discovered_repos(_discovered_from_api(), config)
    assert any(s.name == "tmp-scratch" for s in skipped)


def test_repo_overrides_mode(tmp_path):
    config = {
        "default_mode": "scan_only",
        "include_archived": False,
        "include_forks": False,
        "include_templates": False,
        "include_private": True,
        "exclude_repos": [],
        "exclude_patterns": [],
        "include_repos": [],
        "repo_overrides": {
            "AIAlchemy-Repo-Governor": {"mode": "scan_only", "enabled": True},
        },
    }
    discovered = [d for d in _discovered_from_api() if d.name == "AIAlchemy-Repo-Governor"]
    enabled, _ = build_effective_repo_registry(discovered, config)
    assert enabled[0].mode == "scan_only"


def test_write_and_load_generated_registry(tmp_path):
    from repo_governor.repo_discovery import RegistryRepo

    repos = [
        RegistryRepo(
            name="demo",
            full_name="driaialchemy/demo",
            url="https://github.com/driaialchemy/demo.git",
            branch="main",
            enabled=True,
            mode="scan_only",
            visibility="public",
        )
    ]
    path = write_generated_repo_registry(repos, tmp_path / "repos.generated.yml")
    loaded = load_generated_repo_registry(path)
    assert loaded[0].name == "demo"
    assert loaded[0].mode == "scan_only"


def test_invalid_mode_rejected():
    config = {
        "default_mode": "invalid_mode",
        "include_archived": False,
        "include_forks": False,
        "include_templates": False,
        "exclude_repos": [],
        "exclude_patterns": [],
    }
    with pytest.raises(ValueError, match="Invalid default_mode"):
        filter_discovered_repos([], config)
