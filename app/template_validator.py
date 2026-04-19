from __future__ import annotations

import hashlib
from pathlib import Path

from app.models import TemplateSelection


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_template_integrity(template_selection: TemplateSelection) -> bool:
    """
    Validate that the template file on disk matches the expected template hash.
    """
    template_path = Path(template_selection.template_path)

    if not template_path.exists():
        return False

    template_content = template_path.read_text(encoding="utf-8")
    actual_hash = _sha256_text(template_content)

    return actual_hash == template_selection.template_hash