from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, List, Optional, Tuple

from app.models import ReplayResult


def _append_controlled_divergence(patch_text: str) -> str:
    """
    Deterministically alter replay output so byte-level comparison fails.
    Prototype test hook only.
    """
    if patch_text.endswith("\n"):
        return patch_text + "# replay divergence\n"
    return patch_text + "\n# replay divergence"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_field(obj: Any, field_name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(field_name)
    return getattr(obj, field_name, None)


def _load_text_file(path_value: str) -> str:
    path = Path(path_value)
    if not path.exists():
        raise FileNotFoundError(f"Template path does not exist: {path}")
    return path.read_text(encoding="utf-8")


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _known_template_path_from_template_id(template_id: str) -> Optional[Path]:
    if template_id == "TPL_SQL_PARAM_QUERY_V1":
        return _project_root() / "data" / "templates" / "sql_injection_parameterized_query.tpl"
    return None


def _extract_template_path(template_selection: Any) -> str:
    template_path = _read_field(template_selection, "template_path")
    if isinstance(template_path, str) and template_path.strip():
        return template_path

    template_id = _read_field(template_selection, "template_id")
    if isinstance(template_id, str):
        known_path = _known_template_path_from_template_id(template_id)
        if known_path is not None:
            return str(known_path)

    raise ValueError("Unable to resolve template path from template_selection")


def _parse_patch_lines(template_text: str) -> str:
    """
    Convert template file content into final patch text.
    Only PATCH_LINE_n entries are used.
    """
    parsed_lines: List[Tuple[int, str]] = []

    for raw_line in template_text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^PATCH_LINE_(\d+)=(.*)$", line)
        if match:
            line_number = int(match.group(1))
            patch_value = match.group(2)
            parsed_lines.append((line_number, patch_value))

    if not parsed_lines:
        raise ValueError("No PATCH_LINE_n entries found in template")

    parsed_lines.sort(key=lambda item: item[0])
    ordered_patch_lines = [value for _, value in parsed_lines]
    return "\n".join(ordered_patch_lines)


def _should_force_mismatch(template_selection: Any) -> bool:
    value = _read_field(template_selection, "force_replay_mismatch")
    return bool(value)


def replay_patch_generation(template_selection: Any) -> ReplayResult:
    """
    Rebuild the same final patch text from the template file.
    Optionally force replay mismatch per request.
    """
    template_path = _extract_template_path(template_selection)
    template_text = _load_text_file(template_path)

    replay_patch_text = _parse_patch_lines(template_text)

    if _should_force_mismatch(template_selection):
        replay_patch_text = _append_controlled_divergence(replay_patch_text)

    return ReplayResult(
        replay_patch=replay_patch_text,
        replay_patch_hash=_sha256_text(replay_patch_text),
        replay_status="REPLAY_COMPLETED",
    )