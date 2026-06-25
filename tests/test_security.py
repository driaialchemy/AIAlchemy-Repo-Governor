"""Tests for repo_governor.security redaction and token handling."""
import json
import os
from unittest.mock import patch

from repo_governor.evidence_report import generate_evidence_reports
from repo_governor.multi_repo_runner import MultiRepoRunResult, _sanitize_message
from repo_governor.security import is_valid_github_token, redact_dict, redact_secrets, resolve_github_token


def test_redact_github_pat_pattern():
    msg = "clone failed github_pat_11ABCDEF01234567890"
    redacted = redact_secrets(msg)
    assert "github_pat_" not in redacted
    assert "***REDACTED***" in redacted


def test_redact_embedded_credential_url():
    msg = "https://x-access-token:secretvalue@github.com/org/repo.git"
    redacted = redact_secrets(msg)
    assert "secretvalue" not in redacted


def test_redact_env_var_values():
    with patch.dict(os.environ, {"SMTP_PASSWORD": "super-secret"}, clear=False):
        redacted = redact_secrets("failed login super-secret")
    assert "super-secret" not in redacted


def test_malformed_token_detected():
    assert is_valid_github_token("bad token with spaces") is False
    token, warning = resolve_github_token()
    with patch.dict(os.environ, {"GITHUB_TOKEN": "bad token"}, clear=True):
        token, warning = resolve_github_token()
    assert token is None
    assert warning == "GitHub token is missing or malformed."


def test_valid_token_accepted():
    valid = "g" + "h" + "p_" + "A" * 36
    with patch.dict(os.environ, {"GITHUB_TOKEN": valid}, clear=True):
        token, warning = resolve_github_token()
    assert token == valid
    assert warning is None


def test_redact_dict_recursive():
    data = {"errors": ["failed https://x-access-token:abc@github.com/x"]}
    redacted = redact_dict(data)
    assert "abc" not in json.dumps(redacted)


def test_sanitize_message_uses_security_module():
    token = "github_pat_secret_value"
    msg = f"git clone https://x-access-token:{token}@github.com/org/repo.git failed"
    sanitized = _sanitize_message(msg, token)
    assert token not in sanitized


def test_corrective_actions_in_evidence_report(tmp_path):
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
                "status": "scanned",
                "passed": False,
                "risk_level": "HIGH",
                "remaining_issues": ["Missing CLAUDE.md."],
                "recommended_action": "Add CLAUDE.md",
                "audit_path": "/audit/demo.json",
                "initial_scan": {},
                "mode": "scan_only",
            }
        ],
    )
    paths = generate_evidence_reports(run, output_root=tmp_path / "reports")
    md = paths.markdown_path.read_text(encoding="utf-8")
    txt = paths.text_path.read_text(encoding="utf-8")
    data = json.loads(paths.json_path.read_text(encoding="utf-8"))
    assert "Corrective and Verifiable Actions" in md
    assert "Corrective and Verifiable Actions" in txt
    assert data["corrective_actions"]
    assert "github_pat" not in md
