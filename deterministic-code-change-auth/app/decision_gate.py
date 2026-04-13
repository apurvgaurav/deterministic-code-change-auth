from __future__ import annotations

from app.models import ComparisonResult, DecisionResult, ReplayResult


def make_authorization_decision(
    replay_result: ReplayResult,
    comparison_result: ComparisonResult,
) -> DecisionResult:
    """
    Deterministic authorization rule:

    ALLOW only if:
    - replay completed successfully
    - byte-level comparison matched exactly

    Otherwise BLOCK.
    """

    if replay_result.replay_status != "REPLAY_COMPLETED":
        return DecisionResult(
            decision="BLOCK",
            reason="Replay execution failed",
            rollback_triggered=True,
        )

    if not comparison_result.is_match:
        return DecisionResult(
            decision="BLOCK",
            reason="Replay output mismatch",
            rollback_triggered=True,
        )

    return DecisionResult(
        decision="ALLOW",
        reason="Replay verified: byte-level match confirmed",
        rollback_triggered=False,
    )