from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.models import PRInput
from app.orchestrator import run_authorization
from app.ledger_verifier import verify_ledger_chain

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health() -> tuple:
    is_valid, errors = verify_ledger_chain()

    return (
        jsonify(
            {
                "status": "ok",
                "system": "Deterministic Code Change Authorization System",
                "ledger_chain_valid": is_valid,
                "ledger_errors": errors,
            }
        ),
        200,
    )


@app.post("/authorize")
def authorize() -> tuple:
    try:
        payload = request.get_json(silent=True)

        if not payload:
            return (
                jsonify(
                    {
                        "error": "Invalid request",
                        "message": "Expected JSON request body",
                    }
                ),
                400,
            )

        pr_input = PRInput(
            pr_id=payload["pr_id"],
            file_path=payload["file_path"],
            language=payload["language"],
            raw_diff=payload["raw_diff"],
            force_replay_mismatch=payload.get("force_replay_mismatch", False),
        )

        result = run_authorization(pr_input)

        return jsonify(result.model_dump()), 200

    except KeyError as exc:
        return (
            jsonify(
                {
                    "error": "Missing required field",
                    "message": f"Missing field: {exc.args[0]}",
                    "required_fields": [
                        "pr_id",
                        "file_path",
                        "language",
                        "raw_diff",
                    ],
                }
            ),
            400,
        )

    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "Authorization failed",
                    "message": str(exc),
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)