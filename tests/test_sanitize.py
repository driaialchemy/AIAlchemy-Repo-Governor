"""Tests for secret redaction in error messages."""
from repo_governor.multi_repo_runner import _sanitize_message


def test_sanitize_message_redacts_token():
    token = "github_pat_secret_value"
    msg = f"git clone https://x-access-token:{token}@github.com/org/repo.git failed"
    sanitized = _sanitize_message(msg, token)
    assert token not in sanitized
    assert "***REDACTED***" in sanitized
