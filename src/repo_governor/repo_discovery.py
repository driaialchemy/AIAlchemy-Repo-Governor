"""GitHub repository discovery and effective registry management."""
from __future__ import annotations

import fnmatch
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALID_MODES = frozenset({"scan_only", "prompt_only", "goal_loop"})

DEFAULT_DISCOVERY_CONFIG = Path("config/repo-discovery.yml")
DEFAULT_GENERATED_REGISTRY = Path("config/repos.generated.yml")
DEFAULT_MANUAL_REGISTRY = Path("config/repos.yml")


@dataclass
class DiscoveredRepo:
    name: str
    full_name: str
    clone_url: str
    default_branch: str
    visibility: str
    archived: bool
    fork: bool
    disabled: bool = False
    is_template: bool = False
    last_pushed: str | None = None
    discovery_source: str = "github_api"
    discovery_timestamp: str = field(default_factory=lambda: _utc_now_iso())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RegistryRepo:
    name: str
    full_name: str
    url: str
    branch: str
    enabled: bool = True
    mode: str = "scan_only"
    visibility: str = "unknown"
    archived: bool = False
    fork: bool = False
    skip_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if data["skip_reason"] is None:
            del data["skip_reason"]
        return data


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _github_token() -> str | None:
    return os.environ.get("REPO_GOVERNOR_PAT") or os.environ.get("GITHUB_TOKEN")


def _request_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AIAlchemy-Repo-Governor",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def discover_github_repos(
    owner: str,
    *,
    token: str | None = None,
) -> tuple[list[DiscoveredRepo], list[str]]:
    """Discover all repositories for a GitHub owner with pagination.

    Returns (repos, warnings).
    """
    token = token if token is not None else _github_token()
    warnings: list[str] = []
    if not token:
        warnings.append(
            "No REPO_GOVERNOR_PAT or GITHUB_TOKEN set — only public repositories "
            "will be discovered. Private repos require a token."
        )

    discovered: list[DiscoveredRepo] = []
    page = 1
    discovery_ts = _utc_now_iso()

    while True:
        params = urllib.parse.urlencode({
            "per_page": "100",
            "page": str(page),
            "type": "owner",
        })
        url = f"https://api.github.com/users/{owner}/repos?{params}"
        try:
            payload = _request_json(url, token=token)
        except urllib.error.HTTPError as exc:
            if exc.code == 401 and token:
                warnings.append(
                    "GitHub token was rejected — falling back to unauthenticated "
                    "public repository discovery."
                )
                token = None
                payload = _request_json(url, token=None)
            elif exc.code == 404:
                raise ValueError(f"GitHub owner not found: {owner}") from exc
            elif exc.code == 401:
                raise ValueError("GitHub authentication failed — check your token.") from exc
            else:
                raise ValueError(f"GitHub API error {exc.code}: {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise ValueError(f"GitHub API request failed: {exc.reason}") from exc

        if not payload:
            break

        for item in payload:
            visibility = item.get("visibility") or ("private" if item.get("private") else "public")
            discovered.append(
                DiscoveredRepo(
                    name=item["name"],
                    full_name=item["full_name"],
                    clone_url=item["clone_url"],
                    default_branch=item.get("default_branch") or "main",
                    visibility=visibility,
                    archived=bool(item.get("archived")),
                    fork=bool(item.get("fork")),
                    disabled=bool(item.get("disabled", False)),
                    is_template=bool(item.get("is_template", False)),
                    last_pushed=item.get("pushed_at"),
                    discovery_source="github_api",
                    discovery_timestamp=discovery_ts,
                )
            )

        if len(payload) < 100:
            break
        page += 1

    return discovered, warnings


def load_repo_discovery_config(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or DEFAULT_DISCOVERY_CONFIG
    if not path.exists():
        return {
            "github_owner": "driaialchemy",
            "include_private": True,
            "include_archived": False,
            "include_forks": False,
            "include_templates": False,
            "default_mode": "scan_only",
            "exclude_repos": [],
            "exclude_patterns": [],
            "include_repos": [],
            "repo_overrides": {},
        }
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _matches_exclude_pattern(name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def filter_discovered_repos(
    repos: list[DiscoveredRepo],
    config: dict[str, Any],
) -> tuple[list[DiscoveredRepo], list[RegistryRepo]]:
    """Apply inclusion/exclusion rules. Returns (included, skipped)."""
    include_archived = bool(config.get("include_archived", False))
    include_forks = bool(config.get("include_forks", False))
    include_templates = bool(config.get("include_templates", False))
    include_private = bool(config.get("include_private", True))
    exclude_repos = set(config.get("exclude_repos") or [])
    exclude_patterns = list(config.get("exclude_patterns") or [])
    include_repos = set(config.get("include_repos") or [])
    default_mode = config.get("default_mode", "scan_only")
    if default_mode not in VALID_MODES:
        raise ValueError(f"Invalid default_mode: {default_mode}")

    repo_overrides: dict[str, Any] = config.get("repo_overrides") or {}

    included: list[DiscoveredRepo] = []
    skipped: list[RegistryRepo] = []

    for repo in repos:
        override = repo_overrides.get(repo.name, {})
        if override.get("enabled") is False:
            skipped.append(_to_registry(repo, default_mode, skip_reason="disabled by repo_overrides"))
            continue

        if repo.name in exclude_repos:
            skipped.append(_to_registry(repo, default_mode, skip_reason="listed in exclude_repos"))
            continue

        if _matches_exclude_pattern(repo.name, exclude_patterns):
            skipped.append(_to_registry(repo, default_mode, skip_reason="matched exclude_patterns"))
            continue

        if repo.archived and not include_archived and repo.name not in include_repos:
            skipped.append(_to_registry(repo, default_mode, skip_reason="archived"))
            continue

        if repo.disabled:
            skipped.append(_to_registry(repo, default_mode, skip_reason="disabled on GitHub"))
            continue

        if repo.fork and not include_forks and repo.name not in include_repos:
            skipped.append(_to_registry(repo, default_mode, skip_reason="fork"))
            continue

        if repo.is_template and not include_templates and repo.name not in include_repos:
            skipped.append(_to_registry(repo, default_mode, skip_reason="template repository"))
            continue

        if repo.visibility == "private" and not include_private and not _github_token():
            skipped.append(
                _to_registry(
                    repo,
                    default_mode,
                    skip_reason="private repo but no token available",
                )
            )
            continue

        included.append(repo)

    return included, skipped


def _to_registry(
    repo: DiscoveredRepo,
    default_mode: str,
    *,
    enabled: bool = False,
    skip_reason: str | None = None,
) -> RegistryRepo:
    return RegistryRepo(
        name=repo.name,
        full_name=repo.full_name,
        url=repo.clone_url,
        branch=repo.default_branch,
        enabled=enabled,
        mode=default_mode,
        visibility=repo.visibility,
        archived=repo.archived,
        fork=repo.fork,
        skip_reason=skip_reason,
    )


def build_effective_repo_registry(
    discovered: list[DiscoveredRepo],
    config: dict[str, Any],
    manual_registry: dict[str, Any] | None = None,
) -> tuple[list[RegistryRepo], list[RegistryRepo]]:
    """Build enabled and skipped registry entries from discovery + config."""
    default_mode = config.get("default_mode", "scan_only")
    if default_mode not in VALID_MODES:
        raise ValueError(f"Invalid default_mode: {default_mode}")

    repo_overrides: dict[str, Any] = config.get("repo_overrides") or {}
    included, skipped = filter_discovered_repos(discovered, config)

    enabled: list[RegistryRepo] = []
    for repo in included:
        override = repo_overrides.get(repo.name, {})
        mode = override.get("mode", default_mode)
        if mode not in VALID_MODES:
            raise ValueError(f"Invalid mode for {repo.name}: {mode}")
        enabled.append(
            RegistryRepo(
                name=repo.name,
                full_name=repo.full_name,
                url=repo.clone_url,
                branch=repo.default_branch,
                enabled=override.get("enabled", True),
                mode=mode,
                visibility=repo.visibility,
                archived=repo.archived,
                fork=repo.fork,
            )
        )

    if manual_registry:
        manual_by_name = {
            item["name"]: item
            for item in (manual_registry.get("repos") or [])
            if item.get("name")
        }
        for entry in enabled:
            if entry.name in manual_by_name:
                manual = manual_by_name[entry.name]
                if "enabled" in manual:
                    entry.enabled = bool(manual["enabled"])
                if manual.get("mode"):
                    mode = manual["mode"]
                    if mode not in VALID_MODES:
                        raise ValueError(f"Invalid mode for {entry.name}: {mode}")
                    entry.mode = mode
                if manual.get("branch"):
                    entry.branch = manual["branch"]
                if manual.get("url"):
                    entry.url = manual["url"]

    final_enabled = [e for e in enabled if e.enabled]
    final_skipped = list(skipped)
    for entry in enabled:
        if not entry.enabled:
            entry.skip_reason = "disabled in registry"
            final_skipped.append(entry)

    return final_enabled, final_skipped


def write_generated_repo_registry(
    repos: list[RegistryRepo],
    output_path: Path | None = None,
) -> Path:
    path = output_path or DEFAULT_GENERATED_REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": _utc_now_iso(),
        "repos": [r.to_dict() for r in repos],
    }
    path.write_text(yaml.dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def load_generated_repo_registry(path: Path | None = None) -> list[RegistryRepo]:
    registry_path = path or DEFAULT_GENERATED_REGISTRY
    if not registry_path.exists():
        return []
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    repos: list[RegistryRepo] = []
    for item in data.get("repos") or []:
        repos.append(
            RegistryRepo(
                name=item["name"],
                full_name=item.get("full_name", item["name"]),
                url=item["url"],
                branch=item.get("branch", "main"),
                enabled=bool(item.get("enabled", True)),
                mode=item.get("mode", "scan_only"),
                visibility=item.get("visibility", "unknown"),
                archived=bool(item.get("archived", False)),
                fork=bool(item.get("fork", False)),
                skip_reason=item.get("skip_reason"),
            )
        )
    return repos


def load_effective_repo_registry(
    config_path: Path | None = None,
    generated_path: Path | None = None,
    manual_path: Path | None = None,
) -> tuple[list[RegistryRepo], list[RegistryRepo], list[str]]:
    """Discover, filter, merge overrides, and write generated registry."""
    config = load_repo_discovery_config(config_path)
    owner = config.get("github_owner", "driaialchemy")

    discovered, warnings = discover_github_repos(owner)
    manual_data: dict[str, Any] = {}
    manual_file = manual_path or DEFAULT_MANUAL_REGISTRY
    if manual_file.exists():
        manual_data = yaml.safe_load(manual_file.read_text(encoding="utf-8")) or {}

    enabled, skipped = build_effective_repo_registry(discovered, config, manual_data)
    all_entries = enabled + [s for s in skipped if s.skip_reason]
    write_generated_repo_registry(all_entries, generated_path or DEFAULT_GENERATED_REGISTRY)
    return enabled, skipped, warnings
