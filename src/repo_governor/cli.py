"""CLI entry point for AIAlchemy Repo Governor."""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

# Wrap stdout/stderr so Unicode characters (em-dash, etc.) don't crash on
# Windows consoles that use a narrow code page (cp1252, cp850, etc.).
if sys.stdout.encoding and sys.stdout.encoding.lower().replace("-", "") not in ("utf8", "utf16"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower().replace("-", "") not in ("utf8", "utf16"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from . import __version__
from .classifier import classify_all, classify_repo, RiskLevel
from .policy import write_policy, write_repo_policy
from .reporter import write_all_reports, write_report
from .scanner import scan_repo, scan_root


def cmd_scan(args: argparse.Namespace) -> int:
    root = Path(args.root_path)
    print(f"Scanning: {root}\n")
    try:
        repos = scan_root(root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not repos:
        print("No directories found under the given root.")
        return 0

    print(f"Found {len(repos)} repositories:\n")
    for r in repos:
        marker = "[git]" if r.is_git_repo else "[dir]"
        langs = f"  ({', '.join(r.languages[:2])})" if r.languages else ""
        print(f"  {marker}  {r.name:<40}  {r.file_count:>4} files{langs}")
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    root = Path(args.root_path)
    try:
        repos = scan_root(root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not repos:
        print("No directories found.")
        return 0

    classified = classify_all(repos)
    print(f"\n{'Repository':<42} {'Risk':<10} Agent-Ready")
    print("-" * 68)
    for cr in classified:
        ready = "Yes" if cr.agent_ready else "No"
        print(f"  {cr.repo.name:<40} {cr.risk_level.value:<10} {ready}")

    high = [cr for cr in classified if cr.risk_level == RiskLevel.HIGH]
    if high:
        print(f"\n{len(high)} HIGH-risk repo(s) need immediate attention:")
        for cr in high:
            for factor in cr.risk_factors:
                print(f"  [{cr.repo.name}] {factor}")
    return 0


def cmd_policy_init(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo_path)
    if not repo_path.is_dir():
        print(f"Error: not a directory: {repo_path}", file=sys.stderr)
        return 1

    repo_info = scan_repo(repo_path)
    classified = classify_repo(repo_info)

    try:
        claude_path = write_policy(
            repo_path,
            risk_level=classified.risk_level.value,
            overwrite=args.overwrite,
        )
        yaml_path = write_repo_policy(repo_path, classified, overwrite=args.overwrite)
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("Pass --overwrite to replace existing policy files.", file=sys.stderr)
        return 1

    print(f"CLAUDE.md        -> {claude_path}")
    print(f"repo_policy.yaml -> {yaml_path}")
    print(f"\nRisk level:      {classified.risk_level.value}")
    print(f"Readiness score: {classified.readiness_score}/100")

    if classified.blocking_issues:
        print(f"\n[!] Blocking issues ({len(classified.blocking_issues)}):")
        for issue in classified.blocking_issues:
            print(f"    - {issue}")
        print("\nResolve blocking issues before using an agent in this repository.")
    elif classified.risk_reasons:
        print(f"\nAdvisories ({len(classified.risk_reasons)}):")
        for reason in classified.risk_reasons[:5]:
            print(f"    - {reason}")

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    root = Path(args.root_path)

    print(f"Generating reports for: {root}")
    try:
        repos = scan_root(root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    classified = classify_all(repos)

    if args.output:
        # Single-file mode (legacy --output flag)
        path = write_report(classified, root, output_path=Path(args.output))
        print(f"Report written: {path}")
    else:
        output_dir = Path(args.output_dir) if args.output_dir else Path.cwd() / "reports"
        paths = write_all_reports(classified, root, output_dir)
        for p in paths:
            print(f"  {p}")
        print(f"\n{len(paths)} reports written to: {output_dir}")
    return 0


def cmd_agent_ready(args: argparse.Namespace) -> int:
    root = Path(args.root_path)
    try:
        repos = scan_root(root)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    classified = classify_all(repos)
    ready = [cr for cr in classified if cr.agent_ready]
    not_ready = [cr for cr in classified if not cr.agent_ready]

    if ready:
        print(f"\nAgent-ready ({len(ready)}):")
        for cr in ready:
            print(f"  [OK]  {cr.repo.name}")

    if not_ready:
        print(f"\nNot agent-ready ({len(not_ready)}):")
        for cr in not_ready:
            print(f"  [--]  {cr.repo.name}  [{cr.risk_level.value}]")
            for rec in cr.recommendations[:2]:
                print(f"       ->  {rec}")

    if not classified:
        print("No repositories found.")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-governor",
        description="AIAlchemy Repo Governor — scan, classify, and prepare repos for agent use.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Scan repositories under a root path.")
    p_scan.add_argument("root_path", help="Root directory containing repos.")
    p_scan.set_defaults(func=cmd_scan)

    p_classify = sub.add_parser("classify", help="Classify repo risk levels.")
    p_classify.add_argument("root_path", help="Root directory containing repos.")
    p_classify.set_defaults(func=cmd_classify)

    p_policy = sub.add_parser("policy-init", help="Generate a CLAUDE.md and repo_policy.yaml for a repo.")
    p_policy.add_argument("repo_path", help="Path to the repository.")
    p_policy.add_argument(
        "--overwrite", "--force",
        dest="overwrite",
        action="store_true",
        help="Overwrite existing policy files.",
    )
    p_policy.set_defaults(func=cmd_policy_init)

    p_report = sub.add_parser("report", help="Generate Markdown governance reports.")
    p_report.add_argument("root_path", help="Root directory containing repos.")
    p_report.add_argument(
        "--output", "-o",
        help="Single output file path (omit to write all 3 reports to --output-dir).",
    )
    p_report.add_argument(
        "--output-dir",
        default=None,
        help="Directory for the 3-report set (default: ./reports/).",
    )
    p_report.set_defaults(func=cmd_report)

    p_agent = sub.add_parser("agent-ready", help="Show which repos are ready for agent use.")
    p_agent.add_argument("root_path", help="Root directory containing repos.")
    p_agent.set_defaults(func=cmd_agent_ready)

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
