"""Secret redaction utilities for audit logs, reports, and error messages."""
from __future__ import annotations

import os
import re

_SECRET_ENV_VARS = (
    "REPO_GOVERNOR_PAT",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "SMTP_PASSWORD",
    "SMTP_USERNAME",
)

_TOKEN_LIKE_PATTERNS = (
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"ghp_[A-Za-z0-9]+"),
    re.compile(r"gho_[A-Za-z0-9]+"),
    re.compile(r"ghu_[A-Za-z0-9]+"),
    re.compile(r"ghs_[A-Za-z0-9]+"),
    re.compile(r"ghr_[A-Za-z0-9]+"),
)

_EMBEDDED_CREDENTIAL_URL = re.compile(
    r"https://(?:x-access-token:|[^/@\s]+@)[^@\s]+@",
    re.IGNORECASE,
)


def is_valid_github_token(token: str | None) -> bool:
    """Return True when a token looks usable (no whitespace, reasonable length)."""
    if not token:
        return False
    cleaned = token.strip()
    if not cleaned or any(ch.isspace() for ch in cleaned):
        return False
    if cleaned.lower().startswith("bearer "):
        cleaned = cleaned[7:].strip()
    return len(cleaned) >= 20


def resolve_github_token() -> tuple[str | None, str | None]:
    """Return (token, warning) preferring REPO_GOVERNOR_PAT over GITHUB_TOKEN/GH_TOKEN."""
    for env_var in ("REPO_GOVERNOR_PAT", "GITHUB_TOKEN", "GH_TOKEN"):
        raw = os.environ.get(env_var)
        if not raw:
            continue
        cleaned = raw.strip()
        if cleaned.lower().startswith("bearer "):
            cleaned = cleaned[7:].strip()
        if is_valid_github_token(cleaned):
            return cleaned, None
        return None, "GitHub token is missing or malformed."
    return None, None


def redact_secrets(message: str, extra_values: list[str] | None = None) -> str:
    """Redact secrets, token-like strings, and credential URLs from text."""
    if not message:
        return message

    redacted = message
    for env_var in _SECRET_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            redacted = redacted.replace(value, "***REDACTED***")

    if extra_values:
        for value in extra_values:
            if value:
                redacted = redacted.replace(value, "***REDACTED***")

    redacted = _EMBEDDED_CREDENTIAL_URL.sub("https://***REDACTED***@", redacted)
    redacted = re.sub(
        r"x-access-token:[^@\s]+@",
        "x-access-token:***REDACTED***@",
        redacted,
        flags=re.IGNORECASE,
    )

    for pattern in _TOKEN_LIKE_PATTERNS:
        redacted = pattern.sub("***REDACTED***", redacted)

    return redacted


def redact_dict(data: object) -> object:
    """Recursively redact secrets from dict/list structures."""
    if isinstance(data, dict):
        return {key: redact_dict(value) for key, value in data.items()}
    if isinstance(data, list):
        return [redact_dict(item) for item in data]
    if isinstance(data, str):
        return redact_secrets(data)
    return data
