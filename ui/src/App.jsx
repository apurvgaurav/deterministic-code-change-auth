import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://localhost:5000";

const initialForm = {
  pr_id: "PR-001",
  file_path: "src/auth/login.py",
  language: "Python",
  raw_diff: `- query = "SELECT * FROM users WHERE username = '" + username + "'"
+ query = "SELECT * FROM users WHERE username = %s"

- cursor.execute(query)
+ cursor.execute(query, (username,))`,
  force_replay_mismatch: false,
};

function Badge({ value }) {
  const normalized = String(value).toLowerCase();

  let className = "badge";
  if (
    normalized === "allow" ||
    normalized === "true" ||
    normalized === "ok"
  ) {
    className += " badge-success";
  } else if (
    normalized === "block" ||
    normalized === "false"
  ) {
    className += " badge-danger";
  } else {
    className += " badge-neutral";
  }

  return <span className={className}>{String(value)}</span>;
}

function ResultRow({ label, value }) {
  return (
    <div className="result-row">
      <div className="result-label">{label}</div>
      <div className="result-value">
        {typeof value === "boolean" ? (
          <Badge value={value} />
        ) : value ? (
          value
        ) : (
          <span className="muted">—</span>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [health, setHealth] = useState({ status: "checking" });
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [rawResponse, setRawResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch(() => setHealth({ status: "unhealthy" }));
  }, []);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const payload = {
      pr_id: form.pr_id,
      file_path: form.file_path,
      language: form.language,
      raw_diff: form.raw_diff,
      force_replay_mismatch: form.force_replay_mismatch,
    };

    try {
      const res = await fetch(`${API_BASE}/authorize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      setRawResponse(data);

      const flattened = {
        decision: data.decision_result?.decision,
        execution_id: data.execution_id,
        reason: data.decision_result?.reason,
        replay_match: data.comparison_result?.is_match,
        byte_match: data.ledger_record?.byte_match,
        rollback_triggered: data.decision_result?.rollback_triggered,
        template_id: data.patch_result?.template_id,
        issue_type: data.issue_mapping?.issue_type,
        rule_id: data.issue_mapping?.rule_id,
      };

      setResult(flattened);
    } catch (err) {
      console.error("Authorization error:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      {/* 🔥 CENTERED HEADER */}
      <div style={{ textAlign: "center", marginBottom: "24px" }}>
        <h1 style={{ marginBottom: "6px", letterSpacing: "0.03em" }}>
          Deterministic Code Change Authorization
        </h1>

        <p
          style={{
            color: "#9ba8c7",
            fontSize: "14px",
          }}
        >
          Authorization requires byte-level replay match. No match → no approval.
        </p>
      </div>

      <div className="grid">
        {/* SYSTEM STATUS */}
        <div className="panel">
          <h2>System Status</h2>
          <ResultRow label="API Base" value={API_BASE} />
          <ResultRow label="Health" value={health.status} />
        </div>

        {/* REQUEST PANEL */}
        <div className="panel">
          <h2>Authorization Request</h2>
          <form onSubmit={handleSubmit} className="form">
            <label>
              PR ID
              <input
                type="text"
                value={form.pr_id}
                onChange={(e) =>
                  updateField("pr_id", e.target.value)
                }
              />
            </label>

            <label>
              File Path
              <input
                type="text"
                value={form.file_path}
                onChange={(e) =>
                  updateField("file_path", e.target.value)
                }
              />
            </label>

            <label>
              Language
              <input
                type="text"
                value={form.language}
                onChange={(e) =>
                  updateField("language", e.target.value)
                }
              />
            </label>

            <label>
              Diff
              <textarea
                rows="10"
                value={form.raw_diff}
                onChange={(e) =>
                  updateField("raw_diff", e.target.value)
                }
              />
            </label>

            {/* CHECKBOX */}
            <label className="checkbox-row">
              <input
                type="checkbox"
                checked={form.force_replay_mismatch}
                onChange={(e) =>
                  updateField(
                    "force_replay_mismatch",
                    e.target.checked
                  )
                }
              />
              <span>Force replay mismatch</span>
            </label>

            <button className="primary-btn" type="submit">
              {loading ? "Running..." : "Authorize Change"}
            </button>
          </form>
        </div>

        {/* RESULT PANEL */}
        <div className="panel">
          <h2>Authorization Result</h2>

          {!result && <p className="muted">No result yet</p>}

          {result && (
            <>
              {/* 🔥 DECISION BANNER */}
              <div
                style={{
                  padding: "16px",
                  marginBottom: "12px",
                  borderRadius: "10px",
                  fontWeight: "800",
                  textAlign: "center",
                  fontSize: "20px",
                  letterSpacing: "0.08em",
                  background:
                    result.decision === "ALLOW"
                      ? "#0f5132"
                      : "#842029",
                  color: "white",
                }}
              >
                {result.decision}
              </div>

              {/* 🔥 SUMMARY STRIP */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr 1fr 1fr",
                  gap: "8px",
                  marginBottom: "12px",
                }}
              >
                <div className="mini-card">
                  <div className="mini-label">Replay</div>
                  <div className="mini-value">
                    <Badge value={result.replay_match} />
                  </div>
                </div>

                <div className="mini-card">
                  <div className="mini-label">Byte</div>
                  <div className="mini-value">
                    <Badge value={result.byte_match} />
                  </div>
                </div>

                <div className="mini-card">
                  <div className="mini-label">Rollback</div>
                  <div className="mini-value">
                    <Badge value={result.rollback_triggered} />
                  </div>
                </div>

                <div className="mini-card">
                  <div className="mini-label">Template</div>
                  <div className="mini-value" style={{ fontSize: "11px" }}>
                    {result.template_id}
                  </div>
                </div>
              </div>

              <ResultRow label="Execution ID" value={result.execution_id} />
              <ResultRow label="Reason" value={result.reason} />
              <ResultRow label="Issue Type" value={result.issue_type} />
              <ResultRow label="Rule ID" value={result.rule_id} />
            </>
          )}
        </div>
      </div>

      {/* RAW RESPONSE */}
      <div className="panel">
        <h2>Raw Response</h2>
        <pre>
          {rawResponse
            ? JSON.stringify(rawResponse, null, 2)
            : "No response yet"}
        </pre>
      </div>
    </div>
  );
}