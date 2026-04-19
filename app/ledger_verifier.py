from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import List, Tuple

from app.ledger import GENESIS_PREVIOUS_HASH, LEDGER_FILE_PATH


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _build_record_hash_payload(record: dict) -> str:
    payload = {
        "execution_id": record["execution_id"],
        "environment_fingerprint": record["environment_fingerprint"],
        "pr_id": record["pr_id"],
        "file_path": record["file_path"],
        "normalized_diff_hash": record["normalized_diff_hash"],
        "issue_type": record["issue_type"],
        "rule_id": record["rule_id"],
        "template_id": record["template_id"],
        "template_hash": record["template_hash"],
        "original_patch_hash": record["original_patch_hash"],
        "replay_patch_hash": record["replay_patch_hash"],
        "byte_match": record["byte_match"],
        "decision": record["decision"],
        "reason": record["reason"],
        "timestamp_utc": record["timestamp_utc"],
        "previous_record_hash": record["previous_record_hash"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def verify_ledger_chain() -> Tuple[bool, List[str]]:
    """
    Verify the full hash chain of the local ledger file.

    Returns:
        (is_valid, errors)
    """
    errors: List[str] = []

    if not LEDGER_FILE_PATH.exists():
        return True, []

    with LEDGER_FILE_PATH.open("r", encoding="utf-8") as ledger_file:
        lines = [line.strip() for line in ledger_file if line.strip()]

    previous_expected_hash = GENESIS_PREVIOUS_HASH

    for index, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"Line {index}: invalid JSON")
            continue

        actual_previous_hash = record.get("previous_record_hash")
        actual_record_hash = record.get("record_hash")

        if actual_previous_hash != previous_expected_hash:
            errors.append(
                f"Line {index}: previous_record_hash mismatch "
                f"(expected {previous_expected_hash}, got {actual_previous_hash})"
            )

        try:
            payload = _build_record_hash_payload(record)
            recomputed_hash = _sha256_text(payload)
        except KeyError as exc:
            errors.append(f"Line {index}: missing field for hash verification: {exc}")
            continue

        if actual_record_hash != recomputed_hash:
            errors.append(
                f"Line {index}: record_hash mismatch "
                f"(expected {recomputed_hash}, got {actual_record_hash})"
            )

        previous_expected_hash = actual_record_hash

    return len(errors) == 0, errors