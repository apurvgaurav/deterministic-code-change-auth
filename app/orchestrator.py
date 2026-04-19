from app.config import DECISION_BLOCK
from app.models import AuthorizationResult, DecisionResult, PRInput
from app.normalizer import normalize_pr_input
from app.issue_mapper import map_issue
from app.template_registry import get_template_for_issue
from app.patch_generator import generate_patch
from app.replay_engine import replay_patch_generation
from app.comparator import compare_patches
from app.decision_gate import make_authorization_decision
from app.ledger import write_ledger_record
from app.utils import generate_execution_id, get_environment_fingerprint
from app.template_validator import validate_template_integrity


def _finalize_authorization(
    execution_id,
    environment_fingerprint,
    pr_input,
    normalized,
    issue_mapping,
    decision_result,
    template_selection=None,
    patch_result=None,
    replay_result=None,
    comparison_result=None,
) -> AuthorizationResult:
    ledger_record = write_ledger_record(
        execution_id=execution_id,
        environment_fingerprint=environment_fingerprint,
        pr_input=pr_input,
        normalized_pr=normalized,
        issue_mapping=issue_mapping,
        template_selection=template_selection,
        patch_result=patch_result,
        replay_result=replay_result,
        comparison_result=comparison_result,
        decision_result=decision_result,
    )

    return AuthorizationResult(
        execution_id=execution_id,
        environment_fingerprint=environment_fingerprint,
        normalized_pr=normalized,
        issue_mapping=issue_mapping,
        template_selection=template_selection,
        patch_result=patch_result,
        replay_result=replay_result,
        comparison_result=comparison_result,
        decision_result=decision_result,
        ledger_record=ledger_record,
    )


def run_authorization(pr_input: PRInput) -> AuthorizationResult:
    execution_id = generate_execution_id()
    environment_fingerprint = get_environment_fingerprint()
    normalized = normalize_pr_input(pr_input)
    issue_mapping = map_issue(normalized)

    # ---------------- UNMAPPED PATH ----------------
    if issue_mapping.issue_type == "UNMAPPED_ISSUE":
        decision_result = DecisionResult(
            decision=DECISION_BLOCK,
            reason="Unmapped issue: no deterministic rule available",
            rollback_triggered=True,
        )

        return _finalize_authorization(
            execution_id,
            environment_fingerprint,
            pr_input,
            normalized,
            issue_mapping,
            decision_result,
        )

    # ---------------- MAPPED PATH ----------------
    template_selection = get_template_for_issue(issue_mapping)

    # carry mismatch flag
    template_selection.force_replay_mismatch = getattr(
        pr_input,
        "force_replay_mismatch",
        False,
    )

    # ---------------- TEMPLATE INTEGRITY CHECK ----------------
    if not validate_template_integrity(template_selection):
        decision_result = DecisionResult(
            decision=DECISION_BLOCK,
            reason="Template integrity validation failed",
            rollback_triggered=True,
        )

        return _finalize_authorization(
            execution_id,
            environment_fingerprint,
            pr_input,
            normalized,
            issue_mapping,
            decision_result,
            template_selection=template_selection,
        )

    # ---------------- NORMAL FLOW ----------------
    patch_result = generate_patch(template_selection)
    replay_result = replay_patch_generation(template_selection)
    comparison_result = compare_patches(patch_result, replay_result)
    decision_result = make_authorization_decision(replay_result, comparison_result)

    return _finalize_authorization(
        execution_id,
        environment_fingerprint,
        pr_input,
        normalized,
        issue_mapping,
        decision_result,
        template_selection=template_selection,
        patch_result=patch_result,
        replay_result=replay_result,
        comparison_result=comparison_result,
    )