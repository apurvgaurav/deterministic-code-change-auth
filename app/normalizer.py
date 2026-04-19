import re

from app.models import PRInput, NormalizedPR
from app.utils import sha256_text


def normalize_diff_text(raw_diff: str) -> str:
    """
    Deterministic diff normalization.

    Rules:
    - normalize line endings to \n
    - strip trailing whitespace on each line
    - collapse multiple blank lines into a single blank line
    - trim leading/trailing outer whitespace
    """
    text = raw_diff.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_pr_input(pr_input: PRInput) -> NormalizedPR:
    normalized_diff = normalize_diff_text(pr_input.raw_diff)
    diff_hash = sha256_text(normalized_diff)

    return NormalizedPR(
        pr_id=pr_input.pr_id,
        file_path=pr_input.file_path,
        language=pr_input.language.lower().strip(),
        normalized_diff=normalized_diff,
        diff_hash=diff_hash,
    )