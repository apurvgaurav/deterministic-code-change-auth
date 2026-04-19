from app.models import IssueMapping, NormalizedPR


def map_issue(normalized_pr: NormalizedPR) -> IssueMapping:
    sql_injection_lines = []

    for line in normalized_pr.normalized_diff.splitlines():
        if "SELECT * FROM users WHERE username = '" in line:
            sql_injection_lines.append(line)

    if sql_injection_lines:
        return IssueMapping(
            issue_type="SQL_INJECTION_UNSAFE_QUERY_CONCAT",
            rule_id="RULE_SQL_INJECTION_PARAM_QUERY",
            confidence="DETERMINISTIC",
            matched_lines=sql_injection_lines,
        )

    print_lines = []

    for line in normalized_pr.normalized_diff.splitlines():
        stripped = line.strip()
        if stripped.startswith("- print(") or stripped.startswith("+ print("):
            print_lines.append(line)

    if print_lines:
        return IssueMapping(
            issue_type="PYTHON_DEBUG_PRINT_STATEMENT",
            rule_id="RULE_PY_PRINT_TO_LOGGER_INFO",
            confidence="DETERMINISTIC",
            matched_lines=print_lines,
        )

    return IssueMapping(
        issue_type="UNMAPPED_ISSUE",
        rule_id="RULE_UNMAPPED_BLOCK",
        confidence="DETERMINISTIC",
        matched_lines=[],
    )