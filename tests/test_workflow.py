"""Tests for GitHub Actions workflow configuration."""
from pathlib import Path

import yaml


WORKFLOW_PATH = Path(".github/workflows/weekly-repo-governor-evidence.yml")


def test_workflow_file_exists():
    assert WORKFLOW_PATH.exists()


def test_workflow_has_dispatch_and_schedule():
    data = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert "workflow_dispatch" in data["on"]
    assert "schedule" in data["on"]


def test_workflow_defaults_to_scan_only():
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "scan_only" in text
    assert "github.event.inputs.mode || 'scan_only'" in text


def test_workflow_includes_owner_driaialchemy():
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "driaialchemy" in text


def test_workflow_weekly_schedule_phoenix():
    data = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    schedule = data["on"]["schedule"][0]
    assert schedule["cron"] == "46 15 * * 4"
    assert schedule.get("timezone") == "America/Phoenix"


def test_workflow_send_email_flag():
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "--send-email" in text
