"""Tests for governance_status three-state evaluation."""
from pathlib import Path

from repo_governor.classifier import classify_all, classify_repo
from repo_governor.governance_status import (
    NOT_PRESENT,
    PRESENT_ACTIVE,
    PRESENT_INERT,
    discover_confidence_feeders,
    evaluate_governance_status,
)
from repo_governor.scanner import scan_repo


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_missing_repo_is_all_not_present(tmp_path):
    status = evaluate_governance_status(tmp_path / "does-not-exist")
    assert status == {
        "P1": NOT_PRESENT,
        "P2": NOT_PRESENT,
        "P3": NOT_PRESENT,
        "P4": NOT_PRESENT,
        "uncertainty_monitoring": NOT_PRESENT,
    }


def test_p1_inert_type_only_consumer(tmp_path):
    _write(
        tmp_path / "types.ts",
        "export type PolicyMatched = string;\n"
        "reasoning_path?: string[] | null;\n"
        "policy_matched?: string | null;\n"
        "confidence?: number | null;\n",
    )
    assert evaluate_governance_status(tmp_path)["P1"] == PRESENT_INERT


def test_p1_active_canonical_string_writer(tmp_path):
    _write(
        tmp_path / "types.ts",
        "export type PolicyMatched = string;\n"
        "reasoning_path?: string[] | null;\n"
        "policy_matched?: string | null;\n"
        "confidence?: number | null;\n"
        "export function buildWebhookPayload(activity) { return activity; }\n",
    )
    assert evaluate_governance_status(tmp_path)["P1"] == PRESENT_ACTIVE


def test_p1_inert_object_shape_regression(tmp_path):
    _write(
        tmp_path / "types.ts",
        "export type PolicyMatched = { id: string; name: string };\n"
        "reasoning_path?: string[];\n"
        "policy_matched?: { id: string; name: string };\n"
        "confidence?: number | null;\n",
    )
    assert evaluate_governance_status(tmp_path)["P1"] == PRESENT_INERT


def test_p1_active_string_write_without_type_alias(tmp_path):
    _write(
        tmp_path / "audit_logger.py",
        "reasoning_path = extra.pop('reasoning_path', None)\n"
        "policy_matched = extra.pop('policy_matched', None)\n"
        "confidence = extra.pop('confidence', None)\n"
        "if policy_matched is None and policy_decision:\n"
        "    policy_matched = policy_decision\n"
        'event["policy_matched"] = policy_matched\n',
    )
    assert evaluate_governance_status(tmp_path)["P1"] == PRESENT_ACTIVE


def test_p1_historical_object_read_does_not_regress_string_writer(tmp_path):
    _write(
        tmp_path / "state.py",
        "policy_matched: Optional[str] = None\n"
        "reasoning_path = []\n"
        "confidence = 0.1\n"
        '"policy_matched": clause_type,\n',
    )
    _write(
        tmp_path / "engine.py",
        '"""Accept historical {id, name} policy_matched on read; new writes are id strings."""\n'
        "matched = raw_flag.get('policy_matched')\n",
    )
    assert evaluate_governance_status(tmp_path)["P1"] == PRESENT_ACTIVE


def test_p2_does_not_credit_gap_letter(tmp_path):
    _write(
        tmp_path / "TRUST.md",
        "# TRUST\n\n"
        "## T — Traceability\n\nCited in `audit.py`.\n\n"
        "## T — Testing-via-simulation\n\nGap — not yet implemented.\n",
    )
    assert evaluate_governance_status(tmp_path)["P2"] == PRESENT_ACTIVE


def test_p2_inert_when_all_letters_are_gaps(tmp_path):
    _write(
        tmp_path / "TRUST.md",
        "## T — Traceability\n\nGap — not yet implemented.\n\n"
        "## R — Runtime-guardrails\n\nGap — not yet implemented.\n",
    )
    assert evaluate_governance_status(tmp_path)["P2"] == PRESENT_INERT


def test_p3_active_requires_human_route(tmp_path):
    _write(
        tmp_path / "app.py",
        "AUTO_CLEAR_RISK_THRESHOLD = 4.0\n"
        "if should_auto_clear(risk):\n"
        "    result = auto_clear_decision(risk)\n"
        "else:\n"
        "    result = synthesize(risk)\n",
    )
    assert evaluate_governance_status(tmp_path)["P3"] == PRESENT_ACTIVE


def test_p3_inert_auto_clear_without_human_route(tmp_path):
    _write(tmp_path / "app.py", "AUTO_CLEAR_RISK_THRESHOLD = 4.0\nshould_auto_clear = True\n")
    assert evaluate_governance_status(tmp_path)["P3"] == PRESENT_INERT


def test_p4_inert_when_endpoints_exist_but_axes_unpopulated(tmp_path):
    _write(
        tmp_path / "server.ts",
        'app.get("/decision-inventory", handler);\n'
        'app.patch("/versions/:versionId/taxonomy", handler);\n'
        "function updateVersionTaxonomy() {}\n",
    )
    _write(
        tmp_path / "registry.ts",
        "risk?: string | null;\ncomplexity?: string | null;\n"
        "regulatory_impact?: string | null;\nbusiness_importance?: string | null;\n",
    )
    assert evaluate_governance_status(tmp_path)["P4"] == PRESENT_INERT


def test_p4_active_when_axes_populated(tmp_path):
    _write(
        tmp_path / "server.ts",
        'app.get("/decision-inventory", handler);\n'
        'app.patch("/versions/:versionId/taxonomy", handler);\n'
        "function updateVersionTaxonomy() {}\n",
    )
    _write(tmp_path / "registry.ts", 'complexity: "HIGH",\nregulatory_impact: "MEDIUM",\n')
    assert evaluate_governance_status(tmp_path)["P4"] == PRESENT_ACTIVE


def test_uncertainty_single_source_is_inert(tmp_path):
    monitor = tmp_path / "gov"
    feeder = tmp_path / "review"
    monitor.mkdir()
    feeder.mkdir()
    _write(monitor / "server.ts", 'app.get("/uncertainty-flags", handler);\n')
    _write(
        feeder / "app.py",
        "from governance_logger import require_approval\n"
        "require_approval('x', 'done', {}, confidence=final_result.get('confidence'))\n",
    )
    feeders = discover_confidence_feeders([monitor, feeder])
    assert feeders == ["review"]
    assert (
        evaluate_governance_status(monitor, confidence_feeders=feeders)["uncertainty_monitoring"]
        == PRESENT_INERT
    )


def test_uncertainty_two_feeders_is_active(tmp_path):
    monitor = tmp_path / "gov"
    a = tmp_path / "a"
    b = tmp_path / "b"
    for path in (monitor, a, b):
        path.mkdir()
    _write(monitor / "server.ts", 'app.get("/uncertainty-flags", handler);\n')
    for feeder in (a, b):
        _write(
            feeder / "app.py",
            "require_approval('x', 'done', {}, confidence=result.get('confidence'))\n",
        )
    feeders = discover_confidence_feeders([monitor, a, b])
    assert (
        evaluate_governance_status(monitor, confidence_feeders=feeders)["uncertainty_monitoring"]
        == PRESENT_ACTIVE
    )


def test_governance_status_does_not_change_pass_gates(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    (tmp_path / "CLAUDE.md").write_text("# policy\n")
    (tmp_path / "AGENTS.md").write_text("# agents\n")
    (tmp_path / "README.md").write_text("# readme\n")
    _write(tmp_path / "app.py", "AUTO_CLEAR_RISK_THRESHOLD = 1\n")
    classified = classify_repo(scan_repo(tmp_path))
    assert classified.agent_ready is True
    assert classified.blocking_issues == []
    assert classified.governance_status["P3"] == PRESENT_INERT


def test_classify_all_passes_shared_feeders(tmp_path):
    monitor = tmp_path / "govhub"
    feeder = tmp_path / "workflow"
    other = tmp_path / "plain"
    for path in (monitor, feeder, other):
        path.mkdir()
        (path / "README.md").write_text("# x\n")
    _write(monitor / "server.ts", 'app.get("/uncertainty-flags", handler);\n')
    _write(
        feeder / "app.py",
        "require_approval('x', 'done', {}, confidence=final_result.get('confidence'))\n",
    )
    results = {cr.repo.name: cr.governance_status for cr in classify_all([
        scan_repo(monitor),
        scan_repo(feeder),
        scan_repo(other),
    ])}
    assert results["govhub"]["uncertainty_monitoring"] == PRESENT_INERT
    assert results["workflow"]["uncertainty_monitoring"] == NOT_PRESENT
    assert results["plain"]["P1"] == NOT_PRESENT
