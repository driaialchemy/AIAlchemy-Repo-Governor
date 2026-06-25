"""Tests for repo_governor.email_delivery."""
import os
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

from repo_governor.email_delivery import (
    EmailConfig,
    load_email_config,
    missing_email_env_vars,
    send_evidence_email,
)


def test_missing_email_env_vars():
    with patch.dict(os.environ, {}, clear=True):
        missing = missing_email_env_vars()
    assert "REPORT_EMAIL_FROM" in missing
    assert "SMTP_HOST" in missing
    assert "SMTP_PASSWORD" in missing


def test_load_email_config_returns_none_when_missing():
    with patch.dict(os.environ, {}, clear=True):
        assert load_email_config() is None


def test_load_email_config_success():
    env = {
        "REPORT_EMAIL_FROM": "sender@example.com",
        "REPORT_EMAIL_TO": "draialchemy@gmail.com",
        "SMTP_HOST": "smtp.example.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "user",
        "SMTP_PASSWORD": "secret",
        "SMTP_USE_TLS": "true",
    }
    with patch.dict(os.environ, env, clear=True):
        cfg = load_email_config()
    assert cfg is not None
    assert cfg.to_address == "draialchemy@gmail.com"
    assert cfg.use_tls is True


def test_send_email_skipped_missing_credentials(tmp_path):
    text = tmp_path / "evidence-summary.txt"
    text.write_text("summary", encoding="utf-8")
    with patch.dict(os.environ, {}, clear=True):
        result = send_evidence_email(
            report_date=date.today(),
            text_path=text,
        )
    assert result.status == "skipped_missing_credentials"
    assert result.missing_variables


def test_send_email_with_mocked_smtp(tmp_path):
    text = tmp_path / "evidence-summary.txt"
    text.write_text("Weekly report body", encoding="utf-8")
    md = tmp_path / "evidence-summary.md"
    md.write_text("# Report", encoding="utf-8")

    cfg = EmailConfig(
        to_address="draialchemy@gmail.com",
        from_address="sender@example.com",
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_username="user",
        smtp_password="secret",
        use_tls=True,
    )

    mock_server = MagicMock()
    mock_server.__enter__ = MagicMock(return_value=mock_server)
    mock_server.__exit__ = MagicMock(return_value=False)
    with patch("repo_governor.email_delivery.smtplib.SMTP", return_value=mock_server):
        result = send_evidence_email(
            report_date=date(2026, 6, 25),
            text_path=text,
            markdown_path=md,
            config=cfg,
        )

    assert result.status == "sent"
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("user", "secret")
    mock_server.send_message.assert_called_once()
