"""Combined evidence report generation for multi-repo governance runs."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def summarize_multi_repo_results(run: Any) -> dict[str, Any]:
    """Build a structured summary dict from a multi-repo run."""
    scanned = [r for r in run.repo_results if r.get("status") == "scanned"]
    passed = [r for r in scanned if r.get("passed")]
    failed = [r for r in scanned if not r.get("passed")]

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
        "errors": run.errors,
        "discovery_warnings": run.discovery_warnings,
        "email_delivery_status": run.email_delivery_status,
        "email_delivery_message": run.email_delivery_message,
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

    markdown_path = output_dir / "evidence-summary.md"
    text_path = output_dir / "evidence-summary.txt"
    json_path = output_dir / "evidence-summary.json"

    markdown_path.write_text("\n".join(md_lines), encoding="utf-8")
    text_path.write_text("\n".join(txt_lines), encoding="utf-8")
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

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
