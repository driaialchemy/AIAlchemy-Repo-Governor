"""Evaluate shipped governance patterns as not_present / present_inert / present_active.

Additive only: results never change credential / CLAUDE.md / AGENTS.md / DB PASS gates.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from .scanner import MAX_SCAN_BYTES, SKIP_DIRS

NOT_PRESENT = "not_present"
PRESENT_INERT = "present_inert"
PRESENT_ACTIVE = "present_active"

GOVERNANCE_KEYS = ("P1", "P2", "P3", "P4", "uncertainty_monitoring")

_CODE_EXTS = frozenset({".py", ".ts", ".js", ".tsx", ".jsx"})
_SKIP_FILE_NAMES = frozenset({
    "CHANGELOG.md",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "governance_status.py",
})

_LINEAGE_FIELDS = ("reasoning_path", "policy_matched", "confidence")

_POLICY_STRING = re.compile(
    r"PolicyMatched\s*=\s*string\b"
    r"|policy_matched\s*:\s*Optional\[\s*str\s*\]"
    r"|policy_matched\?\s*:\s*string\b"
    r"|policy_matched\s*:\s*string\s*\|\s*null",
    re.IGNORECASE,
)
_POLICY_OBJECT_WRITE = re.compile(
    r"PolicyMatched\s*=\s*\{"
    r"|policy_matched\??\s*:\s*\{\s*id\b"
    r"|policy_matched\s*:\s*Optional\[\s*dict"
    r"|policy_matched\s*:\s*dict\[",
    re.IGNORECASE,
)
_POLICY_STRING_WRITE = re.compile(
    r"policy_matched\s*=\s*(?!\{)(?!None\b)(?!null\b)"
    r"|[\"']policy_matched[\"']\s*:\s*(?!\{)(?!None\b)(?!null\b)"
    r"|\[[\"']policy_matched[\"']\]\s*=\s*(?!\{)(?!None\b)(?!null\b)",
)
_P1_EMIT = re.compile(
    r"buildWebhookPayload\s*\("
    r"|log_decision\s*\("
    r"|\[[\"']policy_matched[\"']\]\s*="
    r"|[\"']policy_matched[\"']\s*:",
)

_TRUST_HEADING = re.compile(
    r"^##\s+(?P<letter>T-sim|[TRUS]|T)\b[^\n]*",
    re.MULTILINE | re.IGNORECASE,
)
_TRUST_GAP = re.compile(
    r"^\s*(Gap\b|not yet implemented\b)",
    re.IGNORECASE | re.MULTILINE,
)

_AUTO_CLEAR = re.compile(
    r"AUTO_CLEAR_RISK_THRESHOLD|should_auto_clear|classify_compliance_tier|review_route[\"']?\s*:\s*[\"']auto_logged",
)
_HUMAN_ROUTE = re.compile(
    r"review_route[\"']?\s*:\s*[\"']human_review"
    r"|skip_review_queue"
    r"|else:\s*\n\s*(?:synthesis|result)\s*=\s*(?:decision_synthesizer\.)?synthesize",
)

_INVENTORY_GET = re.compile(r"[\"']/decision-inventory[\"']")
_TAXONOMY_PATCH = re.compile(r"[\"']/versions/:[^\"']+/taxonomy[\"']|updateVersionTaxonomy")
_AXIS_POPULATED = re.compile(
    r"\b(?:complexity|regulatory_impact|business_importance)\s*:\s*[\"'][^\"']+[\"']"
)

_UNCERTAINTY_ROUTE = re.compile(r"[\"']/uncertainty-flags[\"']")
_FEEDER_CALL = re.compile(r"(?:require_approval|log_success|logSuccess)\s*\(")
_FEEDER_CONFIDENCE = re.compile(
    r"confidence\s*=\s*(?!None\b)(?!null\b)(?!\s*[,)])"
)
_LOGGER_FILES = frozenset({
    "governance_logger.py",
    "GovernanceLogger.ts",
    "types.ts",
})


def empty_governance_status() -> dict[str, str]:
    return {key: NOT_PRESENT for key in GOVERNANCE_KEYS}


def evaluate_governance_status(
    repo_path: Path,
    *,
    confidence_feeders: list[str] | None = None,
) -> dict[str, str]:
    """Return per-pattern states for one repository."""
    status = empty_governance_status()
    if not repo_path or not Path(repo_path).is_dir():
        return status

    blob = _repo_source_blob(str(Path(repo_path).resolve()))
    status["P1"] = _eval_p1(blob)
    status["P2"] = _eval_p2(Path(repo_path))
    status["P3"] = _eval_p3(blob)
    status["P4"] = _eval_p4(blob)
    status["uncertainty_monitoring"] = _eval_uncertainty(
        Path(repo_path),
        blob,
        confidence_feeders,
    )
    return status


def discover_confidence_feeders(repo_paths: list[Path]) -> list[str]:
    """Repos that POST activity with an upstream confidence value (not logger plumbing)."""
    feeders: list[str] = []
    for path in repo_paths:
        if not path.is_dir():
            continue
        if _is_confidence_feeder(path):
            feeders.append(path.name)
    return feeders


def _eval_p1(blob: str) -> str:
    has_path = "reasoning_path" in blob
    has_policy = "policy_matched" in blob
    if not (has_path and has_policy):
        return NOT_PRESENT
    string_shape = bool(_POLICY_STRING.search(blob) or _POLICY_STRING_WRITE.search(blob))
    object_write = bool(_POLICY_OBJECT_WRITE.search(blob))
    emits = bool(_P1_EMIT.search(blob))
    if string_shape and not object_write and emits:
        return PRESENT_ACTIVE
    return PRESENT_INERT


def _eval_p2(repo_path: Path) -> str:
    trust = repo_path / "TRUST.md"
    if not trust.is_file():
        return NOT_PRESENT
    try:
        text = trust.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return PRESENT_INERT

    implemented = 0
    headings = list(_TRUST_HEADING.finditer(text))
    if not headings:
        return PRESENT_INERT

    for index, match in enumerate(headings):
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[start:end].strip()
        if not body:
            continue
        if _TRUST_GAP.search(body):
            continue
        implemented += 1

    return PRESENT_ACTIVE if implemented else PRESENT_INERT


def _eval_p3(blob: str) -> str:
    has_auto = bool(_AUTO_CLEAR.search(blob))
    if not has_auto:
        return NOT_PRESENT
    if _HUMAN_ROUTE.search(blob):
        return PRESENT_ACTIVE
    return PRESENT_INERT


def _eval_p4(blob: str) -> str:
    has_inventory = bool(_INVENTORY_GET.search(blob))
    has_write = bool(_TAXONOMY_PATCH.search(blob))
    if not (has_inventory and has_write):
        return NOT_PRESENT
    if _AXIS_POPULATED.search(blob):
        return PRESENT_ACTIVE
    return PRESENT_INERT


def _eval_uncertainty(
    repo_path: Path,
    blob: str,
    confidence_feeders: list[str] | None,
) -> str:
    if not _UNCERTAINTY_ROUTE.search(blob):
        return NOT_PRESENT
    feeders = list(confidence_feeders) if confidence_feeders is not None else []
    if confidence_feeders is None:
        parent = repo_path.parent
        if parent.is_dir():
            feeders = discover_confidence_feeders(
                [path for path in parent.iterdir() if path.is_dir()]
            )
    # Single-source (or none) is shipped-but-not-fully-wired — never "complete".
    if len(feeders) >= 2:
        return PRESENT_ACTIVE
    return PRESENT_INERT


def _is_confidence_feeder(repo_path: Path) -> bool:
    for file_path, text in _iter_source_files(repo_path):
        if file_path.name in _LOGGER_FILES:
            continue
        if _FEEDER_CALL.search(text) and _FEEDER_CONFIDENCE.search(text):
            return True
    return False


def clear_source_cache() -> None:
    _repo_source_blob.cache_clear()


@lru_cache(maxsize=64)
def _repo_source_blob(repo_path: str) -> str:
    chunks: list[str] = []
    for _, text in _iter_source_files(Path(repo_path)):
        chunks.append(text)
    return "\n".join(chunks)


def _iter_source_files(root: Path):
    for file_path in _walk_source(root):
        if file_path.name in _SKIP_FILE_NAMES:
            continue
        if _is_test_path(file_path, root):
            continue
        if file_path.suffix.lower() not in _CODE_EXTS and file_path.name != "TRUST.md":
            continue
        try:
            if file_path.stat().st_size > MAX_SCAN_BYTES:
                continue
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        yield file_path, text


def _is_test_path(file_path: Path, root: Path) -> bool:
    try:
        rel = file_path.relative_to(root).as_posix()
    except ValueError:
        rel = file_path.as_posix()
    parts = rel.split("/")
    if "tests" in parts or "__tests__" in parts:
        return True
    name = file_path.name
    return name.startswith("test_") or name.endswith(".test.ts") or name.endswith(".test.js")


def _walk_source(root: Path):
    def _recurse(path: Path):
        try:
            entries = list(path.iterdir())
        except (PermissionError, OSError):
            return
        for entry in entries:
            try:
                if entry.is_symlink():
                    continue
                if entry.is_dir():
                    if entry.name in SKIP_DIRS:
                        continue
                    yield from _recurse(entry)
                elif entry.is_file():
                    yield entry
            except OSError:
                continue

    yield from _recurse(root)
