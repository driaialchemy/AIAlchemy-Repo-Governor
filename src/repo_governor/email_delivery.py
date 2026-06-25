"""SMTP email delivery for evidence reports."""
from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass
from datetime import date
from email.message import EmailMessage
from pathlib import Path
from typing import Literal

from .security import redact_secrets

EmailDeliveryStatus = Literal[
    "sent",
    "skipped_missing_credentials",
    "failed",
]


@dataclass
class EmailConfig:
    to_address: str
    from_address: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    use_tls: bool = True


@dataclass
class EmailDeliveryResult:
    status: EmailDeliveryStatus
    message: str
    missing_variables: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.missing_variables is None:
            self.missing_variables = []


REQUIRED_EMAIL_VARS = [
    "REPORT_EMAIL_FROM",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
]

OPTIONAL_EMAIL_VARS = ["SMTP_USE_TLS", "REPORT_EMAIL_TO"]

GITHUB_SECRETS_HELP = [
    "REPORT_EMAIL_FROM",
    "REPORT_EMAIL_TO",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_USE_TLS",
    "REPO_GOVERNOR_PAT (optional, for private repo discovery)",
]


def default_recipient() -> str:
    return os.environ.get("REPORT_EMAIL_TO", "draialchemy@gmail.com")


def missing_email_env_vars() -> list[str]:
    missing = [var for var in REQUIRED_EMAIL_VARS if not os.environ.get(var)]
    if not os.environ.get("REPORT_EMAIL_TO"):
        pass
    return missing


def load_email_config() -> EmailConfig | None:
    missing = missing_email_env_vars()
    if missing:
        return None
    use_tls_raw = os.environ.get("SMTP_USE_TLS", "true").strip().lower()
    use_tls = use_tls_raw in ("1", "true", "yes", "on")
    return EmailConfig(
        to_address=default_recipient(),
        from_address=os.environ["REPORT_EMAIL_FROM"],
        smtp_host=os.environ["SMTP_HOST"],
        smtp_port=int(os.environ["SMTP_PORT"]),
        smtp_username=os.environ["SMTP_USERNAME"],
        smtp_password=os.environ["SMTP_PASSWORD"],
        use_tls=use_tls,
    )


def send_evidence_email(
    *,
    report_date: date,
    text_path: Path,
    markdown_path: Path | None = None,
    json_path: Path | None = None,
    run_summary_path: Path | None = None,
    config: EmailConfig | None = None,
) -> EmailDeliveryResult:
    """Send the evidence report email with attachments."""
    cfg = config or load_email_config()
    if cfg is None:
        missing = missing_email_env_vars()
        return EmailDeliveryResult(
            status="skipped_missing_credentials",
            message=(
                "Email not sent — missing SMTP credentials. "
                f"Configure GitHub Actions secrets: {', '.join(GITHUB_SECRETS_HELP)}"
            ),
            missing_variables=missing,
        )

    if not text_path.exists():
        return EmailDeliveryResult(
            status="failed",
            message=f"Plain-text report not found: {text_path}",
        )

    subject = f"AIAlchemy Repo Governor Weekly Evidence Report - {report_date.isoformat()}"
    body = text_path.read_text(encoding="utf-8")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg.from_address
    msg["To"] = cfg.to_address
    msg.set_content(body)

    attachments: list[tuple[Path, str]] = [(text_path, "text/plain")]
    if markdown_path and markdown_path.exists():
        attachments.append((markdown_path, "text/markdown"))
    if json_path and json_path.exists():
        attachments.append((json_path, "application/json"))
    if run_summary_path and run_summary_path.exists():
        attachments.append((run_summary_path, "application/json"))

    for path, mime in attachments:
        maintype, subtype = mime.split("/", 1)
        msg.add_attachment(
            path.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=path.name,
        )

    try:
        with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port, timeout=60) as server:
            if cfg.use_tls:
                server.starttls()
            server.login(cfg.smtp_username, cfg.smtp_password)
            server.send_message(msg)
    except Exception as exc:
        return EmailDeliveryResult(
            status="failed",
            message=redact_secrets(f"Email delivery failed: {exc}"),
        )

    return EmailDeliveryResult(
        status="sent",
        message=f"Evidence report emailed to {cfg.to_address}",
    )
