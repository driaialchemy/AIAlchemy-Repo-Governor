"""Repository scanner — discovers and inspects repos under a root path."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


SENSITIVE_FILENAMES = frozenset({
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".env.staging",
    "secrets.json",
    "credentials.json",
    "private_key.pem",
    "id_rsa",
    "id_ed25519",
    "id_dsa",
    ".netrc",
    "token.json",
})

# Directories to skip when walking — never descend into these
SKIP_DIRS = frozenset({
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
})

ARTIFACT_EXTENSIONS = frozenset({
    ".db", ".sqlite", ".sqlite3",
    ".xlsx", ".xls",
    ".csv",
    ".log",
})

# Terms scanned in safe text files to detect external API/operational usage
API_TERMS = frozenset({
    "openai",
    "anthropic",
    "gemini",
    "google.generativeai",
    "requests",
    "httpx",
    "aiohttp",
    "api_key",
    "database_url",
    "postgres",
    "sqlite",
    "supabase",
    "cloudflare",
})

# Only scan files with these extensions for API terms; never scan binaries or secrets
SAFE_SCAN_EXTENSIONS = frozenset({
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".go", ".rs", ".java", ".cs", ".cpp", ".c",
    ".rb", ".php", ".sh", ".ps1",
    ".sql", ".tf",
    ".toml", ".yaml", ".yml", ".json",
    ".txt", ".md", ".rst",
    ".html", ".css",
    ".ini", ".cfg",
})

LANGUAGE_EXTENSIONS: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JavaScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".sh": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".tf": "Terraform",
    ".r": "R",
    ".scala": "Scala",
}

MAX_SCAN_BYTES = 1_048_576  # 1 MB — files larger than this are not content-scanned


@dataclass
class RepoInfo:
    # --- identity ---
    name: str
    path: Path
    # --- version control ---
    is_git_repo: bool
    has_gitignore: bool
    # --- documentation / policy ---
    has_readme: bool
    has_claude_md: bool
    has_agents_md: bool
    # --- Python build ---
    has_pyproject: bool
    has_requirements_txt: bool
    # --- secrets ---
    has_env_files: bool
    # --- fields with defaults (must follow non-default fields) ---
    env_file_paths: list[str] = field(default_factory=list)
    file_count: int = 0
    languages: list[str] = field(default_factory=list)
    last_modified: datetime = field(default_factory=datetime.now)
    # --- environment files ---
    has_env_example: bool = False
    # --- project structure ---
    has_tests_dir: bool = False
    # --- Node.js / frontend ---
    has_package_json: bool = False
    # --- containerisation ---
    has_dockerfile: bool = False
    has_docker_compose: bool = False
    # --- CI/CD ---
    has_github_workflows: bool = False
    # --- deployment configs ---
    has_wrangler_toml: bool = False
    has_vercel_json: bool = False
    has_netlify_toml: bool = False
    has_render_yaml: bool = False
    # --- generated / dependency artefacts (directories) ---
    has_venv: bool = False
    has_pycache: bool = False
    has_node_modules: bool = False
    has_dist_dir: bool = False
    has_build_dir: bool = False
    # --- generated files ---
    artifact_paths: list[str] = field(default_factory=list)
    # --- API / operational usage ---
    api_terms_found: list[str] = field(default_factory=list)


def _walk_repo(root: Path) -> tuple[list[Path], set[str]]:
    """Walk *root* once, skipping SKIP_DIRS.

    Returns:
        files      — every regular file reachable without entering a SKIP_DIR.
        dirs_seen  — names of every directory encountered (including SKIP_DIRS),
                     used for presence detection without descending into them.
    """
    files: list[Path] = []
    dirs_seen: set[str] = set()

    def _recurse(path: Path) -> None:
        try:
            entries = list(path.iterdir())
        except (PermissionError, OSError):
            return
        for entry in entries:
            try:
                if entry.is_symlink():
                    continue
                if entry.is_dir():
                    dirs_seen.add(entry.name)
                    if entry.name not in SKIP_DIRS:
                        _recurse(entry)
                elif entry.is_file():
                    files.append(entry)
            except OSError:
                continue

    _recurse(root)
    return files, dirs_seen


def _scan_text_file(file_path: Path) -> set[str]:
    """Return the subset of API_TERMS found in *file_path*.

    Never reads secret files, binary-extension files, or files larger than
    MAX_SCAN_BYTES.  Returns an empty set on any I/O error.
    """
    if file_path.name in SENSITIVE_FILENAMES:
        return set()
    if file_path.suffix.lower() not in SAFE_SCAN_EXTENSIONS:
        return set()
    try:
        if file_path.stat().st_size > MAX_SCAN_BYTES:
            return set()
        text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return set()
    return {term for term in API_TERMS if term in text}


def scan_repo(repo_path: Path) -> RepoInfo:
    """Scan a single directory and return its RepoInfo."""
    repo_path = repo_path.resolve()

    files, dirs_seen = _walk_repo(repo_path)

    env_files: list[str] = []
    artifact_paths: list[str] = []
    api_terms: set[str] = set()
    lang_counts: dict[str, int] = {}

    try:
        latest_mtime = repo_path.stat().st_mtime
    except OSError:
        latest_mtime = 0.0

    for file_path in files:
        rel = file_path.relative_to(repo_path).as_posix()

        try:
            mtime = file_path.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime
        except OSError:
            pass

        if file_path.name in SENSITIVE_FILENAMES:
            env_files.append(rel)

        suffix = file_path.suffix.lower()

        if suffix in ARTIFACT_EXTENSIONS:
            artifact_paths.append(rel)

        lang = LANGUAGE_EXTENSIONS.get(suffix)
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        api_terms |= _scan_text_file(file_path)

    return RepoInfo(
        name=repo_path.name,
        path=repo_path,
        is_git_repo=(repo_path / ".git").exists(),
        has_gitignore=(repo_path / ".gitignore").exists(),
        has_readme=any(
            (repo_path / n).exists()
            for n in ("README.md", "README.rst", "README.txt", "README")
        ),
        has_claude_md=(repo_path / "CLAUDE.md").exists(),
        has_agents_md=(repo_path / "AGENTS.md").exists(),
        has_pyproject=(repo_path / "pyproject.toml").exists(),
        has_requirements_txt=(repo_path / "requirements.txt").exists(),
        has_env_files=bool(env_files),
        env_file_paths=sorted(env_files),
        file_count=len(files),
        languages=[lang for lang, _ in sorted(lang_counts.items(), key=lambda x: -x[1])],
        last_modified=datetime.fromtimestamp(latest_mtime),
        has_env_example=any(
            (repo_path / n).exists()
            for n in (".env.example", ".env.sample", ".env.template")
        ),
        has_tests_dir=(repo_path / "tests").is_dir(),
        has_package_json=(repo_path / "package.json").exists(),
        has_dockerfile=(repo_path / "Dockerfile").exists(),
        has_docker_compose=any(
            (repo_path / n).exists()
            for n in ("docker-compose.yml", "docker-compose.yaml")
        ),
        has_github_workflows=(repo_path / ".github" / "workflows").is_dir(),
        has_wrangler_toml=(repo_path / "wrangler.toml").exists(),
        has_vercel_json=(repo_path / "vercel.json").exists(),
        has_netlify_toml=(repo_path / "netlify.toml").exists(),
        has_render_yaml=(repo_path / "render.yaml").exists(),
        has_venv=any(d in dirs_seen for d in (".venv", "venv", "env")),
        has_pycache="__pycache__" in dirs_seen,
        has_node_modules="node_modules" in dirs_seen,
        has_dist_dir="dist" in dirs_seen,
        has_build_dir="build" in dirs_seen,
        artifact_paths=sorted(artifact_paths),
        api_terms_found=sorted(api_terms),
    )


def scan_root(root_path: Path) -> list[RepoInfo]:
    """Scan all immediate subdirectories of root_path as potential repos."""
    root_path = root_path.resolve()
    if not root_path.is_dir():
        raise ValueError(f"Not a directory: {root_path}")
    return [scan_repo(entry) for entry in sorted(root_path.iterdir()) if entry.is_dir()]
