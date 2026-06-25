"""Combined evidence report generation for multi-repo governance runs."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .security import redact_dict, redact_secrets


@dataclass
class EvidenceReportPaths:
    markdown_path: Path
    text_path: Path
    json_path: Path
    output_dir: Path


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _missing_controls(result_item: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    scan = result_item.get("initial_scan") or {}
    if not scan.get("has_claude_md"):
        missing.append("CLAUDE.md")
    if not scan.get("has_gitignore"):
        missing.append(".gitignore")
    if not scan.get("has_readme"):
        missing.append("README")
    if not scan.get("has_agents_md"):
        missing.append("AGENTS.md")
    if scan.get("has_env_files"):
        missing.append("secret/credential file handling")
    if not scan.get("is_git_repo"):
        missing.append("version control (git)")
    return missing


def _recommended_action(result_item: dict[str, Any]) -> str:
    if result_item.get("passed"):
        return "No action required — repository is agent-ready."
    mode = result_item.get("mode", "scan_only")
    if result_item.get("risk_level") == "HIGH":
        return "Resolve HIGH-risk blocking issues before allowing any agent access."
    if not result_item.get("has_claude_md"):
        return "Add CLAUDE.md using `repo-governor policy-init` and review before committing."
    if mode == "scan_only":
        return "Review audit evidence and run prompt_only or goal_loop when ready to remediate."
    return "Review remaining issues in the audit file and apply minimal safe fixes."


def _build_corrective_actions(
    run: Any,
    scanned: list[dict[str, Any]],
    failed_status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build corrective and verifiable action items for failed or incomplete checks."""
    actions: list[dict[str, Any]] = []

    for item in scanned:
        if item.get("passed"):
            continue
        repo_name = item.get("full_name", item.get("name", "unknown"))
        for issue in item.get("remaining_issues") or ["Agent-readiness check failed"]:
            actions.append({
                "repo": repo_name,
                "issue": issue,
                "why_it_matters": (
                    "Autonomous coding agents can make unsafe changes when governance "
                    "controls are missing or risk is elevated."
                ),
                "corrective_action": item.get("recommended_action", "Review audit evidence and remediate."),
                "verification_action": (
                    "Re-run `repo-governor weekly-evidence --mode scan_only` and confirm "
                    "agent-ready PASS for this repository."
                ),
                "expected_evidence": (
                    f"Updated audit file with PASS status: {item.get('audit_path', 'n/a')}"
                ),
                "recommended_mode": "prompt_only",
                "human_review_required": item.get("risk_level") == "HIGH",
            })

    for item in failed_status:
        repo_name = item.get("full_name", item.get("name", "unknown"))
        for issue in item.get("errors") or ["Repository scan failed"]:
            actions.append({
                "repo": repo_name,
                "issue": redact_secrets(str(issue)),
                "why_it_matters": "The repository could not be assessed, leaving a governance gap.",
                "corrective_action": (
                    "Verify clone access, branch name, and repository availability; "
                    "then re-run the weekly evidence workflow."
                ),
                "verification_action": (
                    "Confirm the repo appears in the next evidence report with status scanned."
                ),
                "expected_evidence": "Per-repo audit JSON with status scanned.",
                "recommended_mode": run.mode,
                "human_review_required": True,
            })

    if run.mode == "scan_only" and actions:
        for action in actions:
            action.setdefault(
                "note",
                "Weekly scan_only mode reports findings only — target repos are not modified automatically.",
            )

    return actions


def _format_corrective_actions_md(actions: list[dict[str, Any]]) -> list[str]:
    if not actions:
        return []
    lines = ["## Corrective and Verifiable Actions", ""]
    for idx, action in enumerate(actions, start=1):
        lines += [
            f"### {idx}. {action.get('repo', 'unknown')}",
            "",
            f"- **Issue:** {action.get('issue')}",
            f"- **Why it matters:** {action.get('why_it_matters')}",
            f"- **Corrective action:** {action.get('corrective_action')}",
            f"- **Verification action:** {action.get('verification_action')}",
            f"- **Expected evidence:** {action.get('expected_evidence')}",
            f"- **Recommended mode:** {action.get('recommended_mode')}",
            f"- **Human review required:** {'Yes' if action.get('human_review_required') else 'No'}",
        ]
        if action.get("note"):
            lines.append(f"- **Note:** {action['note']}")
        lines.append("")
    return lines


def _format_corrective_actions_txt(actions: list[dict[str, Any]]) -> list[str]:
    if not actions:
        return []
    lines = ["Corrective and Verifiable Actions", ""]
    for idx, action in enumerate(actions, start=1):
        lines += [
            f"{idx}. {action.get('repo', 'unknown')}",
            f"   Issue: {action.get('issue')}",
            f"   Corrective action: {action.get('corrective_action')}",
            f"   Verification: {action.get('verification_action')}",
            f"   Expected evidence: {action.get('expected_evidence')}",
            f"   Recommended mode: {action.get('recommended_mode')}",
            f"   Human review required: {'Yes' if action.get('human_review_required') else 'No'}",
            "",
        ]
    return lines


def summarize_multi_repo_results(run: Any) -> dict[str, Any]:
    """Build a structured summary dict from a multi-repo run."""
    scanned = [r for r in run.repo_results if r.get("status") == "scanned"]
    passed = [r for r in scanned if r.get("passed")]
    failed = [r for r in scanned if not r.get("passed")]
    failed_status = [r for r in run.repo_results if r.get("status") == "failed"]
    corrective_actions = _build_corrective_actions(run, scanned, failed_status)

    return {
        "run_id": run.run_id,
        "report_timestamp": run.timestamp,
        "github_owner": run.github_owner,
        "mode": run.mode,
        "total_discovered": run.total_discovered,
        "total_scanned": len(scanned),
        "total_skipped": len(run.skipped_repos),
        "total_passed": len(passed),
        "total_needs_work": len(failed),
        "skipped_repos": run.skipped_repos,
        "repo_results": run.repo_results,
        "corrective_actions": corrective_actions,
        "errors": [redact_secrets(e) for e in run.errors],
        "discovery_warnings": [redact_secrets(w) for w in run.discovery_warnings],
        "email_delivery_status": run.email_delivery_status,
        "email_delivery_message": redact_secrets(run.email_delivery_message),
        "audit_summary_path": run.audit_summary_path,
    }


def _novice_summary(run: Any, summary: dict[str, Any]) -> str:
    discovered = summary["total_discovered"]
    scanned = summary["total_scanned"]
    skipped = summary["total_skipped"]
    passed = summary["total_passed"]
    needs_work = summary["total_needs_work"]

    lines = [
        (
            f"Repo Governor discovered {discovered} repositories under {run.github_owner}. "
            f"{scanned} were scanned. {skipped} were skipped because they were archived, "
            f"forks, excluded by configuration, or otherwise disabled."
        ),
    ]
    if scanned:
        lines.append(
            f"Of the scanned repositories, {passed} passed agent-readiness checks and "
            f"{needs_work} need additional governance work before an autonomous coding agent "
            f"should be allowed to make changes."
        )
    else:
        lines.append("No repositories were scanned in this run.")

    if run.discovery_warnings:
        lines.append("")
        lines.append("Discovery notes:")
        for warning in run.discovery_warnings:
            lines.append(f"- {warning}")

    if run.email_delivery_status == "skipped_missing_credentials":
        lines.append("")
        lines.append(
            "Email delivery was skipped because SMTP credentials are not configured. "
            "The report was saved locally."
        )
    elif run.email_delivery_status == "sent":
        lines.append("")
        lines.append("The evidence report was emailed successfully.")

    return "\n".join(lines)


def generate_evidence_reports(
    run: Any,
    output_root: Path | None = None,
) -> EvidenceReportPaths:
    """Write evidence-summary.md, .txt, and .json for a multi-repo run."""
    report_date = run.report_date
    output_dir = (output_root or Path("reports")) / report_date
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_multi_repo_results(run)
    novice = _novice_summary(run, summary)

    md_lines = [
        "# AIAlchemy Repo Governor — Weekly Evidence Report",
        "",
        f"**Report date:** {run.timestamp}",
        f"**GitHub owner:** {run.github_owner}",
        f"**Run mode:** {run.mode}",
        "",
        "## Executive Summary",
        "",
        novice,
        "",
        "## Counts",
        "",
        f"- Repositories discovered: {summary['total_discovered']}",
        f"- Repositories scanned: {summary['total_scanned']}",
        f"- Repositories skipped: {summary['total_skipped']}",
        f"- Agent-ready (passed): {summary['total_passed']}",
        f"- Need governance work: {summary['total_needs_work']}",
        "",
    ]

    if run.skipped_repos:
        md_lines += ["## Skipped Repositories", ""]
        for item in run.skipped_repos:
            reason = item.get("skip_reason", "unknown")
            md_lines.append(f"- **{item.get('name')}** — {reason}")
        md_lines.append("")

    scanned = [r for r in run.repo_results if r.get("status") == "scanned"]
    failed_status = [r for r in run.repo_results if r.get("status") == "failed"]
    corrective_actions = summary.get("corrective_actions") or []

    if scanned:
        md_lines += ["## Repository Details", ""]
        for item in scanned:
            md_lines += [
                f"### {item.get('full_name', item.get('name'))}",
                "",
                f"- **Risk level:** {item.get('risk_level', 'unknown')}",
                f"- **Agent-ready:** {'PASS' if item.get('passed') else 'FAIL'}",
                f"- **Readiness score:** {item.get('readiness_score', 'n/a')}/100",
                f"- **Mode:** {item.get('mode', run.mode)}",
                f"- **CLAUDE.md:** {'present' if item.get('has_claude_md') else 'missing'}",
                f"- **Policy artifacts:** {item.get('policy_artifact_status', 'none')}",
                f"- **Remediation status:** {item.get('remediation_status', 'n/a')}",
                f"- **Verification status:** {item.get('verification_status', 'n/a')}",
                f"- **Audit file:** `{item.get('audit_path', 'n/a')}`",
            ]
            missing = item.get("missing_controls") or []
            if missing:
                md_lines.append(f"- **Missing controls:** {', '.join(missing)}")
            remaining = item.get("remaining_issues") or []
            if remaining:
                md_lines.append("- **Remaining issues:**")
                for issue in remaining[:5]:
                    md_lines.append(f"  - {issue}")
            md_lines.append(f"- **Recommended next action:** {item.get('recommended_action', 'Review audit.')}")
            md_lines.append("")

    md_lines += _format_corrective_actions_md(corrective_actions)

    txt_lines = [
        "AIAlchemy Repo Governor — Weekly Evidence Report",
        f"Report date: {run.timestamp}",
        f"GitHub owner: {run.github_owner}",
        f"Run mode: {run.mode}",
        "",
        novice,
        "",
        f"Discovered: {summary['total_discovered']}",
        f"Scanned: {summary['total_scanned']}",
        f"Skipped: {summary['total_skipped']}",
        f"Passed: {summary['total_passed']}",
        f"Needs work: {summary['total_needs_work']}",
        "",
    ]

    if run.skipped_repos:
        txt_lines.append("Skipped repositories:")
        for item in run.skipped_repos:
            txt_lines.append(f"  - {item.get('name')}: {item.get('skip_reason', 'unknown')}")
        txt_lines.append("")

    for item in scanned:
        txt_lines += [
            f"Repo: {item.get('full_name', item.get('name'))}",
            f"  Risk: {item.get('risk_level')}",
            f"  Agent-ready: {'PASS' if item.get('passed') else 'FAIL'}",
            f"  CLAUDE.md: {'yes' if item.get('has_claude_md') else 'no'}",
            f"  Remediation: {item.get('remediation_status', 'n/a')}",
            f"  Audit: {item.get('audit_path', 'n/a')}",
            f"  Next action: {item.get('recommended_action', 'Review audit.')}",
            "",
        ]

    txt_lines += _format_corrective_actions_txt(corrective_actions)

    markdown_path = output_dir / "evidence-summary.md"
    text_path = output_dir / "evidence-summary.txt"
    json_path = output_dir / "evidence-summary.json"

    markdown_path.write_text("\n".join(md_lines), encoding="utf-8")
    text_path.write_text("\n".join(txt_lines), encoding="utf-8")
    json_path.write_text(json.dumps(redact_dict(summary), indent=2), encoding="utf-8")

    return EvidenceReportPaths(
        markdown_path=markdown_path,
        text_path=text_path,
        json_path=json_path,
        output_dir=output_dir,
    )


def enrich_repo_result_for_report(result_item: dict[str, Any]) -> dict[str, Any]:
    """Add report-friendly fields to a per-repo result dict."""
    result_item["missing_controls"] = _missing_controls(result_item)
    result_item["recommended_action"] = _recommended_action(result_item)
    return result_item
