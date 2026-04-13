from app.models import PRInput
from app.orchestrator import run_authorization
from app.ledger_verifier import verify_ledger_chain

def test_mapped_issue_match():
    mapped_pr = PRInput(
        pr_id="PR-001",
        file_path="src/auth/login.py",
        language="Python",
        raw_diff="""
- query = "SELECT * FROM users WHERE username = '" + username + "'"
+ query = "SELECT * FROM users WHERE username = %s"

- cursor.execute(query)
+ cursor.execute(query, (username,))
        """,
        force_replay_mismatch=False,
    )
    result = run_authorization(mapped_pr)
    assert result.decision_result.decision == "ALLOW"

def test_mapped_issue_mismatch():
    mapped_mismatch_pr = PRInput(
        pr_id="PR-003",
        file_path="src/auth/login.py",
        language="Python",
        raw_diff="""
- query = "SELECT * FROM users WHERE username = '" + username + "'"
+ query = "SELECT * FROM users WHERE username = %s"

- cursor.execute(query)
+ cursor.execute(query, (username,))
        """,
        force_replay_mismatch=True,
    )
    result = run_authorization(mapped_mismatch_pr)
    assert result.decision_result.decision == "BLOCK"

def test_unmapped_issue():
    unmapped_pr = PRInput(
        pr_id="PR-002",
        file_path="src/utils/math.py",
        language="Python",
        raw_diff="""
- total = value1 + value2
+ total = sum([value1, value2])
        """,
        force_replay_mismatch=False,
    )
    result = run_authorization(unmapped_pr)
    assert result.decision_result.decision == "BLOCK"

def test_print_rule_match():
    print_rule_pr = PRInput(
        pr_id="PR-004",
        file_path="src/auth/audit.py",
        language="Python",
        raw_diff="""
- print("user authenticated")
+ logger.info("user authenticated")
        """,
        force_replay_mismatch=False,
    )
    result = run_authorization(print_rule_pr)
    assert result.decision_result.decision == "ALLOW"

def test_ledger_chain_valid():
    is_valid, errors = verify_ledger_chain()
    assert is_valid is True, f"Ledger is invalid! Errors: {errors}"
    assert not errors
