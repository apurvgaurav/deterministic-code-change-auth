import re

from app.models import PatchResult, TemplateSelection
from app.utils import sha256_text


def generate_patch(template_selection: TemplateSelection) -> PatchResult:
    template_fields = load_template_fields(template_selection.template_path)

    ordered_patch_items = []
    for key, value in template_fields.items():
        if key.startswith("PATCH_LINE_"):
            line_number = extract_patch_line_number(key)
            ordered_patch_items.append((line_number, value))

    ordered_patch_items.sort(key=lambda item: item[0])

    patch_lines = [value for _, value in ordered_patch_items]

    if not patch_lines:
        raise ValueError(
            f"No patch lines found in template: {template_selection.template_path}"
        )

    generated_patch = "\n".join(patch_lines)
    patch_hash = sha256_text(generated_patch)

    return PatchResult(
        template_id=template_selection.template_id,
        generated_patch=generated_patch,
        patch_hash=patch_hash,
    )


def load_template_fields(template_path: str) -> dict:
    fields = {}

    with open(template_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line:
                continue

            if "=" not in line:
                raise ValueError(f"Malformed template line: {line}")

            key, value = line.split("=", 1)
            fields[key.strip()] = value.strip()

    return fields


def extract_patch_line_number(key: str) -> int:
    match = re.fullmatch(r"PATCH_LINE_(\d+)", key)
    if not match:
        raise ValueError(f"Invalid patch line key: {key}")

    return int(match.group(1))