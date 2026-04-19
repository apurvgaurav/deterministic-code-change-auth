from app.models import ComparisonResult, PatchResult, ReplayResult


def compare_patches(
    original_patch: PatchResult,
    replay_patch: ReplayResult,
) -> ComparisonResult:
    return ComparisonResult(
        is_match=original_patch.generated_patch == replay_patch.replay_patch,
        original_patch_hash=original_patch.patch_hash,
        replay_patch_hash=replay_patch.replay_patch_hash,
    )