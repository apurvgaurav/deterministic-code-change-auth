from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.config import LEDGER_FILE

from app.models import (
    ComparisonResult,
    DecisionResult,
    IssueMapping,
    LedgerRecord,
    NormalizedPR,
    PatchResult,
    PRInput,
    ReplayResult,
    TemplateSelection,
)


LEDGER_FILE_PATH = LEDGER_FILE
GENESIS_PREVIOUS_HASH = "GENESIS"


def _ensure_ledger_file_exists() -> None:
    LEDGER_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER_FILE_PATH.exists():
        LEDGER_FILE_PATH.touch()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_last_record_hash() -> str:
    """
    Return the hash of the most recent ledger record.
    If no records exist yet, return GENESIS.
    """
    _ensure_ledger_file_exists()

    with LEDGER_FILE_PATH.open("rb") as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        
        last_line = f.readline().decode("utf-8").strip()

    if not last_line:
        return GENESIS_PREVIOUS_HASH

    try:
        last_record = json.loads(last_line)
        return last_record.get("record_hash", GENESIS_PREVIOUS_HASH)
    except json.JSONDecodeError:
        return GENESIS_PREVIOUS_HASH


def _build_record_hash_payload(
    *,
    execution_id: str,
    environment_fingerprint: str,
    pr_id: str,
    file_path: str,
    normalized_diff_hash: str,
    issue_type: str,
    rule_id: str,
    template_id: str,
    template_hash: str,
    original_patch_hash: str,
    replay_patch_hash: str,
    byte_match: bool,
    decision: str,
    reason: str,
    timestamp_utc: str,
    previous_record_hash: str,
) -> str:
    """
    Deterministically serialize the current record content for hashing.
    """
    payload = {
        "execution_id": execution_id,
        "environment_fingerprint": environment_fingerprint,
        "pr_id": pr_id,
        "file_path": file_path,
        "normalized_diff_hash": normalized_diff_hash,
        "issue_type": issue_type,
        "rule_id": rule_id,
        "template_id": template_id,
        "template_hash": template_hash,
        "original_patch_hash": original_patch_hash,
        "replay_patch_hash": replay_patch_hash,
        "byte_match": byte_match,
        "decision": decision,
        "reason": reason,
        "timestamp_utc": timestamp_utc,
        "previous_record_hash": previous_record_hash,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _append_record_to_file(ledger_record: LedgerRecord) -> None:
    _ensure_ledger_file_exists()
    with LEDGER_FILE_PATH.open("a", encoding="utf-8") as ledger_file:
        ledger_file.write(ledger_record.model_dump_json())
        ledger_file.write("\n")


def write_ledger_record(
    *,
    execution_id: str,
    environment_fingerprint: str,
    pr_input: PRInput,
    normalized_pr: NormalizedPR,
    issue_mapping: IssueMapping,
    decision_result: DecisionResult,
    template_selection: TemplateSelection | None = None,
    patch_result: PatchResult | None = None,
    replay_result: ReplayResult | None = None,
    comparison_result: ComparisonResult | None = None,
) -> LedgerRecord:
    """
    Create a ledger record, chain it to the previous record hash,
    persist it locally, and return it.
    """
    template_id = template_selection.template_id if template_selection else "N/A"
    template_hash = template_selection.template_hash if template_selection else "N/A"
    original_patch_hash = patch_result.patch_hash if patch_result else "N/A"
    replay_patch_hash = replay_result.replay_patch_hash if replay_result else "N/A"
    byte_match = comparison_result.is_match if comparison_result else False
    timestamp_utc = _utc_now_iso()
    previous_record_hash = _read_last_record_hash()

    record_hash_payload = _build_record_hash_payload(
        execution_id=execution_id,
        environment_fingerprint=environment_fingerprint,
        pr_id=pr_input.pr_id,
        file_path=pr_input.file_path,
        normalized_diff_hash=normalized_pr.diff_hash,
        issue_type=issue_mapping.issue_type,
        rule_id=issue_mapping.rule_id,
        template_id=template_id,
        template_hash=template_hash,
        original_patch_hash=original_patch_hash,
        replay_patch_hash=replay_patch_hash,
        byte_match=byte_match,
        decision=decision_result.decision,
        reason=decision_result.reason,
        timestamp_utc=timestamp_utc,
        previous_record_hash=previous_record_hash,
    )

    record_hash = _sha256_text(record_hash_payload)

    ledger_record = LedgerRecord(
        execution_id=execution_id,
        environment_fingerprint=environment_fingerprint,
        pr_id=pr_input.pr_id,
        file_path=pr_input.file_path,
        normalized_diff_hash=normalized_pr.diff_hash,
        issue_type=issue_mapping.issue_type,
        rule_id=issue_mapping.rule_id,
        template_id=template_id,
        template_hash=template_hash,
        original_patch_hash=original_patch_hash,
        replay_patch_hash=replay_patch_hash,
        byte_match=byte_match,
        decision=decision_result.decision,
        reason=decision_result.reason,
        timestamp_utc=timestamp_utc,
        previous_record_hash=previous_record_hash,
        record_hash=record_hash,
    )

    _append_record_to_file(ledger_record)
    return ledger_record