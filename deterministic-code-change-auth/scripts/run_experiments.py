import os
import json
import time
from pathlib import Path
import sys

# Ensure app is in path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models import PRInput
from app.orchestrator import run_authorization

SCENARIOS = [
    # ---- REPRODUCIBLE (4 scenarios) ----
    {
        "id": "repro_01",
        "category": "reproducible",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-REPRO-1", file_path="src/auth/login.py", language="Python",
            raw_diff="- query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"\n+ query = \"SELECT * FROM users WHERE username = %s\"\n- cursor.execute(query)\n+ cursor.execute(query, (username,))",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "repro_02",
        "category": "reproducible",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-REPRO-2", file_path="src/auth/audit.py", language="Python",
            raw_diff="- print(\"user authenticated\")\n+ logger.info(\"user authenticated\")",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "repro_03",
        "category": "reproducible",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-REPRO-3", file_path="src/db/queries.py", language="Python",
            raw_diff="- q = \"SELECT * FROM roles WHERE role = '\" + role + \"'\"\n+ q = \"SELECT * FROM roles WHERE role = %s\"\n- db.execute(q)\n+ db.execute(q, (role,))",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "repro_04",
        "category": "reproducible",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-REPRO-4", file_path="src/utils/debug.py", language="Python",
            raw_diff="- print(\"fetching data...\")\n+ logger.info(\"fetching data...\")",
            force_replay_mismatch=False,
        )
    },

    # ---- DIVERGENT (4 scenarios) ----
    {
        "id": "diverge_01",
        "category": "divergent",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-DIV-1", file_path="src/auth/login.py", language="Python",
            raw_diff="- query = \"SELECT * FROM users WHERE id = '\" + id + \"'\"\n+ query = \"SELECT * FROM users WHERE id = %s\"\n- cursor.execute(query)\n+ cursor.execute(query, (id,))",
            force_replay_mismatch=True,
        )
    },
    {
        "id": "diverge_02",
        "category": "divergent",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-DIV-2", file_path="src/auth/audit.py", language="Python",
            raw_diff="- print(\"divergent login check\")\n+ logger.info(\"divergent login check\")",
            force_replay_mismatch=True,
        )
    },
    {
        "id": "diverge_03",
        "category": "divergent",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-DIV-3", file_path="src/db/queries.py", language="Python",
            raw_diff="- db_query = \"SELECT id FROM sessions WHERE token='\"+tok+\"'\"\n+ db_query = \"SELECT id FROM sessions WHERE token=%s\"\n- exec(db_query)\n+ exec(db_query, (tok,))",
            force_replay_mismatch=True,
        )
    },
    {
        "id": "diverge_04",
        "category": "divergent",
        "boundary_overlap_flag": False,
        "pr_input": PRInput(
            pr_id="EXP-DIV-4", file_path="src/utils/debug.py", language="Python",
            raw_diff="- print(\"starting div 04\")\n+ logger.info(\"starting div 04\")",
            force_replay_mismatch=True,
        )
    },

    # ---- BOUNDARY / UNMAPPED (4 scenarios) ----
    {
        "id": "boundary_01",
        "category": "boundary",
        "boundary_overlap_flag": True,
        "pr_input": PRInput(
            pr_id="EXP-BOUND-1", file_path="src/utils/math.py", language="Python",
            raw_diff="- total = value1 + value2\n+ total = sum([value1, value2])",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "boundary_02",
        "category": "boundary",
        "boundary_overlap_flag": True,
        "pr_input": PRInput(
            pr_id="EXP-BOUND-2", file_path="src/ui/render.py", language="Python",
            raw_diff="- def render(): return True\n+ def render(ctx=None): return True",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "boundary_03",
        "category": "boundary",
        "boundary_overlap_flag": True,
        "pr_input": PRInput(
            pr_id="EXP-BOUND-3", file_path="src/api/routes.py", language="Python",
            raw_diff="- @app.get('/home')\n+ @app.get('/index')",
            force_replay_mismatch=False,
        )
    },
    {
        "id": "boundary_04",
        "category": "boundary",
        "boundary_overlap_flag": True,
        "pr_input": PRInput(
            pr_id="EXP-BOUND-4", file_path="src/core/loop.py", language="Python",
            raw_diff="- while True: pass\n+ while running: pass",
            force_replay_mismatch=False,
        )
    },
]

RUNS_PER_SCENARIO = 30
LOG_FILE = Path(__file__).resolve().parent.parent / "results_log.jsonl"

def append_log(record):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def main():
    print(f"Starting IEEE Access Experiment Runner for {len(SCENARIOS)} scenarios x {RUNS_PER_SCENARIO} runs = {len(SCENARIOS)*RUNS_PER_SCENARIO} total runs")
    if LOG_FILE.exists():
        LOG_FILE.unlink()
        
    for scenario in SCENARIOS:
        print(f"\nRunning scenario {scenario['id']} ({scenario['category']})...")
        for run in range(1, RUNS_PER_SCENARIO + 1):
            
            # --- IEEE Access Timing Instrumentation ---
            pipeline_start = time.perf_counter()
            
            # Pipeline call
            result = run_authorization(scenario["pr_input"])
            
            pipeline_end = time.perf_counter()
            latency_seconds = round(pipeline_end - pipeline_start, 4)
            # ------------------------------------------
            
            decision = result.decision_result.decision
            
            # Extract divergence logic (without rewriting core app functions)
            divergence_detected = False
            if result.comparison_result and not result.comparison_result.is_match:
                divergence_detected = True
            elif result.decision_result.reason == "Replay execution failed":
                divergence_detected = True
                
            boundary_overlap_flag = scenario["boundary_overlap_flag"]
            
            log_record = {
                "scenario_id": scenario["id"],
                "run_number": run,
                "decision": decision,
                "divergence_detected": divergence_detected,
                "boundary_overlap_flag": boundary_overlap_flag,
                "latency_seconds": latency_seconds
            }
            
            append_log(log_record)
            if run % 10 == 0:
                print(f"  {scenario['id']} run {run}/{RUNS_PER_SCENARIO}: {decision} | latency: {latency_seconds}s")
                
    print("\nExperiment completed. Results saved to results_log.jsonl.")

if __name__ == "__main__":
    main()
