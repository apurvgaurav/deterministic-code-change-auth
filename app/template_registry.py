from pathlib import Path

from app.config import TEMPLATES_DIR
from app.models import IssueMapping, TemplateSelection
from app.utils import sha256_file


ISSUE_TEMPLATE_MAP = {
    "SQL_INJECTION_UNSAFE_QUERY_CONCAT": "sql_injection_parameterized_query.tpl",
    "PYTHON_DEBUG_PRINT_STATEMENT": "python_print_to_logger_info.tpl",
}


def get_template_for_issue(issue_mapping: IssueMapping) -> TemplateSelection:
    if issue_mapping.issue_type not in ISSUE_TEMPLATE_MAP:
        raise ValueError(f"No approved template for issue type: {issue_mapping.issue_type}")

    template_filename = ISSUE_TEMPLATE_MAP[issue_mapping.issue_type]
    template_path = TEMPLATES_DIR / template_filename

    if not template_path.exists():
        raise FileNotFoundError(f"Template file missing: {template_path}")

    template_id = extract_template_id(template_path)
    template_hash = sha256_file(template_path)

    return TemplateSelection(
        template_id=template_id,
        template_path=str(template_path),
        template_hash=template_hash,
        issue_type=issue_mapping.issue_type,
        force_replay_mismatch=False,
    )


def extract_template_id(template_path: Path) -> str:
    with open(template_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("TEMPLATE_ID="):
                return line.split("=", 1)[1]

    raise ValueError(f"TEMPLATE_ID missing in template: {template_path}")