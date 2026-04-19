from app.config import SYSTEM_NAME, SYSTEM_VERSION
from app.models import PRInput
from app.orchestrator import run_authorization
from app.ledger_verifier import verify_ledger_chain


def print_result(title: str, result) -> None:
    print(f"\n================ {title} ================")

    print("\n--- EXECUTION ID ---")
    print(result.execution_id)

    print("\n--- ENVIRONMENT FINGERPRINT ---")
    print(result.environment_fingerprint)

    print("\n--- NORMALIZED PR ---")
    print(result.normalized_pr.model_dump_json(indent=2))

    print("\n--- ISSUE MAPPING ---")
    print(result.issue_mapping.model_dump_json(indent=2))

    if result.template_selection:
        print("\n--- TEMPLATE SELECTION ---")
        print(result.template_selection.model_dump_json(indent=2))

    if result.patch_result:
        print("\n--- PATCH RESULT ---")
        print(result.patch_result.model_dump_json(indent=2))

    if result.replay_result:
        print("\n--- REPLAY RESULT ---")
        print(result.replay_result.model_dump_json(indent=2))

    if result.comparison_result:
        print("\n--- COMPARISON RESULT ---")
        print(result.comparison_result.model_dump_json(indent=2))

    print("\n--- DECISION RESULT ---")
    print(result.decision_result.model_dump_json(indent=2))

    if result.ledger_record:
        print("\n--- LEDGER RECORD ---")
        print(result.ledger_record.model_dump_json(indent=2))


def main() -> None:
    print(f"{SYSTEM_NAME} v{SYSTEM_VERSION}")
    print("Deterministic Code Change Authorization System")
    print("Please use the CLI or API endpoints to submit PR inputs.")
    print("To run tests, use `pytest tests/`")


if __name__ == "__main__":
    main()