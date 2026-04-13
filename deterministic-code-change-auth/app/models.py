from typing import List, Optional
from pydantic import BaseModel


class PRInput(BaseModel):
    pr_id: str
    file_path: str
    language: str
    raw_diff: str
    force_replay_mismatch: bool = False


class NormalizedPR(BaseModel):
    pr_id: str
    file_path: str
    language: str
    normalized_diff: str
    diff_hash: str


class IssueMapping(BaseModel):
    issue_type: str
    rule_id: str
    confidence: str
    matched_lines: List[str]


class TemplateSelection(BaseModel):
    template_id: str
    template_path: str
    template_hash: str
    issue_type: str
    force_replay_mismatch: bool = False


class PatchResult(BaseModel):
    template_id: str
    generated_patch: str
    patch_hash: str


class ReplayResult(BaseModel):
    replay_patch: str
    replay_patch_hash: str
    replay_status: str


class ComparisonResult(BaseModel):
    is_match: bool
    original_patch_hash: str
    replay_patch_hash: str


class DecisionResult(BaseModel):
    decision: str
    reason: str
    rollback_triggered: bool


class LedgerRecord(BaseModel):
    execution_id: str
    environment_fingerprint: str
    pr_id: str
    file_path: str
    normalized_diff_hash: str
    issue_type: str
    rule_id: str
    template_id: str
    template_hash: str
    original_patch_hash: str
    replay_patch_hash: str
    byte_match: bool
    decision: str
    reason: str
    timestamp_utc: str
    previous_record_hash: str
    record_hash: str


class AuthorizationResult(BaseModel):
    execution_id: str
    environment_fingerprint: str
    normalized_pr: NormalizedPR
    issue_mapping: IssueMapping
    template_selection: Optional[TemplateSelection] = None
    patch_result: Optional[PatchResult] = None
    replay_result: Optional[ReplayResult] = None
    comparison_result: Optional[ComparisonResult] = None
    decision_result: DecisionResult
    ledger_record: Optional[LedgerRecord] = None